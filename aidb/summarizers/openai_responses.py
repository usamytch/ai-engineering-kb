"""OpenAI Responses API adapter implemented with the Python standard library."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping


_RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"


class OpenAIResponsesError(RuntimeError):
    """Raised when the Responses API cannot produce a structured result."""


def _output_text(response: Mapping[str, Any]) -> str:
    direct = response.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct
    for item in response.get("output", []):
        if not isinstance(item, Mapping):
            continue
        for content in item.get("content", []):
            if (
                isinstance(content, Mapping)
                and content.get("type") == "output_text"
                and isinstance(content.get("text"), str)
            ):
                return content["text"]
    raise OpenAIResponsesError("Responses API returned no output_text")


@dataclass(frozen=True)
class OpenAIResponsesProvider:
    """Generate strict JSON with Responses API and no enabled tools."""

    model: str = "gpt-5.6"
    timeout_seconds: int = 300

    @property
    def name(self) -> str:
        return f"openai-responses:{self.model}"

    def generate(
        self, prompt: str, schema: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise OpenAIResponsesError("OPENAI_API_KEY is not set")

        payload = {
            "model": self.model,
            "input": prompt,
            "store": False,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "paper_summary",
                    "strict": True,
                    "schema": dict(schema),
                }
            },
        }
        request = urllib.request.Request(
            _RESPONSES_ENDPOINT,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request, timeout=self.timeout_seconds
            ) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise OpenAIResponsesError(
                f"Responses API request failed with HTTP {error.code}"
            ) from error
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            raise OpenAIResponsesError(f"Responses API request failed: {error}") from error

        if not isinstance(response_payload, Mapping):
            raise OpenAIResponsesError("Responses API returned a non-object payload")
        try:
            result = json.loads(_output_text(response_payload))
        except json.JSONDecodeError as error:
            raise OpenAIResponsesError(
                "Responses API output_text was not valid JSON"
            ) from error
        if not isinstance(result, dict):
            raise OpenAIResponsesError("Responses API returned a non-object JSON value")
        return result
