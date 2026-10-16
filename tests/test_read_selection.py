import unittest

from scripts.read_selection import require_note_decision
from scripts.triage_inbox import parse_entries


class ReadSelectionTest(unittest.TestCase):
    def test_preserves_other_triage_decisions(self):
        for marker, decision in (("d", "drop"), ("w", "watch"), ("r", "review"), ("x", "drop"), ("x", "review")):
            with self.subTest(marker=marker, decision=decision):
                entry = parse_entries(f"- [{marker}] **[Paper](https://example.com)**\n  - Triage: {decision}\n")[0]
                with self.assertRaisesRegex(ValueError, "different triage"):
                    require_note_decision(entry)

    def test_untriaged_selected_and_processed_notes_can_resume(self):
        for marker, decision in ((" ", ""), ("n", ""), ("x", "note")):
            entry = parse_entries(f"- [{marker}] **[Paper](https://example.com)**\n  - Triage: {decision}\n")[0]
            require_note_decision(entry)


if __name__ == "__main__":
    unittest.main()
