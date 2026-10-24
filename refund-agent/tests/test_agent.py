from datetime import date
from decimal import Decimal

from refund_agent.agent import handle_customer_message
from refund_agent.intent import CustomerIntent, IntentResult
from refund_agent.models import RefundStatus


def test_handle_customer_message(monkeypatch):
    monkeypatch.setattr(
        "refund_agent.workflow.extract_intent",
        lambda _: IntentResult(
            intent=CustomerIntent.REFUND_REQUEST,
            order_id="4821",
            summary="Item arrived damaged",
        ),
    )

    decision, response = handle_customer_message(
        "I want a refund for order 4821.",
        today=date(2026, 10, 24),
    )

    assert decision.status == RefundStatus.APPROVED
    assert decision.eligible_amount == Decimal("49.99")
    assert "$49.99" in response