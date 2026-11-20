import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from aidb.domain import ArxivRef
from scripts.read_selection import checkpoint_paper, require_note_decision
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

    def test_completion_order_preserves_inbox_decisions_and_prior_results(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            refs = [ArxivRef.parse(value) for value in ("2611.00001v1", "2611.00002v1")]
            untouched = "- [w] **[Unrelated](https://example.com)**\n"
            content = untouched + "".join(
                f"- [ ] **[Paper]({ref.canonical_abs_url})**\n" for ref in refs
            )
            (batch / "index.md").write_text(content)
            (batch / "manifest.json").write_text(json.dumps({"entries": [
                {"paper_version_id": ref.version_id, "status": "discovered"} for ref in refs
            ]}))
            for ref in reversed(refs):
                result = SimpleNamespace(paths=SimpleNamespace(
                    paper_index=batch / ref.version_id / "index.md",
                    summary=batch / ref.version_id / "summary.md",
                ))
                checkpoint_paper(batch, ref, result)
            completed = (batch / "index.md").read_text()
            self.assertTrue(completed.startswith(untouched))
            self.assertEqual(completed.count("- [x]"), 2)
            self.assertEqual(completed.count("  - Triage: note"), 2)
            self.assertEqual(completed.count("  - Summary:"), 2)
            manifest = json.loads((batch / "manifest.json").read_text())
            self.assertTrue(all(entry["status"] == "summarized" for entry in manifest["entries"]))


if __name__ == "__main__":
    unittest.main()
