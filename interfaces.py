from abc import ABC, abstractmethod

from context import RequestContext
from schemas import ProjectBlueprint
from telemetry import GenerationEvent, GenerationResult


class ProjectGeneratorInterface(ABC):

    @abstractmethod
    def generate(
        self,
        project_idea: str,
        context: RequestContext,
    ) -> GenerationResult:
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


class TelemetryRecorderInterface(ABC):

    @abstractmethod
    def record(
        self,
        event: GenerationEvent,
    ) -> None:
        """Record an observability event."""
        raise NotImplementedError