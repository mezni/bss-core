from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class RefundStatus(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"


class RefundRequest(BaseModel):
    order_id: str = Field(min_length=1)
    reason: str = Field(min_length=3)
    requested_amount: Decimal | None = Field(default=None, gt=0)


class Order(BaseModel):
    order_id: str
    delivery_date: date
    item_price: Decimal = Field(gt=0)
    is_final_sale: bool = False
    is_damaged: bool = False
    return_received: bool = False



class RefundDecision(BaseModel):
    order_id: str
    status: RefundStatus
    eligible_amount: Decimal = Field(ge=0)
    reason: str
    requires_human_approval: bool = False
