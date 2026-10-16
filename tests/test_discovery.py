from datetime import datetime, timezone
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from aidb.discovery import collect_paginated
from scripts.refresh_inbox import parse_since


NOW = datetime(2026, 10, 16, tzinfo=timezone.utc)
CUTOFF = datetime(2026, 9, 16, tzinfo=timezone.utc)
FEED = {"name": "arXiv", "url": "https://export.arxiv.org/api/query?search_query=all:agent&max_results=40", "topics": ["agents"]}


def atom(records, start=0, total=100):
    entries = "".join(
        f'<entry><title>Paper</title><id>https://arxiv.org/abs/{ref}</id>'
        f'<published>2026-08-01T00:00:00Z</published><updated>{updated}</updated>'
        f'<link href="https://arxiv.org/abs/{ref}" /></entry>'
        for ref, updated in records
    )
    return (
        '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
        f'<opensearch:totalResults>{total}</opensearch:totalResults>'
        f'<opensearch:startIndex>{start}</opensearch:startIndex>{entries}</feed>'
    ).encode(), {}


class DiscoveryTest(unittest.TestCase):
    def collect(self, replies, feeds=None, limit=0):
        report = {}
        with patch("aidb.discovery.DiscoveryClient.get", side_effect=replies) as get:
            entries, errors = collect_paginated(
                Path("."), feeds or [FEED], cutoff=CUTOFF, until=NOW,
                limit=limit, page_size=2, timeout=20, cache_dir=None, report=report,
            )
        return entries, errors, report, get

    def test_pages_continue_until_cutoff_and_include_revisions(self):
        entries, errors, report, get = self.collect([
            atom([("2608.16889v2", "2026-10-15T00:00:00Z"), ("2610.12345v1", "2026-10-14T00:00:00Z")]),
            atom([("2609.10001v1", "2026-09-16T00:00:00Z"), ("2609.10002v1", "2026-09-15T00:00:00Z")], start=2),
        ])
        self.assertEqual(len(entries), 3)
        self.assertEqual(errors, [])
        self.assertTrue(report["complete"])
        query = parse_qs(urlsplit(get.call_args_list[1].args[0]).query)
        self.assertEqual(query["start"], ["2"])
        self.assertEqual(query["sortBy"], ["lastUpdatedDate"])
        self.assertEqual(query["max_results"], ["2"])

    def test_overlapping_pages_are_deduplicated(self):
        entries, errors, _, _ = self.collect([
            atom([("2610.12345v1", "2026-10-14T00:00:00Z"), ("2610.12346v1", "2026-10-13T00:00:00Z")]),
            atom([("2610.12346v1", "2026-10-13T00:00:00Z"), ("2609.10002v1", "2026-09-15T00:00:00Z")], start=2),
        ])
        self.assertEqual(len(entries), 2)
        self.assertEqual(errors, [])

    def test_failure_keeps_partial_entries_and_marks_incomplete(self):
        entries, errors, report, _ = self.collect([
            atom([("2610.12345v1", "2026-10-14T00:00:00Z")]),
            OSError("network failure"),
        ])
        self.assertEqual(len(entries), 1)
        self.assertEqual(len(errors), 1)
        self.assertFalse(report["complete"])

    def test_empty_page_before_total_is_not_success(self):
        _, errors, report, _ = self.collect([atom([])])
        self.assertIn("empty page", errors[0][1])
        self.assertFalse(report["complete"])

    def test_explicit_cap_is_not_claimed_as_complete(self):
        entries, errors, report, _ = self.collect([
            atom([("2610.12345v1", "2026-10-14T00:00:00Z"), ("2610.12346v1", "2026-10-13T00:00:00Z")]),
        ], limit=1)
        self.assertEqual(len(entries), 1)
        self.assertFalse(report["complete"])
        self.assertIn("limit", errors[0][1])

    def test_github_follows_links_even_after_old_release(self):
        feed = {"name": "Releases", "url": "https://github.com/example/repo/releases.atom"}
        next_url = "https://api.github.com/repos/example/repo/releases?per_page=100&page=2"
        old = {"name": "old", "html_url": "https://github.com/example/repo/releases/tag/old", "published_at": "2026-08-01T00:00:00Z"}
        new = {"name": "new", "html_url": "https://github.com/example/repo/releases/tag/new", "published_at": "2026-10-01T00:00:00Z"}
        entries, errors, report, get = self.collect([
            (json.dumps([old]).encode(), {"link": f'<{next_url}>; rel="next"'}),
            (json.dumps([new]).encode(), {}),
        ], feeds=[feed])
        self.assertEqual([entry.title for entry in entries], ["new"])
        self.assertEqual(get.call_count, 2)
        self.assertTrue(report["complete"])
        self.assertEqual(errors, [])

    def test_repeated_arxiv_page_is_incomplete(self):
        records = [("2610.12345v1", "2026-10-14T00:00:00Z")]
        entries, errors, report, _ = self.collect([atom(records), atom(records, start=1)])
        self.assertEqual(len(entries), 1)
        self.assertIn("repeated a page", errors[0][1])
        self.assertFalse(report["complete"])

    def test_wrong_offset_and_unordered_dates_are_incomplete(self):
        cases = [
            atom([("2610.12345v1", "2026-10-14T00:00:00Z")], start=5),
            atom([("2610.12345v1", "2026-10-13T00:00:00Z"), ("2610.12346v1", "2026-10-14T00:00:00Z")]),
        ]
        for response in cases:
            with self.subTest(response=response):
                _, errors, report, _ = self.collect([response])
                self.assertTrue(errors)
                self.assertFalse(report["complete"])

    def test_github_requires_dates_and_rejects_foreign_next_link(self):
        feed = {"name": "Releases", "url": "https://github.com/example/repo/releases.atom"}
        cases = [
            (json.dumps([{"name": "undated", "html_url": "https://example.com"}]).encode(), {}),
            (b"[]", {"link": '<https://example.com/private>; rel="next"'}),
        ]
        for response in cases:
            with self.subTest(response=response):
                _, errors, report, get = self.collect([response], feeds=[feed])
                self.assertTrue(errors)
                self.assertFalse(report["complete"])
                self.assertEqual(get.call_count, 1)

    def test_other_feeds_continue_after_source_failure(self):
        entries, errors, report, _ = self.collect([
            OSError("network failure"),
            atom([("2610.12345v1", "2026-10-14T00:00:00Z")], total=1),
        ], feeds=[FEED, {**FEED, "name": "second"}])
        self.assertEqual(len(entries), 1)
        self.assertEqual(len(errors), 1)
        self.assertFalse(report["complete"])
        self.assertTrue(report["feeds"][1]["complete"])

    def test_future_updates_are_excluded_without_ending_pagination(self):
        entries, errors, report, _ = self.collect([
            atom([("2610.12345v1", "2026-10-17T00:00:00Z"), ("2610.12346v1", "2026-10-14T00:00:00Z")], total=2),
        ])
        self.assertEqual([entry.url for entry in entries], ["https://arxiv.org/abs/2610.12346v1"])
        self.assertEqual(errors, [])
        self.assertTrue(report["complete"])

    def test_plain_feed_does_not_claim_historical_completeness(self):
        feed = {"name": "RSS", "url": "https://example.com/feed.xml"}
        entries, errors, report, _ = self.collect([
            atom([("2610.12345v1", "2026-10-14T00:00:00Z")], total=1),
        ], feeds=[feed])
        self.assertEqual(len(entries), 1)
        self.assertFalse(report["complete"])
        self.assertIn("historical completeness unknown", errors[0][1])

    def test_since_dates_are_normalized_to_utc(self):
        self.assertEqual(parse_since("2026-09-16"), CUTOFF)
        self.assertEqual(parse_since("2026-09-16T03:00:00+03:00"), CUTOFF)


if __name__ == "__main__":
    unittest.main()
