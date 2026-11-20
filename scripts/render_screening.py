#!/usr/bin/env python3
"""Render a searchable, offline inbox only after complete screening validation."""

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aidb.domain import ArxivRef
from aidb.weekly import validate_week
from scripts.screen_inbox import digest, input_record, validate_records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", required=True, type=validate_week)
    args = parser.parse_args()
    batch = ROOT / "inbox" / args.week
    manifest = json.loads((batch / "manifest.json").read_text())
    since = datetime.fromisoformat(manifest["discovery"]["since"])
    entries = sorted(manifest["entries"], key=lambda entry: entry["id"])
    records = sorted((json.loads(line) for line in (batch / "screening.jsonl").read_text().splitlines()), key=lambda record: record["id"])
    inputs = [input_record(entry) for entry in entries]
    validate_records([{key: value for key, value in record.items() if key != "input_sha256"} for record in records], inputs)
    reviews = json.loads((batch / "web-reading.json").read_text())["articles"] if (batch / "web-reading.json").exists() else []
    web_notes = {review["id"]: review["note"] for review in reviews}
    rows = []
    for entry, record, source in zip(entries, records, inputs):
        if record["input_sha256"] != digest(source):
            raise ValueError(f"stale screening input: {entry['id']}")
        if not entry["url"].startswith(("https://", "http://")):
            raise ValueError("catalog source URL must use HTTP(S)")
        note = web_notes.get(entry["id"], "")
        if entry.get("paper_version_id") and entry.get("status") == "summarized":
            ref = ArxivRef.parse(entry["paper_version_id"])
            note = f"../../papers/arxiv/{ref.path_key}/versions/{ref.version_tag}/summary.md"
        if note and not (batch / note).is_file():
            raise ValueError(f"missing reading note: {note}")
        if entry["source_type"] == "paper":
            event = "new" if datetime.fromisoformat(entry["published"]) >= since else "revision"
        else:
            event = "release" if entry["source_type"] == "release" else "publication"
        rows.append({
            **record, "title": entry["title"], "url": entry["url"],
            "date": (entry.get("updated") or entry.get("published") or "")[:10],
            "feeds": entry["feeds"], "kind": entry["source_type"], "note": note,
            "published": (entry.get("published") or "")[:10],
            "event": event, "already_seen": entry.get("status") == "already-seen",
        })
    payload = json.dumps(rows, ensure_ascii=False).replace("<", "\\u003c")
    template = (ROOT / "templates" / "screening-catalog.html").read_text()
    target = batch / "catalog.html"
    target.write_text(template.replace("__WEEK__", args.week).replace("__RECORDS__", payload))
    print(f"Rendered {target.relative_to(ROOT)}: {len(rows)} verified records")


if __name__ == "__main__":
    main()
