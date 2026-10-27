import sys
from pathlib import Path

# Add project root to sys.path to allow importing from src
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from src.agent import agent

inputs = {"messages": [{"role": "user", "content": "Say hello from try_llm"}]}
result = agent.invoke(inputs)

print("Agent response:")
# Assuming result["messages"] contains the conversation history
if "messages" in result:
    print(result["messages"][-1].content)
else:
    print(result)
