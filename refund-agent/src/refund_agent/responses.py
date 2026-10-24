from refund_agent.models import RefundDecision, RefundStatus


def format_refund_response(decision: RefundDecision) -> str:
    """Convert a refund decision into a customer-facing message."""

    if decision.status == RefundStatus.APPROVED:
        return (
            f"Your refund request for order {decision.order_id} "
            f"has been approved for ${decision.eligible_amount:.2f}. "
            f"Approval does not mean the refund has been processed yet."
        )

    if decision.status == RefundStatus.REJECTED:
        return (
            f"We're unable to approve a refund for order "
            f"{decision.order_id}. Reason: {decision.reason}"
        )

    return (
        f"Your refund request for order {decision.order_id} "
        f"needs further review. Reason: {decision.reason} "
        "A support team member will need to review the request."
    )