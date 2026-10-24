from datetime import date
from decimal import Decimal

from refund_agent.intent import CustomerIntent, IntentResult
from refund_agent.llm import extract_intent

from refund_agent.models import (
    RefundDecision,
    RefundRequest,
    RefundStatus,
)
from refund_agent.orders import get_order
from refund_agent.policy import evaluate_refund


def process_refund(
    customer_message: str,
    today: date | None = None,
) -> RefundDecision:
    """Process a refund request and return a policy-based decision."""
    current_date = today or date.today()

    # 1. Understand the customer's request.
    intent: IntentResult = extract_intent(customer_message)

    if intent.intent != CustomerIntent.REFUND_REQUEST:
        return RefundDecision(
            order_id=intent.order_id or "unknown",
            status=RefundStatus.ESCALATED,
            eligible_amount=Decimal("0.00"),
            reason="This workflow only handles refund requests.",
            requires_human_approval=True,
        )

    # 2. Ensure the customer provided an order ID.
    if not intent.order_id:
        return RefundDecision(
            order_id="unknown",
            status=RefundStatus.ESCALATED,
            eligible_amount=Decimal("0.00"),
            reason="An order ID is required to evaluate a refund.",
            requires_human_approval=True,
        )

    # 3. Validate the request and retrieve the order.
    request = RefundRequest(
        order_id=intent.order_id,
        reason=intent.summary,
    )
    order = get_order(request.order_id)

    if order is None:
        return RefundDecision(
            order_id=request.order_id,
            status=RefundStatus.ESCALATED,
            eligible_amount=Decimal("0.00"),
            reason="Order not found. Verify the order ID.",
            requires_human_approval=True,
        )

    # 4. Apply deterministic business rules.
    return evaluate_refund(
        request=request,
        order=order,
        today=current_date,
    )