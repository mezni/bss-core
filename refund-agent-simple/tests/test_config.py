import pytest

from refund_agent_simple.config import Settings


def test_defaults(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    settings = Settings(_env_file=None)

    assert settings.openai_model == "gpt-6-luna"
    assert settings.openai_api_key is None


def test_model_from_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    settings = Settings()

    assert settings.openai_model == "test-model"


def test_api_key_is_secret(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    settings = Settings()

    assert settings.openai_api_key is not None
    assert settings.openai_api_key.get_secret_value() == "test-key"
    assert "test-key" not in str(settings.openai_api_key)


def test_empty_model_is_rejected(monkeypatch):
    from pydantic import ValidationError

    monkeypatch.setenv("OPENAI_MODEL", "")

    with pytest.raises(ValidationError):
        Settings()
