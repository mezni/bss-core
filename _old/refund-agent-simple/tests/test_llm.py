from langchain_openai import ChatOpenAI

from refund_agent_simple.config import get_settings
from refund_agent_simple.llm import get_llm


def test_llm_uses_configured_model(monkeypatch):
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    get_settings.cache_clear()

    llm = get_llm()

    assert isinstance(llm, ChatOpenAI)
    assert llm.model_name == "test-model"

    get_settings.cache_clear()
