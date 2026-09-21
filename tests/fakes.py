from context import RequestContext
from interfaces import (
    LLMUsage,
    ProjectGeneratorInterface,
    PromptManagerInterface,
)
from schemas import ProjectBlueprint
from telemetry import GenerationResult, GenerationTelemetry


class FakeProjectGenerator(ProjectGeneratorInterface):

    def generate(
        self,
        project_idea: str,
        context: RequestContext,
    ) -> GenerationResult:

        return GenerationResult(
            blueprint=ProjectBlueprint(
                project_name="Test Project",
                business_outcome=(
                    "Test business outcome."
                ),
            ),
            telemetry=GenerationTelemetry(
                request_id=context.request_id,
                model="fake-model",
                prompt_version="test-v1",
                latency_seconds=0.01,
            ),
        )


class FakeLLM:

    @property
    def model_name(self) -> str:
        return "fake-model"

    def generate(self, messages):
        return (
            ProjectBlueprint(
                project_name="Test Project",
                business_outcome="Test business outcome.",
            ),
            LLMUsage(
                input_tokens=100,
                output_tokens=50,
                total_tokens=150,
            ),
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