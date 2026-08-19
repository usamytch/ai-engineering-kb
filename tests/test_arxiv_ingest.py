from __future__ import annotations

from dataclasses import dataclass
from email.message import Message
import gzip
import io
import json
from pathlib import Path
import tarfile
import unittest
from urllib.error import HTTPError

from aidb.extractors.html import (
    ExtractionQualityError,
    extract_html,
    extract_html_metadata,
    write_document,
)
from aidb.extractors.tex import UnsafeArchiveError, extract_tex
from aidb.sources.arxiv import extract_arxiv, fetch_arxiv
from aidb.store import ArtifactStore


FIXTURES = Path(__file__).parent / "fixtures" / "arxiv"


@dataclass(frozen=True)
class Ref:
    base_id: str = "2608.16889"
    version_id: str = "2608.16889v1"
    version_tag: str = "v1"
    path_key: str = "2608.16889"


class FakeResponse(io.BytesIO):
    def __init__(self, body: bytes, mime_type: str, status: int = 200):
        super().__init__(body)
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = mime_type

    def getcode(self) -> int:
        return self.status


class QueueOpener:
    def __init__(self, responses: list[FakeResponse | Exception]):
        self.responses = responses
        self.requests = []

    def __call__(self, request, timeout=0):
        self.requests.append(request)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class ArtifactStoreTests(unittest.TestCase):
    def test_paths_and_atomic_hash(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            store = ArtifactStore(directory)
            record = store.write_stream(
                Ref(),
                "paper.pdf",
                io.BytesIO(b"%PDF-content"),
                url="https://arxiv.org/pdf/2608.16889v1",
                status=200,
                mime_type="application/pdf",
                max_bytes=100,
            )
            self.assertEqual(record.path, ".aidb/artifacts/arxiv/2608.16889/v1/paper.pdf")
            self.assertEqual(record.bytes, 12)
            self.assertEqual(len(record.sha256 or ""), 64)
            self.assertEqual(
                store.tracked_manifest_path(Ref()),
                Path(directory).resolve() / "papers/arxiv/2608.16889/versions/v1/manifest.json",
            )

    def test_rejects_unsafe_paths_and_does_not_leave_partial_file(self):
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            store = ArtifactStore(directory)
            with self.assertRaises(ValueError):
                store.artifact_path(Ref(path_key="../escape"), "paper.pdf")
            with self.assertRaises(ValueError):
                store.write_stream(
                    Ref(),
                    "paper.pdf",
                    io.BytesIO(b"too large"),
                    url=None,
                    status=200,
                    mime_type=None,
                    max_bytes=3,
                )
            self.assertFalse(store.artifact_path(Ref(), "paper.pdf").exists())


class HtmlExtractionTests(unittest.TestCase):
    def test_extracts_semantic_blocks_and_writes_canonical_files(self):
        from tempfile import TemporaryDirectory

        document = extract_html((FIXTURES / "full_article.html").read_bytes())
        kinds = {block.kind for block in document.blocks}
        self.assertTrue({"heading", "paragraph", "list_item", "table", "caption", "pre"} <= kinds)
        self.assertNotIn("alert", document.text)
        self.assertNotIn("feedback form", document.text)
        introduction = next(block for block in document.blocks if block.locator == "html:#introduction")
        self.assertEqual(introduction.section_path[-1], "1 Introduction")
        self.assertEqual(len(introduction.sha256), 64)

        with TemporaryDirectory() as directory:
            jsonl, markdown = write_document(document, directory)
            first = json.loads(jsonl.read_text().splitlines()[0])
            self.assertEqual(
                set(first), {"block_id", "kind", "section_path", "locator", "text", "sha256"}
            )
            self.assertIn("# Reliable Widget Learning", markdown.read_text())

    def test_rejects_abstract_or_error_page(self):
        abstract = "<h1>Paper</h1><h2>Abstract</h2><p>" + ("metadata " * 120) + "</p>"
        with self.assertRaises(ExtractionQualityError):
            extract_html(abstract)
        error = "<h1>Internal Server Error</h1><p>" + ("failure " * 200) + "</p><p>x</p><p>y</p>"
        with self.assertRaises(ExtractionQualityError):
            extract_html(error)

    def test_extracts_title_and_authors_as_convenience_metadata(self):
        html = """
        <html><head><title> A Paper Title </title></head><body>
        <span class="ltx_personname">Ada Lovelace</span>
        <span class="ltx_personname">Alan Turing</span>
        </body></html>
        """
        self.assertEqual(
            extract_html_metadata(html),
            {"title": "A Paper Title", "authors": ["Ada Lovelace", "Alan Turing"]},
        )


class FetchTests(unittest.TestCase):
    def test_normal_policy_fetches_html_and_pdf_then_uses_cache(self):
        from tempfile import TemporaryDirectory

        html = (FIXTURES / "full_article.html").read_bytes()
        opener = QueueOpener(
            [FakeResponse(html, "text/html; charset=utf-8"), FakeResponse(b"%PDF-body", "application/pdf")]
        )
        with TemporaryDirectory() as directory:
            result = fetch_arxiv(Ref(), directory, opener=opener)
            self.assertTrue(result.html_usable)
            self.assertEqual(list(result.artifacts), ["article.html", "paper.pdf"])
            self.assertTrue(all(request.get_header("User-agent") for request in opener.requests))

            cached = fetch_arxiv(Ref(), directory, opener=QueueOpener([]))
            self.assertTrue(all(record.cached for record in cached.artifacts.values()))

    def test_bad_html_triggers_source_fallback(self):
        from tempfile import TemporaryDirectory

        opener = QueueOpener(
            [
                FakeResponse(b"<html><h1>Not Found</h1></html>", "text/html"),
                FakeResponse(b"%PDF-body", "application/pdf"),
                FakeResponse(gzip.compress(_tex_source()), "application/gzip"),
            ]
        )
        with TemporaryDirectory() as directory:
            result = fetch_arxiv(Ref(), directory, opener=opener)
            self.assertFalse(result.html_usable)
            self.assertFalse(result.artifacts["article.html"].available)
            self.assertTrue(result.artifacts["source.tar.gz"].available)
            self.assertEqual(len(opener.requests), 3)
            document = extract_arxiv(Ref(), directory, fetched=result)
            self.assertEqual(document.source_format, "tex")
            self.assertTrue(
                (Path(directory) / ".aidb/artifacts/arxiv/2608.16889/v1/document.jsonl").is_file()
            )

    def test_html_404_is_tolerated_and_review_always_fetches_source(self):
        from tempfile import TemporaryDirectory

        missing = HTTPError("https://arxiv.org/html/id", 404, "not found", Message(), None)
        opener = QueueOpener(
            [missing, FakeResponse(b"%PDF-body", "application/pdf"), FakeResponse(b"plain tex", "text/plain")]
        )
        with TemporaryDirectory() as directory:
            result = fetch_arxiv(Ref(), directory, policy="review", opener=opener)
            self.assertEqual(result.artifacts["article.html"].status, 404)
            self.assertIn("source.tar.gz", result.artifacts)
        missing.close()


class TexExtractionTests(unittest.TestCase):
    def test_extracts_tar_and_gzip_without_compilation(self):
        tar_bytes = _tar_with({"paper/main.tex": _tex_source(), "paper/notes.txt": b"ignored"})
        document = extract_tex(tar_bytes)
        self.assertEqual(document.source_format, "tex")
        self.assertIn("Method", document.text)
        self.assertGreater(len(document.blocks), 5)

        gzip_document = extract_tex(gzip.compress(_tex_source()))
        self.assertEqual(gzip_document.source_format, "tex")

    def test_rejects_path_traversal_symlink_and_archive_bomb_header(self):
        with self.assertRaises(UnsafeArchiveError):
            extract_tex(_tar_with({"../escape.tex": _tex_source()}))

        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w") as archive:
            member = tarfile.TarInfo("link.tex")
            member.type = tarfile.SYMTYPE
            member.linkname = "/etc/passwd"
            archive.addfile(member)
        with self.assertRaises(UnsafeArchiveError):
            extract_tex(stream.getvalue())

        with self.assertRaises(UnsafeArchiveError):
            extract_tex(_tar_with({"large.tex": _tex_source()}), max_file_bytes=32)


def _tar_with(files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        for name, data in files.items():
            member = tarfile.TarInfo(name)
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    return stream.getvalue()


def _tex_source() -> bytes:
    paragraphs = "\n\n".join(
        [
            "We study reliable widget learning under distribution shift and give a calibrated objective with a finite sample correction. " * 3,
            "Existing systems report average accuracy while hiding group failures. Our protocol retains uncertainty and separates training from evaluation observations. " * 3,
            "The proposed estimator fits group conditioned residual variance on held out data and uses that variance to scale the optimization loss. " * 3,
            "Across five seeds the correction improves the difficult benchmark cases. Removing calibration eliminates most of the measured improvement. " * 3,
            "The method remains limited when groups contain very few observations, so the evidence should not be extrapolated beyond this benchmark. " * 3,
        ]
    )
    return (
        "\\documentclass{article}\n"
        "\\title{Reliable Widget Learning}\n"
        "\\begin{document}\n"
        "\\begin{abstract}\n" + paragraphs.split("\n\n")[0] + "\n\\end{abstract}\n\n"
        "\\section{Introduction}\n" + paragraphs.split("\n\n")[1] + "\n\n"
        "\\section{Method}\n" + paragraphs.split("\n\n")[2] + "\n\n"
        "\\section{Results}\n" + paragraphs.split("\n\n")[3] + "\n\n"
        "\\section{Limitations}\n" + paragraphs.split("\n\n")[4] + "\n"
        "\\end{document}\n"
    ).encode()


if __name__ == "__main__":
    unittest.main()
