from llm.prompts import load_system_prompt


def test_system_prompt_is_loaded():
    prompt = load_system_prompt()

    assert "Never invent contract terms" in prompt
    assert "supplied CRM context" in prompt
