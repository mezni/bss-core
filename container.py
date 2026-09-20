from config import LLMConfig, Settings
from generator import ProjectGenerator
from interfaces import (
    ProjectGeneratorInterface,
    PromptManagerInterface,
    StructuredLLMInterface,
)
from prompt_manager import PromptManager
from service import ProjectBlueprintService
from structured_llm import LangChainStructuredLLM


class DependencyContainer:

    def __init__(
        self,
        settings: Settings,
        llm_config: LLMConfig,
    ) -> None:

        self.settings = settings
        self.llm_config = llm_config

    def create_prompt_manager(
        self,
    ) -> PromptManagerInterface:

        return PromptManager()

    def create_structured_llm(
        self,
    ) -> StructuredLLMInterface:

        return LangChainStructuredLLM(
            config=self.llm_config,
            settings=self.settings,
        )

    def create_generator(
        self,
        llm: StructuredLLMInterface,
        prompt_manager: PromptManagerInterface,
    ) -> ProjectGeneratorInterface:

        return ProjectGenerator(
            llm=llm,
            prompt_manager=prompt_manager,
        )

    def create_service(
        self,
        generator: ProjectGeneratorInterface,
    ) -> ProjectBlueprintService:

        return ProjectBlueprintService(
            generator
        )