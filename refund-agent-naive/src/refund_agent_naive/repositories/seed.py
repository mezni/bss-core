from datetime import date, timedelta
from decimal import Decimal

from refund_agent_naive.domain.models import Order


def demo_orders(today: date) -> list[Order]:
    return [
        Order(
            order_id="A1001",
            customer_id="c1",
            category="apparel",
            amount=Decimal("39.90"),
            delivered_on=today - timedelta(days=10),
        ),
        Order(
            order_id="A1002",
            customer_id="c1",
            category="electronics",
            amount=Decimal("349.00"),
            delivered_on=today - timedelta(days=5),
        ),
        Order(
            order_id="A1003",
            customer_id="c1",
            category="apparel",
            amount=Decimal("40.00"),
            delivered_on=today - timedelta(days=60),
        ),
        Order(
            order_id="B2001",
            customer_id="c2",
            category="apparel",
            amount=Decimal("25.00"),
            delivered_on=today - timedelta(days=3),
        ),
    ]
