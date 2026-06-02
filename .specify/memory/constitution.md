<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Placeholder principle 1 -> I. Specification First
- Placeholder principle 2 -> II. Reproducible Python Tooling
- Placeholder principle 3 -> III. Testable Changes
- Placeholder principle 4 -> IV. Agent Context Hygiene
- Placeholder principle 5 -> V. Git Traceability
Added sections:
- Tooling and Environment
- Development Workflow
Removed sections:
- Placeholder SECTION_2_NAME
- Placeholder SECTION_3_NAME
Templates requiring updates:
- .specify/templates/plan-template.md: updated
- .specify/templates/spec-template.md: updated
- .specify/templates/tasks-template.md: updated
Follow-up TODOs: none
-->

# tjcmfrnc_spec-kit Constitution

## Core Principles

### I. Specification First
Every non-trivial change MUST begin with a Spec Kit artifact before
implementation work starts. Feature work MUST define user value, acceptance
scenarios, measurable outcomes, assumptions, and any unclear requirements.
Implementation choices belong in plans and tasks, not in the initial user
problem statement.

Rationale: this repository exists to practice and preserve spec-driven LLM
development, so the specification is the source of truth for downstream work.

### II. Reproducible Python Tooling
Automation for this repository MUST run with the documented Python 3.14
toolchain and PowerShell Spec Kit scripts unless a feature plan explicitly
chooses another runtime. Commands that depend on external packages MUST record
how they are installed and invoked.

Rationale: local setup must be repeatable across Codex, VS Code, and terminal
sessions without relying on hidden machine state.

### III. Testable Changes
Executable behavior MUST include a verification path before it is considered
complete. For code changes, plans and tasks MUST identify the relevant test
command, smoke check, or manual acceptance check. Tests SHOULD be written before
implementation when the behavior is complex, user-facing, or likely to regress.

Rationale: each feature should produce evidence that the built behavior matches
the specification rather than only relying on code inspection.

### IV. Agent Context Hygiene
Agent instructions, skills, and generated context MUST be treated as project
artifacts only when they are needed to reproduce the workflow. Credentials,
tokens, local caches, virtual environments, and private session state MUST NOT
be committed. AGENTS.md MUST point agents to the current plan and avoid
duplicating stale implementation details.

Rationale: agent configuration is useful for collaboration, but unmanaged agent
state can leak private data or contradict the latest specification.

### V. Git Traceability
Work MUST be committed in coherent changes that map to Spec Kit artifacts or
implemented tasks. The default integration branch is `main`; temporary branches
MUST be merged back into `main` when accepted. Commit messages SHOULD state the
artifact or feature being changed.

Rationale: traceable history makes it possible to review how a feature moved
from specification to implementation.

## Tooling and Environment

- Primary runtime: Python 3.14.
- Spec Kit invocation: `py -3.14 -m uv tool run --from git+https://github.com/github/spec-kit.git specify ...`.
- Script platform: PowerShell scripts under `.specify/scripts/powershell/`.
- Source branch for accepted work: `main`.
- Local-only artifacts such as `.venv/`, package caches, credentials, and
  private agent state MUST remain ignored or untracked.

## Development Workflow

1. Establish or update the constitution when project rules change.
2. Use `$speckit-specify` to create a feature specification for new product
   behavior or workflow changes.
3. Use `$speckit-plan` to select technology, structure, constraints, and
   verification gates.
4. Use `$speckit-tasks` to generate independently executable work items.
5. Use `$speckit-implement` to execute tasks, verify behavior, and keep commits
   aligned with completed work.
6. Push accepted work to `origin/main`.

## Governance

This constitution supersedes informal repository practices. Changes to the
constitution require a documented amendment in this file, a version update, and
a review of affected templates under `.specify/templates/`.

Versioning follows semantic versioning:
- MAJOR for incompatible governance or principle changes.
- MINOR for new principles, new mandatory sections, or expanded governance.
- PATCH for clarifications that do not change required behavior.

Every feature plan MUST include a Constitution Check that confirms compliance
or documents justified exceptions. Exceptions MUST include a simpler alternative
that was rejected and the reason it was insufficient.

**Version**: 1.0.0 | **Ratified**: 2026-06-02 | **Last Amended**: 2026-06-02
