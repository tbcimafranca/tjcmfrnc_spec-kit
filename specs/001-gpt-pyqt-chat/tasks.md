# Tasks: GPT-like Desktop Chat

**Input**: Design documents from `/specs/001-gpt-pyqt-chat/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/desktop-chat.md, quickstart.md

**Tests**: Include automated tests for executable behavior. Tests use mocked model responses and do not require an OpenAI API key.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and package structure

- [x] T001 Create Python package structure in src/tjcmfrnc_chat/
- [x] T002 Create pyproject.toml with runtime and dev dependencies
- [x] T003 [P] Create tests package scaffolding in tests/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core modules required before user story implementation

- [x] T004 Implement RuntimeConfig loading in src/tjcmfrnc_chat/config.py
- [x] T005 Implement ChatMessage and Conversation in src/tjcmfrnc_chat/conversation.py
- [x] T006 Implement OpenAI Responses API adapter in src/tjcmfrnc_chat/openai_client.py
- [x] T007 [P] Add config tests in tests/test_config.py
- [x] T008 [P] Add conversation tests in tests/test_conversation.py
- [x] T009 [P] Add OpenAI adapter tests with mocked client in tests/test_openai_client.py

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Send and Receive Chat Messages (Priority: P1) MVP

**Goal**: User can enter a prompt and receive an assistant response in the desktop chat view.

**Independent Test**: Launch the app with a mocked model client, send a prompt, and confirm ordered user/assistant messages.

### Tests and Verification for User Story 1

- [x] T010 [P] [US1] Add UI send-message smoke tests in tests/test_ui_logic.py

### Implementation for User Story 1

- [x] T011 [US1] Implement ChatWorker request thread in src/tjcmfrnc_chat/ui.py
- [x] T012 [US1] Implement MainWindow layout and send behavior in src/tjcmfrnc_chat/ui.py
- [x] T013 [US1] Implement application entry point in src/tjcmfrnc_chat/app.py
- [x] T014 [US1] Implement module entry point in src/tjcmfrnc_chat/__main__.py

**Checkpoint**: User Story 1 is functional and testable independently.

---

## Phase 4: User Story 2 - Manage Conversation Context (Priority: P2)

**Goal**: User can continue multi-turn conversations and clear chat context.

**Independent Test**: Send two related prompts with a mocked client, verify context is retained, then clear the chat.

### Tests and Verification for User Story 2

- [x] T015 [P] [US2] Add context and clear-chat tests in tests/test_ui_logic.py

### Implementation for User Story 2

- [x] T016 [US2] Wire Conversation context into model requests in src/tjcmfrnc_chat/ui.py
- [x] T017 [US2] Implement clear conversation behavior in src/tjcmfrnc_chat/ui.py

**Checkpoint**: User Stories 1 and 2 work independently.

---

## Phase 5: User Story 3 - Configure Runtime Settings Safely (Priority: P3)

**Goal**: User sees safe, actionable errors for missing configuration or request failures.

**Independent Test**: Run mocked missing-key and failed-request flows and confirm input recovers without leaking secrets.

### Tests and Verification for User Story 3

- [x] T018 [P] [US3] Add missing-configuration and failure UI tests in tests/test_ui_logic.py

### Implementation for User Story 3

- [x] T019 [US3] Add safe error display and input recovery in src/tjcmfrnc_chat/ui.py
- [x] T020 [US3] Add startup status text for model/configuration state in src/tjcmfrnc_chat/ui.py

**Checkpoint**: Configuration and failure states are handled safely.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, verification, and repo hygiene

- [x] T021 [P] Update README.md with app run and test commands
- [x] T022 Run py -3.14 -m pytest
- [x] T023 Verify git status excludes secrets, virtual environments, and caches
- [x] T024 Commit completed feature work

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1 and blocks user stories.
- **US1 (Phase 3)**: Depends on Phase 2 and is the MVP.
- **US2 (Phase 4)**: Depends on US1 UI shell and foundation.
- **US3 (Phase 5)**: Depends on US1 UI shell and foundation.
- **Polish (Phase 6)**: Depends on desired user stories.

## Parallel Opportunities

- T003 can run with T001 and T002.
- T007, T008, and T009 can run after T004, T005, and T006 interfaces are defined.
- T010, T015, and T018 target tests and can be expanded independently once UI injection points exist.
- T021 can run in parallel with final verification.

## Implementation Strategy

1. Complete setup and foundational modules.
2. Implement US1 as the MVP.
3. Add conversation clearing/context behavior for US2.
4. Add safe configuration and failure states for US3.
5. Run tests and commit the completed feature.
