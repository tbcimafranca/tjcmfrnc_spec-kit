# Implementation Plan: GPT-like Desktop Chat

**Branch**: `001-gpt-pyqt-chat` | **Date**: 2026-06-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-gpt-pyqt-chat/spec.md`

## Summary

Build a local desktop chat application that provides a GPT-like conversation
experience. The app will use Python 3.14, PyQt6 for the desktop interface, and
OpenAI's Responses API with `gpt-5.5` as the default model. It will keep
conversation state in memory, read secrets from environment variables, and
include tests that verify behavior without making paid external API calls.

## Technical Context

**Language/Version**: Python 3.14

**Primary Dependencies**: PyQt6, openai Python SDK, python-dotenv, pytest

**Storage**: In-memory conversation only for v1; no persistent chat database

**Testing**: `py -3.14 -m pytest`; mocked OpenAI client for automated tests

**Target Platform**: Windows desktop first, with code kept portable for other
desktop platforms supported by PyQt6

**Project Type**: Desktop application

**Performance Goals**: UI remains responsive while a response is in progress;
mocked response path updates the UI in under 2 seconds

**Constraints**: Secrets must come from runtime environment; automated tests
must not require network access or a real OpenAI API key; default model is
`gpt-5.5` and can be overridden by `OPENAI_MODEL`

**Scale/Scope**: Single-user local desktop chat with text-only input/output,
memory-only chat history, no file upload, no voice, no account system

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Specification First**: PASS. [spec.md](spec.md) defines prioritized user
  scenarios, acceptance criteria, measurable outcomes, assumptions, and
  verification requirements.
- **Reproducible Python Tooling**: PASS. The plan uses Python 3.14 and documents
  dependencies and commands in `pyproject.toml` and [quickstart.md](quickstart.md).
- **Testable Changes**: PASS. Unit tests cover configuration, conversation
  state, mocked response handling, and request failures. Manual smoke checks are
  documented in [quickstart.md](quickstart.md).
- **Agent Context Hygiene**: PASS. Secrets remain in `OPENAI_API_KEY`; virtual
  environments and caches remain ignored; AGENTS.md points to this plan.
- **Git Traceability**: PASS. Feature work is isolated on
  `001-gpt-pyqt-chat` and can be merged to `main` after verification.

## Project Structure

### Documentation (this feature)

```text
specs/001-gpt-pyqt-chat/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- desktop-chat.md
|-- checklists/
|   `-- requirements.md
`-- tasks.md
```

### Source Code (repository root)

```text
src/
`-- tjcmfrnc_chat/
    |-- __init__.py
    |-- __main__.py
    |-- app.py
    |-- config.py
    |-- conversation.py
    |-- openai_client.py
    `-- ui.py

tests/
|-- conftest.py
|-- test_config.py
|-- test_conversation.py
|-- test_openai_client.py
`-- test_ui_logic.py
```

**Structure Decision**: Use a single Python package under `src/` to keep the
desktop app small, testable, and easy to run. UI code is separated from
configuration, conversation state, and OpenAI API integration so automated tests
can mock the external service.

## Complexity Tracking

No constitution violations are required.
