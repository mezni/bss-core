from schemas import ProjectBlueprint
from service import ProjectBlueprintService
from telemetry import GenerationResult, GenerationTelemetry


class FakeProjectGenerator:
    def generate(self, project_idea: str) -> GenerationResult:
        return GenerationResult(
            blueprint=ProjectBlueprint(
                project_name="Test Project",
                business_outcome="Test business outcome.",
            ),
            telemetry=GenerationTelemetry(
                request_id="test-request",
                model="test-model",
                latency_seconds=0.1,
            ),
        )


def test_service_generates_blueprint() -> None:
    generator = FakeProjectGenerator()
    service = ProjectBlueprintService(generator)

    result = service.generate_blueprint(
        "Build an AI document classifier."
    )

    assert result.blueprint.project_name == "Test Project"
    assert (
        result.blueprint.business_outcome
        == "Test business outcome."
    )
    assert result.telemetry.request_id == "test-request"