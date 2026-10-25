
import json
import logging
import time
from contextvars import ContextVar
from datetime import UTC, datetime
from uuid import uuid4

request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)

logger = logging.getLogger("refund_agent")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        event = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_context.get(),
        }

        for field in (
            "order_id",
            "status",
            "duration_ms",
            "error_type",
        ):
            value = getattr(record, field, None)
            if value is not None:
                event[field] = value

        if record.exc_info:
            event["exception_type"] = record.exc_info[0].__name__

        return json.dumps(event)


def configure_observability(
    level: int = logging.INFO,
) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def new_request_id() -> str:
    return str(uuid4())


def log_refund_event(
    event: str,
    *,
    order_id: str | None = None,
    status: str | None = None,
    duration_ms: float | None = None,
    error_type: str | None = None,
) -> None:
    logger.info(
        event,
        extra={
            "order_id": order_id,
            "status": status,
            "duration_ms": duration_ms,
            "error_type": error_type,
        },
    )


def elapsed_milliseconds(start: float) -> float:
    return round((time.perf_counter() - start) * 1000, 2)
