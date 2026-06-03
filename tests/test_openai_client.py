from types import SimpleNamespace

import pytest

from tjcmfrnc_chat.config import RuntimeConfig
from tjcmfrnc_chat.conversation import Conversation
from tjcmfrnc_chat.openai_client import ChatClientError, OpenAIChatClient
from tjcmfrnc_chat.prompts import ASSISTANT_SYSTEM_PROMPT


class FakeResponses:
    def __init__(self, response: object | None = None, exc: Exception | None = None) -> None:
        self.response = response or SimpleNamespace(output_text="assistant reply")
        self.exc = exc
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        if self.exc:
            raise self.exc
        return self.response


def test_send_uses_configured_model_and_conversation_input() -> None:
    conversation = Conversation()
    conversation.add_user_message("hello")
    fake = FakeResponses()
    client = OpenAIChatClient(
        RuntimeConfig(api_key="sk-test", model="gpt-5.5", timeout_seconds=60),
        responses_client=fake,
    )

    result = client.send(conversation)

    assert result == "assistant reply"
    assert fake.calls == [
        {
            "model": "gpt-5.5",
            "input": [
                {"role": "system", "content": ASSISTANT_SYSTEM_PROMPT},
                {"role": "user", "content": "hello"},
            ],
        }
    ]


def test_send_requires_api_key() -> None:
    client = OpenAIChatClient(RuntimeConfig(api_key=None), responses_client=FakeResponses())

    with pytest.raises(ChatClientError, match="OPENAI_API_KEY"):
        client.send(Conversation())


def test_send_wraps_request_failures() -> None:
    conversation = Conversation()
    conversation.add_user_message("hello")
    client = OpenAIChatClient(
        RuntimeConfig(api_key="sk-test"),
        responses_client=FakeResponses(exc=RuntimeError("network")),
    )

    with pytest.raises(ChatClientError, match="Assistant request failed"):
        client.send(conversation)


def test_send_rejects_empty_text_response() -> None:
    conversation = Conversation()
    conversation.add_user_message("hello")
    client = OpenAIChatClient(
        RuntimeConfig(api_key="sk-test"),
        responses_client=FakeResponses(response=SimpleNamespace(output_text=" ")),
    )

    with pytest.raises(ChatClientError, match="did not include text"):
        client.send(conversation)
