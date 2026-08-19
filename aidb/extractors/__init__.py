"""Full-text extractors that produce AIDB document blocks."""

from .html import (
    Document,
    DocumentBlock,
    ExtractionQualityError,
    extract_html,
    extract_html_metadata,
    write_document,
)
from .tex import UnsafeArchiveError, extract_tex

__all__ = [
    "Document",
    "DocumentBlock",
    "ExtractionQualityError",
    "UnsafeArchiveError",
    "extract_html",
    "extract_html_metadata",
    "extract_tex",
    "write_document",
]
"""Canonical full-text extractors."""

from .html import Document, DocumentBlock, ExtractionQualityError, extract_html, write_document
from .pdf import PdfExtractionUnavailable, extract_pdf
from .tex import UnsafeArchiveError, extract_tex

__all__ = [
    "Document",
    "DocumentBlock",
    "ExtractionQualityError",
    "PdfExtractionUnavailable",
    "UnsafeArchiveError",
    "extract_html",
    "extract_pdf",
    "extract_tex",
    "write_document",
]
