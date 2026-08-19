from __future__ import annotations

import tempfile
import unittest
import json
from datetime import date
from pathlib import Path

from scripts.triage_inbox import TriageError, apply_plan, plan_inbox_file


def candidate(
    title: str, url: str, marker: str = " ", triage: str | None = None
) -> str:
    result = f"""- [{marker}] **[{title}]({url})**
  - Feed: Test feed
  - Published: 2026-08-03
  - Topics: agents, rag
"""
    if triage is not None:
        result += f"  - Triage: {triage}\n"
    return result


def inbox_content(entries: list[str]) -> str:
    return (
        "# Discovery inbox — 2026-08-04\n\n"
        "## Кандидаты\n\n"
        + "".join(entries)
        + "\n## После triage\n\nDone.\n"
    )


class TriageInboxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "inbox").mkdir()
        self.path = self.root / "inbox" / "2026-08-04.md"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_applies_all_outcomes_and_is_idempotent(self) -> None:
        self.path.write_text(
            inbox_content(
                [
                    candidate("Drop me", "https://example.com/drop", "d"),
                    candidate("Watch me", "https://example.com/watch", "w"),
                    candidate("Note me", "https://example.com/note", "n"),
                    candidate("Review me", "https://example.com/review", "r"),
                    candidate("Untriaged", "https://example.com/open"),
                    candidate(
                        "Already done",
                        "https://example.com/done",
                        "x",
                        triage="watch",
                    ),
                ]
            ),
            encoding="utf-8",
        )

        plan = plan_inbox_file(
            self.path, root=self.root, checked_on=date(2026, 8, 4)
        )
        self.assertEqual(plan.counts["drop"], 1)
        self.assertEqual(plan.counts["watch"], 1)
        self.assertEqual(plan.counts["note"], 1)
        self.assertEqual(plan.counts["review"], 1)
        self.assertEqual(plan.counts["untriaged"], 1)
        self.assertEqual(plan.counts["processed"], 1)
        apply_plan(plan)

        updated = self.path.read_text(encoding="utf-8")
        self.assertNotIn("Drop me", updated)
        self.assertIn("- [x] **[Watch me]", updated)
        self.assertIn("- Triage: watch", updated)
        self.assertIn("- Note: [2026-08-04-note-me.md]", updated)
        self.assertIn("- Review: [2026-08-04-review-me.md]", updated)
        self.assertIn("- [ ] **[Untriaged]", updated)
        self.assertTrue((self.root / "notes" / "2026-08-04-note-me.md").exists())
        self.assertTrue((self.root / "reviews" / "2026-08-04-review-me.md").exists())

        second = plan_inbox_file(
            self.path, root=self.root, checked_on=date(2026, 8, 4)
        )
        self.assertFalse(second.changed)
        self.assertEqual(second.counts["processed"], 4, updated)
        self.assertEqual(second.counts["untriaged"], 1)

    def test_plan_does_not_write(self) -> None:
        original = inbox_content(
            [candidate("Note me", "https://example.com/note", "n")]
        )
        self.path.write_text(original, encoding="utf-8")
        plan = plan_inbox_file(
            self.path, root=self.root, checked_on=date(2026, 8, 4)
        )
        self.assertTrue(plan.changed)
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)
        self.assertFalse((self.root / "notes").exists())

    def test_legacy_triage_field_is_rejected(self) -> None:
        original = inbox_content(
            [candidate("Legacy", "https://example.com/legacy", triage="note")]
        )
        self.path.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(TriageError, "Triage is output-only"):
            plan_inbox_file(self.path, root=self.root, checked_on=date(2026, 8, 4))
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_full_outcome_marker_is_rejected(self) -> None:
        original = inbox_content(
            [
                candidate(
                    "Old format",
                    "https://example.com/old-format",
                    "review",
                )
            ]
        )
        self.path.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(TriageError, "invalid checkbox marker"):
            plan_inbox_file(self.path, root=self.root, checked_on=date(2026, 8, 4))
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_processed_marker_requires_generated_triage_field(self) -> None:
        for triage in (None, "rewiew"):
            with self.subTest(triage=triage):
                original = inbox_content(
                    [
                        candidate(
                            "Invalid processed entry",
                            "https://example.com/processed",
                            "x",
                            triage=triage,
                        )
                    ]
                )
                self.path.write_text(original, encoding="utf-8")
                with self.assertRaisesRegex(TriageError, "must have a generated"):
                    plan_inbox_file(
                        self.path, root=self.root, checked_on=date(2026, 8, 4)
                    )
                self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_weekly_inbox_retains_drop_and_syncs_manifest(self) -> None:
        weekly = self.root / "inbox" / "2026-W34"
        weekly.mkdir()
        path = weekly / "index.md"
        path.write_text(
            inbox_content(
                [
                    candidate("Drop me", "https://example.com/drop", "d"),
                    candidate("Note me", "https://example.com/note", "n"),
                ]
            ),
            encoding="utf-8",
        )
        manifest = {
            "schema_version": 1,
            "entries": [
                {"id": "url:240dc91e09f2f6de9701", "url": "https://example.com/drop"},
                {"id": "url:a75383e51e9f9dad3d39", "url": "https://example.com/note"},
            ],
        }
        from aidb.weekly import source_id

        manifest["entries"][0]["id"] = source_id("https://example.com/drop")
        manifest["entries"][1]["id"] = source_id("https://example.com/note")
        (weekly / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        plan = plan_inbox_file(path, root=self.root, checked_on=date(2026, 8, 19))
        apply_plan(plan)

        updated = path.read_text(encoding="utf-8")
        self.assertIn("- [x] **[Drop me]", updated)
        self.assertIn("- Triage: drop", updated)
        self.assertIn("../../notes/2026-08-19-note-me.md", updated)
        synced = json.loads((weekly / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(synced["entries"][0]["decision"], "drop")
        self.assertEqual(synced["entries"][1]["decision"], "note")


if __name__ == "__main__":
    unittest.main()
