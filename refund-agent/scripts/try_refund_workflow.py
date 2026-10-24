from datetime import date

from refund_agent.workflow import process_refund

message = "I received a damaged item. Please refund order 4821."

decision = process_refund(
    message,
    today=date(2026, 10, 24),
)

print("Customer:", message)
print("\nRefund decision:")
print(decision.model_dump_json(indent=2))