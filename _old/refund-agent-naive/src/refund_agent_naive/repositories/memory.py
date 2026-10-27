from collections.abc import Iterable
from threading import Lock

from refund_agent_naive.domain.models import Order, Refund


class InMemoryOrderRepository:
    def __init__(self, orders: Iterable[Order] = ()) -> None:
        self._orders = {o.order_id: o for o in orders}
        self._lock = Lock()

    def get_for_customer(self, order_id: str, customer_id: str) -> Order | None:
        order = self._orders.get(order_id)
        if order is None or order.customer_id != customer_id:
            return None  # same answer for "missing" and "not yours"
        return order

    def mark_refunded(self, order_id: str) -> None:
        with self._lock:
            order = self._orders[order_id]
            self._orders[order_id] = order.model_copy(update={"refunded": True})


class InMemoryRefundRepository:
    def __init__(self) -> None:
        self._by_order: dict[str, Refund] = {}
        self._lock = Lock()

    def create_if_absent(self, refund: Refund) -> tuple[Refund, bool]:
        with self._lock:
            existing = self._by_order.get(refund.order_id)
            if existing is not None:
                return existing, False
            self._by_order[refund.order_id] = refund
            return refund, True
