from abc import ABC, abstractmethod

from schemas import ProjectBlueprint
from telemetry import GenerationResult


class ProjectGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, project_idea: str) -> GenerationResult:
        """Generate a project blueprint."""
        raise NotImplementedError


class StructuredLLMInterface(ABC):
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the configured model name."""
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        messages: list[tuple[str, str]],
    ) -> ProjectBlueprint:
        """Generate a structured project blueprint."""
        raise NotImplementedError