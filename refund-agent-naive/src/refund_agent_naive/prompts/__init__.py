from importlib.resources import files


def load_prompt(name: str) -> str:
    """Load a versioned prompt, e.g. load_prompt('refund_agent.v1')."""
    return files("refund_agent_naive.prompts").joinpath(f"{name}.md").read_text(encoding="utf-8")
