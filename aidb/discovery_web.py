"""Dated publisher indexes whose sitemap modification dates are not publications."""

from datetime import datetime, timezone
import html
import json
import re


def anthropic_engineering(feed, client, cutoff, until, coverage):
    from scripts.refresh_inbox import Entry, parse_date

    if feed["url"] != "https://www.anthropic.com/engineering":
        raise ValueError("unsupported engineering index URL")
    body, _ = client.get(feed["url"])
    cards = re.findall(r'<article\b[^>]*data-listing-row="[^"]+"[^>]*>(.*?)</article>', body.decode(), re.S)
    if not cards:
        raise ValueError("engineering index has no dated article cards")
    coverage.update(pages=1, scope="Engineering index by publication date; other teams and revisions excluded")
    dates = []
    links = set()
    for card in cards:
        date_match = re.search(r'<time[^>]*>([^<]+)</time>', card)
        link_match = re.search(r'href="(/research/[^"?#]+)"', card)
        if not date_match or not link_match:
            raise ValueError("engineering card is missing its publication date or article link")
        date = datetime.strptime(date_match[1], "%b %d, %Y").replace(tzinfo=timezone.utc)
        dates.append(date)
        url = "https://www.anthropic.com" + html.unescape(link_match[1])
        if url in links:
            raise ValueError("engineering index repeats an article card")
        links.add(url)
        # Listing dates have day precision; confirm exact timestamps on the article.
        if date.date() < cutoff.date() or date.date() > until.date():
            continue
        article, _ = client.get(url)
        coverage["pages"] += 1
        scripts = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', article.decode(), re.S)
        metadata = [json.loads(script) for script in scripts]
        article_meta = next((value for value in metadata if isinstance(value, dict) and value.get("@type") == "Article"), None)
        if not article_meta or article_meta.get("url") != url:
            raise ValueError("engineering article has no matching canonical Article metadata")
        published = parse_date(article_meta.get("datePublished", ""))
        if published is None or published.date() != date.date():
            raise ValueError("engineering article publication date disagrees with index")
        yield Entry(
            title=article_meta["headline"], url=url, published=published,
            feed_name=feed["name"], topics=tuple(feed.get("topics", [])),
            summary=article_meta.get("description", ""), authors=("Anthropic",),
        )
    if dates != sorted(dates, reverse=True):
        raise ValueError("engineering index is not ordered by publication date")
    coverage["oldest_scanned"] = min(dates).isoformat()
    coverage["records_in_snapshot"] = len(cards)
    if min(dates) >= cutoff:
        raise ValueError("engineering index needs pagination to reach the requested window; adapter cannot prove coverage")
    coverage["stop_reason"] = "dated Engineering index crossed the publication window boundary"
