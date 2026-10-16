"""Paginated discovery with explicit coverage and resumable response caching."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from aidb.weekly import source_id


class DiscoveryClient:
    def __init__(self, timeout: float, cache_dir: Path | None = None):
        self.timeout = timeout
        self.cache_dir = cache_dir
        self.last_request = 0.0

    def get(self, url: str) -> tuple[bytes, dict[str, str]]:
        cache = None
        if self.cache_dir:
            cache = self.cache_dir / (hashlib.sha256(url.encode()).hexdigest() + ".json")
            if cache.exists():
                stored = json.loads(cache.read_text(encoding="utf-8"))
                if stored["url"] != url:
                    raise ValueError("discovery cache URL mismatch")
                return stored["body"].encode("utf-8"), stored["headers"]
        for attempt in range(3):
            delay = 3.0 - (time.monotonic() - self.last_request)
            if delay > 0:
                time.sleep(delay)
            self.last_request = time.monotonic()
            request = Request(url, headers={
                "User-Agent": "ai-engineering-kb-discovery/2.0 (+https://github.com/usamytch/ai-engineering-kb)",
                "Accept": "application/atom+xml, application/vnd.github+json, application/xml",
            })
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    body = response.read()
                    headers = {key.lower(): value for key, value in response.headers.items()}
                if cache:
                    cache.parent.mkdir(parents=True, exist_ok=True)
                    cache.write_text(json.dumps({
                        "url": url, "headers": headers, "body": body.decode("utf-8"),
                    }, ensure_ascii=False), encoding="utf-8")
                return body, headers
            except (HTTPError, URLError, TimeoutError) as error:
                if isinstance(error, HTTPError) and error.code not in {429, 500, 502, 503, 504}:
                    raise
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))
        raise RuntimeError("unreachable request state")


def feed_entries(feed, client, cutoff, until, page_size, coverage):
    """Yield records before completion, retaining partial results after errors."""
    from scripts.refresh_inbox import parse_feed

    parsed = urlsplit(str(feed["url"]))
    if parsed.hostname in {"arxiv.org", "export.arxiv.org"} and parsed.path == "/api/query":
        yield from _arxiv_entries(feed, client, cutoff, page_size, coverage)
    elif parsed.hostname == "github.com" and parsed.path.endswith("/releases.atom"):
        yield from _github_entries(feed, client, coverage)
    else:
        body, _ = client.get(str(feed["url"]))
        coverage["pages"] = 1
        yield from parse_feed(body, feed)
        coverage["stop_reason"] = "unpaginated feed; historical completeness unknown"
        return
    coverage["complete"] = True


def _arxiv_entries(feed, client, cutoff, page_size, coverage):
    from scripts.refresh_inbox import parse_feed

    parsed = urlsplit(str(feed["url"]))
    query = dict(parse_qsl(parsed.query))
    query.update(sortBy="lastUpdatedDate", sortOrder="descending", max_results=str(page_size))
    start = 0
    seen_pages = set()
    previous_date = None
    while start < 30000:
        query["start"] = str(start)
        url = urlunsplit(("https", parsed.netloc, parsed.path, urlencode(query), ""))
        body, _ = client.get(url)
        xml = ET.fromstring(body)
        total = xml.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
        if total is None:
            raise ValueError("arXiv response has no totalResults (possible API error)")
        offset = xml.findtext("{http://a9.com/-/spec/opensearch/1.1/}startIndex")
        if offset is not None and int(offset) != start:
            raise ValueError("arXiv returned an unexpected page offset")
        coverage["total_results"] = int(total)
        coverage["pages"] += 1
        entries = parse_feed(body, feed)
        signature = tuple(source_id(entry.url) for entry in entries)
        if signature in seen_pages:
            raise ValueError("arXiv repeated a page; discovery is incomplete")
        seen_pages.add(signature)
        print(f"{feed['name']}: page {coverage['pages']}, offset {start}, records {len(entries)}", file=sys.stderr, flush=True)
        if not entries:
            if start < int(total):
                raise ValueError("arXiv returned an empty page before totalResults")
            coverage["stop_reason"] = "all results exhausted"
            return
        dates = [entry.updated or entry.published for entry in entries]
        if any(value is None for value in dates):
            raise ValueError("arXiv entry has no date; cannot prove window coverage")
        if dates != sorted(dates, reverse=True) or (previous_date and dates[0] > previous_date):
            raise ValueError("arXiv pages are not ordered by update date")
        previous_date = dates[-1]
        yield from entries
        if dates[-1] < cutoff:
            coverage["stop_reason"] = "reached records older than requested window"
            coverage["oldest_scanned"] = dates[-1].isoformat()
            return
        start += len(entries)
        if start >= int(total):
            coverage["stop_reason"] = "all results exhausted"
            return
    raise ValueError("arXiv 30000-result API boundary reached before window boundary")


def _github_entries(feed, client, coverage):
    from scripts.refresh_inbox import Entry, parse_date

    parts = urlsplit(str(feed["url"])).path.strip("/").split("/")
    if len(parts) != 3:
        raise ValueError("invalid GitHub releases feed URL")
    owner, repo, _ = parts
    url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=100&page=1"
    seen_urls = set()
    while url:
        if url in seen_urls:
            raise ValueError("GitHub repeated a pagination link")
        seen_urls.add(url)
        body, headers = client.get(url)
        records = json.loads(body)
        if not isinstance(records, list):
            raise ValueError("GitHub releases response is not a list")
        coverage["pages"] += 1
        print(f"{feed['name']}: page {coverage['pages']}, records {len(records)}", file=sys.stderr, flush=True)
        for record in records:
            if record.get("draft"):
                continue
            published = parse_date(record.get("published_at") or "")
            updated = parse_date(record.get("updated_at") or "") or published
            if updated is None:
                raise ValueError("GitHub release has no date; cannot prove window coverage")
            yield Entry(
                title=record.get("name") or record["tag_name"],
                url=record["html_url"],
                published=published,
                updated=updated,
                feed_name=str(feed["name"]),
                topics=tuple(feed.get("topics", [])),
                summary=record.get("body") or "",
                authors=(record.get("author", {}).get("login", ""),),
            )
        match = re.search(r'<([^>]+)>;\s*rel="next"', headers.get("link", ""))
        url = match.group(1) if match else ""
        if url and (urlsplit(url).scheme != "https" or urlsplit(url).hostname != "api.github.com"):
            raise ValueError("unexpected GitHub pagination destination")
    coverage["stop_reason"] = "all release pages exhausted"


def collect_paginated(root, feeds, *, cutoff, until, limit, page_size, timeout, cache_dir, report):
    if not 1 <= page_size <= 2000:
        raise ValueError("page-size must be between 1 and 2000")
    if limit < 0:
        raise ValueError("limit-per-feed must be non-negative")
    if cutoff > until:
        raise ValueError("since must not be later than the collection time")
    client = DiscoveryClient(timeout, cache_dir)
    entries = []
    errors = []
    report.update({
        "since": cutoff.isoformat(), "until": until.isoformat(),
        "limit_per_feed": limit, "page_size": page_size, "feeds": [],
        "window_basis": "latest update, falling back to publication date",
    })
    for feed in feeds:
        coverage = {"feed": str(feed["name"]), "pages": 0, "selected": 0, "complete": False}
        report["feeds"].append(coverage)
        seen = set()
        try:
            for entry in feed_entries(feed, client, cutoff, until, page_size, coverage):
                date = entry.updated or entry.published
                if date is not None and not cutoff <= date <= until:
                    continue
                key = source_id(entry.url)
                if key in seen:
                    continue
                if limit and len(seen) >= limit:
                    coverage["stop_reason"] = "explicit per-feed limit reached"
                    break
                seen.add(key)
                entries.append(entry)
                coverage["selected"] += 1
            if not coverage["complete"]:
                errors.append((str(feed["name"]), coverage.get("stop_reason", "incomplete pagination")))
        except (OSError, ValueError, KeyError, ET.ParseError) as error:
            coverage["error"] = str(error)
            errors.append((str(feed["name"]), str(error)))
    report["complete"] = not errors
    return entries, errors
