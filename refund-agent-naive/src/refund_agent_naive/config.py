from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="REFUND_", extra="ignore"
    )

    anthropic_api_key: SecretStr
    model_name: str = "gpt-6-luna"
    llm_timeout_s: float = 20.0
    llm_max_retries: int = 2
