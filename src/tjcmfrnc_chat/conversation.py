"""In-memory conversation state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

Role = Literal["user", "assistant", "system"]
VALID_ROLES = {"user", "assistant", "system"}


@dataclass(frozen=True)
class ChatMessage:
    role: Role
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.role not in VALID_ROLES:
            raise ValueError(f"Unsupported message role: {self.role}")
        if not self.content.strip():
            raise ValueError("Message content must not be empty")

    def to_openai_input(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


class Conversation:
    def __init__(self) -> None:
        self._messages: list[ChatMessage] = []

    @property
    def messages(self) -> tuple[ChatMessage, ...]:
        return tuple(self._messages)

    def add_message(self, role: Role, content: str) -> ChatMessage:
        message = ChatMessage(role=role, content=content.strip())
        self._messages.append(message)
        return message

    def add_user_message(self, content: str) -> ChatMessage:
        return self.add_message("user", content)

    def add_assistant_message(self, content: str) -> ChatMessage:
        return self.add_message("assistant", content)

    def clear(self) -> None:
        self._messages.clear()

    def to_openai_input(self) -> list[dict[str, str]]:
        return [message.to_openai_input() for message in self._messages]
