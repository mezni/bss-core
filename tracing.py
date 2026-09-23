from dataclasses import dataclass
import time

from context import RequestContext
from telemetry import TelemetryEvent
from interfaces import TelemetryRecorderInterface


@dataclass
class Span:
    context: RequestContext
    recorder: TelemetryRecorderInterface
    event_type: str
    operation: str
    span_id: str
    start_time: float

    @classmethod
    def start(
        cls,
        context: RequestContext,
        recorder: TelemetryRecorderInterface,
        event_type: str,
        operation: str,
    ) -> "Span":
        return cls(
            context=context,
            recorder=recorder,
            event_type=event_type,
            operation=operation,
            span_id=context.create_span_id(),
            start_time=time.perf_counter(),
        )

    @property
    def latency_seconds(self) -> float:
        return time.perf_counter() - self.start_time

    def finish(
        self,
        *,
        status: str,
        model: str | None = None,
        prompt_version: str | None = None,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        total_tokens: int | None = None,
        input_cost: float | None = None,
        output_cost: float | None = None,
        total_cost: float | None = None,
        error_type: str | None = None,
    ) -> None:
        latency = self.latency_seconds

        event = TelemetryEvent(
            request_id=self.context.request_id,
            trace_id=self.context.trace_id,
            span_id=self.span_id,
            event_type=self.event_type,
            operation=self.operation,
            status=status,
            latency_seconds=latency,
            model=model,
            prompt_version=prompt_version,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            total_cost=total_cost,
            error_type=error_type,
        )

        self.recorder.record(event)