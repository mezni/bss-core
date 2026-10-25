from collections.abc import Callable
from datetime import date

from refund_agent_naive.config import Settings
from refund_agent_naive.domain.policy import RefundPolicy
from refund_agent_naive.repositories.memory import InMemoryOrderRepository, InMemoryRefundRepository
from refund_agent_naive.repositories.seed import demo_orders
from refund_agent_naive.services.refund_service import RefundService


def build_policy(settings: Settings) -> RefundPolicy:
    return RefundPolicy(
        window_days=settings.return_window_days,
        auto_approve_limit=settings.auto_approve_limit,
        non_refundable_categories=settings.non_refundable_categories,
    )


def build_service(settings: Settings, today: Callable[[], date] = date.today) -> RefundService:
    """The only place where concrete implementations are chosen.
    Step 9 swaps the in-memory repos for Postgres here."""
    return RefundService(
        orders=InMemoryOrderRepository(demo_orders(today())),
        refunds=InMemoryRefundRepository(),
        policy=build_policy(settings),
        today=today,
    )
