
from refund_agent.evaluation_thresholds import check_thresholds


THRESHOLDS = {
    "minimum_intent_accuracy": 0.90,
    "minimum_order_id_accuracy": 0.95,
    "minimum_reason_accuracy": 0.85,
    "maximum_critical_errors": 0,
}


def test_passes_when_all_thresholds_are_met():
    report = {
        "intent_accuracy": 0.95,
        "order_id_accuracy": 1.0,
        "reason_accuracy": 0.90,
        "critical_errors": 0,
    }

    result = check_thresholds(report, THRESHOLDS)

    assert result["passed"] is True


def test_fails_when_accuracy_is_too_low():
    report = {
        "intent_accuracy": 0.80,
        "order_id_accuracy": 1.0,
        "reason_accuracy": 0.90,
        "critical_errors": 0,
    }

    result = check_thresholds(report, THRESHOLDS)

    assert result["passed"] is False
    assert result["checks"]["intent_accuracy"]["passed"] is False


def test_fails_when_critical_errors_exist():
    report = {
        "intent_accuracy": 1.0,
        "order_id_accuracy": 1.0,
        "reason_accuracy": 1.0,
        "critical_errors": 1,
    }

    result = check_thresholds(report, THRESHOLDS)

    assert result["passed"] is False
    assert result["checks"]["critical_errors"]["passed"] is False
