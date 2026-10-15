from llm.client import ask_crm_question


def main() -> None:
    context = """
    Contract ID: C-100
    Renewal term: 12 months
    Active add-on: Premium Support
    """

    result = ask_crm_question(
        question="What are the contract terms and active add-ons?",
        context=context,
    )

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
