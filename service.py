from interfaces import ProjectGeneratorInterface
from telemetry import GenerationResult
from tracing import TraceContext


class ProjectBlueprintService:

    def __init__(
        self,
        generator: ProjectGeneratorInterface,
    ) -> None:

        self.generator = generator

    def generate_blueprint(
        self,
        project_idea: str,
        trace: TraceContext,
    ) -> GenerationResult:

        return self.generator.generate(
            project_idea,
            trace,
        )
