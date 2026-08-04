#!/usr/bin/env python3
"""Apply human triage decisions from dated inbox Markdown files."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "inbox"
DATED_INBOX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
ENTRY_RE = re.compile(
    r"^- \[(?P<marker>[^\]\r\n]*)\] \*\*\[(?P<title>.*)\]\((?P<url>.*)\)\*\*\s*$"
)
ENTRY_MARKER_RE = re.compile(r"^- \[[^\]\r\n]*\]")
FIELD_RE = re.compile(
    r"^  - (?P<name>[^:]+):[ \t]*(?P<value>[^\r\n]*?)[ \t]*$", re.MULTILINE
)
TRIAGE_RE = re.compile(
    r"^  - Triage:[ \t]*(?P<value>[^\r\n]*?)[ \t]*$", re.MULTILINE
)
DEFAULT_TRIAGE = "drop | watch | note | review"
VALID_TRIAGE = {"drop", "watch", "note", "review"}


class TriageError(ValueError):
    """Raised when an inbox cannot be triaged safely."""


@dataclass(frozen=True)
class Entry:
    start: int
    end: int
    raw: str
    marker: str
    title: str
    url: str
    fields: dict[str, str]


@dataclass(frozen=True)
class Artifact:
    path: Path
    content: str
    kind: str
    create: bool


@dataclass
class TriagePlan:
    inbox_path: Path
    original: str
    updated: str
    counts: dict[str, int] = field(
        default_factory=lambda: {
            "drop": 0,
            "watch": 0,
            "note": 0,
            "review": 0,
            "untriaged": 0,
            "processed": 0,
        }
    )
    artifacts: list[Artifact] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return self.original != self.updated or any(item.create for item in self.artifacts)


def parse_entries(content: str) -> list[Entry]:
    lines = content.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    starts: list[int] = []
    after_triage = len(lines)
    for index, line in enumerate(lines):
        if line.rstrip("\r\n") == "## После triage":
            after_triage = index
            break
        if ENTRY_RE.match(line.rstrip("\r\n")):
            starts.append(index)

    entries: list[Entry] = []
    for position, start_line in enumerate(starts):
        next_start = starts[position + 1] if position + 1 < len(starts) else after_triage
        start = offsets[start_line]
        end = offsets[next_start]
        raw = content[start:end]
        first_line = lines[start_line].rstrip("\r\n")
        match = ENTRY_RE.match(first_line)
        assert match is not None
        fields = {
            field_match.group("name").strip(): field_match.group("value").strip()
            for field_match in FIELD_RE.finditer(raw)
        }
        entries.append(
            Entry(
                start=start,
                end=end,
                raw=raw,
                marker=match.group("marker").strip().lower(),
                title=match.group("title").strip(),
                url=match.group("url").strip(),
                fields=fields,
            )
        )
    return entries


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")
    return (slug or "source")[:72].rstrip("-")


def infer_source_type(entry: Entry) -> str:
    fingerprint = f"{entry.url} {entry.fields.get('Feed', '')}".lower()
    if "arxiv.org" in fingerprint:
        return "paper"
    if "/releases/tag/" in fingerprint or " releases" in fingerprint:
        return "release"
    if "docs." in fingerprint or "/docs/" in fingerprint:
        return "official-docs"
    if "benchmark" in fingerprint:
        return "benchmark"
    return "secondary"


def render_source_note(entry: Entry, checked_on: date) -> str:
    published = entry.fields.get("Published", "<уточнить>")
    topics = entry.fields.get("Topics", "<уточнить>")
    feed = entry.fields.get("Feed", "<уточнить>")
    source_type = infer_source_type(entry)
    return f"""# {entry.title}

- **URL:** {entry.url}
- **Авторы / организация:** <уточнить>
- **Опубликовано:** {published}
- **Проверено:** {checked_on.isoformat()}
- **Тип:** {source_type}
- **Темы:** {topics}
- **Статус:** watch
- **Источник discovery:** {feed}

## Claim своими словами

<Уточнить после чтения первоисточника.>

## Evidence

<Dataset, benchmark, production data, ablation, открытые artifacts.>

## Ограничения

<Domain mismatch, vendor bias, sample size, отсутствие cost/security/long-term data.>

## Влияние на базу

- Связанные разделы: <links>
- Связанное решение в `ADOPTION.md`: <...>
- Нужен experiment: да / нет

## Мой вывод

Исход triage: `note`. Проверить claim и решить: drop / watch / core / adoption review.
"""


def render_adoption_review(entry: Entry, checked_on: date) -> str:
    published = entry.fields.get("Published", "<уточнить>")
    topics = entry.fields.get("Topics", "<уточнить>")
    return f"""# Adoption review: {entry.title}

- **Дата:** {checked_on.isoformat()}
- **Owner:** <уточнить>
- **Текущий статус:** watch
- **Предлагаемый статус:** explore
- **Источник:** [{entry.title}]({entry.url})
- **Опубликовано:** {published}
- **Темы:** {topics}

## Hypothesis

Если <изменение>, то <метрика> улучшится с <baseline> до <target> для <slice>, не нарушив <cost/latency/safety ceilings>.

## Baseline

<Текущая архитектура, dataset и результаты.>

## Evidence до эксперимента

- [{entry.title}]({entry.url})
- <Почему источник применим и какие у него ограничения.>

## Experiment

- Dataset / slices:
- Primary metric:
- Non-regression metrics:
- Cost/latency budget:
- Security/privacy checks:
- Timebox:
- Stop condition:

## Results

<Таблица результатов, variance, failures и ссылки на artifacts/traces.>

## Operational impact

<Dependencies, state, observability, on-call, migration, rollback.>

## Решение

<Новый статус, scope и следующий review.>
"""


def artifact_path(
    root: Path,
    folder: str,
    title: str,
    url: str,
    checked_on: date,
    reserved: dict[Path, str],
) -> tuple[Path, bool]:
    directory = root / folder
    stem = f"{checked_on.isoformat()}-{slugify(title)}"
    for suffix in range(1, 1000):
        name = f"{stem}.md" if suffix == 1 else f"{stem}-{suffix}.md"
        candidate = directory / name
        if candidate in reserved:
            if reserved[candidate] == url:
                return candidate, False
            continue
        if candidate.exists():
            existing = candidate.read_text(encoding="utf-8")
            if url in existing:
                reserved[candidate] = url
                return candidate, False
            continue
        reserved[candidate] = url
        return candidate, True
    raise TriageError(f"cannot choose artifact filename for {title!r}")


def mark_processed(raw: str, outcome: str, link_line: str | None = None) -> str:
    updated, marker_replacements = ENTRY_MARKER_RE.subn("- [x]", raw, count=1)
    if marker_replacements != 1:
        raise TriageError("candidate misses exactly one checkbox marker")
    updated, replacements = TRIAGE_RE.subn(f"  - Triage: {outcome}", updated, count=1)
    if replacements != 1:
        raise TriageError("candidate misses exactly one Triage field")
    if link_line is None:
        return updated

    lines = updated.splitlines(keepends=True)
    insert_at = len(lines)
    while insert_at > 0 and not lines[insert_at - 1].strip():
        insert_at -= 1
    newline = "\n"
    if lines and lines[0].endswith("\r\n"):
        newline = "\r\n"
    lines.insert(insert_at, link_line + newline)
    return "".join(lines)


def plan_inbox_file(
    inbox_path: Path,
    root: Path = ROOT,
    checked_on: date | None = None,
    reserved: dict[Path, str] | None = None,
) -> TriagePlan:
    checked_on = checked_on or datetime.now(timezone.utc).date()
    reserved = reserved if reserved is not None else {}
    original = inbox_path.read_text(encoding="utf-8")
    entries = parse_entries(original)
    if not entries:
        raise TriageError(f"no candidate entries found in {inbox_path}")

    plan = TriagePlan(inbox_path=inbox_path, original=original, updated=original)
    replacements: list[tuple[int, int, str]] = []

    for entry in entries:
        field_outcome = entry.fields.get("Triage", "").strip().lower()
        if entry.marker == "x":
            plan.counts["processed"] += 1
            continue

        if entry.marker and entry.marker not in VALID_TRIAGE:
            raise TriageError(
                f"{inbox_path.name}: invalid checkbox marker {entry.marker!r} "
                f"for {entry.title!r}"
            )
        if field_outcome and field_outcome != DEFAULT_TRIAGE:
            if field_outcome not in VALID_TRIAGE:
                raise TriageError(
                    f"{inbox_path.name}: invalid triage {field_outcome!r} "
                    f"for {entry.title!r}"
                )
            if entry.marker and entry.marker != field_outcome:
                raise TriageError(
                    f"{inbox_path.name}: conflicting triage outcomes "
                    f"{entry.marker!r} and {field_outcome!r} for {entry.title!r}"
                )

        outcome = entry.marker or field_outcome
        if not outcome or outcome == DEFAULT_TRIAGE:
            plan.counts["untriaged"] += 1
            continue

        plan.counts[outcome] += 1
        if outcome == "drop":
            replacements.append((entry.start, entry.end, ""))
            continue
        if outcome == "watch":
            replacements.append(
                (entry.start, entry.end, mark_processed(entry.raw, outcome))
            )
            continue

        folder = "notes" if outcome == "note" else "reviews"
        target, create = artifact_path(
            root, folder, entry.title, entry.url, checked_on, reserved
        )
        content = (
            render_source_note(entry, checked_on)
            if outcome == "note"
            else render_adoption_review(entry, checked_on)
        )
        plan.artifacts.append(
            Artifact(path=target, content=content, kind=outcome, create=create)
        )
        relative_target = Path("..") / target.relative_to(root)
        label = "Note" if outcome == "note" else "Review"
        link_line = f"  - {label}: [{target.name}]({relative_target.as_posix()})"
        replacements.append(
            (
                entry.start,
                entry.end,
                mark_processed(entry.raw, outcome, link_line=link_line),
            )
        )

    updated = original
    for start, end, replacement in reversed(replacements):
        updated = updated[:start] + replacement + updated[end:]
    plan.updated = updated
    return plan


def apply_plan(plan: TriagePlan) -> None:
    for artifact in plan.artifacts:
        if not artifact.create:
            continue
        artifact.path.parent.mkdir(parents=True, exist_ok=True)
        if artifact.path.exists():
            raise TriageError(f"refusing to overwrite {artifact.path}")
        artifact.path.write_text(artifact.content, encoding="utf-8")
    if plan.original != plan.updated:
        plan.inbox_path.write_text(plan.updated, encoding="utf-8")


def resolve_inbox_file(raw: str, root: Path = ROOT) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path if path.parts and path.parts[0] == "inbox" else root / "inbox" / path
    path = path.resolve()
    inbox_dir = (root / "inbox").resolve()
    if path.parent != inbox_dir or not DATED_INBOX_RE.match(path.name):
        raise TriageError("--file must point to inbox/YYYY-MM-DD.md")
    if not path.exists():
        raise TriageError(f"inbox file not found: {path}")
    return path


def selected_files(args: argparse.Namespace, root: Path = ROOT) -> list[Path]:
    if args.file:
        return [resolve_inbox_file(args.file, root)]
    dated = sorted(
        path for path in (root / "inbox").glob("*.md") if DATED_INBOX_RE.match(path.name)
    )
    if not dated:
        raise TriageError("no dated inbox files found")
    return dated if args.all else [dated[-1]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", help="dated inbox file; defaults to the newest")
    group.add_argument("--all", action="store_true", help="process all dated inbox files")
    parser.add_argument("--dry-run", action="store_true", help="show the plan without writing")
    return parser.parse_args()


def display_plan(plan: TriagePlan, root: Path, dry_run: bool) -> None:
    relative = plan.inbox_path.relative_to(root)
    counts = " ".join(f"{key}={value}" for key, value in plan.counts.items())
    prefix = "DRY RUN " if dry_run else ""
    print(f"{prefix}{relative}: {counts}")
    for artifact in plan.artifacts:
        action = "create" if artifact.create else "reuse"
        print(f"  {action} {artifact.path.relative_to(root)}")
    if not plan.changed:
        print("  no selected triage outcomes; nothing to change")


def main() -> int:
    args = parse_args()
    try:
        files = selected_files(args)
        reserved: dict[Path, str] = {}
        plans = [plan_inbox_file(path, reserved=reserved) for path in files]
        for plan in plans:
            display_plan(plan, ROOT, args.dry_run)
        if not args.dry_run:
            for plan in plans:
                apply_plan(plan)
    except (OSError, TriageError) as exc:
        print(f"triage failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
