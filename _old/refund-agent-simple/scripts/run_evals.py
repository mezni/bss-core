import json
from pathlib import Path

from refund_agent_simple.evaluation import load_cases, run_evaluation

dataset = Path("evals/refund_cases.jsonl")
report = run_evaluation(load_cases(dataset))

print(json.dumps(report, indent=2))

print("\n--- Evaluation Summary ---")
print(f"Cases: {report['total_cases']}")
print(f"Passed: {report['passed']}")
print(f"Failed: {report['failed']}")
print(f"Accuracy: {report['accuracy']:.1%}")
print(f"False approvals: {report['false_approvals']}")
print(f"Approval recall: {report['approval_recall']:.1%}")

if report["failed"] > 0 or report["false_approvals"] > 0:
    raise SystemExit(1)
