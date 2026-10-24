from refund_agent.llm import ask_llm

message = "My order #4821 arrived damaged. Can I get a refund?"

response = ask_llm(message)

print("Customer:", message)
print("\nAI response:", response)
