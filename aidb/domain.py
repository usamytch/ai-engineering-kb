"""Core identifiers shared by AIDB's arXiv pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import unquote, urlsplit


_MODERN_ID_RE = re.compile(
    r"(?P<year_month>\d{4})\.(?P<number>\d{4,5})(?:v(?P<version>[1-9]\d*))?"
)
_LEGACY_ID_RE = re.compile(
    r"(?P<archive>[a-z][a-z0-9.-]*)/(?P<number>\d{7})(?:v(?P<version>[1-9]\d*))?",
    re.IGNORECASE,
)
_ARXIV_PREFIX_RE = re.compile(r"arxiv:\s*", re.IGNORECASE)
_ARXIV_HOSTS = frozenset({"arxiv.org", "www.arxiv.org", "export.arxiv.org"})
_ARXIV_URL_KIND_RE = re.compile(r"/(abs|pdf|html|src)/(.+)")
_MAX_INPUT_LENGTH = 512


@dataclass(frozen=True, slots=True)
class ArxivRef:
    """A canonical arXiv paper identity with an optional explicit version."""

    base_id: str
    version: int | None = None

    def __post_init__(self) -> None:
        canonical_base, embedded_version = _parse_bare_id(self.base_id)
        if embedded_version is not None:
            raise ValueError(
                "base_id must not contain a version suffix; pass version separately"
            )
        if canonical_base != self.base_id:
            raise ValueError(f"base_id is not canonical: {self.base_id!r}")
        if self.version is not None and (
            isinstance(self.version, bool)
            or not isinstance(self.version, int)
            or self.version < 1
        ):
            raise ValueError("version must be a positive integer or None")

    @classmethod
    def parse(cls, value: str) -> ArxivRef:
        """Parse a bare arXiv ID, ``arXiv:`` ID, or supported arXiv URL."""

        if not isinstance(value, str):
            raise ValueError("arXiv reference must be a string")
        candidate = value.strip()
        if not candidate:
            raise ValueError("arXiv reference must not be empty")
        if len(candidate) > _MAX_INPUT_LENGTH:
            raise ValueError("arXiv reference is too long")

        if "://" in candidate:
            candidate = _id_from_url(candidate)
        else:
            candidate = _ARXIV_PREFIX_RE.sub("", candidate, count=1)

        base_id, version = _parse_bare_id(candidate)
        return cls(base_id=base_id, version=version)

    @property
    def version_id(self) -> str:
        suffix = self.version_tag or ""
        return f"{self.base_id}{suffix}"

    @property
    def version_tag(self) -> str | None:
        return f"v{self.version}" if self.version is not None else None

    @property
    def path_key(self) -> str:
        return self.base_id.replace("/", "--")

    @property
    def canonical_abs_url(self) -> str:
        return f"https://arxiv.org/abs/{self.version_id}"


def try_parse_arxiv_ref(value: str) -> ArxivRef | None:
    """Return a parsed reference, or ``None`` when *value* is not one."""

    try:
        return ArxivRef.parse(value)
    except (TypeError, ValueError):
        return None


def _id_from_url(value: str) -> str:
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise ValueError(f"invalid arXiv URL: {value!r}") from exc

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("arXiv URL must use http or https")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("arXiv URL must not contain credentials")
    if parsed.hostname is None or parsed.hostname.lower() not in _ARXIV_HOSTS:
        raise ValueError(f"not an arXiv URL: {value!r}")
    if port is not None:
        raise ValueError("arXiv URL must not contain an explicit port")

    match = _ARXIV_URL_KIND_RE.fullmatch(unquote(parsed.path))
    if match is None:
        raise ValueError("arXiv URL path must start with /abs, /pdf, /html, or /src")

    kind, identifier = match.groups()
    if kind == "pdf" and identifier.lower().endswith(".pdf"):
        identifier = identifier[:-4]
    if not identifier:
        raise ValueError("arXiv URL does not contain a paper ID")
    return identifier


def _parse_bare_id(value: str) -> tuple[str, int | None]:
    modern = _MODERN_ID_RE.fullmatch(value)
    if modern is not None:
        year_month = modern.group("year_month")
        month = int(year_month[2:])
        if not 1 <= month <= 12:
            raise ValueError(f"invalid month in arXiv ID: {value!r}")
        version = modern.group("version")
        return (
            f"{year_month}.{modern.group('number')}",
            int(version) if version is not None else None,
        )

    legacy = _LEGACY_ID_RE.fullmatch(value)
    if legacy is not None:
        number = legacy.group("number")
        month = int(number[2:4])
        if not 1 <= month <= 12:
            raise ValueError(f"invalid month in legacy arXiv ID: {value!r}")
        version = legacy.group("version")
        return (
            f"{legacy.group('archive').lower()}/{number}",
            int(version) if version is not None else None,
        )

    raise ValueError(f"invalid arXiv ID or URL: {value!r}")
