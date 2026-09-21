from telemetry import GenerationEvent
from telemetry_recorder import InMemoryTelemetryRecorder


def test_in_memory_recorder_stores_event():
    recorder = InMemoryTelemetryRecorder()

    event = GenerationEvent(
        request_id="request-123",
        operation="project_blueprint_generation",
        model="fake-model",
        prompt_version="v1",
        status="success",
        latency_seconds=0.5,
    )

    recorder.record(event)

    assert len(recorder.events) == 1
    assert recorder.events[0] == event