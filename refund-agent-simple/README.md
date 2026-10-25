# refund-agent-simple

A small refund support agent built with [LangChain](https://python.langchain.com/)
and OpenAI (`gpt-6-luna`).

The agent can look up orders, check the refund policy, and issue refunds.
Refunds above 100 USD pause for human approval before they are processed.

## Setup

```bash
uv sync
cp .env.example .env
```

Then edit `.env`:

```dotenv
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-6-luna
```

## Usage

Interactive CLI:

```bash
uv run refund-agent-simple
```

Scripted example:

```bash
uv run python scripts/try_agent.py
```

## Refund policy

- Refund window: 30 days from purchase.
- Digital products are non-refundable once downloaded.
- Items must be unused.
- Refunds above 100 USD require human approval.

## Sample orders

| Order | Item | Amount | Age | Notes |
|-------|------|--------|-----|-------|
| 4821 | Wireless Headphones | 89.99 | 12 days | damaged on arrival |
| 4822 | Python Crash Course (ebook) | 29.99 | 3 days | digital, downloaded |
| 4823 | Standing Desk | 349.00 | 45 days | used |
| 4824 | Mechanical Keyboard | 149.00 | 5 days | unused, needs approval |

## Tests

```bash
uv run pytest -q
```

## Evaluations

```bash
uv run python scripts/run_evals.py
```

The small eval suite checks the policy decisions against `evals/refund_cases.jsonl`
and fails on regressions or unexpected refund approvals.


## Structure

```
src/refund_agent_simple/
  agent.py     RefundAgent, human-in-the-loop approval
  cli.py       interactive terminal CLI
  config.py    environment settings
  llm.py       OpenAI chat model
  prompts.py   system prompt
  tools.py     lookup_order, check_refund_policy, issue_refund
scripts/       runnable examples
tests/         pytest suite
```
