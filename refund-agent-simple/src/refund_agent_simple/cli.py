from refund_agent_simple.agent import RefundAgent


def main() -> None:
    agent = RefundAgent()
    thread_id = "cli"

    print("Refund Agent (type 'quit' to exit)")

    while True:
        message = input("\nYou: ").strip()
        if not message:
            continue
        if message.lower() in {"quit", "exit"}:
            break

        result = agent.ask(message, thread_id=thread_id)
        print(f"\nAgent: {result.message}")

        while result.status == "pending_approval":
            answer = input("Approve this refund? [y/N]: ").strip().lower()
            decision = "approve" if answer in {"y", "yes"} else "reject"
            result = agent.resume(decision, thread_id=thread_id)
            print(f"\nAgent: {result.message}")
