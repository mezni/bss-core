import pytest
from pydantic import ValidationError

from refund_agent.intent import (
    CustomerIntent,
    IntentResult,
    RefundReason,
)


def test_create_refund_intent():
    result = IntentResult(
        intent=CustomerIntent.REFUND_REQUEST,
        order_id="4821",
        reason=RefundReason.DAMAGED_ITEM,
        summary="Customer reports a damaged item.",
    )

    assert result.intent == CustomerIntent.REFUND_REQUEST
    assert result.order_id == "4821"
    assert result.reason == RefundReason.DAMAGED_ITEM


def test_order_id_can_be_missing():
    result = IntentResult(
        intent=CustomerIntent.REFUND_REQUEST,
        summary="Customer requests a refund.",
    )

    assert result.order_id is None


def test_invalid_intent_is_rejected():
    with pytest.raises(ValidationError):
        IntentResult(
            intent="refund_maybe",
            summary="Unclear request.",
        )
