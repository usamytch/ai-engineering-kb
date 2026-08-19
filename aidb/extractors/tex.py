"""Safe, static TeX source extraction.

The source is treated as untrusted data.  It is never executed or compiled and
archive members are read in memory only after path, type, count and size checks.
"""

from __future__ import annotations

import gzip
import hashlib
import io
from pathlib import Path, PurePosixPath
import re
import tarfile
from typing import BinaryIO

from .html import Document, DocumentBlock, validate_full_text, write_document


class UnsafeArchiveError(ValueError):
    """An arXiv source archive violates extraction safety limits."""


def extract_tex(
    source: Path | str | bytes,
    *,
    output_dir: Path | str | None = None,
    min_chars: int = 800,
    max_files: int = 2_000,
    max_uncompressed_bytes: int = 100 * 1024 * 1024,
    max_file_bytes: int = 10 * 1024 * 1024,
) -> Document:
    """Extract a canonical document from tar/gzip/plain TeX without compiling."""

    raw = source if isinstance(source, bytes) else Path(source).read_bytes()
    if len(raw) > max_uncompressed_bytes:
        raise UnsafeArchiveError("compressed source exceeds configured size limit")
    files = _read_source_files(
        raw,
        max_files=max_files,
        max_total=max_uncompressed_bytes,
        max_file=max_file_bytes,
    )
    tex_files = [(name, data) for name, data in files if name.lower().endswith((".tex", ".ltx"))]
    if not tex_files:
        # arXiv also serves a gzip-compressed single TeX file with no useful
        # filename.  Accept it only if it has recognizable TeX structure.
        tex_files = [(name, data) for name, data in files if _looks_like_tex(data)]
    if not tex_files:
        raise UnsafeArchiveError("source contains no TeX documents")

    tex_files.sort(key=lambda item: (not _is_main_tex(item[1]), item[0]))
    decoded = "\n\n".join(_decode_tex(data) for _, data in tex_files)
    document = _parse_tex(decoded)
    validate_full_text(document, min_chars=min_chars)
    if output_dir is not None:
        write_document(document, output_dir)
    return document


def _read_source_files(raw: bytes, *, max_files: int, max_total: int, max_file: int) -> list[tuple[str, bytes]]:
    try:
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:*") as archive:
            members = archive.getmembers()
            if len(members) > max_files:
                raise UnsafeArchiveError(f"archive has more than {max_files} members")
            total = 0
            result: list[tuple[str, bytes]] = []
            for member in members:
                _validate_member(member)
                if member.isdir():
                    continue
                if not member.isfile():
                    raise UnsafeArchiveError(f"unsupported archive member type: {member.name}")
                if member.size < 0 or member.size > max_file:
                    raise UnsafeArchiveError(f"archive member is too large: {member.name}")
                total += member.size
                if total > max_total:
                    raise UnsafeArchiveError("archive exceeds total uncompressed size limit")
                stream = archive.extractfile(member)
                if stream is None:
                    raise UnsafeArchiveError(f"cannot read archive member: {member.name}")
                data = _read_limited(stream, max_file)
                if len(data) != member.size:
                    raise UnsafeArchiveError(f"truncated archive member: {member.name}")
                result.append((member.name, data))
            return result
    except tarfile.ReadError:
        pass

    if raw.startswith(b"\x1f\x8b"):
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(raw), mode="rb") as stream:
                return [("source.tex", _read_limited(stream, max_total))]
        except (OSError, EOFError) as error:
            raise UnsafeArchiveError(f"invalid gzip source: {error}") from error
    return [("source.tex", raw)]


def _validate_member(member: tarfile.TarInfo) -> None:
    name = member.name
    path = PurePosixPath(name)
    if not name or "\\" in name or path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise UnsafeArchiveError(f"unsafe archive path: {name!r}")
    if member.issym() or member.islnk():
        raise UnsafeArchiveError(f"links are not allowed in source archives: {name}")


def _read_limited(stream: BinaryIO, limit: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = stream.read(min(64 * 1024, limit + 1 - total))
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            raise UnsafeArchiveError(f"decompressed data exceeds {limit} byte limit")


def _looks_like_tex(data: bytes) -> bool:
    sample = data[:64 * 1024].lower()
    return b"\\documentclass" in sample or b"\\begin{document}" in sample or b"\\section{" in sample


def _is_main_tex(data: bytes) -> bool:
    sample = data[:256 * 1024].lower()
    return b"\\documentclass" in sample or b"\\begin{document}" in sample


def _decode_tex(data: bytes) -> str:
    for encoding in ("utf-8", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _parse_tex(tex: str) -> Document:
    tex = _strip_comments(tex)
    tex = re.sub(r"\\begin\s*\{abstract\}", r"\\section{Abstract}", tex, flags=re.IGNORECASE)
    tex = re.sub(r"\\end\s*\{abstract\}", "\n\n", tex, flags=re.IGNORECASE)
    heading_re = re.compile(
        r"\\(?P<command>title|section|subsection|subsubsection|paragraph)\*?\s*\{(?P<title>[^{}]{1,500})\}",
        flags=re.IGNORECASE,
    )
    raw_blocks: list[tuple[str, tuple[str, ...], str, str]] = []
    section_stack: list[str] = []
    cursor = 0
    locator_index = 0

    for match in heading_re.finditer(tex):
        locator_index = _append_tex_paragraphs(tex[cursor : match.start()], section_stack, raw_blocks, locator_index)
        command = match.group("command").lower()
        heading = _clean_tex(match.group("title"))
        if heading:
            level = {"title": 1, "section": 2, "subsection": 3, "subsubsection": 4, "paragraph": 5}[command]
            section_stack = section_stack[: level - 1]
            section_stack.append(heading)
            locator_index += 1
            raw_blocks.append(("heading", tuple(section_stack), f"tex:block[{locator_index}]", heading))
        cursor = match.end()
    _append_tex_paragraphs(tex[cursor:], section_stack, raw_blocks, locator_index)

    blocks: list[DocumentBlock] = []
    for index, (kind, section_path, locator, text) in enumerate(raw_blocks, start=1):
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        blocks.append(DocumentBlock(f"b{index:05d}-{digest[:10]}", kind, section_path, locator, text, digest))
    return Document(source_format="tex", blocks=tuple(blocks))


def _append_tex_paragraphs(
    fragment: str,
    section_stack: list[str],
    output: list[tuple[str, tuple[str, ...], str, str]],
    locator_index: int,
) -> int:
    fragment = re.sub(r"\\(?:begin|end)\s*\{[^{}]+\}", "\n\n", fragment)
    for raw_paragraph in re.split(r"\n\s*\n+", fragment):
        paragraph = _clean_tex(raw_paragraph)
        if len(paragraph) < 20:
            continue
        locator_index += 1
        output.append(("paragraph", tuple(section_stack), f"tex:block[{locator_index}]", paragraph))
    return locator_index


def _strip_comments(tex: str) -> str:
    lines: list[str] = []
    for line in tex.replace("\r\n", "\n").split("\n"):
        position = None
        for match in re.finditer(r"%", line):
            backslashes = len(line[: match.start()]) - len(line[: match.start()].rstrip("\\"))
            if backslashes % 2 == 0:
                position = match.start()
                break
        lines.append(line if position is None else line[:position])
    return "\n".join(lines)


def _clean_tex(text: str) -> str:
    text = re.sub(r"\$\$(.*?)\$\$", r" \1 ", text, flags=re.DOTALL)
    text = re.sub(r"\$(.*?)\$", r" \1 ", text, flags=re.DOTALL)
    text = re.sub(r"\\(?:cite|ref|label|url|href|includegraphics|input|include)\*?(?:\[[^\]]*\])?\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ").replace("~", " ")
    return re.sub(r"\s+", " ", text).strip()
