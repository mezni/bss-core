from datetime import date
from decimal import Decimal

import pytest

from refund_agent_naive.domain.policy import RefundPolicy
from refund_agent_naive.repositories.memory import InMemoryOrderRepository, InMemoryRefundRepository
from refund_agent_naive.repositories.seed import demo_orders
from refund_agent_naive.services.refund_service import RefundService

TODAY = date(2026, 10, 25)


@pytest.fixture
def orders():
    return InMemoryOrderRepository(demo_orders(TODAY))


@pytest.fixture
def refunds():
    return InMemoryRefundRepository()


@pytest.fixture
def service(orders, refunds):
    policy = RefundPolicy(30, Decimal("50.00"), frozenset({"gift_card"}))
    return RefundService(orders, refunds, policy, today=lambda: TODAY)
