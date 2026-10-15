from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from crm.models import (
    Addon,
    AddonStatus,
    Contract,
    Customer,
)


def test_customer_contains_contract():
    contract = Contract(
        contract_id="C-100",
        customer_id="CUS-001",
        start_date=date(2026, 1, 1),
        monthly_fee=Decimal("199.00"),
    )

    customer = Customer(
        customer_id="CUS-001",
        name="Example Customer",
        contracts=[contract],
    )

    assert customer.contracts[0].contract_id == "C-100"


def test_addon_status_is_validated():
    addon = Addon(
        addon_id="ADD-01",
        name="Premium Support",
        status=AddonStatus.ACTIVE,
    )

    assert addon.status == AddonStatus.ACTIVE


def test_negative_monthly_fee_is_rejected():
    with pytest.raises(ValidationError):
        Contract(
            contract_id="C-100",
            customer_id="CUS-001",
            start_date=date(2026, 1, 1),
            monthly_fee=Decimal("-1.00"),
        )
