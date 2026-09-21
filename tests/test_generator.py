from context import RequestContext
from generator import ProjectGenerator
from telemetry_recorder import InMemoryTelemetryRecorder
from tests.fakes import FakeLLM, FakePromptManager


def test_generator_uses_injected_dependencies() -> None:
    recorder = InMemoryTelemetryRecorder()

    generator = ProjectGenerator(
        llm=FakeLLM(),
        prompt_manager=FakePromptManager(),
        telemetry_recorder=recorder,
    )

    context = RequestContext.create()

    result = generator.generate(
        "Build an AI document classifier.",
        context,
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

    assert result.telemetry.input_tokens == 100
    assert result.telemetry.output_tokens == 50
    assert result.telemetry.total_tokens == 150

    assert len(recorder.events) == 1

    event = recorder.events[0]

    assert event.request_id == context.request_id
    assert event.operation == "project_blueprint_generation"
    assert event.status == "success"
    assert event.model == "fake-model"
    assert event.prompt_version == "test-v1"
    assert event.input_tokens == 100
    assert event.output_tokens == 50
    assert event.total_tokens == 150