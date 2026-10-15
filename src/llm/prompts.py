from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_system_prompt() -> str:
    prompt_path = PROMPT_DIR / "crm_system.txt"
    return prompt_path.read_text(encoding="utf-8")
