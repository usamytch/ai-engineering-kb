"""Apply weekly decisions, enriching selected arXiv papers before completion."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping

from aidb.domain import try_parse_arxiv_ref
from aidb.pipeline import PipelineError, ProcessResult, process_paper
from aidb.ritual import resolve_batch
from aidb.summarizers.base import SummaryProvider
from aidb.weekly import save_manifest, source_id
from scripts.triage_inbox import (
    Artifact,
    TriageError,
    append_metadata_line,
    artifact_path,
    mark_processed,
    parse_entries,
    render_adoption_review,
    render_source_note,
)


VALID_MARKERS = {"", "d", "w", "n", "r", "x"}
OUTCOMES = {"d": "drop", "w": "watch", "n": "note", "r": "review"}
ERROR_LINE_RE = re.compile(r"^  - Error:.*(?:\r?\n|$)", re.MULTILINE)


@dataclass
class WeekProcessReport:
    week: str
    counts: dict[str, int] = field(
        default_factory=lambda: {
            "drop": 0,
            "watch": 0,
            "note": 0,
            "review": 0,
            "failed": 0,
            "untriaged": 0,
            "processed": 0,
        }
    )
    papers: list[ProcessResult] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def process_week(
    root: Path,
    week: str | None,
    provider: SummaryProvider | None,
    *,
    profile: str = "deep",
    dry_run: bool = False,
    force_fetch: bool = False,
    force_summary: bool = False,
) -> WeekProcessReport:
    batch = resolve_batch(root, week)
    index_path = batch / "index.md"
    original = index_path.read_text(encoding="utf-8")
    entries = parse_entries(original)
    if not entries:
        raise TriageError(f"no candidate entries found in {index_path}")
    manifest_path = batch / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    metadata_by_id = _metadata_by_id(manifest)
    report = WeekProcessReport(batch.name)
    replacements: list[tuple[int, int, str]] = []
    reserved: dict[Path, str] = {}

    for entry in entries:
        marker = entry.marker
        if marker not in VALID_MARKERS:
            raise TriageError(f"invalid checkbox marker {marker!r} for {entry.title!r}")
        if marker == "x":
            report.counts["processed"] += 1
            continue
        if not marker:
            report.counts["untriaged"] += 1
            continue
        if entry.fields.get("Triage"):
            raise TriageError(f"Triage is output-only for {entry.title!r}")

        outcome = OUTCOMES[marker]
        if dry_run:
            report.counts[outcome] += 1
            continue
        if marker in {"d", "w"}:
            replacements.append(
                (entry.start, entry.end, mark_processed(_clear_error(entry.raw), outcome))
            )
            report.counts[outcome] += 1
            _set_manifest_state(manifest, source_id(entry.url), outcome, "processed")
            continue

        ref = try_parse_arxiv_ref(entry.url)
        if ref is None:
            artifact = _legacy_artifact(entry, outcome, root, batch, reserved)
            report.artifacts.append(artifact)
            label = "Note" if outcome == "note" else "Review"
            link = _relative_link(batch, artifact.path)
            updated = mark_processed(
                _clear_error(entry.raw), outcome, f"  - {label}: [{artifact.path.name}]({link})"
            )
            replacements.append((entry.start, entry.end, updated))
            report.counts[outcome] += 1
            _set_manifest_state(manifest, source_id(entry.url), outcome, "processed")
            continue
        if ref.version is None:
            _record_failure(
                report,
                replacements,
                entry,
                manifest,
                "arXiv URL is not version-pinned; refresh metadata or add vN",
            )
            continue
        if provider is None:
            _record_failure(
                report,
                replacements,
                entry,
                manifest,
                "no LLM provider configured for deep summary",
            )
            continue

        candidate_metadata = metadata_by_id.get(source_id(entry.url), {})
        metadata = dict(candidate_metadata)
        metadata.setdefault("title", entry.title)
        try:
            result = process_paper(
                root,
                ref,
                provider,
                policy="review" if marker == "r" else "normal",
                profile=profile,
                force_fetch=force_fetch,
                force_summary=force_summary,
                metadata=metadata,
            )
        except (OSError, ValueError, PipelineError, RuntimeError) as error:
            _record_failure(report, replacements, entry, manifest, str(error))
            continue

        report.papers.append(result)
        paper_link = _relative_link(batch, result.paths.paper_index)
        summary_link = _relative_link(batch, result.paths.summary)
        updated = mark_processed(_clear_error(entry.raw), outcome)
        updated = append_metadata_line(
            updated, f"  - Paper: [{ref.version_id}]({paper_link})"
        )
        updated = append_metadata_line(
            updated, f"  - Summary: [{ref.version_tag} deep summary]({summary_link})"
        )
        if outcome == "review":
            artifact = _legacy_artifact(entry, outcome, root, batch, reserved)
            artifact = Artifact(
                path=artifact.path,
                content=_add_summary_to_review(artifact.content, artifact.path, result.paths.summary),
                kind=artifact.kind,
                create=artifact.create,
            )
            report.artifacts.append(artifact)
            review_link = _relative_link(batch, artifact.path)
            updated = append_metadata_line(
                updated, f"  - Review: [{artifact.path.name}]({review_link})"
            )
        replacements.append((entry.start, entry.end, updated))
        report.counts[outcome] += 1
        _set_manifest_state(manifest, source_id(entry.url), outcome, "summarized")

    if dry_run:
        return report
    for artifact in report.artifacts:
        if not artifact.create:
            continue
        artifact.path.parent.mkdir(parents=True, exist_ok=True)
        if artifact.path.exists():
            raise TriageError(f"refusing to overwrite {artifact.path}")
        artifact.path.write_text(artifact.content, encoding="utf-8")
    updated = original
    for start, end, replacement in reversed(replacements):
        updated = updated[:start] + replacement + updated[end:]
    index_path.write_text(updated, encoding="utf-8")
    manifest["processed_at"] = datetime.now(timezone.utc).isoformat()
    save_manifest(batch, manifest)
    return report


def _metadata_by_id(manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    values = manifest.get("entries", [])
    if not isinstance(values, list):
        return {}
    return {
        str(item["id"]): item
        for item in values
        if isinstance(item, dict) and item.get("id")
    }


def _set_manifest_state(
    manifest: dict[str, Any], stable_id: str, decision: str, status: str, error: str | None = None
) -> None:
    entries = manifest.get("entries", [])
    if not isinstance(entries, list):
        return
    for item in entries:
        if isinstance(item, dict) and item.get("id") == stable_id:
            item["decision"] = decision
            item["status"] = status
            if error:
                item["error"] = error
            else:
                item.pop("error", None)
            return


def _record_failure(
    report: WeekProcessReport,
    replacements: list[tuple[int, int, str]],
    entry: Any,
    manifest: dict[str, Any],
    message: str,
) -> None:
    compact = " ".join(message.split())[:500]
    raw = append_metadata_line(_clear_error(entry.raw), f"  - Error: {compact}")
    replacements.append((entry.start, entry.end, raw))
    report.counts["failed"] += 1
    report.errors.append(f"{entry.title}: {compact}")
    _set_manifest_state(manifest, source_id(entry.url), OUTCOMES[entry.marker], "failed", compact)


def _clear_error(raw: str) -> str:
    return ERROR_LINE_RE.sub("", raw)


def _legacy_artifact(
    entry: Any,
    outcome: str,
    root: Path,
    batch: Path,
    reserved: dict[Path, str],
) -> Artifact:
    folder = "notes" if outcome == "note" else "reviews"
    target, create = artifact_path(
        root,
        folder,
        entry.title,
        entry.url,
        datetime.now(timezone.utc).date(),
        reserved,
    )
    content = (
        render_source_note(entry, datetime.now(timezone.utc).date())
        if outcome == "note"
        else render_adoption_review(entry, datetime.now(timezone.utc).date())
    )
    return Artifact(target, content, outcome, create)


def _relative_link(batch: Path, target: Path) -> str:
    return Path(os.path.relpath(target, batch)).as_posix()


def _add_summary_to_review(content: str, review_path: Path, summary_path: Path) -> str:
    relative = Path(os.path.relpath(summary_path, review_path.parent)).as_posix()
    marker = "- **Источник:**"
    line = f"- **Deep summary:** [validated AI draft]({relative})\n"
    position = content.find(marker)
    if position < 0:
        return line + content
    end = content.find("\n", position)
    return content[: end + 1] + line + content[end + 1 :]
