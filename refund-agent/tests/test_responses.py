from decimal import Decimal

from refund_agent.models import RefundDecision, RefundStatus
from refund_agent.responses import format_refund_response


def test_approved_response_does_not_claim_refund_was_processed():
    decision = RefundDecision(
        order_id="4821",
        status=RefundStatus.APPROVED,
        eligible_amount=Decimal("49.99"),
        reason="Order meets the refund eligibility rules.",
    )

    response = format_refund_response(decision)

    assert "approved" in response.lower()
    assert "$49.99" in response
    assert "processed yet" in response.lower()


def test_rejected_response_includes_reason():
    decision = RefundDecision(
        order_id="4823",
        status=RefundStatus.REJECTED,
        eligible_amount=Decimal("0.00"),
        reason="Final-sale items are not refundable.",
    )

    response = format_refund_response(decision)

    assert "unable to approve" in response.lower()
    assert "Final-sale items are not refundable." in response


def test_escalated_response_requests_review():
    decision = RefundDecision(
        order_id="9999",
        status=RefundStatus.ESCALATED,
        eligible_amount=Decimal("0.00"),
        reason="Order not found. Verify the order ID.",
        requires_human_approval=True,
    )

    response = format_refund_response(decision)

    assert "further review" in response.lower()
    assert "support team member" in response.lower()