"""Optional PDF text fallback using the sandboxable ``pdftotext`` binary."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import shutil
import subprocess
from typing import Callable

from .html import Document, DocumentBlock, validate_full_text, write_document


class PdfExtractionUnavailable(RuntimeError):
    """No supported PDF text extractor is installed."""


def extract_pdf(
    source: Path | str,
    *,
    output_dir: Path | str | None = None,
    min_chars: int = 800,
    executable: str | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> Document:
    """Extract page-anchored blocks without invoking a shell or executing PDF content."""

    binary = executable if executable is not None else shutil.which("pdftotext")
    if not binary:
        raise PdfExtractionUnavailable(
            "PDF fallback needs Poppler pdftotext; HTML or TeX extraction was unavailable"
        )
    path = Path(source).resolve()
    completed = runner(
        [binary, "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    document = _document_from_text(completed.stdout)
    validate_full_text(document, min_chars=min_chars)
    if output_dir is not None:
        write_document(document, output_dir)
    return document


def _document_from_text(text: str) -> Document:
    blocks: list[DocumentBlock] = []
    for page_number, page in enumerate(text.replace("\r\n", "\n").split("\f"), start=1):
        paragraphs = re.split(r"\n\s*\n+", page)
        for paragraph_number, paragraph in enumerate(paragraphs, start=1):
            cleaned = re.sub(r"[ \t]+", " ", paragraph).strip()
            cleaned = re.sub(r"(?<=\w)-\n(?=\w)", "", cleaned)
            cleaned = re.sub(r"\n+", " ", cleaned).strip()
            if len(cleaned) < 20:
                continue
            digest = hashlib.sha256(cleaned.encode("utf-8")).hexdigest()
            blocks.append(
                DocumentBlock(
                    block_id=f"p{page_number:04d}b{paragraph_number:04d}-{digest[:10]}",
                    kind="paragraph",
                    section_path=(),
                    locator=f"pdf:page={page_number};paragraph={paragraph_number}",
                    text=cleaned,
                    sha256=digest,
                )
            )
    return Document(source_format="pdf", blocks=tuple(blocks))
