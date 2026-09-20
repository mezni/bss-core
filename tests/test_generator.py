from generator import ProjectGenerator
from tests.fakes import FakeLLM, FakePromptManager


def test_generator_uses_injected_dependencies() -> None:
    generator = ProjectGenerator(
        llm=FakeLLM(),
        prompt_manager=FakePromptManager(),
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

    assert (
        result.telemetry.prompt_version
        == "test-v1"
    )