"""Dependency-free extraction of semantic blocks from arXiv HTML."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from html.parser import HTMLParser
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Iterable


IGNORED_TAGS = {
    "script",
    "style",
    "noscript",
    "nav",
    "form",
    "footer",
    "aside",
    "iframe",
    "annotation",
    "svg",
    "canvas",
}
BLOCK_TAGS = {
    "p": "paragraph",
    "li": "list_item",
    "table": "table",
    "caption": "caption",
    "pre": "pre",
    "blockquote": "quote",
    "figcaption": "caption",
}
ERROR_PHRASES = (
    "internal server error",
    "page not found",
    "404 not found",
    "access denied",
    "temporarily unavailable",
)
NON_BODY_HEADINGS = {
    "abstract",
    "references",
    "bibliography",
    "acknowledgements",
    "acknowledgments",
    "contents",
}


class ExtractionQualityError(ValueError):
    """The downloaded page is not credible full paper text."""


@dataclass(frozen=True)
class DocumentBlock:
    block_id: str
    kind: str
    section_path: tuple[str, ...]
    locator: str
    text: str
    sha256: str

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["section_path"] = list(self.section_path)
        return payload


@dataclass(frozen=True)
class Document:
    source_format: str
    blocks: tuple[DocumentBlock, ...]

    @property
    def text(self) -> str:
        return "\n\n".join(block.text for block in self.blocks)


@dataclass
class _Collector:
    tag: str
    kind: str
    locator: str
    heading_level: int | None
    chunks: list[str]


class _SemanticHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, tuple[str, ...], str, str]] = []
        self.collectors: list[_Collector] = []
        self.section_stack: list[str] = []
        self.ignored_depth = 0
        self.tag_counts: dict[str, int] = {}

    def handle_comment(self, data: str) -> None:
        return

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if self.ignored_depth:
            if tag in IGNORED_TAGS:
                self.ignored_depth += 1
            return
        if tag in IGNORED_TAGS:
            self.ignored_depth = 1
            return

        kind: str | None = None
        heading_level: int | None = None
        if re.fullmatch(r"h[1-6]", tag):
            kind = "heading"
            heading_level = int(tag[1])
        elif tag in BLOCK_TAGS:
            kind = BLOCK_TAGS[tag]
        if kind is None:
            if tag in {"br", "hr"}:
                for collector in self.collectors:
                    collector.chunks.append("\n")
            return

        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
        attrs_dict = dict(attrs)
        element_id = attrs_dict.get("id")
        locator = f"html:#{element_id}" if element_id else f"html:{tag}[{self.tag_counts[tag]}]"
        self.collectors.append(_Collector(tag, kind, locator, heading_level, []))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self.ignored_depth:
            return
        for collector in self.collectors:
            collector.chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.ignored_depth:
            if tag in IGNORED_TAGS:
                self.ignored_depth -= 1
            return
        position = next((i for i in range(len(self.collectors) - 1, -1, -1) if self.collectors[i].tag == tag), None)
        if position is None:
            return
        collector = self.collectors.pop(position)
        text = _normalize_pre(collector.chunks) if collector.kind == "pre" else _normalize_text(collector.chunks)
        if not text:
            return
        if collector.kind == "heading" and collector.heading_level is not None:
            depth = max(1, collector.heading_level)
            self.section_stack = self.section_stack[: depth - 1]
            self.section_stack.append(text)
        self.blocks.append((collector.kind, tuple(self.section_stack), collector.locator, text))


class _MetadataHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_chunks: list[str] = []
        self.person_chunks: list[list[str]] = []
        self._title_depth = 0
        self._person_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        classes = set((dict(attrs).get("class") or "").split())
        if tag == "title":
            self._title_depth += 1
        if "ltx_personname" in classes:
            self._person_depth += 1
            self.person_chunks.append([])

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self._title_depth:
            self._title_depth -= 1
        if tag == "span" and self._person_depth:
            self._person_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._title_depth:
            self.title_chunks.append(data)
        if self._person_depth and self.person_chunks:
            self.person_chunks[-1].append(data)


def extract_html(data: bytes | str, *, min_chars: int = 800) -> Document:
    """Parse HTML and reject pages that do not resemble full paper text."""

    text = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data
    parser = _SemanticHTMLParser()
    parser.feed(text)
    parser.close()
    blocks = _materialize_blocks(parser.blocks)
    document = Document(source_format="html", blocks=blocks)
    validate_full_text(document, min_chars=min_chars)
    return document


def extract_html_metadata(data: bytes | str) -> dict[str, object]:
    """Extract non-authoritative convenience metadata from downloaded paper HTML."""

    text = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data
    parser = _MetadataHTMLParser()
    parser.feed(text)
    parser.close()
    title = _normalize_text(parser.title_chunks)
    authors = [
        _normalize_text(chunks)
        for chunks in parser.person_chunks
        if _normalize_text(chunks)
    ]
    result: dict[str, object] = {}
    if title:
        result["title"] = title
    if authors:
        result["authors"] = authors
    return result


def looks_like_article(data: bytes | str, *, min_chars: int = 800) -> bool:
    try:
        extract_html(data, min_chars=min_chars)
    except (ExtractionQualityError, UnicodeError):
        return False
    return True


def validate_full_text(document: Document, *, min_chars: int = 800) -> None:
    normalized = document.text.strip()
    lowered = normalized.lower()
    if len(normalized) < min_chars:
        raise ExtractionQualityError(f"full text is too short ({len(normalized)} < {min_chars} characters)")
    if any(phrase in lowered for phrase in ERROR_PHRASES) and len(normalized) < max(4000, min_chars * 3):
        raise ExtractionQualityError("HTML looks like an error page")

    content_blocks = [block for block in document.blocks if block.kind in {"paragraph", "list_item", "table", "pre", "quote"}]
    if len(content_blocks) < 3:
        raise ExtractionQualityError("too few semantic content blocks")
    headings = {
        _heading_key(block.text)
        for block in document.blocks
        if block.kind == "heading"
    }
    body_headings = {heading for heading in headings if heading and heading not in NON_BODY_HEADINGS}
    # A title is normally the first h1, so one heading alone does not establish
    # that we fetched more than an abstract landing page.
    if len(body_headings) < 2 and "abstract" in headings:
        raise ExtractionQualityError("HTML appears to contain only title/abstract metadata")


def write_document(document: Document, output_dir: Path | str) -> tuple[Path, Path]:
    """Atomically write canonical JSONL plus a human-readable Markdown mirror."""

    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    jsonl = directory / "document.jsonl"
    markdown = directory / "document.md"
    json_payload = "".join(
        json.dumps(block.to_dict(), ensure_ascii=False, sort_keys=True) + "\n"
        for block in document.blocks
    )
    md_payload = _render_markdown(document)
    _atomic_text(jsonl, json_payload)
    _atomic_text(markdown, md_payload)
    return jsonl, markdown


def _materialize_blocks(raw: Iterable[tuple[str, tuple[str, ...], str, str]]) -> tuple[DocumentBlock, ...]:
    result: list[DocumentBlock] = []
    for index, (kind, section_path, locator, text) in enumerate(raw, start=1):
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        result.append(
            DocumentBlock(
                block_id=f"b{index:05d}-{digest[:10]}",
                kind=kind,
                section_path=section_path,
                locator=locator,
                text=text,
                sha256=digest,
            )
        )
    return tuple(result)


def _normalize_text(chunks: Iterable[str]) -> str:
    return re.sub(r"\s+", " ", "".join(chunks)).strip()


def _normalize_pre(chunks: Iterable[str]) -> str:
    lines = [line.rstrip() for line in "".join(chunks).replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip()


def _heading_key(text: str) -> str:
    return re.sub(r"^\s*\d+(?:\.\d+)*[.)]?\s*", "", text).strip().lower()


def _render_markdown(document: Document) -> str:
    lines = [f"<!-- source_format: {document.source_format} -->", ""]
    for block in document.blocks:
        if block.kind == "heading":
            depth = max(1, min(6, len(block.section_path)))
            lines.extend((f"{'#' * depth} {block.text}", ""))
        elif block.kind == "list_item":
            lines.extend((f"- {block.text}", ""))
        elif block.kind == "pre":
            lines.extend(("```text", block.text, "```", ""))
        elif block.kind == "quote":
            lines.extend(("\n".join(f"> {line}" for line in block.text.splitlines()), ""))
        else:
            lines.extend((block.text, ""))
    return "\n".join(lines).rstrip() + "\n"


def _atomic_text(path: Path, content: str) -> None:
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as output:
            temporary = Path(output.name)
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    except BaseException:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise
