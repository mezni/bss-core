from datetime import date
from decimal import Decimal
from unittest.mock import patch

from refund_agent.agent import handle_customer_message
from refund_agent.models import RefundDecision, RefundStatus
from refund_agent.observability import (
    elapsed_milliseconds,
    new_request_id,
    request_id_context,
)


def test_request_ids_are_unique():
    assert new_request_id() != new_request_id()


def test_elapsed_time_is_non_negative():
    import time

    start = time.perf_counter()

    assert elapsed_milliseconds(start) >= 0


def test_agent_sets_and_resets_request_context():
    decision = RefundDecision(
        order_id="4821",
        status=RefundStatus.APPROVED,
        eligible_amount=Decimal("49.99"),
        reason="Eligible under refund policy.",
    )

    with patch(
        "refund_agent.agent.process_refund",
        return_value=decision,
    ):
        returned_decision, response = handle_customer_message(
            "Refund order 4821",
            today=date(2026, 10, 24),
        )

    assert returned_decision == decision
    assert "approved" in response.lower()
    assert request_id_context.get() == "-"
