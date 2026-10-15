import pytest
from pydantic import ValidationError

from llm.schemas import CRMContractResponse


def test_valid_crm_response():
    result = CRMContractResponse(
        contract_id="C-100",
        contract_terms=["Renewal term: 12 months"],
        active_addons=["Premium Support"],
        found_in_context=True,
        missing_information=[],
    )

    assert result.contract_id == "C-100"
    assert result.active_addons == ["Premium Support"]


def test_missing_required_field_is_rejected():
    with pytest.raises(ValidationError):
        CRMContractResponse(
            contract_id="C-100",
            contract_terms=[],
            active_addons=[],
        )


def test_unexpected_field_is_rejected():
    with pytest.raises(ValidationError):
        CRMContractResponse(
            contract_id="C-100",
            contract_terms=[],
            active_addons=[],
            found_in_context=True,
            unexpected_field="not allowed",
        )
