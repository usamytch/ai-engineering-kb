from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from aidb.weekly import (
    Candidate,
    merge_candidates,
    parse_card_states,
    source_id,
    write_week_batch,
)
from scripts.refresh_inbox import Entry


class WeeklyInboxTest(unittest.TestCase):
    def test_arxiv_forms_share_a_stable_version_id(self) -> None:
        self.assertEqual(
            source_id("https://arxiv.org/pdf/2608.16889v1.pdf"),
            "arxiv:2608.16889v1",
        )
        self.assertEqual(
            source_id("https://arxiv.org/abs/2608.16889v1"),
            "arxiv:2608.16889v1",
        )

    def test_merge_combines_discovery_sources_and_topics(self) -> None:
        first = Candidate(
            id="arxiv:2608.16889v1",
            title="Paper",
            url="https://arxiv.org/abs/2608.16889v1",
            published="2026-08-17T00:00:00+00:00",
            feeds=["feed-a"],
            topics=["agents"],
        )
        second = Candidate(
            id=first.id,
            title="Paper",
            url=first.url,
            published=first.published,
            feeds=["feed-b"],
            topics=["rag"],
        )

        merged = merge_candidates([first, second])

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].feeds, ["feed-a", "feed-b"])
        self.assertEqual(merged[0].topics, ["agents", "rag"])

    def test_week_batch_contains_manifest_and_preserves_manual_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            entry = Entry(
                title="Paper",
                url="https://arxiv.org/abs/2608.16889v1",
                published=datetime(2026, 8, 17, tzinfo=timezone.utc),
                feed_name="arXiv",
                topics=("agents",),
                summary="A full abstract.",
                authors=("Ada Lovelace",),
                categories=("cs.AI",),
            )
            now = datetime(2026, 8, 19, 12, tzinfo=timezone.utc)
            batch, count = write_week_batch(root, [entry], [], now, "2026-W34")
            self.assertEqual(count, 1)
            index = batch / "index.md"
            content = index.read_text(encoding="utf-8")
            self.assertIn("<!-- aidb:id=arxiv:2608.16889v1 -->", content)
            self.assertIn("A full abstract.", content)
            self.assertTrue((batch / "manifest.json").exists())

            index.write_text(content.replace("- [ ] **[Paper]", "- [n] **[Paper]"), encoding="utf-8")
            write_week_batch(root, [entry], [], now, "2026-W34")
            rerendered = index.read_text(encoding="utf-8")
            self.assertIn("- [n] **[Paper]", rerendered)
            self.assertEqual(
                parse_card_states(rerendered)["arxiv:2608.16889v1"].marker,
                "n",
            )
            manifest = json.loads((batch / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["entries"][0]["paper_version_id"], "2608.16889v1")

    def test_previous_version_is_suppressed_but_new_revision_is_surfaced(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            previous = root / "inbox" / "2026-W33"
            previous.mkdir(parents=True)
            (previous / "manifest.json").write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "id": "arxiv:2608.16889v1",
                                "paper_id": "2608.16889",
                                "paper_version_id": "2608.16889v1",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            now = datetime(2026, 8, 19, tzinfo=timezone.utc)
            entries = [
                Entry("Old", "https://arxiv.org/abs/2608.16889v1", now, "arXiv", ("agents",)),
                Entry("Revision", "https://arxiv.org/abs/2608.16889v2", now, "arXiv", ("agents",)),
            ]

            batch, _ = write_week_batch(root, entries, [], now, "2026-W34")

            content = (batch / "index.md").read_text(encoding="utf-8")
            self.assertNotIn("**[Old]", content)
            self.assertIn("**[Revision]", content)
            self.assertIn("новая версия", content)
            self.assertIn("1 уже встречавшихся", content)
            manifest = json.loads((batch / "manifest.json").read_text(encoding="utf-8"))
            statuses = {item["id"]: item["status"] for item in manifest["entries"]}
            self.assertEqual(statuses["arxiv:2608.16889v1"], "already-seen")
            self.assertEqual(statuses["arxiv:2608.16889v2"], "revision")

    def test_fetching_current_batch_does_not_hide_it_on_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            now = datetime(2026, 8, 19, tzinfo=timezone.utc)
            entry = Entry("Paper", "https://arxiv.org/abs/2608.16889v1", now, "arXiv", ())
            batch, _ = write_week_batch(root, [entry], [], now, "2026-W34")
            version = root / "papers/arxiv/2608.16889/versions/v1/manifest.json"
            version.parent.mkdir(parents=True)
            version.write_text("{}")
            write_week_batch(root, [entry], [], now, "2026-W34")
            self.assertIn("**[Paper]", (batch / "index.md").read_text())

    def test_legacy_inbox_and_downloaded_versions_are_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "inbox").mkdir()
            (root / "inbox/2026-08-17.md").write_text(
                "- [ ] **[Old](https://arxiv.org/pdf/2608.16889v1.pdf)**\n"
            )
            version = root / "papers/arxiv/2608.16890/versions/v1/manifest.json"
            version.parent.mkdir(parents=True)
            version.write_text("{}")
            now = datetime(2026, 8, 19, tzinfo=timezone.utc)
            entries = [
                Entry("Legacy", "https://arxiv.org/abs/2608.16889v1", now, "arXiv", ()),
                Entry("Downloaded", "https://arxiv.org/abs/2608.16890v1", now, "arXiv", ()),
                Entry("Revised", "https://arxiv.org/abs/2608.16889v2", now, "arXiv", ()),
            ]
            batch, _ = write_week_batch(root, entries, [], now, "2026-W34")
            content = (batch / "index.md").read_text()
            self.assertNotIn("**[Legacy]", content)
            self.assertNotIn("**[Downloaded]", content)
            self.assertIn("**[Revised]", content)

    def test_refresh_preserves_summary_status_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            now = datetime(2026, 8, 19, tzinfo=timezone.utc)
            entry = Entry("Paper", "https://arxiv.org/abs/2608.16889v1", now, "arXiv", ())
            report = {"complete": True, "since": "2026-08-01", "until": "2026-08-19"}
            batch, _ = write_week_batch(root, [entry], [], now, "2026-W34", discovery=report)
            manifest = json.loads((batch / "manifest.json").read_text())
            manifest["entries"][0].update(status="summarized", decision="note")
            (batch / "manifest.json").write_text(json.dumps(manifest))
            index = batch / "index.md"
            index.write_text(index.read_text().replace(
                "- [ ] **[Paper](https://arxiv.org/abs/2608.16889v1)**",
                "- [x] **[Paper](https://arxiv.org/abs/2608.16889v1)**\n  - Triage: note",
            ))
            self.assertEqual(parse_card_states(index.read_text())["arxiv:2608.16889v1"].fields["Triage"], "note")
            write_week_batch(root, [entry], [], now, "2026-W34")
            updated = json.loads((batch / "manifest.json").read_text())
            self.assertEqual(updated["entries"][0]["status"], "summarized")
            self.assertEqual(updated["discovery"], report)
            self.assertIn("полное для настроенных источников", index.read_text())


if __name__ == "__main__":
    unittest.main()
