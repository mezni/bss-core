from refund_agent.metrics import AgentMetrics
from refund_agent.models import RefundStatus


def test_metrics_record_requests_and_latency():
    metrics = AgentMetrics()

    metrics.record_request(100.0)
    metrics.record_request(200.0)

    snapshot = metrics.snapshot()

    assert snapshot["requests_total"] == 2
    assert snapshot["latency_ms"]["count"] == 2
    assert snapshot["latency_ms"]["average"] == 150.0


def test_metrics_record_outcomes():
    metrics = AgentMetrics()

    metrics.record_outcome(RefundStatus.APPROVED)
    metrics.record_outcome(RefundStatus.APPROVED)
    metrics.record_outcome(RefundStatus.ESCALATED)

    snapshot = metrics.snapshot()

    assert snapshot["outcomes"]["approved"] == 2
    assert snapshot["outcomes"]["escalated"] == 1


def test_metrics_record_errors():
    metrics = AgentMetrics()

    metrics.record_error()

    assert metrics.snapshot()["errors_total"] == 1


def test_empty_metrics_are_safe():
    snapshot = AgentMetrics().snapshot()

    assert snapshot["requests_total"] == 0
    assert snapshot["latency_ms"]["average"] == 0.0
    assert snapshot["latency_ms"]["p95"] == 0.0
