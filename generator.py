import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from prompts import SYSTEM_PROMPT, build_user_prompt

# Ensure load_dotenv() runs before accessing os.getenv
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key missing. Ensure OPENROUTER_API_KEY is set in your .env file.")


class ProjectGenerator:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            temperature=0.2,
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key),
        )

    def generate(self, project_idea: str) -> str:
        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", build_user_prompt(project_idea)),
        ]
        response = self.llm.invoke(messages)
        return response.content