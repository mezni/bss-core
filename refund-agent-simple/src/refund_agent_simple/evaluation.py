import json
from pathlib import Path
from typing import Any

from refund_agent_simple.tools import _policy_result


def load_cases(path: Path) -> list[dict[str, Any]]:
    """Load evaluation cases from a JSONL file."""
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the refund policy decision for one case."""
    policy = _policy_result(case["order_id"])

    if "error" in policy:
        actual = "error"
    elif not policy["eligible"]:
        actual = "rejected"
    elif policy["requires_human_approval"]:
        actual = "pending_approval"
    else:
        actual = "refunded"

    return {
        "id": case["id"],
        "expected": case["expected_outcome"],
        "actual": actual,
        "passed": actual == case["expected_outcome"],
    }


def run_evaluation(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Run the policy eval suite and return a summary report."""
    results = [evaluate_case(case) for case in cases]

    total = len(results)
    passed = sum(result["passed"] for result in results)
    false_approvals = sum(
        result["actual"] == "refunded" and result["expected"] != "refunded"
        for result in results
    )

    expected_refunds = [
        result for result in results if result["expected"] == "refunded"
    ]
    correctly_refunded = sum(
        result["actual"] == "refunded" for result in expected_refunds
    )
    approval_recall = (
        correctly_refunded / len(expected_refunds) if expected_refunds else 1.0
    )

    return {
        "total_cases": total,
        "passed": passed,
        "failed": total - passed,
        "accuracy": passed / total if total else 0.0,
        "false_approvals": false_approvals,
        "approval_recall": approval_recall,
        "results": results,
    }
