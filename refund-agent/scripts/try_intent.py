from refund_agent.llm import extract_intent

message = "My order #4821 arrived damaged. Can I get a refund?"

result = extract_intent(message)

print("Intent:", result.intent.value)
print("Order ID:", result.order_id)
print("Reason:", result.reason.value)
print("Summary:", result.summary)
