from dataclasses import dataclass

from schemas import ProjectBlueprint


@dataclass
class GenerationTelemetry:
    request_id: str
    model: str
    prompt_version: str
    latency_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass
class GenerationResult:
    blueprint: ProjectBlueprint
    telemetry: GenerationTelemetry