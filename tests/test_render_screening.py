import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import render_screening
from scripts.screen_inbox import digest, input_record


class CatalogTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.batch = self.root / "inbox" / "2026-W47"
        self.batch.mkdir(parents=True)
        (self.root / "templates").mkdir()
        (self.root / "templates" / "screening-catalog.html").write_text(
            '<title>__WEEK__</title><script type="application/json">__RECORDS__</script>'
        )
        self.entry = {
            "id": "arxiv:2610.00001v2", "title": "Memory </script><script>bad()</script>",
            "abstract": "We compare raw history and memory.", "categories": ["cs.AI"],
            "source_type": "paper", "feeds": ["arXiv"],
            "url": "https://arxiv.org/abs/2610.00001v2",
            "published": "2026-10-01T00:00:00+00:00", "updated": "2026-11-01T00:00:00+00:00",
        }
        self.record = {
            "id": self.entry["id"], "priority": "read", "topic": "memory",
            "assessment": "Авторы сравнивают память с исходной историей.",
            "evidence": "compare raw history and memory",
            "input_sha256": digest(input_record(self.entry)),
        }
        self.write_inputs([self.record])

    def write_inputs(self, records):
        (self.batch / "manifest.json").write_text(json.dumps({
            "entries": [self.entry], "discovery": {"since": "2026-10-16T13:00:00+00:00"},
        }))
        (self.batch / "screening.jsonl").write_text("".join(json.dumps(row) + "\n" for row in records))

    def render(self):
        with patch.object(render_screening, "ROOT", self.root), patch(
            "sys.argv", ["render_screening.py", "--week", "2026-W47"]
        ), contextlib.redirect_stdout(io.StringIO()):
            render_screening.main()

    def test_incomplete_or_stale_analysis_cannot_publish_catalog(self):
        self.write_inputs([])
        with self.assertRaisesRegex(ValueError, "every input"):
            self.render()
        self.entry["title"] = "Changed title"
        self.write_inputs([self.record])
        with self.assertRaisesRegex(ValueError, "stale screening"):
            self.render()
        self.assertFalse((self.batch / "catalog.html").exists())

    def test_source_text_cannot_close_data_script_and_revisions_are_labeled(self):
        self.render()
        result = (self.batch / "catalog.html").read_text()
        self.assertEqual(result.count("</script>"), 1)
        data = json.loads(result.split('type="application/json">')[1].split("</script>")[0])
        self.assertEqual(data[0]["title"], self.entry["title"])
        self.assertEqual(data[0]["event"], "revision")


if __name__ == "__main__":
    unittest.main()
