from telemetry import GenerationEvent


class InMemoryTelemetryRecorder:

    def __init__(self) -> None:
        self.events: list[GenerationEvent] = []

    def record(
        self,
        event: GenerationEvent,
    ) -> None:
        self.events.append(event)