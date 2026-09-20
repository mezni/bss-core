from application import create_application
from config import LLMConfig, Settings
from container import DependencyContainer
from schemas import GenerateBlueprintRequest
from tests.fakes import FakeProjectGenerator


def test_create_application_with_custom_generator() -> None:
    container = DependencyContainer(
        settings=Settings(
            openrouter_api_key="test-key",
        ),
        llm_config=LLMConfig(
            provider="openrouter",
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4o-mini",
            temperature=0.2,
            max_tokens=1000,
        ),
    )

    application = create_application(
        generator=FakeProjectGenerator(),
        container=container,
    )

    request = GenerateBlueprintRequest(
        project_idea="Build an AI document classifier."
    )

    result = application.generate_blueprint(request)

    assert result.blueprint.project_name == "Test Project"
    assert result.telemetry.request_id
    assert len(result.telemetry.request_id) == 36
    assert result.telemetry.model == "fake-model"
    assert result.telemetry.prompt_version == "test-v1"