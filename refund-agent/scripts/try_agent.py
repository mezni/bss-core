from refund_agent.logging_config import configure_logging
from refund_agent.agent import handle_customer_message

configure_logging()

message = input("Customer message: ")

decision, response = handle_customer_message(message)

print("\n--- Refund Decision ---")
print(decision.model_dump_json(indent=2))

print("\n--- Customer Response ---")
print(response)
