from refund_agent_simple.llm import get_llm
from refund_agent_simple.prompts import refund_prompt

message = "My order #4821 arrived damaged. Can I get a refund?"

response = (refund_prompt | get_llm()).invoke({"message": message})

print("Customer:", message)
print("\nAI response:", response.content)
