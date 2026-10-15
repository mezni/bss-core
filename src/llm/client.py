
import os

from openai import OpenAI


def ask_llm(prompt: str) -> str:
    """Send a prompt to an LLM and return its text response."""
    model = os.getenv("OPENAI_MODEL", "gpt-5.5")

    client = OpenAI(
        timeout=30.0,
        max_retries=2,
    )

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    return response.output_text
