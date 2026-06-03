"""OpenAI Responses API adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .config import RuntimeConfig
from .conversation import Conversation
from .prompts import ASSISTANT_SYSTEM_PROMPT


class ChatClientError(RuntimeError):
    """Raised when the assistant response cannot be produced."""


class ResponsesClientProtocol(Protocol):
    def create(self, **kwargs: object) -> object:
        ...


@dataclass
class OpenAIChatClient:
    config: RuntimeConfig
    responses_client: ResponsesClientProtocol | None = None

    def send(self, conversation: Conversation) -> str:
        if not self.config.api_key_present:
            raise ChatClientError("OPENAI_API_KEY is not configured.")

        responses = self.responses_client or self._build_responses_client()
        try:
            response = responses.create(
                model=self.config.model,
                input=[
                    {"role": "system", "content": ASSISTANT_SYSTEM_PROMPT},
                    *conversation.to_openai_input(),
                ],
            )
        except Exception as exc:  # pragma: no cover - exact SDK exceptions vary
            raise ChatClientError("Assistant request failed. Check your connection and API configuration.") from exc

        text = _extract_output_text(response)
        if not text:
            raise ChatClientError("Assistant response did not include text output.")
        return text

    def _build_responses_client(self) -> ResponsesClientProtocol:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - dependency check
            raise ChatClientError("The openai package is not installed.") from exc

        client = OpenAI(api_key=self.config.api_key, timeout=self.config.timeout_seconds)
        return client.responses


def _extract_output_text(response: object) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str):
        return output_text.strip()

    if isinstance(response, dict):
        value = response.get("output_text")
        if isinstance(value, str):
            return value.strip()

    return ""
