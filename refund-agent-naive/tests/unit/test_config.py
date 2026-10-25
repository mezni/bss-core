from decimal import Decimal

from refund_agent_naive.config import Settings


def test_defaults(monkeypatch):
    monkeypatch.setenv("REFUND_OPENAI_API_KEY", "x")
    s = Settings(_env_file=None)
    assert s.auto_approve_limit == Decimal("50.00")
    assert s.return_window_days == 30
    assert s.model_name == "gpt-4o-mini"
