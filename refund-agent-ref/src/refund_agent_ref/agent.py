from dataclasses import dataclass
from typing import Any, Literal


from langchain.agents import create_agent
from langchain.messages import HumanMessage

# from refund_agent_ref.llm import get_llm
from refund_agent_ref.tools import lookup_order
from refund_agent_ref.prompts import refund_system_prompt
# from refund_agent_ref.models import Refund

# model = get_model()

ApprovalDecision = Literal["approve", "reject"]


@dataclass
class AgentResult:
    status: Literal["completed", "pending_approval"]
    message: str
    interrupt: Any | None = None


class RefundAgent:
    def __init__(
        self,
        llm: str | None = None,
        tools: list | None = None,
        checkpointer: Any | None = None,
    ) -> None:
        self._agent = create_agent(
            model=llm,
            system_prompt=refund_system_prompt,
            tools=[lookup_order],
            response_format=AgentResult,
        )
