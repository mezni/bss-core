from decimal import Decimal

from refund_agent.orders import get_order
from refund_agent.models import Order


def test_get_existing_order():
    order = get_order("4821")

    assert isinstance(order, Order)
    assert order.order_id == "4821"
    assert order.item_price == Decimal("49.99")
    assert order.is_damaged is True


def test_get_final_sale_order():
    order = get_order("4823")

    assert order is not None
    assert order.is_final_sale is True


def test_get_missing_order():
    order = get_order("9999")

    assert order is None
