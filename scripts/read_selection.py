#!/usr/bin/env python3
"""Read a declared selection sequentially, checkpointing each completed paper."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from aidb.domain import ArxivRef
from aidb.pipeline import extract_paper, fetch_paper, paper_paths, process_paper, write_paper_metadata
from aidb.summarizers.codex_exec import CodexExecProvider
from aidb.weekly import save_manifest, validate_week
from scripts.triage_inbox import append_metadata_line, mark_processed, parse_entries


class RecordedProvider:
    """Keep candidates locally so a rejected analysis can be inspected and retried."""

    def __init__(self, provider, directory):
        self.provider = provider
        self.directory = directory
        self.calls = 0

    @property
    def name(self):
        return self.provider.name

    def generate(self, prompt, schema):
        self.calls += 1
        result = self.provider.generate(prompt, schema)
        self.directory.mkdir(parents=True, exist_ok=True)
        prefix = "reviewed-candidate" if self.provider.name == "reviewed-candidate" else "candidate"
        path = self.directory / f"{prefix}-{self.calls}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        return result


class ReviewedCandidateProvider:
    """Revalidate a locally reviewed candidate without another generation call."""

    name = "reviewed-candidate"

    def __init__(self, path):
        self.result = json.loads(path.read_text(encoding="utf-8"))

    def generate(self, prompt, schema):
        return self.result


def require_note_decision(entry):
    if entry.marker not in {"", "n", "x"} or (
        entry.marker == "x" and entry.fields.get("Triage") != "note"
    ):
        raise ValueError(f"refusing to replace a different triage decision for {entry.url}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", required=True, type=validate_week)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--paper", action="append", help="restrict this run to a selected version")
    parser.add_argument("--fetch-only", action="store_true", help="cache and extract full text without summarizing")
    parser.add_argument("--candidate", type=Path, help="revalidate a reviewed JSON candidate for exactly one --paper")
    args = parser.parse_args()
    if args.candidate and (not args.paper or len(args.paper) != 1 or args.fetch_only):
        parser.error("--candidate requires exactly one --paper and cannot be used with --fetch-only")
    batch = ROOT / "inbox" / args.week
    selection = json.loads((batch / "reading-selection.json").read_text())
    selected_ids = {ArxivRef.parse(item["id"]).version_id for item in selection["papers"]}
    if args.paper and set(args.paper) - selected_ids:
        parser.error("--paper must name a version in reading-selection.json")
    runtime = ROOT / "artifacts" / "summary-runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    os.environ["TMPDIR"] = str(runtime)
    # tempfile may have resolved its default before TMPDIR was set.
    import tempfile
    tempfile.tempdir = str(runtime)
    log_dir = ROOT / "artifacts" / "reading" / args.week
    log_dir.mkdir(parents=True, exist_ok=True)
    provider = ReviewedCandidateProvider(args.candidate) if args.candidate else CodexExecProvider(timeout_seconds=args.timeout)
    failure_path = log_dir / ("fetch-failures.json" if args.fetch_only else "failures.json")
    failures = json.loads(failure_path.read_text()) if failure_path.exists() else []
    for number, selected in enumerate(selection["papers"], 1):
        ref = ArxivRef.parse(selected["id"])
        if args.paper and ref.version_id not in args.paper:
            continue
        failures = [failure for failure in failures if failure.get("id") != ref.version_id]
        manifest = json.loads((batch / "manifest.json").read_text())
        candidate = next(item for item in manifest["entries"] if item.get("paper_version_id") == ref.version_id)
        content = (batch / "index.md").read_text()
        entry = next(entry for entry in parse_entries(content) if entry.url == ref.canonical_abs_url)
        require_note_decision(entry)
        metadata = {key: value for key, value in candidate.items() if key not in {"decision", "status", "error"}}
        print(f"[{number}/{len(selection['papers'])}] Reading {ref.version_id}: {candidate['title']}", flush=True)
        try:
            if args.fetch_only:
                paths = paper_paths(ROOT, ref)
                if paths.document_jsonl.exists():
                    print(f"CACHED {ref.version_id}", flush=True)
                    continue
                write_paper_metadata(ROOT, ref, metadata)
                fetched = fetch_paper(ROOT, ref)
                document = extract_paper(ROOT, ref, fetched=fetched)
                print(f"FETCHED {ref.version_id}: {len(document.blocks)} blocks", flush=True)
                continue
            recorded = RecordedProvider(provider, log_dir / ref.version_id.replace("/", "--"))
            result = process_paper(ROOT, ref, recorded, metadata=metadata)
        except (OSError, ValueError, RuntimeError) as error:
            failures.append({"id": ref.version_id, "error": str(error)})
            print(f"FAILED {ref.version_id}: {str(error)[:500]}", flush=True)
            failure_path.write_text(json.dumps(failures, ensure_ascii=False, indent=2) + "\n")
            continue
        content = (batch / "index.md").read_text()
        entry = next(
            entry for entry in parse_entries(content) if entry.url == ref.canonical_abs_url
        )
        require_note_decision(entry)
        if entry.marker != "x":
            updated = mark_processed(entry.raw, "note")
            for label, path in (("Paper", result.paths.paper_index), ("Summary", result.paths.summary)):
                link = Path(os.path.relpath(path, batch)).as_posix()
                updated = append_metadata_line(updated, f"  - {label}: [{ref.version_id} {label.lower()}]({link})")
            (batch / "index.md").write_text(content[:entry.start] + updated + content[entry.end:])
        manifest = json.loads((batch / "manifest.json").read_text())
        candidate = next(item for item in manifest["entries"] if item.get("paper_version_id") == ref.version_id)
        candidate.update(decision="note", status="summarized")
        manifest["processed_at"] = datetime.now(timezone.utc).isoformat()
        save_manifest(batch, manifest)
        print(f"DONE {ref.version_id}: {result.source_format}, {result.block_count} blocks", flush=True)
    failure_path.write_text(json.dumps(failures, ensure_ascii=False, indent=2) + "\n")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
