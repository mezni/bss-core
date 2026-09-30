from dataclasses import dataclass

from failure import Failure


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")

    def should_retry(
        self,
        failure: Failure,
        attempt: int,
    ) -> bool:
        if attempt < 1:
            raise ValueError("attempt must be at least 1.")

        if not failure.retryable:
            return False

        return attempt < self.max_attempts
