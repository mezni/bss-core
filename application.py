from generator import ProjectGenerator
from interfaces import ProjectGeneratorInterface
from service import ProjectBlueprintService


class Application:
    def __init__(
        self,
        blueprint_service: ProjectBlueprintService,
    ) -> None:
        self.blueprint_service = blueprint_service

    def generate_blueprint(self, project_idea: str):
        return self.blueprint_service.generate_blueprint(
            project_idea
        )


def create_application(
    generator: ProjectGeneratorInterface | None = None,
) -> Application:
    if generator is None:
        generator = ProjectGenerator()

    service = ProjectBlueprintService(generator)

    return Application(service)