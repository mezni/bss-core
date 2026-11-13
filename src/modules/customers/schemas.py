# src/modules/customers/schemas.py
from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
  name: str
  email: EmailStr
  phone: str | None = None


class CustomerResponse(BaseModel):
  id: int
  name: str
  email: str
  phone: str | None
  owner_id: int | None

  class Config:
    from_attributes = True
