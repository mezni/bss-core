from datetime import date

from openai import APIError

from refund_agent.models import (
    RefundDecision,
    RefundStatus,
)
from refund_agent.responses import format_refund_response
from refund_agent.workflow import process_refund


def handle_customer_message(
    customer_message: str,
    today: date | None = None,
) -> tuple[RefundDecision, str]:
    """Process a message and safely handle known LLM API failures."""

    try:
        decision = process_refund(
            customer_message=customer_message,
            today=today,
        )
    except APIError:
        decision = RefundDecision(
            order_id="unknown",
            status=RefundStatus.ESCALATED,
            eligible_amount=0,
            reason=(
                "The request could not be evaluated because "
                "the language service is temporarily unavailable."
            ),
            requires_human_approval=True,
        )

    response = format_refund_response(decision)
    return decision, response
