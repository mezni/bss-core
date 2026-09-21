from telemetry import GenerationEvent


def test_generation_event_contains_observability_data():
    event = GenerationEvent(
        request_id="request-123",
        operation="project_blueprint_generation",
        model="fake-model",
        prompt_version="v1",
        status="success",
        latency_seconds=0.42,
        input_tokens=100,
        output_tokens=50,
        total_tokens=150,
    )

    assert event.request_id == "request-123"
    assert event.operation == "project_blueprint_generation"
    assert event.model == "fake-model"
    assert event.prompt_version == "v1"
    assert event.status == "success"
    assert event.latency_seconds == 0.42
    assert event.total_tokens == 150


def test_generation_event_can_represent_failure():
    event = GenerationEvent(
        request_id="request-456",
        operation="project_blueprint_generation",
        model="fake-model",
        prompt_version="v1",
        status="error",
        latency_seconds=0.25,
        error_type="ProjectGenerationError",
    )

    assert event.status == "error"
    assert event.error_type == "ProjectGenerationError"