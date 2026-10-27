from openai import APIError

from refund_agent.agent import handle_customer_message
from refund_agent.models import RefundStatus


def test_api_failure_escalates_without_approval(monkeypatch):
    def fail_with_api_error(*args, **kwargs):
        raise APIError(
            message="Service unavailable",
            request=None,
            body=None,
        )

    monkeypatch.setattr(
        "refund_agent.agent.process_refund",
        fail_with_api_error,
    )

    decision, response = handle_customer_message("I want a refund for order 4821.")

    assert decision.status == RefundStatus.ESCALATED
    assert decision.requires_human_approval is True
    assert decision.eligible_amount == 0
    assert "temporarily unavailable" in response.lower()
