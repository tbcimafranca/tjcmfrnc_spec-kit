# tjcmfrnc_spec-kit

This repo contains a GitHub Spec Kit workspace configured for Codex-assisted,
spec-driven development.

## Workflow

Use the installed Spec Kit skills in order:

1. `$speckit-constitution`
2. `$speckit-specify`
3. `$speckit-plan`
4. `$speckit-tasks`
5. `$speckit-implement`

The current constitution lives in `.specify/memory/constitution.md`.

## Tooling

- Python 3.14
- PowerShell Spec Kit scripts
- Codex integration under `.agents/skills/`

## GPT-like Desktop Chat

The current feature builds a local PyQt desktop chat app backed by OpenAI's
Responses API. The default model is `gpt-5.5`.

### Install

```powershell
py -3.14 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
py -3.14 -m pip install -e ".[dev]"
```

### Configure

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
$env:OPENAI_MODEL = "gpt-5.5"
```

`OPENAI_MODEL` is optional. Do not commit API keys or `.env` files.

### Run

```powershell
py -3.14 -m tjcmfrnc_chat
```

### Test

```powershell
py -3.14 -m pytest
```

Automated tests use mocked assistant responses and do not require an API key.
