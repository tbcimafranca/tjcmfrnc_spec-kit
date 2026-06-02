# Quickstart: GPT-like Desktop Chat

## 1. Create a virtual environment

```powershell
py -3.14 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

## 2. Install dependencies

```powershell
py -3.14 -m pip install -e ".[dev]"
```

## 3. Configure the API key

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

Optional model override:

```powershell
$env:OPENAI_MODEL = "gpt-5.5"
```

## 4. Run the app

```powershell
py -3.14 -m tjcmfrnc_chat
```

## 5. Run automated checks

```powershell
py -3.14 -m pytest
```

Automated tests use mocked model responses and do not require an API key.

## 6. Manual smoke check

1. Launch the app with `OPENAI_API_KEY` set.
2. Type `Say hello in one sentence.`
3. Send the message.
4. Confirm the user message appears immediately.
5. Confirm the assistant response appears below it.
6. Click Clear and confirm the conversation is empty.
