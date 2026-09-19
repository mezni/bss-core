import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from schemas import ProjectBlueprint

from config import load_llm_config
from prompts import SYSTEM_PROMPT, build_user_prompt

# Ensure load_dotenv() runs before accessing os.getenv
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key missing. Ensure OPENROUTER_API_KEY is set in your .env file.")


class ProjectGenerator:
    def __init__(self) -> None:
        config = load_llm_config()
        
        self.llm = ChatOpenAI(
            model=config["model"],
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            base_url=config["base_url"],
            api_key=SecretStr(api_key),
        )

        self.structured_llm = self.llm.with_structured_output(
            ProjectBlueprint
        )

    def generate(self, project_idea: str) -> ProjectBlueprint:
        project_idea = project_idea.strip()

        if not project_idea:
            raise ValueError("Project idea cannot be empty.")

        messages = [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            (
                "human",
                build_user_prompt(project_idea),
            ),
        ]

        return self.structured_llm.invoke(messages)