from context import RequestContext
from service import ProjectBlueprintService
from telemetry_recorder import InMemoryTelemetryRecorder
from tests.fakes import FakeProjectGenerator
from tracing import TraceContext


def test_service_generates_blueprint() -> None:
    generator = FakeProjectGenerator()
    service = ProjectBlueprintService(generator)

    context = RequestContext.create()

    trace = TraceContext(
        context=context,
        recorder=InMemoryTelemetryRecorder(),
    )

    result = service.generate_blueprint(
        "Build an AI document classifier.",
        trace,
    )

    assert result.blueprint.project_name == "Test Project"
    assert result.blueprint.business_outcome == "Test business outcome."
    assert result.telemetry.request_id == context.request_id
