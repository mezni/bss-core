from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AddonStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ContractTerm(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    value: str


class Addon(BaseModel):
    model_config = ConfigDict(extra="forbid")

    addon_id: str
    name: str
    status: AddonStatus


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str
    customer_id: str
    start_date: date
    end_date: date | None = None
    currency: str = "CAD"
    monthly_fee: Decimal = Field(ge=0)
    terms: list[ContractTerm] = Field(default_factory=list)
    addons: list[Addon] = Field(default_factory=list)


class Customer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str
    name: str
    contracts: list[Contract] = Field(default_factory=list)
