"""Runtime configuration for the desktop chat app."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_MODEL = "gpt-5.5"
DEFAULT_TIMEOUT_SECONDS = 60


@dataclass(frozen=True)
class RuntimeConfig:
    api_key: str | None
    model: str = DEFAULT_MODEL
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS

    @property
    def api_key_present(self) -> bool:
        return bool(self.api_key)

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "RuntimeConfig":
        source = env if env is not None else os.environ
        api_key = _clean_optional(source.get("OPENAI_API_KEY"))
        model = _clean_optional(source.get("OPENAI_MODEL")) or DEFAULT_MODEL
        timeout_seconds = _parse_timeout(source.get("OPENAI_TIMEOUT_SECONDS"))
        return cls(api_key=api_key, model=model, timeout_seconds=timeout_seconds)


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _parse_timeout(value: str | None) -> int:
    if value is None:
        return DEFAULT_TIMEOUT_SECONDS
    try:
        parsed = int(value)
    except ValueError:
        return DEFAULT_TIMEOUT_SECONDS
    if parsed <= 0:
        return DEFAULT_TIMEOUT_SECONDS
    return parsed
