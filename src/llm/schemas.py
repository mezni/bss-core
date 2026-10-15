from pydantic import BaseModel, ConfigDict, Field


class CRMContractResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str | None = None
    contract_terms: list[str] = Field(default_factory=list)
    active_addons: list[str] = Field(default_factory=list)
    found_in_context: bool
    missing_information: list[str] = Field(default_factory=list)
