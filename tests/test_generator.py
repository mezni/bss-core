from generator import ProjectGenerator
from prompt_manager import PromptManager
from tests.fakes import FakeLLM


def test_generator_uses_injected_llm() -> None:
    generator = ProjectGenerator(
        llm=FakeLLM(),
        prompt_manager=PromptManager(),
    )

    result = generator.generate(
        "Build an AI document classifier."
    )

    assert result.blueprint.project_name == "Test Project"
    assert (
        result.blueprint.business_outcome
        == "Test business outcome."
    )
    assert result.telemetry.model == "fake-model"
    assert result.telemetry.prompt_version == "v1"