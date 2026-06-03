from __future__ import annotations

import time

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtWidgets import QApplication, QMessageBox

from tjcmfrnc_chat.config import RuntimeConfig
from tjcmfrnc_chat.conversation import Conversation
from tjcmfrnc_chat.ui import MainWindow


class FakeClient:
    def __init__(
        self,
        reply: str = "assistant reply",
        exc: Exception | None = None,
        delay_seconds: float = 0,
    ) -> None:
        self.reply = reply
        self.exc = exc
        self.delay_seconds = delay_seconds
        self.inputs: list[list[dict[str, str]]] = []

    def send(self, conversation: Conversation) -> str:
        self.inputs.append(conversation.to_openai_input())
        if self.delay_seconds:
            time.sleep(self.delay_seconds)
        if self.exc:
            raise self.exc
        return self.reply


@pytest.fixture
def app() -> QApplication:
    return QApplication.instance() or QApplication([])


@pytest.fixture(autouse=True)
def no_modal_warnings(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    messages: list[str] = []

    def fake_warning(_parent: object, _title: str, message: str) -> None:
        messages.append(message)

    monkeypatch.setattr(QMessageBox, "warning", fake_warning)
    return messages


def wait_for_worker(app: QApplication, window: MainWindow) -> None:
    deadline = time.time() + 2
    while window._thread is not None and time.time() < deadline:  # noqa: SLF001
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()


def test_send_message_appends_user_and_assistant(app: QApplication) -> None:
    client = FakeClient(reply="hello back")
    window = MainWindow(RuntimeConfig(api_key="sk-test", model="gpt-5.5"), client=client)  # type: ignore[arg-type]

    window.input_box.setPlainText("hello")
    window.send_message()
    wait_for_worker(app, window)

    assert "You:" in window.history.toPlainText()
    assert "hello" in window.history.toPlainText()
    assert "Assistant:" in window.history.toPlainText()
    assert "hello back" in window.history.toPlainText()
    assert client.inputs[0] == [{"role": "user", "content": "hello"}]


def test_thinking_indicator_is_visible_while_waiting(app: QApplication) -> None:
    client = FakeClient(reply="done", delay_seconds=0.05)
    window = MainWindow(RuntimeConfig(api_key="sk-test", model="gpt-5.5"), client=client)  # type: ignore[arg-type]

    window.input_box.setPlainText("think")
    window.send_message()

    assert not window.thinking_label.isHidden()
    assert "Thinking" in window.thinking_label.text()
    first_frame = window.thinking_label.text()
    window._advance_thinking_indicator()  # noqa: SLF001
    assert window.thinking_label.text() != first_frame

    wait_for_worker(app, window)

    assert window.thinking_label.isHidden()


def test_clear_chat_resets_history_and_context(app: QApplication) -> None:
    window = MainWindow(RuntimeConfig(api_key="sk-test"), client=FakeClient())  # type: ignore[arg-type]
    window.conversation.add_user_message("hello")
    window.history.append("hello")

    window.clear_chat()

    assert window.conversation.messages == ()
    assert window.history.toPlainText() == ""


def test_empty_message_shows_error(app: QApplication, no_modal_warnings: list[str]) -> None:
    window = MainWindow(RuntimeConfig(api_key="sk-test"), client=FakeClient())  # type: ignore[arg-type]

    window.input_box.setPlainText(" ")
    window.send_message()

    assert no_modal_warnings == ["Enter a message before sending."]


def test_failed_request_recovers_input(app: QApplication, no_modal_warnings: list[str]) -> None:
    client = FakeClient(exc=RuntimeError("boom"))
    window = MainWindow(RuntimeConfig(api_key="sk-test"), client=client)  # type: ignore[arg-type]

    window.input_box.setPlainText("hello")
    window.send_message()
    wait_for_worker(app, window)

    assert window.send_button.isEnabled()
    assert "Unexpected assistant error." in window.history.toPlainText()
    assert no_modal_warnings == ["Unexpected assistant error."]
