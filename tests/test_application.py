from application import create_application
from interfaces import ProjectGeneratorInterface
from schemas import ProjectBlueprint
from telemetry import GenerationResult, GenerationTelemetry


class FakeProjectGenerator(ProjectGeneratorInterface):
    def generate(self, project_idea: str) -> GenerationResult:
        return GenerationResult(
            blueprint=ProjectBlueprint(
                project_name="Test Project",
                business_outcome="Test business outcome.",
            ),
            telemetry=GenerationTelemetry(
                request_id="test-request",
                model="test-model",
                prompt_version="v1",
                latency_seconds=0.1,
            ),
        )


def test_create_application_with_custom_generator() -> None:
    application = create_application(
        generator=FakeProjectGenerator()
    )

    result = application.generate_blueprint(
        "Build an AI document classifier."
    )

    assert result.blueprint.project_name == "Test Project"
    assert result.telemetry.request_id == "test-request"