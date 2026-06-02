# Contract: Desktop Chat UI

## Launch Contract

Command:

```powershell
py -3.14 -m tjcmfrnc_chat
```

Expected behavior:
- Opens a desktop chat window.
- Shows a message input area, send action, clear action, status text, and
  conversation history area.
- Does not require an API call until the user sends a message.

## Runtime Configuration Contract

Environment variables:

- `OPENAI_API_KEY`: required for live assistant responses.
- `OPENAI_MODEL`: optional model override. Defaults to `gpt-5.5`.
- `OPENAI_TIMEOUT_SECONDS`: optional positive integer timeout. Defaults to `60`.

Expected behavior:
- Missing `OPENAI_API_KEY` prevents live requests and shows a non-secret error.
- Missing `OPENAI_MODEL` uses `gpt-5.5`.
- Invalid timeout falls back to the default timeout.

## Send Message Contract

Input:
- Non-empty user message text.

Expected behavior:
- App appends the user message to the conversation.
- App disables duplicate sends while a response is running.
- App sends the full in-memory conversation context to the model client.
- App appends the assistant response below the user message.
- App re-enables input after success or failure.

## Clear Conversation Contract

Input:
- User activates clear action.

Expected behavior:
- Visible conversation history is cleared.
- In-memory context is cleared.
- Any configured secrets remain untouched and undisplayed.
