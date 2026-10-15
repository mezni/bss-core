import os

from openai import OpenAI
from llm.schemas import CRMContractResponse


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


def ask_crm_question(
    question: str,
    context: str,
) -> CRMContractResponse:
    """Return a structured answer grounded in supplied context."""
    client = OpenAI(
        timeout=30.0,
        max_retries=2,
    )

    model = os.getenv("OPENAI_MODEL", "gpt-5.5")

    response = client.responses.parse(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "Answer using only the supplied CRM context. "
                    "Never invent contract terms or add-ons. "
                    "If information is missing, leave the relevant "
                    "lists empty and identify the missing information. "
                    "Set found_in_context to true only when the "
                    "context contains relevant contract information."
                ),
            },
            {
                "role": "user",
                "content": (f"Question: {question}\n\nCRM context:\n{context}"),
            },
        ],
        text_format=CRMContractResponse,
    )

    if response.output_parsed is None:
        raise ValueError("The model returned no parsed CRM response.")

    return response.output_parsed
