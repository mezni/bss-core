from pydantic import BaseModel, Field, field_validator


class ProjectBlueprint(BaseModel):
    project_name: str = Field(
        description="A concise and meaningful name for the AI project."
    )

    business_outcome: str = Field(
        description=(
            "The primary business result the AI project should achieve. "
            "Focus on measurable business value rather than technical implementation."
        )
    )

    @field_validator("project_name", "business_outcome")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value