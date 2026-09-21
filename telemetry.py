from dataclasses import dataclass

from schemas import ProjectBlueprint


@dataclass(frozen=True)
class GenerationTelemetry:
    request_id: str
    model: str
    prompt_version: str
    latency_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(frozen=True)
class GenerationEvent:
    request_id: str
    operation: str
    model: str
    prompt_version: str
    status: str
    latency_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    error_type: str | None = None


@dataclass(frozen=True)
class GenerationResult:
    blueprint: ProjectBlueprint
    telemetry: GenerationTelemetry