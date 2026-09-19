from pathlib import Path

import yaml
from pydantic import BaseModel, Field


CONFIG_PATH = Path("config/llm.yaml")


class LLMConfig(BaseModel):
    provider: str
    base_url: str
    model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(gt=0)


def load_llm_config() -> LLMConfig:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_PATH}"
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not data:
        raise ValueError("LLM configuration is empty.")

    return LLMConfig.model_validate(data)