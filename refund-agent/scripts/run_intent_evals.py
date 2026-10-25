
import json
from pathlib import Path

from refund_agent.evaluation_thresholds import check_thresholds
from refund_agent.intent_eval_data import load_intent_cases
from refund_agent.intent_evaluation import evaluate_intent_cases
from refund_agent.llm import extract_intent


def main() -> None:
    dataset = Path("evals/intent_cases.jsonl")
    thresholds_path = Path("evals/thresholds.json")

    cases = load_intent_cases(dataset)
    thresholds = json.loads(
        thresholds_path.read_text(encoding="utf-8")
    )

    report = evaluate_intent_cases(
        cases=cases,
        extractor=extract_intent,
    )

    threshold_report = check_thresholds(report, thresholds)

    print("--- Evaluation Report ---")
    print(json.dumps(report, indent=2))

    print("\n--- Threshold Results ---")
    print(json.dumps(threshold_report, indent=2))

    if not threshold_report["passed"]:
        print("\nEvaluation failed: one or more thresholds were not met.")
        raise SystemExit(1)

    print("\nEvaluation passed.")


if __name__ == "__main__":
    main()
