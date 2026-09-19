from pathlib import Path

import yaml


CONFIG_PATH = Path("config/llm.yaml")


def load_llm_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_PATH}"
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError("LLM configuration is empty.")

    return config