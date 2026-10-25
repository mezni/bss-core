
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    environment: Literal["development", "test", "production"] = Field(
        default="development",
        alias="REFUND_AGENT_ENVIRONMENT",
    )

    openai_api_key: SecretStr | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    refund_agent_api_key: SecretStr | None = Field(
        default=None,
        alias="REFUND_AGENT_API_KEY",
    )

    llm_model: str = Field(
        default="gpt-4o-mini",
        alias="REFUND_AGENT_LLM_MODEL",
        min_length=1,
    )

    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.environment == "production":
            if not self.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY is required in production."
                )

            if not self.refund_agent_api_key:
                raise ValueError(
                    "REFUND_AGENT_API_KEY is required in production."
                )

        return self


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()



customer_service_api_key: SecretStr | None = Field(
    default=None,
    alias="REFUND_AGENT_CUSTOMER_API_KEY",
)

refund_reviewer_api_key: SecretStr | None = Field(
    default=None,
    alias="REFUND_AGENT_REVIEWER_API_KEY",
)

admin_api_key: SecretStr | None = Field(
    default=None,
    alias="REFUND_AGENT_ADMIN_API_KEY",
)
