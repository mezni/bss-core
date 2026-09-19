from pydantic import BaseModel, Field, field_validator


class ProjectBlueprint(BaseModel):
    project_name: str = Field(
        description="A clear and concise name for the proposed AI project."
    )

    business_outcome: str = Field(
        description="The measurable business outcome the AI project should achieve."
    )

    @field_validator("project_name", "business_outcome")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value