"""Chat client factory and shared protocol."""

from __future__ import annotations

from typing import Protocol

from .config import RuntimeConfig
from .conversation import Conversation
from .ollama_client import OllamaChatClient
from .openai_client import ChatClientError, OpenAIChatClient


class ChatClient(Protocol):
    def send(self, conversation: Conversation) -> str:
        ...


def build_chat_client(config: RuntimeConfig) -> ChatClient:
    if config.provider == "ollama":
        return OllamaChatClient(config)
    return OpenAIChatClient(config)


__all__ = ["ChatClient", "ChatClientError", "build_chat_client"]
