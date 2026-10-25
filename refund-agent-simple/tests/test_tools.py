import json

from refund_agent_simple.tools import lookup_order


def test_lookup_existing_order():
    result = json.loads(lookup_order.invoke({"order_id": "4821"}))

    assert result["order_id"] == "4821"
    assert result["amount_usd"] == 89.99


def test_lookup_missing_order_returns_error():
    result = json.loads(lookup_order.invoke({"order_id": "9999"}))

    assert "error" in result
