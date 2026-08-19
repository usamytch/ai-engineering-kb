"""Deterministic Markdown rendering for validated paper summaries."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from aidb.validation import labels_for_language


def _text(value: Any) -> str:
    return " ".join(str(value).split())


def _evidence(references: Sequence[Mapping[str, Any]]) -> str:
    return "; ".join(
        f"[{_text(reference['block_id'])}] “{reference['quote']}”"
        for reference in references
    )


def _bullets(values: Sequence[Any]) -> list[str]:
    return [f"- {_text(value)}" for value in values] or ["- —"]


def _grounded(
    values: Sequence[Mapping[str, Any]], evidence_label: str
) -> list[str]:
    lines: list[str] = []
    for value in values:
        lines.extend(
            [
                f"- {_text(value['text'])}",
                f"  - {evidence_label}: {_evidence(value['evidence'])}",
            ]
        )
    return lines or ["- —"]


def render_summary(summary: Mapping[str, Any]) -> str:
    """Render the schema in a stable order without model-authored Markdown."""

    problem = summary["problem"]
    method = summary["method"]
    reproducibility = summary["reproducibility"]
    assessment = summary["aidb_assessment"]
    evaluation = summary["evaluation"]
    provenance = summary["provenance"]
    language = summary["language"]
    labels = labels_for_language(language["code"], summary["labels"])
    lines = [
        f"# {_text(summary['title'])}",
        "",
        f"## {labels['executive_summary']}",
        "",
        _text(summary["executive_summary"]),
        "",
        f"## {labels['problem']}",
        "",
        f"**{labels['statement']}.** {_text(problem['statement'])}",
        "",
        f"**{labels['importance']}.** {_text(problem['importance'])}",
        "",
        f"**{labels['scope']}.** {_text(problem['scope'])}",
        "",
        f"## {labels['method']}",
        "",
        _text(method["overview"]),
        "",
        f"### {labels['key_components']}",
        "",
        *_bullets(method["key_components"]),
        "",
        f"### {labels['assumptions']}",
        "",
        *_bullets(method["assumptions"]),
        "",
        f"## {labels['claims']}",
        "",
    ]
    for item in summary["claims"]:
        lines.extend(
            [
                f"- **{_text(item['claim'])}**",
                f"  - {labels['evidence']}: {_evidence(item['evidence'])}",
            ]
        )
    lines.extend(["", f"## {labels['results']}", ""])
    for item in summary["results"]:
        lines.extend(
            [
                f"- **{_text(item['result'])}**",
                f"  - {labels['context']}: {_text(item['context'])}",
                f"  - {labels['evidence']}: {_evidence(item['evidence'])}",
            ]
        )
    lines.extend(["", f"## {labels['evaluation']}", ""])
    for key in ("datasets", "baselines", "metrics", "ablations", "negative_results"):
        lines.extend(
            [
                f"### {labels[key]}",
                "",
                *_grounded(evaluation[key], labels["evidence"]),
                "",
            ]
        )
    lines.extend(["", f"## {labels['limitations']}", ""])
    for item in summary["limitations"]:
        lines.extend(
            [
                f"- {_text(item['limitation'])}",
                f"  - {labels['evidence']}: {_evidence(item['evidence'])}",
            ]
        )
    lines.extend(
        [
            "",
            f"## {labels['reproducibility']}",
            "",
            f"**{labels['status']}:** {labels['status_' + reproducibility['status']]}",
            "",
            _text(reproducibility["assessment"]),
            "",
            f"**{labels['available_artifacts']}**",
            "",
            *_bullets(reproducibility["artifacts"]),
            "",
            f"**{labels['missing_pieces']}**",
            "",
            *_bullets(reproducibility["missing"]),
            "",
            f"## {labels['aidb_assessment']}",
            "",
            f"- {labels['novelty']}: {_text(assessment['novelty'])}",
            f"- {labels['usefulness']}: {_text(assessment['usefulness'])}",
            f"- {labels['confidence']}: {labels['confidence_' + assessment['confidence']]}",
            f"- {labels['recommended_action']}: {labels['action_' + assessment['recommended_action']]}",
            f"- {labels['rationale']}: {_text(assessment['rationale'])}",
            "",
            f"## {labels['uncertainties']}",
            "",
        ]
    )
    for item in summary["uncertainties"]:
        lines.extend(
            [
                f"- **{_text(item['uncertainty'])}** — {_text(item['why_it_matters'])}",
                f"  - {labels['evidence']}: {_evidence(item['evidence'])}",
            ]
        )
    lines.extend(
        ["", f"## {labels['open_questions']}", "", *_bullets(summary["open_questions"])]
    )
    lines.extend(["", f"## {labels['proposed_experiments']}", ""])
    if not summary["proposed_experiments"]:
        lines.append("- —")
    for item in summary["proposed_experiments"]:
        lines.extend(
            [
                f"- **{labels['hypothesis']}:** {_text(item['hypothesis'])}",
                f"  - {labels['baseline']}: {_text(item['baseline'])}",
                f"  - {labels['primary_metric']}: {_text(item['primary_metric'])}",
                f"  - {labels['stop_condition']}: {_text(item['stop_condition'])}",
            ]
        )
    lines.extend(
        [
            "",
            f"## {labels['provenance']}",
            "",
            f"- {labels['schema']}: `{_text(provenance['schema_version'])}`",
            f"- {labels['profile']}: `{_text(provenance['profile'])}`",
            f"- {labels['provider']}: `{_text(provenance['provider'])}`",
            f"- {labels['generated']}: `{_text(provenance['generated_at'])}`",
            f"- {labels['document_sha256']}: `{_text(provenance['document_sha256'])}`",
            f"- {labels['metadata_sha256']}: `{_text(provenance['metadata_sha256'])}`",
            f"- {labels['blocks']}: {provenance['block_count']}",
            f"- {labels['repair_count']}: {provenance['repair_count']}",
            "",
        ]
    )
    return "\n".join(lines)
