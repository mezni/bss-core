from typing import Any, ClassVar

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import BaseMessage

from refund_agent_simple.agent import RefundAgent


class CapturingChatModel(FakeListChatModel):
    captured: ClassVar[list[list[BaseMessage]]] = []

    def _call(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> str:
        self.captured.append(messages)
        return super()._call(messages, stop, run_manager, **kwargs)


def test_agent_returns_model_response():
    llm = FakeListChatModel(responses=["Please share your order ID."])
    agent = RefundAgent(llm=llm)

    response = agent.ask("I want a refund.")

    assert response == "Please share your order ID."


def test_agent_passes_customer_message_to_model():
    llm = CapturingChatModel(responses=["ok"])
    agent = RefundAgent(llm=llm)

    agent.ask("Refund order 42")

    messages = llm.captured[0]
    assert messages[-1].content == "Refund order 42"
