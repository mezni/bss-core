
import pytest
from pydantic import ValidationError

from refund_agent.config import Settings


def test_development_settings_can_omit_secrets():
    settings = Settings(
        REFUND_AGENT_ENVIRONMENT="development",
        OPENAI_API_KEY="",
        REFUND_AGENT_API_KEY="",
    )

    assert settings.environment == "development"


def test_production_requires_openai_key():
    with pytest.raises(ValidationError):
        Settings(
            REFUND_AGENT_ENVIRONMENT="production",
            REFUND_AGENT_API_KEY="test-api-key",
        )


def test_production_requires_api_key():
    with pytest.raises(ValidationError):
        Settings(
            REFUND_AGENT_ENVIRONMENT="production",
            OPENAI_API_KEY="test-openai-key",
        )


def test_secret_is_masked_in_representation():
    secret = "test-secret-value"
    settings = Settings(
        REFUND_AGENT_ENVIRONMENT="development",
        REFUND_AGENT_API_KEY=secret,
    )

    assert secret not in str(settings.refund_agent_api_key)
    assert settings.refund_agent_api_key.get_secret_value() == secret
