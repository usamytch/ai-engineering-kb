"""Weekly inbox batches: stable IDs, manifests, rendering, and state merge."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence
from urllib.parse import urlsplit, urlunsplit

from aidb.domain import ArxivRef, try_parse_arxiv_ref


WEEK_RE = re.compile(r"^\d{4}-W(?:0[1-9]|[1-4]\d|5[0-3])$")
CARD_RE = re.compile(
    r"^- \[(?P<marker>[^\]\r\n]*)\] \*\*\[(?P<title>.*)\]\((?P<url>.*)\)\*\*\s*$",
    re.MULTILINE,
)
ID_RE = re.compile(r"^  <!-- aidb:id=(?P<id>[^\r\n]+) -->\s*$", re.MULTILINE)
FIELD_RE = re.compile(
    r"^  - (?P<name>[^:]+):[ \t]*(?P<value>[^\r\n]*?)[ \t]*$", re.MULTILINE
)


def current_iso_week(now: datetime | None = None) -> str:
    current = now or datetime.now(timezone.utc)
    year, week, _ = current.isocalendar()
    return f"{year:04d}-W{week:02d}"


def validate_week(value: str) -> str:
    if not WEEK_RE.fullmatch(value):
        raise ValueError(f"invalid ISO week {value!r}; expected YYYY-Www")
    return value


def normalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return url.strip()
    host = parsed.netloc.lower()
    scheme = parsed.scheme.lower()
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((scheme, host, path, parsed.query, ""))


def source_id(url: str) -> str:
    ref = try_parse_arxiv_ref(url)
    if ref is not None:
        return f"arxiv:{ref.version_id}"
    normalized = normalize_url(url)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:20]
    return f"url:{digest}"


@dataclass
class Candidate:
    id: str
    title: str
    url: str
    published: str | None
    updated: str | None = None
    feeds: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    abstract: str = ""
    doi: str = ""
    journal_ref: str = ""
    comment: str = ""
    license_url: str = ""
    source_type: str = "secondary"
    paper_id: str | None = None
    paper_version_id: str | None = None
    decision: str = "untriaged"
    status: str = "discovered"

    @classmethod
    def from_entry(cls, entry: object) -> "Candidate":
        url = str(getattr(entry, "url"))
        ref = try_parse_arxiv_ref(url)
        published = _datetime_text(getattr(entry, "published", None))
        updated = _datetime_text(getattr(entry, "updated", None))
        feed_name = str(getattr(entry, "feed_name", "unknown"))
        topics = [str(value) for value in getattr(entry, "topics", ())]
        authors = [str(value) for value in getattr(entry, "authors", ())]
        categories = [str(value) for value in getattr(entry, "categories", ())]
        source_type = "paper" if ref is not None else _infer_source_type(url, feed_name)
        return cls(
            id=source_id(url),
            title=str(getattr(entry, "title")),
            url=ref.canonical_abs_url if ref is not None else normalize_url(url),
            published=published,
            updated=updated,
            feeds=[feed_name],
            topics=topics,
            authors=authors,
            categories=_unique(categories),
            abstract=" ".join(str(getattr(entry, "summary", "")).split()),
            doi=str(getattr(entry, "doi", "")),
            journal_ref=str(getattr(entry, "journal_ref", "")),
            comment=str(getattr(entry, "comment", "")),
            license_url=str(getattr(entry, "license_url", "")),
            source_type=source_type,
            paper_id=ref.base_id if ref is not None else None,
            paper_version_id=ref.version_id if ref is not None else None,
        )

    @classmethod
    def from_dict(cls, value: Mapping[str, object]) -> "Candidate":
        known = {
            name: value[name]
            for name in cls.__dataclass_fields__
            if name in value
        }
        return cls(**known)  # type: ignore[arg-type]

    def merge(self, other: "Candidate") -> "Candidate":
        if self.id != other.id:
            raise ValueError("cannot merge candidates with different IDs")
        return Candidate(
            id=self.id,
            title=other.title or self.title,
            url=other.url or self.url,
            published=_earliest(self.published, other.published),
            updated=_latest(self.updated, other.updated),
            feeds=_unique(self.feeds + other.feeds),
            topics=_unique(self.topics + other.topics),
            authors=other.authors or self.authors,
            categories=_unique(self.categories + other.categories),
            abstract=other.abstract or self.abstract,
            doi=other.doi or self.doi,
            journal_ref=other.journal_ref or self.journal_ref,
            comment=other.comment or self.comment,
            license_url=other.license_url or self.license_url,
            source_type=other.source_type or self.source_type,
            paper_id=other.paper_id or self.paper_id,
            paper_version_id=other.paper_version_id or self.paper_version_id,
            decision=self.decision if self.decision != "untriaged" else other.decision,
            status=self.status if self.status != "discovered" else other.status,
        )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class CardState:
    marker: str
    fields: Mapping[str, str]


def _datetime_text(value: object) -> str | None:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat(timespec="seconds")
    if isinstance(value, str) and value:
        return value
    return None


def _infer_source_type(url: str, feed: str) -> str:
    value = f"{url} {feed}".lower()
    if "/releases/" in value or " releases" in value:
        return "release"
    if "docs." in value or "/docs/" in value:
        return "official-docs"
    return "secondary"


def _unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _latest(left: str | None, right: str | None) -> str | None:
    return max(value for value in (left, right) if value) if left or right else None


def _earliest(left: str | None, right: str | None) -> str | None:
    return min(value for value in (left, right) if value) if left or right else None


def merge_candidates(candidates: Iterable[Candidate]) -> list[Candidate]:
    merged: dict[str, Candidate] = {}
    for candidate in candidates:
        if candidate.id in merged:
            merged[candidate.id] = merged[candidate.id].merge(candidate)
        else:
            merged[candidate.id] = candidate
    return sorted(
        merged.values(),
        key=lambda item: item.updated or item.published or "",
        reverse=True,
    )


def parse_card_states(content: str) -> dict[str, CardState]:
    matches = list(CARD_RE.finditer(content))
    section_end = content.find("\n## После triage")
    if section_end < 0:
        section_end = len(content)
    result: dict[str, CardState] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else section_end
        raw = content[match.start():end]
        id_match = ID_RE.search(raw)
        stable_id = id_match.group("id").strip() if id_match else source_id(match.group("url"))
        fields = {
            field_match.group("name").strip(): field_match.group("value").strip()
            for field_match in FIELD_RE.finditer(raw)
        }
        result[stable_id] = CardState(match.group("marker").strip().lower(), fields)
    return result


def _short(value: str, limit: int = 700) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def _date_only(value: str | None) -> str:
    return value[:10] if value else "date unknown"


def render_week_index(
    week: str,
    candidates: Sequence[Candidate],
    errors: Sequence[tuple[str, str]],
    generated_at: datetime,
    states: Mapping[str, CardState] | None = None,
) -> str:
    validate_week(week)
    states = states or {}
    lines = [
        f"# Weekly discovery — {week}",
        "",
        "> Это очередь решений, а не склад статей. Полные HTML/PDF/TeX скачиваются только для `[n]` и `[r]`.",
        ">",
        "> `[d]` drop · `[w]` watch · `[n]` deep note · `[r]` deep review · `[x]` обработано.",
        "",
        f"Сгенерировано: {generated_at.astimezone(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Кандидаты",
        "",
    ]
    surfaced = [candidate for candidate in candidates if candidate.status != "already-seen"]
    suppressed = [candidate for candidate in candidates if candidate.status == "already-seen"]
    if not surfaced:
        lines.extend(["Свежих записей в заданном окне не найдено.", ""])
    for candidate in surfaced:
        state = states.get(candidate.id, CardState("", {}))
        marker = state.marker or " "
        lines.extend(
            [
                f"- [{marker}] **[{candidate.title}]({candidate.url})**",
                f"  <!-- aidb:id={candidate.id} -->",
                f"  - Feed: {', '.join(candidate.feeds)}",
                f"  - Published: {_date_only(candidate.published)}",
            ]
        )
        if candidate.updated and _date_only(candidate.updated) != _date_only(candidate.published):
            lines.append(f"  - Updated: {_date_only(candidate.updated)}")
        if candidate.status == "revision":
            lines.append("  - Signal: новая версия уже известной arXiv-статьи")
        lines.append(f"  - Topics: {', '.join(candidate.topics)}")
        if candidate.authors:
            lines.append(f"  - Authors: {_short(', '.join(candidate.authors), 300)}")
        if candidate.categories:
            lines.append(f"  - Categories: {', '.join(candidate.categories)}")
        if candidate.abstract:
            lines.append(f"  - Abstract: {_short(candidate.abstract)}")
        if candidate.doi:
            lines.append(f"  - DOI: {candidate.doi}")
        if candidate.comment:
            lines.append(f"  - Comment: {_short(candidate.comment, 300)}")
        for name in ("Triage", "Paper", "Summary", "Note", "Review", "Error"):
            if state.fields.get(name):
                lines.append(f"  - {name}: {state.fields[name]}")
    if suppressed:
        lines.extend(
            [
                "",
                "## Suppressed duplicates",
                "",
                f"{len(suppressed)} уже встречавшихся записей сохранены в `manifest.json`, но не требуют повторного triage.",
            ]
        )
    if errors:
        lines.extend(["", "## Ошибки feeds", ""])
        lines.extend(f"- **{name}:** `{error}`" for name, error in errors)
    lines.extend(
        [
            "",
            "## После triage",
            "",
            "Запустить `make week-process`: выбранные arXiv `[n]`/`[r]` пройдут full-text ingest, extraction, deep summary и evidence checks. Перенос в основную KB остаётся ручным решением.",
            "",
        ]
    )
    return "\n".join(lines)


def write_week_batch(
    root: Path,
    entries: Iterable[object],
    errors: Sequence[tuple[str, str]],
    generated_at: datetime,
    week: str | None = None,
) -> tuple[Path, int]:
    batch_id = validate_week(week or current_iso_week(generated_at))
    batch_dir = root / "inbox" / batch_id
    index_path = batch_dir / "index.md"
    manifest_path = batch_dir / "manifest.json"
    states: dict[str, CardState] = {}
    existing: list[Candidate] = []
    if index_path.exists():
        states = parse_card_states(index_path.read_text(encoding="utf-8"))
    if manifest_path.exists():
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        existing = [Candidate.from_dict(value) for value in payload.get("entries", [])]

    history_ids, history_papers = _discovery_history(root, batch_id)
    discovered = [Candidate.from_entry(entry) for entry in entries]
    for candidate in discovered:
        if candidate.id in history_ids:
            candidate.status = "already-seen"
        elif candidate.paper_id and candidate.paper_id in history_papers:
            candidate.status = "revision"
    candidates = merge_candidates([*existing, *discovered])
    for candidate in candidates:
        state = states.get(candidate.id)
        if state and state.fields.get("Triage"):
            candidate.decision = state.fields["Triage"]
            candidate.status = "processed" if state.marker == "x" else candidate.status

    manifest = {
        "schema_version": 1,
        "batch_id": batch_id,
        "generated_at": generated_at.astimezone(timezone.utc).isoformat(timespec="seconds"),
        "entries": [candidate.to_dict() for candidate in candidates],
        "errors": [{"feed": name, "error": error} for name, error in errors],
    }
    batch_dir.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        render_week_index(batch_id, candidates, errors, generated_at, states),
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return batch_dir, len(discovered)


def _discovery_history(root: Path, current_batch: str) -> tuple[set[str], dict[str, set[str]]]:
    ids: set[str] = set()
    papers: dict[str, set[str]] = {}
    inbox = root / "inbox"
    for manifest_path in sorted(inbox.glob("*/manifest.json")):
        if manifest_path.parent.name == current_batch:
            continue
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        values = payload.get("entries", [])
        if not isinstance(values, list):
            continue
        for value in values:
            if not isinstance(value, dict):
                continue
            stable_id = value.get("id")
            if stable_id:
                ids.add(str(stable_id))
            paper_id = value.get("paper_id")
            version_id = value.get("paper_version_id")
            if paper_id:
                papers.setdefault(str(paper_id), set()).add(str(version_id or ""))
    return ids, papers


def load_manifest(batch_dir: Path) -> dict[str, object]:
    return json.loads((batch_dir / "manifest.json").read_text(encoding="utf-8"))


def save_manifest(batch_dir: Path, payload: Mapping[str, object]) -> None:
    (batch_dir / "manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
