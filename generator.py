import logging
import uuid

from langchain_openai import ChatOpenAI

from config import load_llm_config, load_settings
from exceptions import ProjectGenerationError
from prompts import SYSTEM_PROMPT, build_user_prompt
from schemas import ProjectBlueprint


logger = logging.getLogger(__name__)


class ProjectGenerator:
    def __init__(self) -> None:
        settings = load_settings()
        config = load_llm_config()

        self.llm = ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            base_url=config.base_url,
            api_key=settings.openrouter_api_key,
        )

        self.structured_llm = self.llm.with_structured_output(
            ProjectBlueprint
        )

    def generate(self, project_idea: str) -> ProjectBlueprint:
        request_id = str(uuid.uuid4())

        logger.info(
            "Starting project generation | request_id=%s",
            request_id,
        )

        project_idea = project_idea.strip()

        if not project_idea:
            logger.warning(
                "Empty project idea | request_id=%s",
                request_id,
            )
            raise ValueError("Project idea cannot be empty.")

        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", build_user_prompt(project_idea)),
        ]

        try:
            logger.info(
                "Calling LLM | request_id=%s",
                request_id,
            )

            blueprint = self.structured_llm.invoke(messages)

            logger.info(
                "Project generation completed | request_id=%s",
                request_id,
            )

            return blueprint

        except Exception as exc:
            logger.exception(
                "Project generation failed | request_id=%s",
                request_id,
            )

            raise ProjectGenerationError(
                "Failed to generate the project blueprint."
            ) from exc