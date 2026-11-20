from datetime import datetime, timezone
import json
import unittest
from unittest.mock import Mock

from aidb.discovery_web import anthropic_engineering


class EngineeringIndexTest(unittest.TestCase):
    def collect(self, old_date="Oct 13, 2026", article_date="2026-11-06T00:00:00Z"):
        feed = {"name": "Anthropic", "url": "https://www.anthropic.com/engineering"}
        card = '<article data-listing-row="{}"><time>{}</time><a href="/research/{}">Title</a></article>'
        index = card.format("new", "Nov 6, 2026", "memory") + card.format("old", old_date, "old")
        article = {
            "@type": "Article", "url": "https://www.anthropic.com/research/memory",
            "headline": "Memory", "description": "A memory study", "datePublished": article_date,
            "dateModified": "2026-11-19T00:00:00Z",
        }
        payload = '<script type="application/ld+json">' + json.dumps(article) + '</script>'
        client = Mock()
        client.get.side_effect = [(index.encode(), {}), (payload.encode(), {})]
        coverage = {}
        entries = list(anthropic_engineering(
            feed, client, datetime(2026, 10, 16, tzinfo=timezone.utc),
            datetime(2026, 11, 20, tzinfo=timezone.utc), coverage,
        ))
        return entries, coverage

    def test_publication_dates_are_verified_without_using_site_modification(self):
        entries, coverage = self.collect()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].published.day, 6)
        self.assertIsNone(entries[0].updated)
        self.assertEqual(coverage["pages"], 2)
        self.assertIn("other teams and revisions excluded", coverage["scope"])

    def test_changed_article_date_is_not_silently_accepted(self):
        with self.assertRaisesRegex(ValueError, "disagrees"):
            self.collect(article_date="2026-11-07T00:00:00Z")

    def test_unsorted_index_is_not_claimed_complete(self):
        with self.assertRaisesRegex(ValueError, "not ordered"):
            self.collect(old_date="Nov 25, 2026")


if __name__ == "__main__":
    unittest.main()
