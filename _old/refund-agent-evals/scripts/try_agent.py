import sys
from pathlib import Path

# Add project root to sys.path to allow importing from src
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from src.agent import agent

inputs = {
    "messages": [
        {
            "role": "user",
            "content": "Hi, I bought headphones under order ORD-101 and they arrived damaged. I'd like a refund.",
        }
    ]
}
result = agent.invoke(inputs)

print("Agent response:")
# Assuming result["messages"] contains the conversation history
if "messages" in result:
    print(result["messages"][-1].content)
else:
    print(result)
