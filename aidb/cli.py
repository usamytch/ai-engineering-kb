"""Single command-line interface for the AIDB weekly paper-review ritual."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any

from aidb.domain import ArxivRef
from aidb.pipeline import (
    PipelineError,
    approve_paper,
    extract_paper,
    fetch_paper,
    paper_paths,
    process_paper,
    summarize_paper,
)
from aidb.ritual import RitualError, close_week, week_status
from aidb.summarizers.codex_exec import CodexExecProvider
from aidb.summarizers.openai_responses import OpenAIResponsesProvider
from aidb.week_process import process_week
from aidb.weekly import (
    Candidate,
    current_iso_week,
    merge_candidates,
    render_week_index,
    write_week_batch,
)
from scripts.refresh_inbox import collect_entries


def _default_root() -> Path:
    configured = os.environ.get("AIDB_ROOT")
    if configured:
        return Path(configured).resolve()
    cwd = Path.cwd().resolve()
    if (cwd / "watchlist.json").exists():
        return cwd
    return Path(__file__).resolve().parents[1]


def _add_provider_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--provider",
        choices=("codex", "openai"),
        default="codex",
        help="LLM backend; codex uses a new isolated codex exec session",
    )
    parser.add_argument("--model", help="provider model; omitted means configured Codex default")
    parser.add_argument("--profile", choices=("deep", "verified"), default="deep")
    parser.add_argument("--timeout", type=int, default=900, help="LLM timeout in seconds")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aidb", description=__doc__)
    parser.add_argument("--root", type=Path, default=_default_root(), help="AIDB repository root")
    commands = parser.add_subparsers(dest="command", required=True)

    start = commands.add_parser("week-start", help="collect feeds into an ISO-week inbox folder")
    start.add_argument("--week", default=current_iso_week())
    start.add_argument("--days", type=int, default=8)
    start.add_argument("--limit-per-feed", type=int, default=10)
    start.add_argument("--network-timeout", type=float, default=20.0)
    start.add_argument("--dry-run", action="store_true")

    status = commands.add_parser("week-status", help="show weekly decision and processing counts")
    status.add_argument("--week")
    status.add_argument("--json", action="store_true")

    process = commands.add_parser("week-process", help="apply decisions and deep-read selected papers")
    process.add_argument("--week")
    process.add_argument("--dry-run", action="store_true")
    process.add_argument("--force-fetch", action="store_true")
    process.add_argument("--force-summary", action="store_true")
    _add_provider_arguments(process)

    close = commands.add_parser("week-close", help="create digest and closeout after processing")
    close.add_argument("--week")
    close.add_argument("--allow-open", action="store_true")

    review = commands.add_parser("review", help="list AI drafts waiting for human approval")
    review.add_argument("--json", action="store_true")

    paper = commands.add_parser("paper", help="operate on one explicit arXiv version")
    paper_commands = paper.add_subparsers(dest="paper_command", required=True)

    fetch = paper_commands.add_parser("fetch", help="download full paper artifacts")
    fetch.add_argument("reference")
    fetch.add_argument("--policy", choices=("normal", "full", "review"), default="normal")
    fetch.add_argument("--force", action="store_true")

    extract = paper_commands.add_parser("extract", help="normalize HTML, TeX, or PDF into blocks")
    extract.add_argument("reference")

    summarize = paper_commands.add_parser("summarize", help="make a validated deep summary")
    summarize.add_argument("reference")
    summarize.add_argument("--force", action="store_true")
    _add_provider_arguments(summarize)

    full = paper_commands.add_parser("process", help="fetch, extract, and summarize")
    full.add_argument("reference")
    full.add_argument("--policy", choices=("normal", "full", "review"), default="normal")
    full.add_argument("--force-fetch", action="store_true")
    full.add_argument("--force-summary", action="store_true")
    _add_provider_arguments(full)

    paper_status = paper_commands.add_parser("status", help="show tracked version manifest")
    paper_status.add_argument("reference")

    approve = paper_commands.add_parser("approve", help="mark a validated summary human-verified")
    approve.add_argument("reference")
    approve.add_argument("--reviewer", required=True)
    return parser


def _provider(args: argparse.Namespace):
    if args.provider == "codex":
        return CodexExecProvider(timeout_seconds=args.timeout, model=args.model)
    model = args.model or "gpt-5.6"
    return OpenAIResponsesProvider(model=model, timeout_seconds=args.timeout)


def _parse_ref(value: str) -> ArxivRef:
    return ArxivRef.parse(value)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "week-start":
            return _week_start(root, args)
        if args.command == "week-status":
            return _week_status(root, args)
        if args.command == "week-process":
            return _week_process(root, args)
        if args.command == "week-close":
            digest, closeout = close_week(root, args.week, allow_open=args.allow_open)
            print(f"Wrote {digest.relative_to(root)} and {closeout.relative_to(root)}")
            return 0
        if args.command == "review":
            return _review(root, args)
        if args.command == "paper":
            return _paper(root, args)
    except (OSError, ValueError, PipelineError, RitualError, RuntimeError) as error:
        print(f"aidb failed: {error}", file=sys.stderr)
        return 2
    parser.error("unknown command")
    return 2


def _week_start(root: Path, args: argparse.Namespace) -> int:
    now, entries, errors, feed_count = collect_entries(
        root,
        days=args.days,
        limit_per_feed=args.limit_per_feed,
        timeout=args.network_timeout,
    )
    if args.dry_run:
        candidates = merge_candidates(Candidate.from_entry(entry) for entry in entries)
        print(render_week_index(args.week, candidates, errors, now))
    else:
        batch, discovered = write_week_batch(root, entries, errors, now, args.week)
        print(
            f"Wrote {batch.relative_to(root)}: discovered={discovered} "
            f"unique={len(merge_candidates(Candidate.from_entry(entry) for entry in entries))} "
            f"feed_errors={len(errors)}"
        )
    return 0 if entries or len(errors) < feed_count else 1


def _week_status(root: Path, args: argparse.Namespace) -> int:
    status = week_status(root, args.week)
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        markers = " ".join(f"{key}={value}" for key, value in status["markers"].items())
        outcomes = " ".join(f"{key}={value}" for key, value in status["outcomes"].items())
        print(
            f"{status['week']}: discovered={status['discovered']} processed={status['processed']} "
            f"selected={status['selected']} open={status['open']} feed_errors={status['feed_errors']}"
        )
        print(f"markers: {markers or 'none'}")
        print(f"outcomes: {outcomes or 'none'}")
    return 0


def _week_process(root: Path, args: argparse.Namespace) -> int:
    report = process_week(
        root,
        args.week,
        _provider(args),
        profile=args.profile,
        dry_run=args.dry_run,
        force_fetch=args.force_fetch,
        force_summary=args.force_summary,
    )
    prefix = "DRY RUN " if args.dry_run else ""
    print(prefix + report.week + ": " + " ".join(f"{k}={v}" for k, v in report.counts.items()))
    for paper in report.papers:
        cache = "cached" if paper.cached_summary else "generated"
        print(
            f"  {paper.ref.version_id}: {paper.source_format}, {paper.block_count} blocks, summary {cache}"
        )
    for error in report.errors:
        print(f"  failed: {error}")
    return 1 if report.errors else 0


def _paper(root: Path, args: argparse.Namespace) -> int:
    ref = _parse_ref(args.reference)
    if args.paper_command == "fetch":
        result = fetch_paper(root, ref, policy=args.policy, force=args.force)
        available = sum(record.available for record in result.artifacts.values())
        print(f"Fetched {result.version_id}: {available}/{len(result.artifacts)} artifacts available")
        return 0
    if args.paper_command == "extract":
        document = extract_paper(root, ref)
        print(f"Extracted {ref.version_id}: {document.source_format}, {len(document.blocks)} blocks")
        return 0
    if args.paper_command == "summarize":
        _, cached = summarize_paper(
            root, ref, _provider(args), profile=args.profile, force=args.force
        )
        paths = paper_paths(root, ref)
        print(f"{'Reused' if cached else 'Wrote'} {paths.summary.relative_to(root)}")
        return 0
    if args.paper_command == "process":
        result = process_paper(
            root,
            ref,
            _provider(args),
            policy=args.policy,
            profile=args.profile,
            force_fetch=args.force_fetch,
            force_summary=args.force_summary,
        )
        print(
            f"Processed {ref.version_id}: {result.source_format}, {result.block_count} blocks; "
            f"{result.paths.summary.relative_to(root)}"
        )
        return 0
    if args.paper_command == "status":
        path = paper_paths(root, ref).manifest
        if not path.exists():
            raise PipelineError(f"paper manifest not found: {path.relative_to(root)}")
        print(path.read_text(encoding="utf-8"), end="")
        return 0
    if args.paper_command == "approve":
        path = approve_paper(root, ref, reviewer=args.reviewer)
        print(f"Verified {ref.version_id} in {path.relative_to(root)}")
        return 0
    raise PipelineError(f"unknown paper command: {args.paper_command}")


def _review(root: Path, args: argparse.Namespace) -> int:
    drafts: list[dict[str, Any]] = []
    for manifest_path in sorted((root / "papers" / "arxiv").glob("*/versions/v*/manifest.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        summary = manifest.get("summary")
        if not isinstance(summary, dict) or summary.get("status") != "ai-draft":
            continue
        summary_path = manifest_path.parent / "summary.md"
        drafts.append(
            {
                "version_id": manifest.get("version_id"),
                "provider": summary.get("provider"),
                "generated_at": summary.get("generated_at"),
                "summary": str(summary_path.relative_to(root)),
            }
        )
    if args.json:
        print(json.dumps(drafts, ensure_ascii=False, indent=2, sort_keys=True))
    elif not drafts:
        print("No AI drafts waiting for review")
    else:
        print("AI drafts waiting for human review:")
        for item in drafts:
            print(f"- {item['version_id']}: {item['summary']} ({item['provider']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
