from refund_agent_simple.agent import RefundAgent

message = "My order #4824 is unused. Can I get a refund?"
thread_id = "demo"

agent = RefundAgent()
result = agent.ask(message, thread_id=thread_id)

print("Customer:", message)
print("\nAI response:", result.message)

if result.status == "pending_approval":
    print("\nApproval requested:")
    print(result.interrupt.value)

    result = agent.resume("approve", thread_id=thread_id)
    print("\nAfter approval:", result.message)
