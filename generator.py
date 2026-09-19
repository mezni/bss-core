from langchain_openai import ChatOpenAI

from config import load_llm_config, load_settings
from prompts import SYSTEM_PROMPT, build_user_prompt
from schemas import ProjectBlueprint


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
        project_idea = project_idea.strip()

        if not project_idea:
            raise ValueError("Project idea cannot be empty.")

        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", build_user_prompt(project_idea)),
        ]

        return self.structured_llm.invoke(messages)