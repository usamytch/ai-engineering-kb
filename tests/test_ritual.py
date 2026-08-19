from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from aidb.ritual import RitualError, close_week, week_status


class RitualTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.batch = self.root / "inbox" / "2026-W34"
        self.batch.mkdir(parents=True)
        self.manifest = {
            "schema_version": 1,
            "batch_id": "2026-W34",
            "entries": [
                {
                    "id": "url:item",
                    "title": "Item",
                    "url": "https://example.com/item",
                }
            ],
            "errors": [],
        }
        (self.batch / "manifest.json").write_text(
            json.dumps(self.manifest), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_index(self, marker: str, extra: str = "") -> None:
        (self.batch / "index.md").write_text(
            "# Weekly discovery — 2026-W34\n\n"
            "## Кандидаты\n\n"
            f"- [{marker}] **[Item](https://example.com/item)**\n"
            "  <!-- aidb:id=url:item -->\n"
            "  - Feed: test\n"
            f"{extra}"
            "\n## После triage\n",
            encoding="utf-8",
        )

    def test_status_counts_selection(self) -> None:
        self.write_index("n")
        status = week_status(self.root, "2026-W34")
        self.assertEqual(status["selected"], 1)
        self.assertEqual(status["markers"], {"note": 1})

    def test_close_requires_processed_or_explicitly_allows_open(self) -> None:
        self.write_index(" ")
        with self.assertRaisesRegex(RitualError, "untriaged"):
            close_week(self.root, "2026-W34")

        digest, closeout = close_week(
            self.root,
            "2026-W34",
            allow_open=True,
            now=datetime(2026, 8, 23, tzinfo=timezone.utc),
        )
        self.assertTrue(digest.exists())
        self.assertTrue(closeout.exists())
        self.assertIn("Weekly AI Engineering Review", digest.read_text(encoding="utf-8"))

    def test_close_renders_summary_link(self) -> None:
        self.write_index(
            "x",
            "  - Triage: note\n"
            "  - Summary: ../../papers/arxiv/2608.1/versions/v1/summary.md\n",
        )
        digest, _ = close_week(self.root, "2026-W34")
        self.assertIn("../../papers/arxiv", digest.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
