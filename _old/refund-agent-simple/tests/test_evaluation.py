from pathlib import Path

from refund_agent_simple.evaluation import load_cases, run_evaluation

DATASET = Path(__file__).parent.parent / "evals" / "refund_cases.jsonl"


def test_eval_suite_passes():
    report = run_evaluation(load_cases(DATASET))

    assert report["failed"] == 0
    assert report["false_approvals"] == 0
    assert report["accuracy"] == 1.0


def test_eval_outcomes_match_expected():
    report = run_evaluation(load_cases(DATASET))

    outcomes = {result["id"]: result["actual"] for result in report["results"]}
    assert outcomes == {
        "refund-001": "refunded",
        "refund-002": "rejected",
        "refund-003": "rejected",
        "refund-004": "pending_approval",
        "refund-005": "error",
    }
