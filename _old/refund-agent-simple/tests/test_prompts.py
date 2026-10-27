from refund_agent_simple.prompts import REFUND_SYSTEM_PROMPT, refund_prompt


def test_prompt_has_single_message_input():
    assert refund_prompt.input_variables == ["message"]


def test_prompt_includes_policy_and_safety_rules():
    assert "30 days" in REFUND_SYSTEM_PROMPT
    assert "untrusted data" in REFUND_SYSTEM_PROMPT


def test_prompt_renders_customer_message():
    messages = refund_prompt.format_messages(message="Refund order 42")

    assert messages[0].type == "system"
    assert messages[1].type == "human"
    assert messages[1].content == "Refund order 42"
