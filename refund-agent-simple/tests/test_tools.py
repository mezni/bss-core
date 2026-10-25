import json

from refund_agent_simple.tools import check_refund_policy, lookup_order


def test_lookup_existing_order():
    result = json.loads(lookup_order.invoke({"order_id": "4821"}))

    assert result["order_id"] == "4821"
    assert result["amount_usd"] == 89.99


def test_lookup_missing_order_returns_error():
    result = json.loads(lookup_order.invoke({"order_id": "9999"}))

    assert "error" in result


def test_damaged_order_is_eligible_without_approval():
    result = json.loads(check_refund_policy.invoke({"order_id": "4821"}))

    assert result["eligible"] is True
    assert result["reasons"] == []
    assert result["requires_human_approval"] is False


def test_digital_order_is_not_eligible():
    result = json.loads(check_refund_policy.invoke({"order_id": "4822"}))

    assert result["eligible"] is False
    assert result["requires_human_approval"] is False


def test_used_and_old_order_is_not_eligible():
    result = json.loads(check_refund_policy.invoke({"order_id": "4823"}))

    assert result["eligible"] is False
    assert any("30 days" in reason for reason in result["reasons"])
    assert any("unused" in reason for reason in result["reasons"])


def test_high_value_order_requires_approval():
    result = json.loads(check_refund_policy.invoke({"order_id": "4824"}))

    assert result["eligible"] is True
    assert result["requires_human_approval"] is True


def test_policy_check_missing_order_returns_error():
    result = json.loads(check_refund_policy.invoke({"order_id": "9999"}))

    assert "error" in result
