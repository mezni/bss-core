from decimal import Decimal
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="REFUND_", extra="ignore")

    openai_api_key: SecretStr
    model_name: str = "gpt-4o-mini"
    llm_timeout_s: float = 20.0
    llm_max_retries: int = 2
    max_agent_steps: int = 6

    return_window_days: int = 30
    auto_approve_limit: Decimal = Decimal("50.00")
    non_refundable_categories: frozenset[str] = frozenset({"gift_card"})


@lru_cache
def get_settings() -> Settings:
    return Settings()
