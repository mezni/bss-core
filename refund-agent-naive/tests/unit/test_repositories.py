from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, date, datetime
from decimal import Decimal

import pytest

from refund_agent_naive.domain.models import Refund, RefundReason
from refund_agent_naive.repositories.memory import (
    InMemoryOrderRepository,
    InMemoryRefundRepository,
)
from refund_agent_naive.repositories.seed import demo_orders

TODAY = date(2026, 10, 25)


@pytest.fixture(params=["memory"])  # add "postgres" in a later step
def repos(request):
    return (
        InMemoryOrderRepository(demo_orders(TODAY)),
        InMemoryRefundRepository(),
    )


def make_refund(order_id: str = "A1001") -> Refund:
    return Refund(
        refund_id=f"r-{order_id}",
        order_id=order_id,
        customer_id="c1",
        amount=Decimal("10.00"),
        reason=RefundReason.DEFECTIVE,
        approved_by="auto",
        created_at=datetime.now(UTC),
    )


def test_owner_can_read_order(repos):
    orders, _ = repos
    assert orders.get_for_customer("A1001", "c1") is not None


def test_other_customers_order_is_hidden(repos):
    orders, _ = repos
    assert orders.get_for_customer("A1001", "c2") is None


def test_missing_order_looks_the_same_as_foreign_order(repos):
    orders, _ = repos
    assert orders.get_for_customer("NOPE", "c1") is None


def test_mark_refunded(repos):
    orders, _ = repos
    orders.mark_refunded("A1001")
    assert orders.get_for_customer("A1001", "c1").refunded is True


def test_create_if_absent_is_idempotent(repos):
    _, refunds = repos
    first, created1 = refunds.create_if_absent(make_refund())
    second, created2 = refunds.create_if_absent(make_refund())
    assert created1 is True and created2 is False
    assert first == second


def test_concurrent_duplicates_create_exactly_one(repos):
    _, refunds = repos
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: refunds.create_if_absent(make_refund()), range(20)))
    assert sum(1 for _, created in results if created) == 1
