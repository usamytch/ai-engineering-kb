"""Deterministic validation for evidence-first paper summaries."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any


class SummaryValidationError(ValueError):
    """Raised when a summary is structurally invalid or unsupported."""


_EN_LABELS = {
    "executive_summary": "Executive summary",
    "problem": "Problem",
    "statement": "Statement",
    "importance": "Why it matters",
    "scope": "Scope",
    "method": "Method",
    "key_components": "Key components",
    "assumptions": "Assumptions",
    "claims": "Main claims",
    "results": "Results",
    "context": "Context",
    "evidence": "Evidence",
    "evaluation": "Experimental evaluation",
    "datasets": "Datasets",
    "baselines": "Baselines",
    "metrics": "Metrics",
    "ablations": "Ablations",
    "negative_results": "Negative results",
    "limitations": "Limitations",
    "reproducibility": "Reproducibility",
    "status": "Status",
    "available_artifacts": "Available artifacts",
    "missing_pieces": "Missing pieces",
    "aidb_assessment": "AIDB assessment",
    "novelty": "Novelty",
    "usefulness": "Usefulness",
    "confidence": "Confidence",
    "recommended_action": "Recommended action",
    "rationale": "Rationale",
    "uncertainties": "Uncertainties",
    "open_questions": "Open questions",
    "proposed_experiments": "Proposed AIDB experiments",
    "hypothesis": "Hypothesis",
    "baseline": "Baseline",
    "primary_metric": "Primary metric",
    "stop_condition": "Stop condition",
    "provenance": "Provenance",
    "schema": "Schema",
    "profile": "Profile",
    "provider": "Provider",
    "generated": "Generated",
    "document_sha256": "Document SHA-256",
    "metadata_sha256": "Metadata SHA-256",
    "blocks": "Blocks",
    "repair_count": "Deterministic repair attempts",
    "status_strong": "strong",
    "status_partial": "partial",
    "status_weak": "weak",
    "status_unknown": "unknown",
    "confidence_high": "high",
    "confidence_medium": "medium",
    "confidence_low": "low",
    "action_adopt": "adopt",
    "action_watch": "watch",
    "action_read": "read",
    "action_reject": "reject",
}

_RU_LABELS = {
    "executive_summary": "Краткое резюме",
    "problem": "Задача",
    "statement": "Постановка",
    "importance": "Почему это важно",
    "scope": "Область исследования",
    "method": "Метод",
    "key_components": "Ключевые компоненты",
    "assumptions": "Допущения",
    "claims": "Основные утверждения",
    "results": "Результаты",
    "context": "Контекст",
    "evidence": "Доказательства",
    "evaluation": "Экспериментальная оценка",
    "datasets": "Датасеты",
    "baselines": "Базовые методы",
    "metrics": "Метрики",
    "ablations": "Абляции",
    "negative_results": "Отрицательные результаты",
    "limitations": "Ограничения",
    "reproducibility": "Воспроизводимость",
    "status": "Статус",
    "available_artifacts": "Доступные артефакты",
    "missing_pieces": "Чего не хватает",
    "aidb_assessment": "Оценка AIDB",
    "novelty": "Новизна",
    "usefulness": "Полезность",
    "confidence": "Уверенность",
    "recommended_action": "Рекомендация",
    "rationale": "Обоснование",
    "uncertainties": "Неопределённости",
    "open_questions": "Открытые вопросы",
    "proposed_experiments": "Предлагаемые эксперименты AIDB",
    "hypothesis": "Гипотеза",
    "baseline": "Базовый вариант",
    "primary_metric": "Главная метрика",
    "stop_condition": "Условие остановки",
    "provenance": "Данные о происхождении",
    "schema": "Схема",
    "profile": "Профиль",
    "provider": "Провайдер",
    "generated": "Сгенерировано",
    "document_sha256": "SHA-256 документа",
    "metadata_sha256": "SHA-256 метаданных",
    "blocks": "Блоки",
    "repair_count": "Попытки детерминированного исправления",
    "status_strong": "высокая",
    "status_partial": "частичная",
    "status_weak": "низкая",
    "status_unknown": "неизвестна",
    "confidence_high": "высокая",
    "confidence_medium": "средняя",
    "confidence_low": "низкая",
    "action_adopt": "внедрить",
    "action_watch": "наблюдать",
    "action_read": "прочитать",
    "action_reject": "отклонить",
}

_KNOWN_LABELS = {"en": _EN_LABELS, "ru": _RU_LABELS}


def _primary_language(code: Any) -> str:
    if not isinstance(code, str):
        return ""
    return code.strip().lower().split("-", 1)[0]


def labels_for_language(
    language_code: Any, authored_labels: Mapping[str, Any]
) -> dict[str, Any]:
    """Return deterministic en/ru labels or model-authored fallback labels."""

    known = _KNOWN_LABELS.get(_primary_language(language_code))
    return dict(known if known is not None else authored_labels)


def canonicalize_language_contract(summary: dict[str, Any]) -> None:
    """Replace model-authored labels for known locales with trusted labels."""

    language = summary.get("language")
    if not isinstance(language, Mapping):
        return
    known = _KNOWN_LABELS.get(_primary_language(language.get("code")))
    if known is not None:
        summary["labels"] = dict(known)


def normalize_evidence_text(value: str) -> str:
    """Normalize Unicode and whitespace without changing words or numbers."""

    return " ".join(unicodedata.normalize("NFKC", value).split())


def _fail(path: str, message: str) -> None:
    raise SummaryValidationError(f"{path}: {message}")


def _resolve_ref(reference: str, root_schema: Mapping[str, Any]) -> Mapping[str, Any]:
    if not reference.startswith("#/"):
        raise SummaryValidationError(f"unsupported schema reference: {reference}")
    resolved: Any = root_schema
    for token in reference[2:].split("/"):
        key = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(resolved, Mapping) or key not in resolved:
            raise SummaryValidationError(f"unresolved schema reference: {reference}")
        resolved = resolved[key]
    if not isinstance(resolved, Mapping):
        raise SummaryValidationError(f"schema reference is not an object: {reference}")
    return resolved


def _validate_schema(
    value: Any,
    schema: Mapping[str, Any],
    path: str = "$",
    root_schema: Mapping[str, Any] | None = None,
) -> None:
    if root_schema is None:
        root_schema = schema
    reference = schema.get("$ref")
    if isinstance(reference, str):
        _validate_schema(value, _resolve_ref(reference, root_schema), path, root_schema)
        return
    expected = schema.get("type")
    type_checks = {
        "object": lambda item: isinstance(item, Mapping),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "boolean": lambda item: isinstance(item, bool),
        "null": lambda item: item is None,
    }
    if expected in type_checks and not type_checks[expected](value):
        _fail(path, f"expected {expected}")
    if "const" in schema and value != schema["const"]:
        _fail(path, f"expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        _fail(path, f"expected one of {schema['enum']!r}")

    if expected == "object" and isinstance(value, Mapping):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                _fail(path, f"missing required field {key!r}")
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                _fail(path, f"unknown fields: {', '.join(unknown)}")
        for key, child in properties.items():
            if key in value and isinstance(child, Mapping):
                _validate_schema(value[key], child, f"{path}.{key}", root_schema)
    elif expected == "array" and isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            _fail(path, f"expected at least {schema['minItems']} items")
        child = schema.get("items")
        if isinstance(child, Mapping):
            for index, item in enumerate(value):
                _validate_schema(item, child, f"{path}[{index}]", root_schema)
    elif expected == "string" and isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            _fail(path, f"expected at least {schema['minLength']} characters")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            _fail(path, f"expected at most {schema['maxLength']} characters")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            _fail(path, f"does not match required pattern {pattern!r}")


_NUMBER_RE = re.compile(
    r"(?<![\w.])[+-]?\d+(?:[.,]\d+)?(?:%|(?![\w.%]))"
)


def _evidence_groups(summary: Mapping[str, Any]) -> list[tuple[str, Mapping[str, Any]]]:
    groups: list[tuple[str, Mapping[str, Any]]] = []
    for section in ("claims", "results", "limitations", "uncertainties"):
        for index, item in enumerate(summary.get(section, [])):
            if isinstance(item, Mapping):
                groups.append((f"$.{section}[{index}]", item))
    evaluation = summary.get("evaluation", {})
    if isinstance(evaluation, Mapping):
        for section in ("datasets", "baselines", "metrics", "ablations", "negative_results"):
            for index, item in enumerate(evaluation.get(section, [])):
                if isinstance(item, Mapping):
                    groups.append((f"$.evaluation.{section}[{index}]", item))
    return groups


def validate_summary(
    summary: Mapping[str, Any],
    blocks: Sequence[Mapping[str, Any]],
    *,
    schema: Mapping[str, Any] | None = None,
) -> None:
    """Validate structure, citations, exact quotes, and numeric grounding."""

    if not isinstance(summary, Mapping):
        raise SummaryValidationError("$: expected object")
    if schema is not None:
        _validate_schema(summary, schema)

    _validate_document_language(summary, blocks)

    block_text: dict[str, str] = {}
    for block in blocks:
        block_id = block.get("id", block.get("block_id"))
        text = block.get("text")
        if isinstance(block_id, str) and isinstance(text, str):
            block_text[block_id] = normalize_evidence_text(text)

    for path, item in _evidence_groups(summary):
        evidence = item.get("evidence")
        if path.startswith(("$.claims", "$.results", "$.evaluation")) and not evidence:
            _fail(f"{path}.evidence", "at least one evidence reference is required")
        if not isinstance(evidence, list):
            continue

        quoted_texts: list[str] = []
        for evidence_index, reference in enumerate(evidence):
            reference_path = f"{path}.evidence[{evidence_index}]"
            if not isinstance(reference, Mapping):
                _fail(reference_path, "expected object")
            block_id = reference.get("block_id")
            quote = reference.get("quote")
            if block_id not in block_text:
                _fail(reference_path, f"unknown block id {block_id!r}")
            if not isinstance(quote, str) or not quote.strip():
                _fail(reference_path, "quote must be a non-empty string")
            normalized_quote = normalize_evidence_text(quote)
            if normalized_quote not in block_text[block_id]:
                _fail(reference_path, "quote is not an exact normalized block substring")
            quoted_texts.append(normalized_quote)

        if path.startswith("$.results"):
            result_text = item.get("result", "")
            numbers = _NUMBER_RE.findall(result_text) if isinstance(result_text, str) else []
            quoted = " ".join(quoted_texts)
            quoted_numbers = {
                _canonical_number(number) for number in _NUMBER_RE.findall(quoted)
            }
            missing = [
                number
                for number in numbers
                if _canonical_number(number) not in quoted_numbers
            ]
            if missing:
                _fail(
                    f"{path}.result",
                    "numeric values absent from cited quotes: " + ", ".join(missing),
                )


def _canonical_number(value: str) -> str:
    """Compare numeric values while allowing prose/table percent formatting."""

    return value.rstrip("%").replace(",", ".")


def _validate_document_language(
    summary: Mapping[str, Any], blocks: Sequence[Mapping[str, Any]]
) -> None:
    """Catch clear en/ru mismatches without guessing among Latin languages."""

    language = summary.get("language")
    if not isinstance(language, Mapping):
        return
    primary = _primary_language(language.get("code"))
    source = " ".join(
        str(block.get("text", ""))
        for block in blocks
        if isinstance(block, Mapping)
    )
    cyrillic = len(re.findall(r"[А-Яа-яЁё]", source))
    latin = len(re.findall(r"[A-Za-z]", source))
    letters = cyrillic + latin
    if letters < 80:
        return
    if cyrillic / letters >= 0.65 and primary != "ru":
        _fail("$.language.code", "does not match predominantly Russian source text")
    if latin / letters >= 0.85 and primary == "ru":
        _fail("$.language.code", "does not match predominantly Latin source text")
