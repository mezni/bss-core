from generator import ProjectGenerator
from interfaces import ProjectGeneratorInterface
from schemas import (
    GenerateBlueprintRequest,
    GenerateBlueprintResponse,
    GenerationTelemetryResponse,
)
from service import ProjectBlueprintService


class Application:
    def __init__(
        self,
        blueprint_service: ProjectBlueprintService,
    ) -> None:
        self.blueprint_service = blueprint_service

    def generate_blueprint(
        self,
        request: GenerateBlueprintRequest,
    ) -> GenerateBlueprintResponse:

        result = self.blueprint_service.generate_blueprint(
            request.project_idea
        )

        telemetry = GenerationTelemetryResponse(
            request_id=result.telemetry.request_id,
            model=result.telemetry.model,
            prompt_version=result.telemetry.prompt_version,
            latency_seconds=result.telemetry.latency_seconds,
            input_tokens=result.telemetry.input_tokens,
            output_tokens=result.telemetry.output_tokens,
            total_tokens=result.telemetry.total_tokens,
        )

        return GenerateBlueprintResponse(
            blueprint=result.blueprint,
            telemetry=telemetry,
        )


def create_application(
    generator: ProjectGeneratorInterface | None = None,
) -> Application:

    if generator is None:
        generator = ProjectGenerator()

    service = ProjectBlueprintService(generator)

    return Application(service)