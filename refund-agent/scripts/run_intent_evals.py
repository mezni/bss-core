
import json
from pathlib import Path

from refund_agent.intent_eval_data import load_intent_cases
from refund_agent.intent_evaluation import evaluate_intent_cases
from refund_agent.llm import extract_intent


def main() -> None:
    dataset = Path("evals/intent_cases.jsonl")
    cases = load_intent_cases(dataset)

    report = evaluate_intent_cases(
        cases=cases,
        extractor=extract_intent,
    )

    print(json.dumps(report, indent=2))

    print("\n--- LLM Intent Evaluation ---")
    print(f"Cases: {report['total_cases']}")
    print(f"Intent accuracy: {report['intent_accuracy']:.1%}")
    print(f"Order ID accuracy: {report['order_id_accuracy']:.1%}")
    print(f"Reason accuracy: {report['reason_accuracy']:.1%}")
    print(f"Critical errors: {report['critical_errors']}")

    if report["critical_errors"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
