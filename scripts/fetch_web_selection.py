#!/usr/bin/env python3
"""Cache publisher articles and canonical text for an explicit reading selection."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aidb.discovery import DiscoveryClient
from aidb.extractors.html import extract_html
from aidb.weekly import validate_week


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", required=True, type=validate_week)
    args = parser.parse_args()
    batch = ROOT / "inbox" / args.week
    selected = json.loads((batch / "web-selection.json").read_text())["articles"]
    destination = ROOT / "artifacts" / f"web-reading-{args.week}"
    destination.mkdir(parents=True, exist_ok=True)
    client = DiscoveryClient(60, destination / "responses")
    failures = []
    for item in selected:
        url = item["url"]
        slug = urlsplit(url).path.strip("/").rsplit("/", 1)[-1]
        try:
            body, _ = client.get(url)
            document = extract_html(body)
            result = {
                "url": url, "source_sha256": hashlib.sha256(body).hexdigest(),
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "blocks": [block.to_dict() for block in document.blocks],
            }
            (destination / f"{slug}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(f"FETCHED {slug}: {len(document.blocks)} blocks", flush=True)
        except (OSError, ValueError) as error:
            failures.append({"url": url, "error": str(error)})
            print(f"FAILED {slug}: {error}", flush=True)
    (destination / "failures.json").write_text(json.dumps(failures, ensure_ascii=False, indent=2) + "\n")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
