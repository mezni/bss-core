from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from refund_agent_simple.llm import get_llm
from refund_agent_simple.prompts import REFUND_SYSTEM_PROMPT


class RefundAgent:
    def __init__(
        self,
        llm: BaseChatModel | None = None,
        tools: list | None = None,
    ) -> None:
        self._agent = create_agent(
            model=llm or get_llm(),
            tools=tools or [],
            system_prompt=REFUND_SYSTEM_PROMPT,
        )

    def ask(self, message: str) -> str:
        result = self._agent.invoke({"messages": [HumanMessage(content=message)]})
        return result["messages"][-1].text
