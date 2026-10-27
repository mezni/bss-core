from refund_agent.tool_agent import answer_with_tools

message = "Look up order 4821 and tell me whether it is marked as damaged."

response = answer_with_tools(message)

print("Customer:", message)
print("\nAgent:", response)
