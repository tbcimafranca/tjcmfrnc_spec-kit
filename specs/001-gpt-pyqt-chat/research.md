# Research: GPT-like Desktop Chat

## Decision: Use OpenAI Responses API

**Rationale**: OpenAI documentation describes the Responses API as the
recommended API for new projects, supporting stateful interactions and text
generation through the official SDK. This aligns with a new desktop chat app.

**Alternatives considered**:
- Chat Completions API: still supported, but Responses is recommended for new
  builds.
- Direct HTTP calls: increases boilerplate and error handling compared with the
  official SDK.

## Decision: Default to `gpt-5.5`

**Rationale**: Official OpenAI model docs list `gpt-5.5` as the newest frontier
model and show Responses API support. The user explicitly requested model 5.5,
so the app will default to model ID `gpt-5.5`.

**Alternatives considered**:
- `gpt-5.4-mini`: lower cost and latency, but not the requested model.
- `gpt-5`: older model family member, not the requested model.

## Decision: Use PyQt6 for the desktop interface

**Rationale**: The user requested a PyQt interface. PyQt6 is the current Qt 6
binding and supports a native desktop UI with worker threads to keep the
interface responsive during API calls.

**Alternatives considered**:
- PySide6: similar Qt 6 binding, but user specifically requested PyQt.
- Tkinter: built in, but less suitable for a polished GPT-like desktop
  experience.

## Decision: Keep conversation history in memory for v1

**Rationale**: The first version needs reliable local chat behavior without
extra storage complexity. Memory-only state satisfies the spec and avoids
handling local data persistence and deletion policies.

**Alternatives considered**:
- SQLite persistence: useful later, but outside the requested first version.
- Plain text logs: easier but raises accidental secret or prompt-data leakage
  concerns.

## Decision: Mock API calls in automated tests

**Rationale**: The constitution requires verification without relying on hidden
machine state. Mocking avoids network access, paid token usage, and API key
requirements in CI or local tests.

**Alternatives considered**:
- Live API tests: useful as a manual smoke check, but unsuitable as default
  automated verification.
