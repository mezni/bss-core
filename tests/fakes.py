from interfaces import PromptManagerInterface
from schemas import ProjectBlueprint


class FakeLLM:

    @property
    def model_name(self) -> str:
        return "fake-model"

    def generate(self, messages):
        return ProjectBlueprint(
            project_name="Test Project",
            business_outcome="Test business outcome.",
        )


class FakePromptManager(PromptManagerInterface):

    def get_system_prompt(self) -> str:
        return "Fake system prompt."

    def build_user_prompt(
        self,
        project_idea: str,
    ) -> str:
        return f"Fake prompt: {project_idea}"

    def get_version(self) -> str:
        return "test-v1"