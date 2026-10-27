from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    openai_api_key: SecretStr | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    openai_model: str = Field(
        default="gpt-6-luna",
        alias="OPENAI_MODEL",
        min_length=1,
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
