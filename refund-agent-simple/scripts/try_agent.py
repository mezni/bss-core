from refund_agent_simple.agent import RefundAgent

message = "My order #4821 arrived damaged. Can I get a refund?"

agent = RefundAgent()
response = agent.ask(message)

print("Customer:", message)
print("\nAI response:", response)
