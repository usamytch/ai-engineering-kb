"""Safe, cache-aware downloads of full arXiv paper artifacts."""

from __future__ import annotations

from dataclasses import dataclass
import io
from pathlib import Path
import subprocess
from typing import Callable, Mapping, Protocol
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from aidb.extractors.html import (
    Document,
    ExtractionQualityError,
    extract_html,
    looks_like_article,
    write_document,
)
from aidb.extractors.pdf import PdfExtractionUnavailable, extract_pdf
from aidb.extractors.tex import extract_tex
from aidb.store import ArtifactRecord, ArtifactStore, ArxivRefLike, unavailable_record


USER_AGENT = "AIDB/1.0 (+local research library; respectful sequential fetch)"
MAX_BYTES = {
    "article.html": 30 * 1024 * 1024,
    "paper.pdf": 100 * 1024 * 1024,
    "source.tar.gz": 200 * 1024 * 1024,
}


class FullArxivRef(ArxivRefLike, Protocol):
    base_id: str
    version_id: str


@dataclass(frozen=True)
class FetchResult:
    base_id: str
    version_id: str
    path_key: str
    version_tag: str
    policy: str
    html_usable: bool
    artifacts: Mapping[str, ArtifactRecord]

    def to_manifest(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "source": "arxiv",
            "base_id": self.base_id,
            "version_id": self.version_id,
            "path_key": self.path_key,
            "version_tag": self.version_tag,
            "policy": self.policy,
            "html_usable": self.html_usable,
            "artifacts": {name: record.to_dict() for name, record in self.artifacts.items()},
        }


class _Response(Protocol):
    headers: object
    status: int

    def read(self, size: int = -1) -> bytes: ...
    def close(self) -> None: ...
    def __enter__(self) -> "_Response": ...
    def __exit__(self, *args: object) -> object: ...


Opener = Callable[..., _Response]


def fetch_arxiv(
    ref: FullArxivRef,
    root_or_store: Path | str | ArtifactStore,
    *,
    policy: str = "normal",
    force: bool = False,
    opener: Opener = urlopen,
    timeout: float = 60.0,
) -> FetchResult:
    """Fetch HTML and PDF sequentially, adding TeX source when warranted.

    ``normal`` corresponds to a normal read: HTML + PDF, with source as a
    fallback when HTML is missing or is not a full article. ``full`` and
    ``review`` always retain the source archive as well.
    """

    policy = {"n": "normal", "r": "review"}.get(policy, policy)
    if policy not in {"normal", "full", "review"}:
        raise ValueError(f"unknown arXiv fetch policy: {policy!r}")
    store = root_or_store if isinstance(root_or_store, ArtifactStore) else ArtifactStore(root_or_store)
    escaped_id = quote(ref.version_id, safe="/")
    urls = {
        "article.html": f"https://arxiv.org/html/{escaped_id}",
        "paper.pdf": f"https://arxiv.org/pdf/{escaped_id}",
        "source.tar.gz": f"https://export.arxiv.org/e-print/{escaped_id}",
    }
    records: dict[str, ArtifactRecord] = {}

    html_record, html_usable = _fetch_html(ref, store, urls["article.html"], force, opener, timeout)
    records["article.html"] = html_record
    records["paper.pdf"] = _fetch_binary(
        ref,
        store,
        "paper.pdf",
        urls["paper.pdf"],
        force,
        opener,
        timeout,
        expected_magic=b"%PDF-",
    )

    if policy in {"full", "review"} or not html_usable:
        records["source.tar.gz"] = _fetch_binary(
            ref,
            store,
            "source.tar.gz",
            urls["source.tar.gz"],
            force,
            opener,
            timeout,
        )

    return FetchResult(
        base_id=ref.base_id,
        version_id=ref.version_id,
        path_key=ref.path_key,
        version_tag=ref.version_tag,
        policy=policy,
        html_usable=html_usable,
        artifacts=records,
    )


def extract_arxiv(
    ref: FullArxivRef,
    root_or_store: Path | str | ArtifactStore,
    *,
    fetched: FetchResult | None = None,
    min_chars: int = 800,
) -> Document:
    """Choose the strongest available representation and write canonical text.

    HTML is preferred because it preserves semantic structure and locators.
    Static TeX parsing is next.  PDF text extraction is a final optional fallback
    and runs only the installed ``pdftotext`` binary, never TeX or shell code.
    """

    store = root_or_store if isinstance(root_or_store, ArtifactStore) else ArtifactStore(root_or_store)
    failures: list[str] = []
    candidates = fetched.artifacts if fetched is not None else {}

    html_path = store.artifact_path(ref, "article.html")
    if html_path.is_file() and _candidate_available(candidates, "article.html"):
        try:
            document = extract_html(html_path.read_bytes(), min_chars=min_chars)
            write_document(document, store.artifact_dir(ref))
            return document
        except (ExtractionQualityError, OSError) as error:
            failures.append(f"HTML: {error}")

    source_path = store.artifact_path(ref, "source.tar.gz")
    if source_path.is_file() and _candidate_available(candidates, "source.tar.gz"):
        try:
            return extract_tex(source_path, output_dir=store.artifact_dir(ref), min_chars=min_chars)
        except (ExtractionQualityError, OSError, ValueError) as error:
            failures.append(f"TeX: {error}")

    pdf_path = store.artifact_path(ref, "paper.pdf")
    if pdf_path.is_file() and _candidate_available(candidates, "paper.pdf"):
        try:
            document = extract_pdf(pdf_path, min_chars=min_chars)
            write_document(document, store.artifact_dir(ref))
            return document
        except (
            ExtractionQualityError,
            PdfExtractionUnavailable,
            OSError,
            subprocess.SubprocessError,
        ) as error:
            failures.append(f"PDF: {error}")

    detail = "; ".join(failures) if failures else "no downloaded full-text artifacts"
    raise ExtractionQualityError(f"could not extract arXiv {ref.version_id}: {detail}")


def _fetch_html(
    ref: FullArxivRef,
    store: ArtifactStore,
    url: str,
    force: bool,
    opener: Opener,
    timeout: float,
) -> tuple[ArtifactRecord, bool]:
    if not force:
        cached = store.existing_record(ref, "article.html", url=url, mime_type="text/html")
        if cached is not None:
            path = store.root / (cached.path or "")
            if looks_like_article(path.read_bytes()):
                return cached, True
    try:
        body, status, mime_type = _request(url, opener, timeout, MAX_BYTES["article.html"])
    except HTTPError as error:
        return unavailable_record(
            "article.html", url=url, status=error.code, mime_type=_header_mime(error.headers), error=str(error)
        ), False
    if not looks_like_article(body):
        return unavailable_record(
            "article.html",
            url=url,
            status="quality-rejected",
            mime_type=mime_type,
            error="response is not credible full paper HTML",
        ), False
    record = store.write_stream(
        ref,
        "article.html",
        io.BytesIO(body),
        url=url,
        status=status,
        mime_type=mime_type,
        max_bytes=MAX_BYTES["article.html"],
    )
    return record, True


def _candidate_available(candidates: Mapping[str, ArtifactRecord], name: str) -> bool:
    record = candidates.get(name)
    return record is None or record.available


def _fetch_binary(
    ref: FullArxivRef,
    store: ArtifactStore,
    name: str,
    url: str,
    force: bool,
    opener: Opener,
    timeout: float,
    *,
    expected_magic: bytes | None = None,
) -> ArtifactRecord:
    if not force:
        cached = store.existing_record(ref, name, url=url)
        if cached is not None:
            if expected_magic is None:
                return cached
            path = store.root / (cached.path or "")
            with path.open("rb") as source:
                if source.read(len(expected_magic)) == expected_magic:
                    return cached
    try:
        body, status, mime_type = _request(url, opener, timeout, MAX_BYTES[name])
    except HTTPError as error:
        return unavailable_record(name, url=url, status=error.code, mime_type=_header_mime(error.headers), error=str(error))
    if expected_magic is not None and not body.startswith(expected_magic):
        return unavailable_record(
            name,
            url=url,
            status="quality-rejected",
            mime_type=mime_type,
            error=f"response does not start with {expected_magic!r}",
        )
    return store.write_stream(
        ref,
        name,
        io.BytesIO(body),
        url=url,
        status=status,
        mime_type=mime_type,
        max_bytes=MAX_BYTES[name],
    )


def _request(url: str, opener: Opener, timeout: float, max_bytes: int) -> tuple[bytes, int, str | None]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with opener(request, timeout=timeout) as response:
        body = _read_limited(response, max_bytes)
        status = getattr(response, "status", None) or response.getcode()
        mime_type = _header_mime(getattr(response, "headers", None))
    return body, int(status), mime_type


def _read_limited(response: _Response, limit: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(64 * 1024, limit + 1 - total))
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            raise ValueError(f"download exceeds {limit} byte limit")


def _header_mime(headers: object) -> str | None:
    if headers is None:
        return None
    get_content_type = getattr(headers, "get_content_type", None)
    if callable(get_content_type):
        return str(get_content_type())
    get = getattr(headers, "get", None)
    value = get("Content-Type") if callable(get) else None
    return str(value).split(";", 1)[0].strip() if value else None
