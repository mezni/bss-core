from refund_agent.tools import lookup_order


def test_lookup_existing_order():
    result = lookup_order.invoke({"order_id": "4821"})

    assert "Order ID: 4821" in result
    assert "Item price: 49.99" in result
    assert "Damaged: True" in result


def test_lookup_missing_order():
    result = lookup_order.invoke({"order_id": "9999"})

    assert "was not found" in result
