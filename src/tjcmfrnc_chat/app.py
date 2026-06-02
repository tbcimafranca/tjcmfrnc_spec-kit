"""Application entry point."""

from __future__ import annotations

from dotenv import load_dotenv

from .chat_client import build_chat_client
from .config import RuntimeConfig
from .ui import run_app


def main() -> int:
    load_dotenv()
    config = RuntimeConfig.from_env()
    return run_app(config, build_chat_client(config))


if __name__ == "__main__":
    raise SystemExit(main())
