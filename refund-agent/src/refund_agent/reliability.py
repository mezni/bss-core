import logging
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


def retry_call(
    operation: Callable[[], T],
    *,
    attempts: int = 3,
    delay_seconds: float = 0.5,
    retryable_exceptions: tuple[type[Exception], ...] = (TimeoutError,),
) -> T:
    """Retry an operation for explicitly configured transient errors."""

    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    if delay_seconds < 0:
        raise ValueError("delay_seconds cannot be negative")

    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except retryable_exceptions:
            if attempt == attempts:
                logger.exception(
                    "operation_failed",
                    extra={
                        "attempt": attempt,
                        "max_attempts": attempts,
                    },
                )
                raise

            logger.warning(
                "operation_retry",
                extra={
                    "attempt": attempt,
                    "max_attempts": attempts,
                },
            )
            time.sleep(delay_seconds)

    raise RuntimeError("Unreachable retry state")
