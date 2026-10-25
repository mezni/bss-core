from typing import Any, ClassVar

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import BaseMessage

from refund_agent_simple.agent import RefundAgent


class CapturingChatModel(FakeListChatModel):
    captured: ClassVar[list[list[BaseMessage]]] = []
    bound_tools: ClassVar[list[Any]] = []

    def bind_tools(self, tools: Any, **kwargs: Any) -> "CapturingChatModel":
        self.bound_tools.extend(tools)
        return self

    def _call(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> str:
        self.captured.append(messages)
        return super()._call(messages, stop, run_manager, **kwargs)


@pytest.fixture(autouse=True)
def reset_captures():
    CapturingChatModel.captured.clear()
    CapturingChatModel.bound_tools.clear()
    yield


def test_agent_returns_model_response():
    llm = CapturingChatModel(responses=["Please share your order ID."])
    agent = RefundAgent(llm=llm)

    response = agent.ask("I want a refund.")

    assert response == "Please share your order ID."


def test_agent_passes_customer_message_to_model():
    llm = CapturingChatModel(responses=["ok"])
    agent = RefundAgent(llm=llm)

    agent.ask("Refund order 42")

    messages = llm.captured[0]
    assert messages[-1].content == "Refund order 42"


def test_agent_has_default_tools():
    llm = CapturingChatModel(responses=["ok"])
    agent = RefundAgent(llm=llm)

    agent.ask("Refund order 42")

    names = {tool.name for tool in llm.bound_tools}
    assert names == {"lookup_order", "check_refund_policy", "issue_refund"}


def test_agent_accepts_custom_tools():
    llm = CapturingChatModel(responses=["ok"])
    agent = RefundAgent(llm=llm, tools=[])

    agent.ask("Refund order 42")

    assert llm.bound_tools == []
