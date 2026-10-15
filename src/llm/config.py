import os

from dotenv import load_dotenv

load_dotenv()


def get_required_setting(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required setting: {name}")

    return value


def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-5.5")
