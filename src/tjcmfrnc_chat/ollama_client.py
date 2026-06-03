"""Local Ollama chat adapter."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from .config import RuntimeConfig
from .conversation import Conversation
from .openai_client import ChatClientError
from .prompts import ASSISTANT_SYSTEM_PROMPT


@dataclass
class OllamaChatClient:
    config: RuntimeConfig

    def send(self, conversation: Conversation) -> str:
        payload = {
            "model": self.config.ollama_model,
            "messages": [
                {
                    "role": "system",
                    "content": ASSISTANT_SYSTEM_PROMPT,
                },
                *conversation.to_openai_input(),
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,
                "repeat_penalty": 1.2,
            },
        }
        request = urllib.request.Request(
            f"{self.config.ollama_base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise ChatClientError(_format_ollama_error(detail)) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ChatClientError(
                "Ollama is not reachable. Start Ollama and pull the configured model."
            ) from exc
        except json.JSONDecodeError as exc:
            raise ChatClientError("Ollama returned an invalid response.") from exc

        message = data.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()

        raise ChatClientError("Ollama response did not include text output.")


def _format_ollama_error(detail: str) -> str:
    try:
        parsed = json.loads(detail)
    except json.JSONDecodeError:
        parsed = {}
    error = parsed.get("error") if isinstance(parsed, dict) else None
    if isinstance(error, str) and error.strip():
        return f"Ollama request failed: {error.strip()}"
    return "Ollama request failed. Check that the model is installed."
