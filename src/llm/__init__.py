from llm.client import ask_llm


def main() -> None:
    prompt = (
        "Explain what contract terms and active add-ons mean "
        "in a CRM system. Use three bullet points."
    )

    answer = ask_llm(prompt)

    print("\nLLM response:")
    print(answer)
