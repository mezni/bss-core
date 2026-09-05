"""Typed application configuration driven by environment variables.

Defines the configuration surface from `contracts/environment-config.md`
(FR-004/FR-005): every value has a documented local default and can be
overridden through an environment variable without code changes.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime settings for the application."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://telco:telco@db:5432/telco"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    db_retry_window: int = 30


@lru_cache
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance (env vars read once)."""
    return Settings()
