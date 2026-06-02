import json
from io import BytesIO

import pytest

from tjcmfrnc_chat.config import RuntimeConfig
from tjcmfrnc_chat.conversation import Conversation
from tjcmfrnc_chat.ollama_client import OllamaChatClient
from tjcmfrnc_chat.openai_client import ChatClientError


class FakeHTTPResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def __enter__(self) -> "FakeHTTPResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def test_ollama_send_posts_chat_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_urlopen(request: object, timeout: int) -> FakeHTTPResponse:
        calls.append(
            {
                "url": request.full_url,
                "timeout": timeout,
                "payload": json.loads(request.data.decode("utf-8")),
            }
        )
        return FakeHTTPResponse({"message": {"content": "local reply"}})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    conversation = Conversation()
    conversation.add_user_message("hello")
    client = OllamaChatClient(
        RuntimeConfig(
            api_key=None,
            provider="ollama",
            ollama_base_url="http://localhost:11434",
            ollama_model="smollm2:135m",
            timeout_seconds=30,
        )
    )

    result = client.send(conversation)

    assert result == "local reply"
    assert calls == [
        {
            "url": "http://localhost:11434/api/chat",
            "timeout": 30,
            "payload": {
                "model": "smollm2:135m",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful desktop chat assistant. Answer clearly, "
                            "briefly, and do not repeat symbols or words."
                        ),
                    },
                    {"role": "user", "content": "hello"},
                ],
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "repeat_penalty": 1.2,
                },
            },
        }
    ]


def test_ollama_send_rejects_empty_response(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(_request: object, timeout: int) -> FakeHTTPResponse:
        assert timeout == 60
        return FakeHTTPResponse({"message": {"content": ""}})

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = OllamaChatClient(RuntimeConfig(api_key=None, provider="ollama"))

    with pytest.raises(ChatClientError, match="did not include text"):
        client.send(Conversation())
