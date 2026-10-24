from enum import StrEnum

from pydantic import BaseModel, Field


class CustomerIntent(StrEnum):
    REFUND_REQUEST = "refund_request"
    EXCHANGE = "exchange"
    ORDER_INQUIRY = "order_inquiry"
    OTHER = "other"


class RefundReason(StrEnum):
    DAMAGED_ITEM = "damaged_item"
    DEFECTIVE_ITEM = "defective_item"
    UNWANTED_ITEM = "unwanted_item"
    WRONG_ITEM = "wrong_item"
    OTHER = "other"


class IntentResult(BaseModel):
    intent: CustomerIntent
    order_id: str | None = None
    reason: RefundReason = RefundReason.OTHER
    summary: str = Field(description="A short summary of the customer's request.")
