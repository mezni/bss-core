from crm.models import Addon, Contract, ContractTerm
from crm.sample_data import customer


def get_contract(contract_id: str) -> Contract | None:
    """Return a contract by ID, or None if it does not exist."""
    for customer_record in [customer]:
        for contract in customer_record.contracts:
            if contract.contract_id == contract_id:
                return contract

    return None


def get_contract_terms(
    contract_id: str,
) -> list[ContractTerm]:
    """Return the terms for a contract."""
    contract = get_contract(contract_id)

    if contract is None:
        return []

    return contract.terms


def get_active_addons(contract_id: str) -> list[Addon]:
    """Return only active add-ons for a contract."""
    contract = get_contract(contract_id)

    if contract is None:
        return []

    return [addon for addon in contract.addons if addon.status == "active"]
