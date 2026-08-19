"""Status and deterministic closeout for the weekly research ritual."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from aidb.weekly import CardState, current_iso_week, parse_card_states, validate_week


class RitualError(RuntimeError):
    """Raised when a weekly batch cannot safely move to the requested state."""


def resolve_batch(root: Path, week: str | None = None) -> Path:
    batch_id = validate_week(week or current_iso_week())
    batch = root / "inbox" / batch_id
    if not (batch / "index.md").exists() or not (batch / "manifest.json").exists():
        raise RitualError(f"weekly inbox not found: inbox/{batch_id}")
    return batch


def week_status(root: Path, week: str | None = None) -> dict[str, object]:
    batch = resolve_batch(root, week)
    manifest = json.loads((batch / "manifest.json").read_text(encoding="utf-8"))
    states = parse_card_states((batch / "index.md").read_text(encoding="utf-8"))
    marker_counts = Counter(_marker_name(state.marker) for state in states.values())
    outcome_counts = Counter(
        state.fields.get("Triage", "")
        for state in states.values()
        if state.fields.get("Triage")
    )
    entries = manifest.get("entries", [])
    errors = manifest.get("errors", [])
    return {
        "week": batch.name,
        "discovered": len(entries) if isinstance(entries, list) else 0,
        "markers": dict(sorted(marker_counts.items())),
        "outcomes": dict(sorted(outcome_counts.items())),
        "feed_errors": len(errors) if isinstance(errors, list) else 0,
        "selected": sum(marker_counts.get(value, 0) for value in ("drop", "watch", "note", "review")),
        "open": marker_counts.get("untriaged", 0),
        "processed": marker_counts.get("processed", 0),
    }


def _marker_name(marker: str) -> str:
    return {
        "": "untriaged",
        "d": "drop",
        "w": "watch",
        "n": "note",
        "r": "review",
        "x": "processed",
    }.get(marker, "invalid")


def _entry_by_id(manifest: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    result: dict[str, Mapping[str, object]] = {}
    values = manifest.get("entries", [])
    if not isinstance(values, list):
        return result
    for value in values:
        if isinstance(value, dict) and value.get("id"):
            result[str(value["id"])] = value
    return result


def render_digest(
    week: str,
    status: Mapping[str, object],
    manifest: Mapping[str, object],
    states: Mapping[str, CardState],
) -> str:
    entries = _entry_by_id(manifest)
    lines = [
        f"# Weekly AI Engineering Review — {week}",
        "",
        f"- Discovered: {status['discovered']}",
        f"- Processed: {status['processed']}",
        f"- Open: {status['open']}",
        f"- Feed errors: {status['feed_errors']}",
        "",
        "## Глубоко разобрано",
        "",
    ]
    deep = 0
    for stable_id, state in states.items():
        if state.fields.get("Triage") not in {"note", "review"}:
            continue
        entry = entries.get(stable_id, {})
        title = str(entry.get("title", stable_id))
        summary = state.fields.get("Summary")
        if summary:
            lines.append(f"- [{title}]({summary}) — `{state.fields['Triage']}`")
        else:
            lines.append(f"- {title} — `{state.fields['Triage']}` (без summary link)")
        deep += 1
    if deep == 0:
        lines.append("Глубоких разборов на этой неделе нет.")

    for heading, outcome in (("Watchlist", "watch"), ("Отброшено", "drop")):
        lines.extend(["", f"## {heading}", ""])
        found = 0
        for stable_id, state in states.items():
            if state.fields.get("Triage") != outcome:
                continue
            entry = entries.get(stable_id, {})
            title = str(entry.get("title", stable_id))
            url = str(entry.get("url", ""))
            lines.append(f"- [{title}]({url})" if url else f"- {title}")
            found += 1
        if not found:
            lines.append("Нет.")

    lines.extend(
        [
            "",
            "## Что действительно изменилось",
            "",
            "<Заполнить после человеческой проверки summaries.>",
            "",
            "## Следующие эксперименты",
            "",
            "<Добавить только измеримые hypotheses с baseline и stop condition.>",
            "",
        ]
    )
    return "\n".join(lines)


def close_week(
    root: Path,
    week: str | None = None,
    *,
    allow_open: bool = False,
    now: datetime | None = None,
) -> tuple[Path, Path]:
    batch = resolve_batch(root, week)
    status = week_status(root, batch.name)
    if int(status["selected"]) > 0:
        raise RitualError(
            f"{status['selected']} selected entries are not processed; run make week-process"
        )
    if int(status["open"]) > 0 and not allow_open:
        raise RitualError(
            f"{status['open']} entries are still untriaged; mark them or pass --allow-open"
        )

    manifest_path = batch / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    states = parse_card_states((batch / "index.md").read_text(encoding="utf-8"))
    closed_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    closeout = {
        "schema_version": 1,
        "batch_id": batch.name,
        "closed_at": closed_at.isoformat(timespec="seconds"),
        "status": status,
    }
    closeout_path = batch / "closeout.json"
    closeout_path.write_text(
        json.dumps(closeout, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    digest_dir = root / "digests"
    digest_dir.mkdir(parents=True, exist_ok=True)
    digest_path = digest_dir / f"{batch.name}.md"
    digest_path.write_text(
        render_digest(batch.name, status, manifest, states), encoding="utf-8"
    )
    return digest_path, closeout_path
