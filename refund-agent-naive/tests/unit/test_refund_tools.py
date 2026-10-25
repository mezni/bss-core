from decimal import Decimal
from types import SimpleNamespace

import pytest

from refund_agent_naive.context import AgentContext
from refund_agent_naive.tools.refund_tools import build_refund_tools


@pytest.fixture
def tools(service):
    return {t.name: t for t in build_refund_tools(service)}


def rt(customer_id: str):
    return SimpleNamespace(context=AgentContext(customer_id=customer_id))


def test_customer_id_is_not_exposed_to_the_model(tools):
    for t in tools.values():
        assert "customer_id" not in t.args


def test_tool_uses_context_customer(tools):
    out = tools["get_order"].func(order_id="A1001", runtime=rt("c1"))
    assert out["order_id"] == "A1001"


def test_tool_cannot_read_other_customers_order(tools):
    out = tools["get_order"].func(order_id="B2001", runtime=rt("c1"))
    assert out == {"error": "Order not found."}


def test_issue_refund_small(tools):
    out = tools["issue_refund"].func(
        order_id="A1001", amount=Decimal("20.00"), reason="defective", runtime=rt("c1")
    )
    assert out["outcome"] == "refunded"


def test_issue_refund_large_is_pending(tools):
    out = tools["issue_refund"].func(
        order_id="A1002", amount=Decimal("349.00"), reason="defective", runtime=rt("c1")
    )
    assert out["outcome"] == "pending_approval"