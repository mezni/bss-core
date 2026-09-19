import pytest
from pydantic import ValidationError

from schemas import ProjectBlueprint


def test_project_blueprint_accepts_valid_data() -> None:
    blueprint = ProjectBlueprint(
        project_name="Document Classification System",
        business_outcome="Reduce manual document classification effort.",
    )

    assert blueprint.project_name == "Document Classification System"
    assert (
        blueprint.business_outcome
        == "Reduce manual document classification effort."
    )


def test_project_blueprint_rejects_empty_project_name() -> None:
    with pytest.raises(ValidationError):
        ProjectBlueprint(
            project_name="   ",
            business_outcome="Reduce manual classification effort.",
        )


def test_project_blueprint_rejects_empty_business_outcome() -> None:
    with pytest.raises(ValidationError):
        ProjectBlueprint(
            project_name="Document Classification System",
            business_outcome="   ",
        )