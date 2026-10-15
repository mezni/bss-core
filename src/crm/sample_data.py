from datetime import date
from decimal import Decimal

from crm.models import (
    Addon,
    AddonStatus,
    Contract,
    ContractTerm,
    Customer,
)


customer = Customer(
    customer_id="CUS-001",
    name="Example Customer",
    contracts=[
        Contract(
            contract_id="C-100",
            customer_id="CUS-001",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            currency="CAD",
            monthly_fee=Decimal("199.00"),
            terms=[
                ContractTerm(
                    name="renewal_term",
                    value="12 months",
                ),
                ContractTerm(
                    name="notice_period",
                    value="30 days",
                ),
            ],
            addons=[
                Addon(
                    addon_id="ADD-01",
                    name="Premium Support",
                    status=AddonStatus.ACTIVE,
                ),
                Addon(
                    addon_id="ADD-02",
                    name="Advanced Analytics",
                    status=AddonStatus.INACTIVE,
                ),
            ],
        ),
    ],
)
