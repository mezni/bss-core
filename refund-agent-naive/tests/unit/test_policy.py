from datetime import date, timedelta
from decimal import Decimal

import pytest

from refund_agent_naive.domain.models import Decision, Order
from refund_agent_naive.domain.policy import RefundPolicy

TODAY = date(2026, 10, 25)
POLICY = RefundPolicy(30, Decimal("50.00"), frozenset({"gift_card"}))


def make_order(**kw) -> Order:
    base = dict(
        order_id="A1",
        customer_id="c1",
        category="apparel",
        amount=Decimal("80.00"),
        delivered_on=TODAY - timedelta(days=5),
    )
    return Order(**{**base, **kw})


def test_small_refund_auto_approved():
    r = POLICY.evaluate(make_order(), Decimal("49.99"), TODAY)
    assert r.decision is Decision.AUTO_APPROVE


def test_threshold_needs_manager():
    r = POLICY.evaluate(make_order(), Decimal("50.00"), TODAY)
    assert r.decision is Decision.NEEDS_MANAGER


@pytest.mark.parametrize(
    "order_kw, requested",
    [
        ({"refunded": True}, "10"),
        ({"category": "gift_card"}, "10"),
        ({"delivered_on": TODAY - timedelta(days=31)}, "10"),
        ({"delivered_on": TODAY + timedelta(days=1)}, "10"),
        ({}, "0"),
        ({}, "-5"),
        ({}, "80.01"),
    ],
)
def test_denials(order_kw, requested):
    r = POLICY.evaluate(make_order(**order_kw), Decimal(requested), TODAY)
    assert r.decision is Decision.DENY


def test_window_boundary():
    on_day_30 = make_order(delivered_on=TODAY - timedelta(days=30))
    assert POLICY.evaluate(on_day_30, Decimal("10"), TODAY).decision is Decision.AUTO_APPROVE
