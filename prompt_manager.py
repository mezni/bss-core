from prompts import SYSTEM_PROMPT, build_user_prompt


class PromptManager:
    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def build_user_prompt(self, project_idea: str) -> str:
        return build_user_prompt(project_idea)