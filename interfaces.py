from abc import ABC, abstractmethod

from telemetry import GenerationResult


class ProjectGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, project_idea: str) -> GenerationResult:
        """Generate a project blueprint."""
        raise NotImplementedError


class LLMInterface(ABC):
    @abstractmethod
    def invoke(self, messages):
        """Invoke the language model."""
        raise NotImplementedError