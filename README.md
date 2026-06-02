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

Option 1: create a local `.env` file from the example and replace the placeholder
with your real key.

```powershell
Copy-Item .env.example .env
notepad .env
```

Option 2: set environment variables for the current PowerShell session.

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
$env:OPENAI_MODEL = "gpt-5.5"
```

`OPENAI_MODEL` and `OPENAI_TIMEOUT_SECONDS` are optional. Do not commit API keys
or `.env` files.

### Local Open-Source Model

You can run the app without an OpenAI API key by using Ollama with a small local
model.

1. Install Ollama from https://ollama.com/download
2. Pull a tiny model:

```powershell
ollama pull smollm2:135m
```

Another small option:

```powershell
ollama pull qwen2.5:0.5b-instruct
```

3. Configure `.env`:

```text
CHAT_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=smollm2:135m
```

When `CHAT_PROVIDER=ollama`, `OPENAI_API_KEY` is not required.

### Run

```powershell
py -3.14 -m tjcmfrnc_chat
```

### Test

```powershell
py -3.14 -m pytest
```

Automated tests use mocked assistant responses and do not require an API key.
