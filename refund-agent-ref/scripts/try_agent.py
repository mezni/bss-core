from refund_agent_ref.llm import get_llm
from refund_agent_ref.agent import RefundAgent

model = get_llm()
agent = RefundAgent(llm=model)
