
from pathlib import Path

from refund_agent.evaluation import load_cases, run_evaluation


def test_refund_evaluation_dataset():
    cases = load_cases(Path("evals/refund_cases.jsonl"))
    report = run_evaluation(cases)

    assert report["total_cases"] == 6
    assert report["failed"] == 0
    assert report["false_approvals"] == 0
    assert report["accuracy"] == 1.0
    assert report["escalation_recall"] == 1.0
