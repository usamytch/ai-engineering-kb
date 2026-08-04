from __future__ import annotations

import tempfile
import unittest
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
                    candidate("Drop me", "https://example.com/drop", "drop"),
                    candidate("Watch me", "https://example.com/watch", "watch"),
                    candidate("Note me", "https://example.com/note", "note"),
                    candidate("Review me", "https://example.com/review", "review"),
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
            [candidate("Note me", "https://example.com/note", "note")]
        )
        self.path.write_text(original, encoding="utf-8")
        plan = plan_inbox_file(
            self.path, root=self.root, checked_on=date(2026, 8, 4)
        )
        self.assertTrue(plan.changed)
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)
        self.assertFalse((self.root / "notes").exists())

    def test_legacy_triage_field_is_still_supported(self) -> None:
        self.path.write_text(
            inbox_content(
                [
                    candidate("Drop me", "https://example.com/drop", triage="drop"),
                    candidate("Note me", "https://example.com/note", triage="note"),
                ]
            ),
            encoding="utf-8",
        )

        plan = plan_inbox_file(
            self.path, root=self.root, checked_on=date(2026, 8, 4)
        )
        self.assertEqual(plan.counts["drop"], 1)
        self.assertEqual(plan.counts["note"], 1)
        apply_plan(plan)

        updated = self.path.read_text(encoding="utf-8")
        self.assertNotIn("Drop me", updated)
        self.assertIn("- [x] **[Note me]", updated)
        self.assertIn("- Triage: note", updated)
        self.assertTrue((self.root / "notes" / "2026-08-04-note-me.md").exists())

    def test_conflicting_marker_and_field_outcomes_fail(self) -> None:
        original = inbox_content(
            [
                candidate(
                    "Conflict",
                    "https://example.com/conflict",
                    "note",
                    triage="review",
                )
            ]
        )
        self.path.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(TriageError, "conflicting triage outcomes"):
            plan_inbox_file(self.path, root=self.root, checked_on=date(2026, 8, 4))
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_invalid_checkbox_marker_fails_instead_of_being_ignored(self) -> None:
        original = inbox_content(
            [
                candidate(
                    "Typo",
                    "https://example.com/typo",
                    "rewiew",
                )
            ]
        )
        self.path.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(TriageError, "invalid checkbox marker"):
            plan_inbox_file(self.path, root=self.root, checked_on=date(2026, 8, 4))
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_invalid_outcome_fails_before_writing(self) -> None:
        original = inbox_content(
            [candidate("Typo", "https://example.com/typo", triage="rewiew")]
        )
        self.path.write_text(original, encoding="utf-8")
        with self.assertRaises(TriageError):
            plan_inbox_file(self.path, root=self.root, checked_on=date(2026, 8, 4))
        self.assertEqual(self.path.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
