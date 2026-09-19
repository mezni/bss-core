from abc import ABC, abstractmethod

from telemetry import GenerationResult


class ProjectGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, project_idea: str) -> GenerationResult:
        """Generate a project blueprint."""
        raise NotImplementedError