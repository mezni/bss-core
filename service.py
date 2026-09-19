from generator import ProjectGenerator
from telemetry import GenerationResult


class ProjectBlueprintService:
    def __init__(self, generator: ProjectGenerator) -> None:
        self.generator = generator

    def generate_blueprint(
        self,
        project_idea: str,
    ) -> GenerationResult:
        return self.generator.generate(project_idea)