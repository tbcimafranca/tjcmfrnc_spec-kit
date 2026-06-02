"""PyQt6 user interface for the desktop chat app."""

from __future__ import annotations

from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .config import RuntimeConfig
from .conversation import Conversation
from .openai_client import ChatClientError, OpenAIChatClient


class ChatWorker(QObject):
    finished = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, client: OpenAIChatClient, conversation: Conversation) -> None:
        super().__init__()
        self._client = client
        self._conversation = conversation

    def run(self) -> None:
        try:
            self.finished.emit(self._client.send(self._conversation))
        except ChatClientError as exc:
            self.failed.emit(str(exc))
        except Exception:
            self.failed.emit("Unexpected assistant error.")


class MainWindow(QMainWindow):
    def __init__(
        self,
        config: RuntimeConfig | None = None,
        client: OpenAIChatClient | None = None,
    ) -> None:
        super().__init__()
        self.config = config or RuntimeConfig.from_env()
        self.conversation = Conversation()
        self.client = client or OpenAIChatClient(self.config)
        self._thread: QThread | None = None
        self._worker: ChatWorker | None = None

        self.setWindowTitle("tjcmfrnc GPT Chat")
        self.resize(860, 640)
        self._build_layout()
        self._set_idle_status()

    def _build_layout(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.history = QTextEdit()
        self.history.setReadOnly(True)
        layout.addWidget(self.history, stretch=1)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Message GPT-5.5...")
        self.input_box.setFixedHeight(96)
        layout.addWidget(self.input_box)

        actions = QHBoxLayout()
        self.send_button = QPushButton("Send")
        self.clear_button = QPushButton("Clear")
        self.send_button.clicked.connect(self.send_message)
        self.clear_button.clicked.connect(self.clear_chat)
        actions.addWidget(self.clear_button)
        actions.addStretch(1)
        actions.addWidget(self.send_button)
        layout.addLayout(actions)

        self.setCentralWidget(root)

    def send_message(self) -> None:
        text = self.input_box.toPlainText().strip()
        if not text:
            self._show_error("Enter a message before sending.")
            return
        if self._thread is not None:
            self._show_error("Wait for the current response to finish.")
            return

        self.conversation.add_user_message(text)
        self._append_message("You", text)
        self.input_box.clear()
        self._set_busy(True)

        self._thread = QThread()
        self._worker = ChatWorker(self.client, self.conversation)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._handle_success)
        self._worker.failed.connect(self._handle_failure)
        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup_worker)
        self._thread.start()

    def clear_chat(self) -> None:
        if self._thread is not None:
            self._show_error("Wait for the current response to finish before clearing.")
            return
        self.conversation.clear()
        self.history.clear()
        self._set_idle_status()

    def _handle_success(self, text: str) -> None:
        self.conversation.add_assistant_message(text)
        self._append_message("Assistant", text)
        self._set_busy(False)

    def _handle_failure(self, message: str) -> None:
        self._append_message("Error", message)
        self._show_error(message)
        self._set_busy(False)

    def _cleanup_worker(self) -> None:
        if self._worker is not None:
            self._worker.deleteLater()
        if self._thread is not None:
            self._thread.deleteLater()
        self._worker = None
        self._thread = None

    def _append_message(self, speaker: str, text: str) -> None:
        self.history.append(f"<b>{speaker}:</b>")
        self.history.append(_escape_html(text))
        self.history.append("")

    def _set_busy(self, busy: bool) -> None:
        self.send_button.setEnabled(not busy)
        self.clear_button.setEnabled(not busy)
        self.input_box.setEnabled(not busy)
        if busy:
            self.status_label.setText(f"Assistant is responding with {self.config.model}...")
        else:
            self._set_idle_status()

    def _set_idle_status(self) -> None:
        if self.config.api_key_present:
            self.status_label.setText(f"Ready. Model: {self.config.model}")
        else:
            self.status_label.setText("OPENAI_API_KEY is not configured. Live responses will fail.")

    def _show_error(self, message: str) -> None:
        QMessageBox.warning(self, "Chat Error", message)


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br>")
    )


def run_app(config: RuntimeConfig | None = None) -> int:
    app = QApplication.instance() or QApplication([])
    window = MainWindow(config=config)
    window.show()
    return app.exec()
