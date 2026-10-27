from decimal import Decimal

from refund_agent.models import (
    Order,
    RefundDecision,
    RefundRequest,
    RefundStatus,
)
from refund_agent.policy import AUTONOMOUS_REFUND_LIMIT


def apply_guardrails(
    request: RefundRequest,
    order: Order,
    decision: RefundDecision,
) -> RefundDecision:
    """Apply safety checks before returning a refund decision."""

    # Never override an explicit policy rejection.
    if decision.status == RefundStatus.REJECTED:
        return decision

    # Damaged-item claims require verified evidence.
    if order.is_damaged and not order.damage_evidence_verified:
        return RefundDecision(
            order_id=request.order_id,
            status=RefundStatus.ESCALATED,
            eligible_amount=Decimal("0.00"),
            reason=("Damage evidence has not been verified. Human review is required."),
            requires_human_approval=True,
        )

    # Enforce the autonomous approval limit independently.
    if decision.eligible_amount > AUTONOMOUS_REFUND_LIMIT:
        return RefundDecision(
            order_id=request.order_id,
            status=RefundStatus.ESCALATED,
            eligible_amount=decision.eligible_amount,
            reason=(
                "Refund exceeds the autonomous approval limit. "
                "Human approval is required."
            ),
            requires_human_approval=True,
        )

    # Escalated decisions must always require human approval.
    if decision.status == RefundStatus.ESCALATED:
        return decision.model_copy(update={"requires_human_approval": True})

    return decision
