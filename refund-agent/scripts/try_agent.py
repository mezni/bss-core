from refund_agent.agent import handle_customer_message

message = input("Customer message: ")

try:
    decision, response = handle_customer_message(message)

    print("\n--- Refund Decision ---")
    print(decision.model_dump_json(indent=2))

    print("\n--- Customer Response ---")
    print(response)

except Exception:
    print(
        "\nUnable to process this request right now. "
        "Please try again or contact support."
    )