from datetime import date
from decimal import Decimal

from refund_agent.models import Order

MOCK_ORDERS: dict[str, Order] = {
    "4821": Order(
        order_id="4821",
        delivery_date=date(2026, 10, 20),
        item_price=Decimal("49.99"),
        is_damaged=True,
        damage_evidence_verified=True,
    ),
    "4822": Order(
        order_id="4822",
        delivery_date=date(2026, 9, 1),
        item_price=Decimal("79.99"),
    ),
    "4823": Order(
        order_id="4823",
        delivery_date=date(2026, 10, 21),
        item_price=Decimal("149.99"),
        is_final_sale=True,
    ),
}


def get_order(order_id: str) -> Order | None:
    """Return an order by ID, or None if it does not exist."""
    return MOCK_ORDERS.get(order_id)
