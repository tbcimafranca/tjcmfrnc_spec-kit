"""Runtime configuration for the desktop chat app."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_MODEL = "gpt-5.5"
DEFAULT_PROVIDER = "openai"
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "smollm2:135m"
DEFAULT_TIMEOUT_SECONDS = 60


@dataclass(frozen=True)
class RuntimeConfig:
    api_key: str | None
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL
    ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL
    ollama_model: str = DEFAULT_OLLAMA_MODEL
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS

    @property
    def api_key_present(self) -> bool:
        return bool(self.api_key)

    @property
    def active_model(self) -> str:
        if self.provider == "ollama":
            return self.ollama_model
        return self.model

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "RuntimeConfig":
        source = env if env is not None else os.environ
        api_key = _clean_optional(source.get("OPENAI_API_KEY"))
        provider = (_clean_optional(source.get("CHAT_PROVIDER")) or DEFAULT_PROVIDER).lower()
        model = _clean_optional(source.get("OPENAI_MODEL")) or DEFAULT_MODEL
        ollama_base_url = _clean_optional(source.get("OLLAMA_BASE_URL")) or DEFAULT_OLLAMA_BASE_URL
        ollama_model = _clean_optional(source.get("OLLAMA_MODEL")) or DEFAULT_OLLAMA_MODEL
        timeout_seconds = _parse_timeout(source.get("OPENAI_TIMEOUT_SECONDS"))
        if provider not in {"openai", "ollama"}:
            provider = DEFAULT_PROVIDER
        return cls(
            api_key=api_key,
            provider=provider,
            model=model,
            ollama_base_url=ollama_base_url.rstrip("/"),
            ollama_model=ollama_model,
            timeout_seconds=timeout_seconds,
        )


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
