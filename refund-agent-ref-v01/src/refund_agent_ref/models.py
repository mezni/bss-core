from pydantic import BaseModel, Field


class Refund(BaseModel):
    reason: str


class Order(BaseModel):
    order_id: str
