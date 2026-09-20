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


class PromptManagerInterface(ABC):

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt."""
        raise NotImplementedError

    @abstractmethod
    def build_user_prompt(
        self,
        project_idea: str,
    ) -> str:
        """Build the user prompt."""
        raise NotImplementedError

    @abstractmethod
    def get_version(self) -> str:
        """Return the active prompt version."""
        raise NotImplementedError