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


ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "ai-engineering-kb-discovery/1.0 (+https://github.com/usamytch)"


@dataclass(frozen=True)
class Entry:
    title: str
    url: str
    published: datetime | None
    feed_name: str
    topics: tuple[str, ...]


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
        if not url:
            continue
        result.append(
            Entry(
                title=title,
                url=url,
                published=parse_date(date_text),
                feed_name=str(feed["name"]),
                topics=tuple(str(topic) for topic in feed.get("topics", [])),
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
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.days < 1 or args.limit_per_feed < 1 or args.timeout <= 0:
        print("days, limit-per-feed and timeout must be positive", file=sys.stderr)
        return 2

    watchlist = json.loads((ROOT / "watchlist.json").read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=args.days)
    entries: list[Entry] = []
    errors: list[tuple[str, str]] = []

    for feed in watchlist["feeds"]:
        try:
            recent = [
                entry
                for entry in fetch(feed, args.timeout)
                if entry.published is None or entry.published >= cutoff
            ][: args.limit_per_feed]
            entries.extend(recent)
        except (OSError, KeyError, ValueError, UnicodeError) as exc:
            errors.append((str(feed.get("name", "unknown feed")), str(exc)))

    unique: dict[str, Entry] = {}
    for entry in entries:
        unique.setdefault(entry.url, entry)
    entries = sorted(
        unique.values(),
        key=lambda item: item.published or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    content = render(entries, errors, now)
    if args.dry_run:
        print(content)
        return 0 if entries or len(errors) < len(watchlist["feeds"]) else 1

    output = args.output or ROOT / "inbox" / f"{now.date().isoformat()}.md"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {output.relative_to(ROOT)}; {len(errors)} feed errors")
    return 0 if entries or len(errors) < len(watchlist["feeds"]) else 1


if __name__ == "__main__":
    sys.exit(main())
