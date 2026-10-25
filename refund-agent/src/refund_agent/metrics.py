from collections import Counter
from threading import Lock
from time import perf_counter
from typing import Any

from refund_agent.models import RefundStatus


class AgentMetrics:
    def __init__(self) -> None:
        self._lock = Lock()
        self._requests = 0
        self._errors = 0
        self._outcomes: Counter[str] = Counter()
        self._latencies_ms: list[float] = []

    def record_request(self, duration_ms: float) -> None:
        with self._lock:
            self._requests += 1
            self._latencies_ms.append(max(0.0, duration_ms))

    def record_outcome(self, status: RefundStatus) -> None:
        with self._lock:
            self._outcomes[status.value] += 1

    def record_error(self) -> None:
        with self._lock:
            self._errors += 1

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            latencies = sorted(self._latencies_ms)
            count = len(latencies)

            p95_index = max(0, int(count * 0.95) - 1)
            p95_latency = latencies[p95_index] if count else 0.0

            return {
                "requests_total": self._requests,
                "errors_total": self._errors,
                "outcomes": dict(self._outcomes),
                "latency_ms": {
                    "count": count,
                    "average": (sum(latencies) / count if count else 0.0),
                    "p95": p95_latency,
                },
            }


agent_metrics = AgentMetrics()


def elapsed_ms(start: float) -> float:
    return round((perf_counter() - start) * 1000, 2)
