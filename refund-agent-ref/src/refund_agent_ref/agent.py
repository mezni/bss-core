from dataclasses import dataclass
from typing import Any, Literal


from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from refund_agent_ref.llm import get_llm
from refund_agent_ref.tools import lookup_order
from refund_agent_ref.prompts import refund_system_prompt

ApprovalDecision = Literal["approve", "reject"]


@dataclass
class AgentResult:
    status: Literal["completed", "pending_approval"]
    message: str
    interrupt: Any | None = None


class RefundAgent:
    def __init__(
        self,
        llm: Any | None = None,
        tools: list | None = None,
        checkpointer: Any | None = None,
    ) -> None:
        if llm is None:
            llm = get_llm()
        self._agent = create_agent(
            model=llm,
            system_prompt=refund_system_prompt,
            tools=tools if tools is not None else [lookup_order],
            response_format=AgentResult,
            checkpointer=checkpointer or InMemorySaver(),
        )

    def ask(self, message: str, thread_id: str = "default") -> AgentResult:
        result = self._agent.invoke(
            {"messages": [HumanMessage(content=message)]},
            self._config(thread_id),
        )
        return self._to_result(result)

    @staticmethod
    def _config(thread_id: str) -> dict[str, Any]:
        return {"configurable": {"thread_id": thread_id}}

    @staticmethod
    def _to_result(result: dict[str, Any]) -> AgentResult:
        if interrupts := result.get("__interrupt__"):
            return AgentResult(
                status="pending_approval",
                message="This refund requires human approval.",
                interrupt=interrupts[0],
            )
        return AgentResult(
            status="completed",
            message=result["messages"][-1].text,
            interrupt=None,
        )
