"""End-to-end arXiv paper processing with tracked provenance and local raw data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Mapping

from aidb.domain import ArxivRef
from aidb.extractors.html import Document, extract_html_metadata
from aidb.render import render_summary
from aidb.sources.arxiv import FetchResult, extract_arxiv, fetch_arxiv
from aidb.store import ArtifactStore
from aidb.summarizers.base import SummaryProvider, analyze_document


class PipelineError(RuntimeError):
    """The selected paper could not reach a durable pipeline state."""


@dataclass(frozen=True)
class PaperPaths:
    root: Path
    paper_dir: Path
    version_dir: Path
    artifact_dir: Path
    metadata: Path
    paper_index: Path
    manifest: Path
    document_jsonl: Path
    document_markdown: Path
    analysis: Path
    summary: Path


@dataclass(frozen=True)
class ProcessResult:
    ref: ArxivRef
    paths: PaperPaths
    source_format: str
    block_count: int
    cached_summary: bool


def require_version(ref: ArxivRef) -> ArxivRef:
    if ref.version is None:
        raise PipelineError(
            f"arXiv {ref.base_id} is not version-pinned; use an explicit vN for reproducibility"
        )
    return ref


def paper_paths(root: Path | str, ref: ArxivRef) -> PaperPaths:
    ref = require_version(ref)
    base = Path(root).resolve()
    paper_dir = base / "papers" / "arxiv" / ref.path_key
    version_dir = paper_dir / "versions" / str(ref.version_tag)
    artifact_dir = base / ".aidb" / "artifacts" / "arxiv" / ref.path_key / str(ref.version_tag)
    return PaperPaths(
        root=base,
        paper_dir=paper_dir,
        version_dir=version_dir,
        artifact_dir=artifact_dir,
        metadata=paper_dir / "metadata.json",
        paper_index=paper_dir / "index.md",
        manifest=version_dir / "manifest.json",
        document_jsonl=artifact_dir / "document.jsonl",
        document_markdown=artifact_dir / "document.md",
        analysis=version_dir / "analysis.json",
        summary=version_dir / "summary.md",
    )


def write_paper_metadata(
    root: Path | str,
    ref: ArxivRef,
    metadata: Mapping[str, Any] | None = None,
) -> Path:
    paths = paper_paths(root, ref)
    current: dict[str, Any] = {}
    if paths.metadata.exists():
        current = json.loads(paths.metadata.read_text(encoding="utf-8"))
    incoming = dict(metadata or {})
    current.update({key: value for key, value in incoming.items() if value not in (None, "", [])})
    current.update(
        {
            "schema_version": 1,
            "source": "arxiv",
            "paper_id": ref.base_id,
            "canonical_url": ref.canonical_abs_url,
            "latest_seen_version": max(
                int(current.get("latest_seen_version", 0)), ref.version or 0
            ),
        }
    )
    _atomic_json(paths.metadata, current)
    _write_paper_index(paths, current)
    return paths.metadata


def fetch_paper(
    root: Path | str,
    ref: ArxivRef,
    *,
    policy: str = "normal",
    force: bool = False,
) -> FetchResult:
    ref = require_version(ref)
    store = ArtifactStore(root)
    result = fetch_arxiv(ref, store, policy=policy, force=force)
    manifest = result.to_manifest()
    manifest["pipeline_version"] = 1
    manifest["updated_at"] = _now()
    existing = _read_json(store.tracked_manifest_path(ref))
    if existing:
        existing.update(manifest)
        manifest = existing
    store.write_json_atomic(store.tracked_manifest_path(ref), manifest)
    convenience_metadata: dict[str, Any] = {}
    html_record = result.artifacts.get("article.html")
    if html_record is not None and html_record.available:
        html_path = store.artifact_path(ref, "article.html")
        if html_path.exists():
            convenience_metadata = extract_html_metadata(html_path.read_bytes())
    write_paper_metadata(root, ref, convenience_metadata)
    return result


def extract_paper(
    root: Path | str,
    ref: ArxivRef,
    *,
    fetched: FetchResult | None = None,
) -> Document:
    ref = require_version(ref)
    paths = paper_paths(root, ref)
    document = extract_arxiv(ref, root, fetched=fetched)
    extraction = {
        "source_format": document.source_format,
        "block_count": len(document.blocks),
        "document_jsonl_sha256": _sha256(paths.document_jsonl),
        "document_markdown_sha256": _sha256(paths.document_markdown),
        "extractor_version": 1,
        "extracted_at": _now(),
    }
    manifest = _read_json(paths.manifest)
    manifest.update(
        {
            "schema_version": 1,
            "source": "arxiv",
            "base_id": ref.base_id,
            "version_id": ref.version_id,
            "version_tag": ref.version_tag,
            "extraction": extraction,
            "updated_at": _now(),
        }
    )
    _atomic_json(paths.manifest, manifest)
    return document


def read_document_blocks(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise PipelineError(f"canonical full text is missing: {path}")
    blocks: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise PipelineError(f"invalid document JSONL at line {line_number}: {error}") from error
        if not isinstance(value, dict):
            raise PipelineError(f"document JSONL line {line_number} is not an object")
        blocks.append(value)
    if not blocks:
        raise PipelineError("canonical document contains no blocks")
    return blocks


def summarize_paper(
    root: Path | str,
    ref: ArxivRef,
    provider: SummaryProvider,
    *,
    profile: str = "deep",
    force: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], bool]:
    ref = require_version(ref)
    paths = paper_paths(root, ref)
    blocks = read_document_blocks(paths.document_jsonl)
    stored_metadata = _read_json(paths.metadata)
    if metadata:
        stored_metadata.update(metadata)
    stored_metadata.update(
        {
            "arxiv_id": ref.version_id,
            "paper_id": ref.base_id,
            "canonical_url": ref.canonical_abs_url,
        }
    )
    write_paper_metadata(root, ref, stored_metadata)

    schema_path = paths.root / "schemas" / "paper-summary-v1.json"
    prompt_path = paths.root / "prompts" / "paper-summary-v1.md"
    cache_key = {
        "document_jsonl_sha256": _sha256(paths.document_jsonl),
        "metadata_sha256": hashlib.sha256(
            json.dumps(
                stored_metadata,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode("utf-8")
        ).hexdigest(),
        "schema_sha256": _sha256(schema_path),
        "prompt_sha256": _sha256(prompt_path),
        "provider": provider.name,
        "profile": profile,
        "pipeline_version": 1,
    }
    manifest = _read_json(paths.manifest)
    prior = manifest.get("summary")
    if isinstance(prior, dict) and paths.analysis.exists() and "metadata_sha256" not in prior:
        prior_analysis = _read_json(paths.analysis)
        prior_provenance = prior_analysis.get("provenance", {})
        if (
            isinstance(prior_provenance, dict)
            and prior_provenance.get("metadata_sha256") == cache_key["metadata_sha256"]
        ):
            prior["metadata_sha256"] = cache_key["metadata_sha256"]
            _atomic_json(paths.manifest, manifest)
    if (
        not force
        and isinstance(prior, dict)
        and all(prior.get(key) == value for key, value in cache_key.items())
        and paths.analysis.exists()
        and paths.summary.exists()
    ):
        return json.loads(paths.analysis.read_text(encoding="utf-8")), True

    result = analyze_document(blocks, stored_metadata, provider, schema_path, profile)
    _atomic_json(paths.analysis, result)
    _atomic_text(paths.summary, render_summary(result))
    manifest["summary"] = {
        **cache_key,
        "analysis_sha256": _sha256(paths.analysis),
        "summary_sha256": _sha256(paths.summary),
        "status": "ai-draft",
        "generated_at": result["provenance"]["generated_at"],
    }
    manifest["updated_at"] = _now()
    _atomic_json(paths.manifest, manifest)
    _write_paper_index(paths, stored_metadata)
    return result, False


def process_paper(
    root: Path | str,
    ref: ArxivRef,
    provider: SummaryProvider,
    *,
    policy: str = "normal",
    profile: str = "deep",
    force_fetch: bool = False,
    force_summary: bool = False,
    metadata: Mapping[str, Any] | None = None,
) -> ProcessResult:
    ref = require_version(ref)
    write_paper_metadata(root, ref, metadata)
    fetched = fetch_paper(root, ref, policy=policy, force=force_fetch)
    document = extract_paper(root, ref, fetched=fetched)
    _, cached = summarize_paper(
        root,
        ref,
        provider,
        profile=profile,
        force=force_summary,
        metadata=metadata,
    )
    return ProcessResult(
        ref=ref,
        paths=paper_paths(root, ref),
        source_format=document.source_format,
        block_count=len(document.blocks),
        cached_summary=cached,
    )


def approve_paper(
    root: Path | str,
    ref: ArxivRef,
    *,
    reviewer: str,
    now: datetime | None = None,
) -> Path:
    if not reviewer.strip():
        raise PipelineError("reviewer must be non-empty")
    paths = paper_paths(root, require_version(ref))
    manifest = _read_json(paths.manifest)
    summary = manifest.get("summary")
    if not isinstance(summary, dict) or not paths.summary.exists():
        raise PipelineError("cannot approve a paper without a validated summary")
    summary["status"] = "verified"
    summary["verified_by"] = reviewer.strip()
    summary["verified_at"] = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    manifest["updated_at"] = _now()
    _atomic_json(paths.manifest, manifest)
    _write_paper_index(paths, _read_json(paths.metadata))
    return paths.manifest


def _write_paper_index(paths: PaperPaths, metadata: Mapping[str, Any]) -> None:
    title = str(metadata.get("title") or metadata.get("paper_id") or paths.paper_dir.name)
    paper_id = str(metadata.get("paper_id") or paths.paper_dir.name.replace("--", "/"))
    lines = [
        f"# {title}",
        "",
        f"- **arXiv:** [{paper_id}](https://arxiv.org/abs/{paper_id})",
        f"- **Latest seen version:** v{metadata.get('latest_seen_version', '?')}",
        "",
        "## Versions",
        "",
    ]
    versions_root = paths.paper_dir / "versions"
    versions: list[Path] = sorted(versions_root.glob("v*")) if versions_root.exists() else []
    if not versions:
        lines.append("Пока нет обработанных версий.")
    for version in versions:
        summary_path = version / "summary.md"
        manifest = _read_json(version / "manifest.json")
        summary_state = manifest.get("summary", {})
        status = summary_state.get("status", "fetched") if isinstance(summary_state, dict) else "fetched"
        if summary_path.exists():
            lines.append(f"- [{version.name} deep summary](versions/{version.name}/summary.md) — `{status}`")
        else:
            lines.append(f"- {version.name} — `{status}`")
    lines.extend(
        [
            "",
            "> AI summary — это draft до `aidb paper approve`; перенос в knowledge/ADOPTION остаётся ручным.",
            "",
        ]
    )
    _atomic_text(paths.paper_index, "\n".join(lines))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PipelineError(f"expected JSON object in {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    _atomic_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def _atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as output:
            temporary = Path(output.name)
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    except BaseException:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
