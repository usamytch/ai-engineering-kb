from __future__ import annotations

import unittest
from datetime import datetime, timezone

from scripts.refresh_inbox import Entry, render


class RefreshInboxTest(unittest.TestCase):
    def test_render_uses_checkbox_as_the_only_manual_triage_input(self) -> None:
        generated_at = datetime(2026, 8, 4, 12, 0, tzinfo=timezone.utc)
        entry = Entry(
            title="Example",
            url="https://example.com/article",
            published=generated_at,
            feed_name="Test feed",
            topics=("agents", "rag"),
        )

        content = render([entry], [], generated_at)

        self.assertIn("- [ ] **[Example](https://example.com/article)**", content)
        self.assertIn("`[d]` — drop", content)
        self.assertIn("`[w]` — watch", content)
        self.assertIn("`[n]` — note", content)
        self.assertIn("`[r]` — review", content)
        self.assertIn("`[x]` — обработано", content)
        self.assertNotIn("Triage:", content)

    def test_legacy_render_deduplicates_canonical_versions_across_feeds(self) -> None:
        generated_at = datetime(2026, 10, 16, tzinfo=timezone.utc)
        entries = [
            Entry("Paper", "https://arxiv.org/abs/2610.12345v1", generated_at, "first", ()),
            Entry("Paper PDF", "https://arxiv.org/pdf/2610.12345v1.pdf", generated_at, "second", ()),
            Entry("Revision", "https://arxiv.org/abs/2610.12345v2", generated_at, "first", ()),
        ]
        content = render(entries, [], generated_at)
        self.assertEqual(content.count("- [ ] **["), 2)
        self.assertIn("**[Revision]", content)


if __name__ == "__main__":
    unittest.main()
