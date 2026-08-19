"""Local storage for immutable, downloaded paper artifacts.

Raw files deliberately live below ``.aidb`` and are not intended for Git.  The
small manifest describing them lives next to the tracked paper analysis.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import mimetypes
import os
from pathlib import Path, PurePosixPath
import tempfile
from typing import BinaryIO, Mapping, Protocol


class ArxivRefLike(Protocol):
    path_key: str
    version_tag: str


def _safe_relative(value: str, *, field: str) -> Path:
    posix = PurePosixPath(value)
    if not value or posix.is_absolute() or any(part in {"", ".", ".."} for part in posix.parts):
        raise ValueError(f"unsafe {field}: {value!r}")
    return Path(*posix.parts)


@dataclass(frozen=True)
class ArtifactRecord:
    name: str
    path: str | None
    available: bool
    status: int | str
    mime_type: str | None
    sha256: str | None
    bytes: int
    fetched_at: str
    url: str | None = None
    cached: bool = False
    error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class ArtifactStore:
    """Resolve artifact paths and write downloads atomically."""

    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()

    def artifact_dir(self, ref: ArxivRefLike) -> Path:
        key = _safe_relative(ref.path_key, field="arXiv path key")
        version = _safe_relative(ref.version_tag, field="arXiv version")
        if len(version.parts) != 1:
            raise ValueError(f"unsafe arXiv version: {ref.version_tag!r}")
        return self.root / ".aidb" / "artifacts" / "arxiv" / key / version

    def artifact_path(self, ref: ArxivRefLike, name: str) -> Path:
        relative = _safe_relative(name, field="artifact name")
        if len(relative.parts) != 1:
            raise ValueError(f"artifact name must be a file name: {name!r}")
        return self.artifact_dir(ref) / relative

    def tracked_manifest_path(self, ref: ArxivRefLike) -> Path:
        key = _safe_relative(ref.path_key, field="arXiv path key")
        version = _safe_relative(ref.version_tag, field="arXiv version")
        if len(version.parts) != 1:
            raise ValueError(f"unsafe arXiv version: {ref.version_tag!r}")
        return self.root / "papers" / "arxiv" / key / "versions" / version / "manifest.json"

    def write_stream(
        self,
        ref: ArxivRefLike,
        name: str,
        stream: BinaryIO,
        *,
        url: str | None,
        status: int | str,
        mime_type: str | None,
        max_bytes: int,
        fetched_at: str | None = None,
    ) -> ArtifactRecord:
        destination = self.artifact_path(ref, name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256()
        size = 0
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=destination.parent, prefix=f".{destination.name}.", delete=False
            ) as output:
                temporary = Path(output.name)
                while True:
                    chunk = stream.read(64 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > max_bytes:
                        raise ValueError(f"artifact exceeds {max_bytes} byte limit: {name}")
                    output.write(chunk)
                    digest.update(chunk)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, destination)
        except BaseException:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
            raise

        return ArtifactRecord(
            name=name,
            path=str(destination.relative_to(self.root)),
            available=True,
            status=status,
            mime_type=mime_type,
            sha256=digest.hexdigest(),
            bytes=size,
            fetched_at=fetched_at or _now(),
            url=url,
        )

    def existing_record(
        self,
        ref: ArxivRefLike,
        name: str,
        *,
        url: str | None = None,
        mime_type: str | None = None,
    ) -> ArtifactRecord | None:
        path = self.artifact_path(ref, name)
        if not path.is_file():
            return None
        digest = hashlib.sha256()
        size = 0
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(64 * 1024), b""):
                size += len(chunk)
                digest.update(chunk)
        timestamp = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        return ArtifactRecord(
            name=name,
            path=str(path.relative_to(self.root)),
            available=True,
            status="cached",
            mime_type=mime_type or mimetypes.guess_type(path.name)[0],
            sha256=digest.hexdigest(),
            bytes=size,
            fetched_at=timestamp,
            url=url,
            cached=True,
        )

    def write_json_atomic(self, path: Path, payload: Mapping[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = (json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        temporary: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=path.parent, prefix=f".{path.name}.", delete=False
            ) as output:
                temporary = Path(output.name)
                output.write(data)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, path)
        except BaseException:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
            raise


def unavailable_record(
    name: str,
    *,
    url: str,
    status: int | str,
    mime_type: str | None = None,
    error: str | None = None,
) -> ArtifactRecord:
    return ArtifactRecord(
        name=name,
        path=None,
        available=False,
        status=status,
        mime_type=mime_type,
        sha256=None,
        bytes=0,
        fetched_at=_now(),
        url=url,
        error=error,
    )


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
