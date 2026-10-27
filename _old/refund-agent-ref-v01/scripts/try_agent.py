from refund_agent_ref.llm import get_llm
from refund_agent_ref.agent import RefundAgent

model = get_llm()

message = "My order #4824 is unused. Can I get a refund?"
thread_id = "demo"

agent = RefundAgent()
result = agent.ask(message, thread_id=thread_id)

print("Customer:", message)
print("\nAI response:", result.message)
