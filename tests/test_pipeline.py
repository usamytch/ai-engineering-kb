from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from aidb.domain import ArxivRef
from aidb.pipeline import (
    PipelineError,
    approve_paper,
    paper_paths,
    summarize_paper,
    write_paper_metadata,
)
from tests.test_summary_pipeline import BLOCKS, FakeProvider


class PaperPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "schemas").mkdir()
        (self.root / "prompts").mkdir()
        source_root = Path(__file__).resolve().parents[1]
        (self.root / "schemas" / "paper-summary-v1.json").write_text(
            (source_root / "schemas" / "paper-summary-v1.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (self.root / "prompts" / "paper-summary-v1.md").write_text(
            (source_root / "prompts" / "paper-summary-v1.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        self.ref = ArxivRef.parse("2608.16889v1")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_paths_require_explicit_version(self) -> None:
        with self.assertRaisesRegex(PipelineError, "version-pinned"):
            paper_paths(self.root, ArxivRef.parse("2608.16889"))

    def test_summary_is_tracked_and_second_run_uses_cache(self) -> None:
        paths = paper_paths(self.root, self.ref)
        paths.artifact_dir.mkdir(parents=True)
        paths.document_jsonl.write_text(
            "".join(json.dumps(block) + "\n" for block in BLOCKS),
            encoding="utf-8",
        )
        write_paper_metadata(
            self.root,
            self.ref,
            {"title": "Compact retrieval for scientific papers"},
        )
        provider = FakeProvider()

        result, cached = summarize_paper(self.root, self.ref, provider)
        second, second_cached = summarize_paper(self.root, self.ref, provider)

        self.assertFalse(cached)
        self.assertTrue(second_cached)
        self.assertEqual(result, second)
        self.assertTrue(paths.analysis.exists())
        self.assertIn("## Results", paths.summary.read_text(encoding="utf-8"))
        manifest = json.loads(paths.manifest.read_text(encoding="utf-8"))
        self.assertEqual(manifest["summary"]["status"], "ai-draft")
        self.assertIn("v1 deep summary", paths.paper_index.read_text(encoding="utf-8"))

    def test_human_approval_is_explicit(self) -> None:
        paths = paper_paths(self.root, self.ref)
        paths.artifact_dir.mkdir(parents=True)
        paths.document_jsonl.write_text(
            "".join(json.dumps(block) + "\n" for block in BLOCKS),
            encoding="utf-8",
        )
        summarize_paper(self.root, self.ref, FakeProvider())

        approve_paper(
            self.root,
            self.ref,
            reviewer="mesherin",
            now=datetime(2026, 8, 19, tzinfo=timezone.utc),
        )

        manifest = json.loads(paths.manifest.read_text(encoding="utf-8"))
        self.assertEqual(manifest["summary"]["status"], "verified")
        self.assertEqual(manifest["summary"]["verified_by"], "mesherin")

    def test_metadata_change_invalidates_summary_cache(self) -> None:
        paths = paper_paths(self.root, self.ref)
        paths.artifact_dir.mkdir(parents=True)
        paths.document_jsonl.write_text(
            "".join(json.dumps(block) + "\n" for block in BLOCKS),
            encoding="utf-8",
        )
        summarize_paper(self.root, self.ref, FakeProvider())
        write_paper_metadata(self.root, self.ref, {"comment": "new metadata"})

        _, cached = summarize_paper(self.root, self.ref, FakeProvider())

        self.assertFalse(cached)


if __name__ == "__main__":
    unittest.main()
