from langchain_openai import ChatOpenAI

from config import LLMConfig, Settings
from interfaces import StructuredLLMInterface
from schemas import ProjectBlueprint


class LangChainStructuredLLM(StructuredLLMInterface):
    def __init__(
        self,
        config: LLMConfig,
        settings: Settings,
    ) -> None:

        self._model_name = config.model

        llm = ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            base_url=config.base_url,
            api_key=settings.openrouter_api_key,
        )

        self.llm = llm.with_structured_output(
            ProjectBlueprint
        )

    @property
    def model_name(self) -> str:
        return self._model_name

    def generate(
        self,
        messages: list[tuple[str, str]],
    ) -> ProjectBlueprint:

        return self.llm.invoke(messages)