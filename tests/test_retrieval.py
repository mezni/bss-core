from crm.retrieval import (
    get_active_addons,
    get_contract,
    get_contract_terms,
)


def test_get_existing_contract():
    contract = get_contract("C-100")

    assert contract is not None
    assert contract.contract_id == "C-100"


def test_get_unknown_contract():
    assert get_contract("C-999") is None


def test_get_contract_terms():
    terms = get_contract_terms("C-100")

    assert len(terms) == 2
    assert terms[0].name == "renewal_term"
    assert terms[0].value == "12 months"


def test_only_active_addons_are_returned():
    addons = get_active_addons("C-100")

    assert [addon.name for addon in addons] == ["Premium Support"]


def test_unknown_contract_has_no_active_addons():
    assert get_active_addons("C-999") == []
