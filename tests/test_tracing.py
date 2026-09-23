from context import RequestContext
from telemetry_recorder import InMemoryTelemetryRecorder
from tracing import Span


def test_span_records_success_event():
    context = RequestContext.create()
    recorder = InMemoryTelemetryRecorder()

    span = Span.start(
        context=context,
        recorder=recorder,
        event_type="generation",
        operation="test_operation",
    )

    span.finish(
        status="success",
        model="fake-model",
    )

    assert len(recorder.events) == 1

    event = recorder.events[0]

    assert event.request_id == context.request_id
    assert event.trace_id == context.trace_id
    assert event.span_id
    assert event.event_type == "generation"
    assert event.operation == "test_operation"
    assert event.status == "success"
    assert event.model == "fake-model"
    assert event.latency_seconds >= 0


def test_span_records_error_event():
    context = RequestContext.create()
    recorder = InMemoryTelemetryRecorder()

    span = Span.start(
        context=context,
        recorder=recorder,
        event_type="generation",
        operation="test_operation",
    )

    span.finish(
        status="error",
        error_type="TimeoutError",
    )

    event = recorder.events[0]

    assert event.status == "error"
    assert event.error_type == "TimeoutError"
    assert event.latency_seconds >= 0