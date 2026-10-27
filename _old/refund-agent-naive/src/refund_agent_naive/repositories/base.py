from typing import Protocol

from refund_agent_naive.domain.models import Order, Refund


class OrderRepository(Protocol):
    def get_for_customer(self, order_id: str, customer_id: str) -> Order | None:
        """Return the order only if it exists AND belongs to the customer."""
        ...

    def mark_refunded(self, order_id: str) -> None: ...


class RefundRepository(Protocol):
    def create_if_absent(self, refund: Refund) -> tuple[Refund, bool]:
        """Atomically store the refund unless one already exists for the order.
        Returns (stored_refund, created). created=False means a duplicate."""
        ...
