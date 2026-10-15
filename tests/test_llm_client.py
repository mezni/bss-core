
from types import SimpleNamespace

from llm import client as llm_client


def test_ask_llm_returns_generated_text(monkeypatch):
    def fake_create(**kwargs):
        assert kwargs["model"] == "test-model"
        assert kwargs["input"] == "Explain a CRM contract."
        return SimpleNamespace(
            output_text="A CRM contract defines agreed terms."
        )

    fake_client = SimpleNamespace(
        responses=SimpleNamespace(
            create=fake_create
        )
    )

    monkeypatch.setattr(
        llm_client,
        "OpenAI",
        lambda **kwargs: fake_client,
    )
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    result = llm_client.ask_llm("Explain a CRM contract.")

    assert result == "A CRM contract defines agreed terms."
