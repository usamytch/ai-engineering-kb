#!/usr/bin/env python3
"""Collect recent Atom/RSS entries into a review-only Markdown inbox."""

from __future__ import annotations

import argparse
import email.utils
import html
import json
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

from aidb.weekly import current_iso_week, write_week_batch


ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "ai-engineering-kb-discovery/1.0 (+https://github.com/usamytch)"


@dataclass(frozen=True)
class Entry:
    title: str
    url: str
    published: datetime | None
    feed_name: str
    topics: tuple[str, ...]
    updated: datetime | None = None
    summary: str = ""
    authors: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()
    doi: str = ""
    journal_ref: str = ""
    comment: str = ""
    license_url: str = ""


class FeedParser(HTMLParser):
    """Small Atom/RSS parser that avoids platform-specific XML libraries."""

    TEXT_FIELDS = {
        "title",
        "published",
        "updated",
        "pubdate",
        "date",
        "created",
        "guid",
        "id",
        "link",
        "summary",
        "description",
        "name",
        "arxiv:doi",
        "arxiv:journal_ref",
        "arxiv:comment",
        "arxiv:license",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.items: list[dict[str, object]] = []
        self.current: dict[str, object] | None = None
        self.stack: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        self.stack.append(tag)
        if tag in {"entry", "item"}:
            self.current = {"fields": {}, "links": []}
            return
        if self.current is None or tag != "link":
            if self.current is not None and tag in {"category", "arxiv:primary_category"}:
                term = (dict(attrs).get("term") or "").strip()
                if term:
                    categories = self.current.setdefault("categories", [])
                    assert isinstance(categories, list)
                    categories.append(term)
            return
        attributes = dict(attrs)
        href = (attributes.get("href") or "").strip()
        if href:
            links = self.current["links"]
            assert isinstance(links, list)
            links.append((attributes.get("rel") or "alternate", href))

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self.current is None or not self.stack:
            return
        field = self.stack[-1]
        if field not in self.TEXT_FIELDS:
            return
        fields = self.current["fields"]
        assert isinstance(fields, dict)
        fields.setdefault(field, []).append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"entry", "item"} and self.current is not None:
            self.items.append(self.current)
            self.current = None
        if tag in self.stack:
            reverse_index = self.stack[::-1].index(tag)
            del self.stack[len(self.stack) - 1 - reverse_index :]


def field_text(item: dict[str, object], names: tuple[str, ...]) -> str:
    fields = item["fields"]
    assert isinstance(fields, dict)
    for name in names:
        parts = fields.get(name, [])
        if isinstance(parts, list):
            value = " ".join(" ".join(str(part).split()) for part in parts).strip()
            if value:
                return html.unescape(value)
    return ""


def item_link(item: dict[str, object]) -> str:
    links = item["links"]
    assert isinstance(links, list)
    for rel, href in links:
        if rel == "alternate":
            return str(href)
    if links:
        return str(links[0][1])
    return field_text(item, ("link", "guid", "id"))


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_feed(payload: bytes, feed: dict[str, object]) -> list[Entry]:
    parser = FeedParser()
    parser.feed(payload.decode("utf-8", errors="replace"))
    result: list[Entry] = []
    for item in parser.items:
        title = field_text(item, ("title",)) or "Untitled"
        url = item_link(item)
        date_text = field_text(
            item, ("published", "updated", "pubdate", "date", "created")
        )
        updated_text = field_text(item, ("updated",))
        fields = item["fields"]
        assert isinstance(fields, dict)
        author_parts = fields.get("name", [])
        authors = tuple(
            html.unescape(" ".join(str(part).split()))
            for part in author_parts
            if str(part).strip()
        ) if isinstance(author_parts, list) else ()
        category_parts = item.get("categories", [])
        categories = tuple(str(part) for part in category_parts) if isinstance(category_parts, list) else ()
        if not url:
            continue
        result.append(
            Entry(
                title=title,
                url=url,
                published=parse_date(date_text),
                feed_name=str(feed["name"]),
                topics=tuple(str(topic) for topic in feed.get("topics", [])),
                updated=parse_date(updated_text),
                summary=field_text(item, ("summary", "description")),
                authors=authors,
                categories=categories,
                doi=field_text(item, ("arxiv:doi",)),
                journal_ref=field_text(item, ("arxiv:journal_ref",)),
                comment=field_text(item, ("arxiv:comment",)),
                license_url=field_text(item, ("arxiv:license",)),
            )
        )
    return result


def fetch(feed: dict[str, object], timeout: float) -> list[Entry]:
    request = urllib.request.Request(
        str(feed["url"]),
        headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml, application/rss+xml, application/xml, text/xml"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return parse_feed(response.read(), feed)


def render(
    entries: list[Entry], errors: list[tuple[str, str]], generated_at: datetime
) -> str:
    lines = [
        f"# Discovery inbox — {generated_at.date().isoformat()}",
        "",
        "> Автоматическая подборка. Запись не считается проверенной и не меняет adoption status.",
        ">",
        "> Checkbox: `[ ]` — не разобрано; `[d]` — drop; `[w]` — watch; `[n]` — note; `[r]` — review; `[x]` — обработано (ставит `make triage`).",
        "",
        f"Сгенерировано: {generated_at.isoformat(timespec='seconds')}",
        "",
        "## Кандидаты",
        "",
    ]
    if not entries:
        lines.extend(["Свежих записей в заданном окне не найдено.", ""])
    for entry in entries:
        published = entry.published.date().isoformat() if entry.published else "date unknown"
        topics = ", ".join(entry.topics)
        lines.extend(
            [
                f"- [ ] **[{entry.title}]({entry.url})**",
                f"  - Feed: {entry.feed_name}",
                f"  - Published: {published}",
                f"  - Topics: {topics}",
            ]
        )
    if errors:
        lines.extend(["", "## Ошибки feeds", ""])
        for name, error in errors:
            lines.append(f"- **{name}:** `{error}`")
    lines.extend(
        [
            "",
            "## После triage",
            "",
            "Проверить первоисточник, claim и ограничения. Важное переносить в `SOURCES.md` и тематический раздел; изменение позиции — отдельно в `ADOPTION.md` и `CHANGELOG.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=14, help="lookback window")
    parser.add_argument("--limit-per-feed", type=int, default=10)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--week", help="ISO week YYYY-Www; defaults to current week")
    parser.add_argument(
        "--legacy-flat",
        action="store_true",
        help="write the old inbox/YYYY-MM-DD.md format",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def collect_entries(
    root: Path,
    *,
    days: int = 14,
    limit_per_feed: int = 10,
    timeout: float = 20.0,
    now: datetime | None = None,
) -> tuple[datetime, list[Entry], list[tuple[str, str]], int]:
    if days < 1 or limit_per_feed < 1 or timeout <= 0:
        raise ValueError("days, limit-per-feed and timeout must be positive")
    watchlist = json.loads((root / "watchlist.json").read_text(encoding="utf-8"))
    generated_at = now or datetime.now(timezone.utc)
    cutoff = generated_at - timedelta(days=days)
    entries: list[Entry] = []
    errors: list[tuple[str, str]] = []

    for feed in watchlist["feeds"]:
        try:
            recent = [
                entry
                for entry in fetch(feed, timeout)
                if (entry.updated or entry.published) is None
                or (entry.updated or entry.published) >= cutoff
            ][:limit_per_feed]
            entries.extend(recent)
        except (OSError, KeyError, ValueError, UnicodeError) as exc:
            errors.append((str(feed.get("name", "unknown feed")), str(exc)))

    unique: dict[str, Entry] = {}
    for entry in entries:
        unique.setdefault(entry.url, entry)
    entries = sorted(
        unique.values(),
        key=lambda item: item.updated
        or item.published
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    return generated_at, entries, errors, len(watchlist["feeds"])


def main() -> int:
    args = parse_args()
    try:
        now, entries, errors, feed_count = collect_entries(
            ROOT,
            days=args.days,
            limit_per_feed=args.limit_per_feed,
            timeout=args.timeout,
        )
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"discovery failed: {exc}", file=sys.stderr)
        return 2

    content = render(entries, errors, now)
    if args.dry_run:
        if args.legacy_flat:
            print(content)
        else:
            from aidb.weekly import Candidate, merge_candidates, render_week_index

            candidates = merge_candidates(Candidate.from_entry(entry) for entry in entries)
            print(render_week_index(args.week or current_iso_week(now), candidates, errors, now))
        return 0 if entries or len(errors) < feed_count else 1

    if args.output or args.legacy_flat:
        output = args.output or ROOT / "inbox" / f"{now.date().isoformat()}.md"
        if not output.is_absolute():
            output = ROOT / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        destination = output.relative_to(ROOT)
    else:
        batch_dir, _ = write_week_batch(ROOT, entries, errors, now, args.week)
        destination = batch_dir.relative_to(ROOT)
    print(f"Wrote {len(entries)} entries to {destination}; {len(errors)} feed errors")
    return 0 if entries or len(errors) < feed_count else 1


if __name__ == "__main__":
    sys.exit(main())
