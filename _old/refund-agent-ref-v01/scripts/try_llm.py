from refund_agent_ref.llm import get_llm

model = get_llm()

message = "My order #4821 arrived damaged. Can I get a refund?"
response = model.invoke(message)
print(response)
