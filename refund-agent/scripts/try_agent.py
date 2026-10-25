from refund_agent.agent import handle_customer_message
from refund_agent.observability import configure_observability


def main() -> None:
    configure_observability()
    _, response = handle_customer_message(
        "The item arrived damaged. Please refund order 4821."
    )
    print(response)


if __name__ == "__main__":
    main()
