"""Provider-neutral, evidence-first paper analysis pipeline."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

from aidb.validation import (
    SummaryValidationError,
    canonicalize_language_contract,
    validate_summary,
)


@runtime_checkable
class SummaryProvider(Protocol):
    """Minimal interface implemented by local and remote LLM providers."""

    @property
    def name(self) -> str:
        """Stable provider name recorded in generated provenance."""

    def generate(
        self, prompt: str, schema: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        """Return a JSON-like object conforming to ``schema``."""


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def _normalize_blocks(blocks: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for position, raw in enumerate(blocks):
        block_id = raw.get("id", raw.get("block_id"))
        text = raw.get("text")
        if not isinstance(block_id, str) or not block_id.strip():
            raise SummaryValidationError(f"block {position} has no non-empty id")
        if block_id in seen:
            raise SummaryValidationError(f"duplicate block id: {block_id}")
        if not isinstance(text, str) or not text.strip():
            raise SummaryValidationError(f"block {block_id} has no text")
        seen.add(block_id)
        block: dict[str, Any] = {"id": block_id, "text": text}
        for key in ("kind", "section_path", "locator"):
            if key in raw:
                block[key] = raw[key]
        normalized.append(block)
    if not normalized:
        raise SummaryValidationError("cannot analyze an empty document")
    return normalized


def _provider_schema(final_schema: Mapping[str, Any]) -> dict[str, Any]:
    """Remove code-owned provenance from the schema sent to the model."""

    schema = copy.deepcopy(dict(final_schema))
    # Keep the provider schema inside the Structured Outputs JSON Schema
    # subset. These document annotations remain in the tracked final schema.
    for annotation in ("$schema", "$id", "title"):
        schema.pop(annotation, None)
    properties = schema.get("properties")
    if isinstance(properties, dict):
        properties.pop("provenance", None)
    required = schema.get("required")
    if isinstance(required, list):
        schema["required"] = [key for key in required if key != "provenance"]
    return schema


def _schema_version(schema: Mapping[str, Any]) -> str:
    try:
        value = schema["properties"]["provenance"]["properties"][
            "schema_version"
        ]["const"]
    except (KeyError, TypeError):
        return "paper-summary-v1"
    return str(value)


def _load_prompt_template() -> str:
    path = Path(__file__).resolve().parents[2] / "prompts" / "paper-summary-v1.md"
    return path.read_text(encoding="utf-8")


def analyze_document(
    blocks: Sequence[Mapping[str, Any]],
    metadata: Mapping[str, Any],
    provider: SummaryProvider,
    schema_path: str | Path,
    profile: str = "deep",
) -> dict[str, Any]:
    """Analyze normalized blocks and reject any unsupported model claims.

    The LLM never controls provenance. The provider receives a schema without
    the ``provenance`` field; this function validates the model output, adds
    hashes and generation metadata, then validates the final result again.
    """

    normalized_blocks = _normalize_blocks(blocks)
    if not isinstance(metadata, Mapping):
        raise SummaryValidationError("metadata must be an object")
    if not isinstance(profile, str) or not profile.strip():
        raise SummaryValidationError("profile must be a non-empty string")

    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise SummaryValidationError("summary schema must be a JSON object")
    model_schema = _provider_schema(schema)

    input_payload = {
        "profile": profile,
        "metadata": dict(metadata),
        "blocks": normalized_blocks,
    }
    prompt = _load_prompt_template().replace(
        "{{PROFILE}}", profile
    ).replace("{{DOCUMENT_JSON}}", json.dumps(input_payload, ensure_ascii=False))

    generated = provider.generate(prompt, model_schema)
    if not isinstance(generated, Mapping):
        raise SummaryValidationError("summary provider returned a non-object")
    result = copy.deepcopy(dict(generated))
    canonicalize_language_contract(result)
    repair_count = 0
    try:
        validate_summary(result, normalized_blocks, schema=model_schema)
    except SummaryValidationError as first_error:
        repair_prompt = (
            prompt
            + "\n\nThe previous candidate failed deterministic validation. Correct the complete "
            "JSON object using only exact quotes copied from the supplied blocks. Do not "
            "explain the correction.\n\nValidator error:\n"
            + str(first_error)
            + "\n\nPrevious candidate JSON:\n"
            + json.dumps(result, ensure_ascii=False)
        )
        repaired = provider.generate(repair_prompt, model_schema)
        if not isinstance(repaired, Mapping):
            raise SummaryValidationError("summary provider returned a non-object repair")
        result = copy.deepcopy(dict(repaired))
        canonicalize_language_contract(result)
        validate_summary(result, normalized_blocks, schema=model_schema)
        repair_count = 1

    result["provenance"] = {
        "schema_version": _schema_version(schema),
        "profile": profile,
        "provider": provider.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "document_sha256": hashlib.sha256(
            _canonical_json(normalized_blocks).encode("utf-8")
        ).hexdigest(),
        "metadata_sha256": hashlib.sha256(
            _canonical_json(dict(metadata)).encode("utf-8")
        ).hexdigest(),
        "block_count": len(normalized_blocks),
        "repair_count": repair_count,
    }
    validate_summary(result, normalized_blocks, schema=schema)
    return result
