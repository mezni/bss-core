from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from refund_agent_naive.domain.models import Decision, Order, PolicyResult


@dataclass(frozen=True)
class RefundPolicy:
    window_days: int
    auto_approve_limit: Decimal
    non_refundable_categories: frozenset[str]

    def evaluate(self, order: Order, requested: Decimal, today: date) -> PolicyResult:
        if order.refunded:
            return self._deny("Order has already been refunded.")
        if order.category in self.non_refundable_categories:
            return self._deny(f"Category '{order.category}' is non-refundable.")

        age_days = (today - order.delivered_on).days
        if age_days < 0:
            return self._deny("Order has not been delivered yet.")
        if age_days > self.window_days:
            return self._deny(
                f"Outside the {self.window_days}-day window ({age_days} days since delivery)."
            )

        if requested <= 0:
            return self._deny("Refund amount must be positive.")
        if requested > order.amount:
            return self._deny(f"Requested amount exceeds order total of {order.amount}.")

        if requested >= self.auto_approve_limit:
            return PolicyResult(
                decision=Decision.NEEDS_MANAGER,
                reason=f"Refunds of {self.auto_approve_limit} or more need manager approval.",
                max_refund=order.amount,
            )
        return PolicyResult(
            decision=Decision.AUTO_APPROVE, reason="Within policy.", max_refund=order.amount
        )

    @staticmethod
    def _deny(reason: str) -> PolicyResult:
        return PolicyResult(decision=Decision.DENY, reason=reason)
