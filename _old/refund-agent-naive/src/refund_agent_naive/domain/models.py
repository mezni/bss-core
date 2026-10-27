from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Decision(StrEnum):
    AUTO_APPROVE = "auto_approve"
    NEEDS_MANAGER = "needs_manager"
    DENY = "deny"


class Order(BaseModel):
    model_config = ConfigDict(frozen=True)

    order_id: str
    customer_id: str
    category: str
    amount: Decimal
    delivered_on: date
    refunded: bool = False


class PolicyResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    decision: Decision
    reason: str
    max_refund: Decimal = Decimal("0")


class RefundReason(StrEnum):
    DEFECTIVE = "defective"
    NOT_AS_DESCRIBED = "not_as_described"
    CHANGED_MIND = "changed_mind"
    LATE = "late"
    OTHER = "other"


class Refund(BaseModel):
    model_config = ConfigDict(frozen=True)

    refund_id: str
    order_id: str
    customer_id: str
    amount: Decimal
    reason: RefundReason
    approved_by: str  # "auto" or the manager's id
    created_at: datetime
