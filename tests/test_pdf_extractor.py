from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from aidb.extractors.pdf import PdfExtractionUnavailable, extract_pdf


class PdfExtractorTest(unittest.TestCase):
    def test_requires_an_installed_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            paper = Path(temp) / "paper.pdf"
            paper.write_bytes(b"%PDF-placeholder")
            with self.assertRaises(PdfExtractionUnavailable):
                extract_pdf(paper, executable="")

    def test_creates_page_anchored_blocks(self) -> None:
        text = (
            ("First page describes the method and experimental design in enough detail. " * 12)
            + "\n\n"
            + ("A second paragraph reports baseline comparisons and limitations. " * 12)
            + "\f"
            + ("Second page contains ablations and a reproducibility discussion. " * 12)
        )

        def runner(*args, **kwargs):
            return subprocess.CompletedProcess(args[0], 0, stdout=text, stderr="")

        with tempfile.TemporaryDirectory() as temp:
            paper = Path(temp) / "paper.pdf"
            paper.write_bytes(b"%PDF-placeholder")
            document = extract_pdf(
                paper,
                executable="pdftotext-test",
                runner=runner,
                min_chars=100,
            )
        self.assertEqual(document.source_format, "pdf")
        self.assertTrue(any(block.locator.startswith("pdf:page=2") for block in document.blocks))


if __name__ == "__main__":
    unittest.main()
