from datetime import date

from refund_agent.models import RefundDecision
from refund_agent.responses import format_refund_response
from refund_agent.workflow import process_refund


def handle_customer_message(
    customer_message: str,
    today: date | None = None,
) -> tuple[RefundDecision, str]:
    """Process a customer message and return the decision and response."""

    decision = process_refund(
        customer_message=customer_message,
        today=today,
    )

    response = format_refund_response(decision)

    return decision, response
