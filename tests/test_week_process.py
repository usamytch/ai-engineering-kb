from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from aidb.domain import ArxivRef
from aidb.pipeline import ProcessResult, paper_paths
from aidb.week_process import process_week
from aidb.weekly import source_id


class DummyProvider:
    name = "dummy"

    def generate(self, prompt, schema):
        raise AssertionError("mocked process_paper should own provider calls")


def card(title: str, url: str, marker: str) -> str:
    return (
        f"- [{marker}] **[{title}]({url})**\n"
        f"  <!-- aidb:id={source_id(url)} -->\n"
        "  - Feed: test\n"
        "  - Published: 2026-08-17\n"
        "  - Topics: agents\n"
    )


class WeekProcessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.batch = self.root / "inbox" / "2026-W34"
        self.batch.mkdir(parents=True)
        self.urls = {
            "drop": "https://example.com/drop",
            "note": "https://arxiv.org/abs/2608.16889v1",
            "review": "https://arxiv.org/abs/2608.16876v1",
            "open": "https://example.com/open",
        }
        index = (
            "# Weekly discovery — 2026-W34\n\n## Кандидаты\n\n"
            + card("Drop", self.urls["drop"], "d")
            + card("Note", self.urls["note"], "n")
            + card("Review", self.urls["review"], "r")
            + card("Open", self.urls["open"], " ")
            + "\n## После triage\n"
        )
        (self.batch / "index.md").write_text(index, encoding="utf-8")
        manifest = {
            "schema_version": 1,
            "entries": [
                {"id": source_id(url), "title": name.title(), "url": url}
                for name, url in self.urls.items()
            ],
            "errors": [],
        }
        (self.batch / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_success_is_marked_but_failed_paper_remains_selected(self) -> None:
        note_ref = ArxivRef.parse(self.urls["note"])
        note_paths = paper_paths(self.root, note_ref)
        note_paths.summary.parent.mkdir(parents=True)
        note_paths.summary.write_text("summary", encoding="utf-8")
        note_paths.paper_index.write_text("index", encoding="utf-8")
        success = ProcessResult(note_ref, note_paths, "html", 12, False)

        def fake_process(root, ref, provider, **kwargs):
            if ref.base_id == note_ref.base_id:
                return success
            raise RuntimeError("network unavailable")

        with mock.patch("aidb.week_process.process_paper", side_effect=fake_process):
            report = process_week(self.root, "2026-W34", DummyProvider())

        content = (self.batch / "index.md").read_text(encoding="utf-8")
        self.assertIn("- [x] **[Drop]", content)
        self.assertIn("- Triage: drop", content)
        self.assertIn("- [x] **[Note]", content)
        self.assertIn("- Summary: [v1 deep summary]", content)
        self.assertIn("- [r] **[Review]", content)
        self.assertIn("- Error: network unavailable", content)
        self.assertEqual(report.counts["failed"], 1)
        manifest = json.loads((self.batch / "manifest.json").read_text(encoding="utf-8"))
        states = {item["id"]: item["status"] for item in manifest["entries"] if "status" in item}
        self.assertEqual(states[source_id(self.urls["note"])], "summarized")
        self.assertEqual(states[source_id(self.urls["review"])], "failed")

    def test_dry_run_does_not_modify_index(self) -> None:
        index = self.batch / "index.md"
        original = index.read_text(encoding="utf-8")
        report = process_week(self.root, "2026-W34", DummyProvider(), dry_run=True)
        self.assertEqual(index.read_text(encoding="utf-8"), original)
        self.assertEqual(report.counts["note"], 1)
        self.assertEqual(report.counts["review"], 1)


if __name__ == "__main__":
    unittest.main()
