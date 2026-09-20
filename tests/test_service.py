from context import RequestContext
from service import ProjectBlueprintService
from tests.fakes import FakeProjectGenerator


def test_service_generates_blueprint() -> None:
    generator = FakeProjectGenerator()
    service = ProjectBlueprintService(generator)

    context = RequestContext.create()

    result = service.generate_blueprint(
        "Build an AI document classifier.",
        context,
    )

    assert result.blueprint.project_name == "Test Project"
    assert result.blueprint.business_outcome == "Test business outcome."
    assert result.telemetry.request_id == context.request_id