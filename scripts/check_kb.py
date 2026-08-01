#!/usr/bin/env python3
"""Fast, dependency-free structural checks for the Markdown knowledge base."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REQUIRED_DATED = [
    ROOT / "PROCESS.md",
    ROOT / "ADOPTION.md",
    ROOT / "SOURCES.md",
    *sorted((ROOT / "knowledge").glob("*.md")),
]


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and ".venv" not in path.parts
    )


def local_target(raw: str, source: Path) -> Path | None:
    target = raw.strip().split(maxsplit=1)[0].strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith(("#", "mailto:")):
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    return (source.parent / path_text).resolve()


def main() -> int:
    errors: list[str] = []
    files = markdown_files()

    if not files:
        errors.append("no Markdown files found")

    for path in files:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            errors.append(f"empty file: {path.relative_to(ROOT)}")
        for raw in LINK_RE.findall(text):
            target = local_target(raw, path)
            if target is not None and not target.exists():
                errors.append(
                    f"broken local link in {path.relative_to(ROOT)}: {raw}"
                )

    for path in REQUIRED_DATED:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if "2026-" not in text and "**Обновлено:**" not in text and "**Проверено:**" not in text:
            errors.append(f"missing review date: {path.relative_to(ROOT)}")

    watchlist_path = ROOT / "watchlist.json"
    try:
        watchlist = json.loads(watchlist_path.read_text(encoding="utf-8"))
        feeds = watchlist["feeds"]
        if not isinstance(feeds, list) or not feeds:
            errors.append("watchlist.json must contain a non-empty feeds list")
        for index, feed in enumerate(feeds):
            for field in ("name", "url", "topics"):
                if field not in feed or not feed[field]:
                    errors.append(f"watchlist feed #{index + 1} misses {field}")
            if not str(feed.get("url", "")).startswith("https://"):
                errors.append(f"watchlist feed #{index + 1} must use https")
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append(f"invalid watchlist.json: {exc}")

    if errors:
        print("KB checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"KB checks passed: {len(files)} Markdown files, {len(feeds)} feeds")
    return 0


if __name__ == "__main__":
    sys.exit(main())

