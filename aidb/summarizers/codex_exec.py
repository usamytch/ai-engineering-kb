"""Local Codex CLI adapter with an isolated, read-only execution context."""

from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


class CodexExecError(RuntimeError):
    """Raised when the Codex CLI cannot produce a structured result."""


@dataclass(frozen=True)
class CodexExecProvider:
    """Run one stateless Codex analysis outside the repository.

    User configuration is ignored so project MCP servers and other tools are
    not inherited. The model is confined to an empty temporary directory with
    a read-only sandbox; all source material is supplied through stdin.
    """

    executable: str = "codex"
    timeout_seconds: int = 900
    model: str | None = None

    @property
    def name(self) -> str:
        return f"codex-exec:{self.model}" if self.model else "codex-exec:configured-default"

    def generate(
        self, prompt: str, schema: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        with tempfile.TemporaryDirectory(prefix="aidb-summary-") as directory:
            workdir = Path(directory)
            schema_path = workdir / "output-schema.json"
            output_path = workdir / "last-message.json"
            schema_path.write_text(
                json.dumps(schema, ensure_ascii=False), encoding="utf-8"
            )
            command = [
                self.executable,
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--output-schema",
                str(schema_path),
                "--output-last-message",
                str(output_path),
            ]
            if self.model:
                command.extend(["--model", self.model])
            command.append("-")
            try:
                completed = subprocess.run(
                    command,
                    cwd=workdir,
                    input=prompt,
                    text=True,
                    capture_output=True,
                    timeout=self.timeout_seconds,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as error:
                raise CodexExecError(f"codex exec failed: {error}") from error
            if completed.returncode != 0:
                detail = (completed.stderr or completed.stdout or "unknown error").strip()
                raise CodexExecError(
                    f"codex exec exited with {completed.returncode}: {detail[:500]}"
                )
            try:
                result = json.loads(output_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise CodexExecError(
                    "codex exec did not write a valid structured final message"
                ) from error
            if not isinstance(result, dict):
                raise CodexExecError("codex exec returned a non-object JSON value")
            return result
