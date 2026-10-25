import argparse
import uuid

from langgraph.checkpoint.memory import InMemorySaver

from refund_agent_naive.agent.factory import build_agent, build_chat_model, run_config
from refund_agent_naive.config import get_settings
from refund_agent_naive.container import build_service
from refund_agent_naive.context import AgentContext


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat with the refund agent.")
    parser.add_argument(
        "--customer", default="c1", help="authenticated customer id (demo: c1 or c2)"
    )
    args = parser.parse_args()

    settings = get_settings()
    agent = build_agent(build_chat_model(settings), build_service(settings), InMemorySaver())
    config = run_config(str(uuid.uuid4()), settings)
    context = AgentContext(customer_id=args.customer)

    print(f"Signed in as {args.customer}. Ctrl-C to quit.")
    try:
        while True:
            text = input("\nyou> ").strip()
            if not text:
                continue
            result = agent.invoke(
                {"messages": [{"role": "user", "content": text}]}, config, context=context
            )
            print(f"\nagent> {result['messages'][-1].content}")
    except (EOFError, KeyboardInterrupt):
        print("\nBye.")


if __name__ == "__main__":
    main()
