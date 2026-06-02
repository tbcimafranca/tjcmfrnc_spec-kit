import pytest

from tjcmfrnc_chat.conversation import ChatMessage, Conversation


def test_chat_message_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        ChatMessage(role="user", content="  ")


def test_chat_message_rejects_unknown_role() -> None:
    with pytest.raises(ValueError, match="Unsupported message role"):
        ChatMessage(role="tool", content="hello")  # type: ignore[arg-type]


def test_conversation_orders_messages_and_exports_openai_input() -> None:
    conversation = Conversation()
    conversation.add_user_message(" hello ")
    conversation.add_assistant_message("Hi")

    assert [message.role for message in conversation.messages] == ["user", "assistant"]
    assert conversation.to_openai_input() == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "Hi"},
    ]


def test_conversation_clear_removes_context() -> None:
    conversation = Conversation()
    conversation.add_user_message("hello")
    conversation.clear()

    assert conversation.messages == ()
    assert conversation.to_openai_input() == []
