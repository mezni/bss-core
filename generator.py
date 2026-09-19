import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts import SYSTEM_PROMPT, build_user_prompt


load_dotenv()


class ProjectGenerator:
    def __init__(self) -> None:
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not configured.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def generate(self, project_idea: str) -> str:
        response = self.client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": build_user_prompt(project_idea),
                },
            ],
        )

        return response.choices[0].message.content or ""