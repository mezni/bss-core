from dataclasses import dataclass


@dataclass
class GenerationTelemetry:
    request_id: str
    model: str
    latency_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None