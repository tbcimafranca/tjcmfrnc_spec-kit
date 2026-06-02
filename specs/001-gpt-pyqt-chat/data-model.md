# Data Model: GPT-like Desktop Chat

## ChatMessage

Represents one message in the conversation.

**Fields**:
- `role`: one of `user`, `assistant`, or `system`
- `content`: non-empty message text
- `created_at`: UTC timestamp for display and ordering

**Validation**:
- `content` must contain non-whitespace text.
- `role` must be one of the supported role values.

## Conversation

Represents the ordered in-memory chat history.

**Fields**:
- `messages`: ordered list of `ChatMessage`

**Operations**:
- Add user message.
- Add assistant message.
- Clear all messages.
- Convert messages to OpenAI Responses API input format.

**Validation**:
- Messages are appended in chronological order.
- Clearing the conversation removes all stored context.

## RuntimeConfig

Represents runtime settings needed by the app.

**Fields**:
- `api_key_present`: whether `OPENAI_API_KEY` is available
- `model`: model identifier, default `gpt-5.5`
- `timeout_seconds`: request timeout, default 60

**Validation**:
- API key must be present before a live request is attempted.
- Model must be non-empty.
- Timeout must be a positive integer.

## AssistantRequest

Represents the lifecycle of a submitted user prompt.

**Fields**:
- `status`: `idle`, `running`, `succeeded`, or `failed`
- `error_message`: visible non-secret error text when failed

**State Transitions**:
- `idle` -> `running` when a prompt is submitted.
- `running` -> `succeeded` when a response is received.
- `running` -> `failed` when configuration or request handling fails.
- Any terminal state -> `idle` after the UI is ready for the next prompt.
