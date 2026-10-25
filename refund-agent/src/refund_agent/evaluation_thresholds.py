from typing import Any


def check_thresholds(
    report: dict[str, Any],
    thresholds: dict[str, Any],
) -> dict[str, Any]:
    checks = {
        "intent_accuracy": (
            report["intent_accuracy"],
            thresholds["minimum_intent_accuracy"],
            ">=",
        ),
        "order_id_accuracy": (
            report["order_id_accuracy"],
            thresholds["minimum_order_id_accuracy"],
            ">=",
        ),
        "reason_accuracy": (
            report["reason_accuracy"],
            thresholds["minimum_reason_accuracy"],
            ">=",
        ),
        "critical_errors": (
            report["critical_errors"],
            thresholds["maximum_critical_errors"],
            "<=",
        ),
    }

    results = {}

    for metric, (actual, threshold, operator) in checks.items():
        passed = actual >= threshold if operator == ">=" else actual <= threshold

        results[metric] = {
            "actual": actual,
            "threshold": threshold,
            "operator": operator,
            "passed": passed,
        }

    return {
        "passed": all(item["passed"] for item in results.values()),
        "checks": results,
    }
