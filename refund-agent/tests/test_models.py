from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from refund_agent.models import (
    Order,
    RefundDecision,
    RefundRequest,
    RefundStatus,
)


def test_create_refund_request():
    request = RefundRequest(
        order_id="4821",
        reason="Item arrived damaged",
        requested_amount=Decimal("49.99"),
    )

    assert request.order_id == "4821"
    assert request.requested_amount == Decimal("49.99")


def test_create_order():
    order = Order(
        order_id="4821",
        delivery_date=date(2026, 10, 20),
        item_price=Decimal("49.99"),
        is_damaged=True,
    )

    assert order.is_damaged is True
    assert order.return_received is False


def test_reject_invalid_refund_amount():
    with pytest.raises(ValidationError):
        RefundRequest(
            order_id="4821",
            reason="Damaged item",
            requested_amount=Decimal("-10.00"),
        )


def test_create_refund_decision():
    decision = RefundDecision(
        order_id="4821",
        status=RefundStatus.APPROVED,
        eligible_amount=Decimal("49.99"),
        reason="Order meets the eligibility criteria",
    )

    assert decision.status == RefundStatus.APPROVED
    assert decision.requires_human_approval is False
