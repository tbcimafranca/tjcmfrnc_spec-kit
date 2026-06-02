from tjcmfrnc_chat.config import DEFAULT_MODEL, DEFAULT_TIMEOUT_SECONDS, RuntimeConfig


def test_config_defaults_without_env() -> None:
    config = RuntimeConfig.from_env({})

    assert config.api_key is None
    assert config.api_key_present is False
    assert config.model == DEFAULT_MODEL
    assert config.timeout_seconds == DEFAULT_TIMEOUT_SECONDS


def test_config_reads_env_values() -> None:
    config = RuntimeConfig.from_env(
        {
            "OPENAI_API_KEY": " sk-test ",
            "OPENAI_MODEL": "gpt-5.5-2026-04-23",
            "OPENAI_TIMEOUT_SECONDS": "90",
        }
    )

    assert config.api_key == "sk-test"
    assert config.api_key_present is True
    assert config.model == "gpt-5.5-2026-04-23"
    assert config.timeout_seconds == 90


def test_config_uses_default_timeout_for_invalid_value() -> None:
    assert RuntimeConfig.from_env({"OPENAI_TIMEOUT_SECONDS": "bad"}).timeout_seconds == DEFAULT_TIMEOUT_SECONDS
    assert RuntimeConfig.from_env({"OPENAI_TIMEOUT_SECONDS": "0"}).timeout_seconds == DEFAULT_TIMEOUT_SECONDS
