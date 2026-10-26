.PHONY: dev test evals lint

dev:
	uv run uvicorn app.main:app --reload

test:
	uv run pytest

evals:
	uv run python -m evals.run_evals

lint:
	uv run ruff check . && uv run ruff format --check .
