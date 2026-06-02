"""Application entry point."""

from __future__ import annotations

from dotenv import load_dotenv

from .config import RuntimeConfig
from .ui import run_app


def main() -> int:
    load_dotenv()
    return run_app(RuntimeConfig.from_env())


if __name__ == "__main__":
    raise SystemExit(main())
