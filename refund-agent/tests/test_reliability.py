import pytest

from refund_agent.reliability import retry_call


def test_retry_succeeds_after_transient_failure():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1

        if calls < 3:
            raise TimeoutError("Temporary timeout")

        return "success"

    result = retry_call(
        operation,
        attempts=3,
        delay_seconds=0,
        retryable_exceptions=(TimeoutError,),
    )

    assert result == "success"
    assert calls == 3


def test_retry_stops_after_maximum_attempts():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        raise TimeoutError("Still unavailable")

    with pytest.raises(TimeoutError):
        retry_call(
            operation,
            attempts=3,
            delay_seconds=0,
            retryable_exceptions=(TimeoutError,),
        )

    assert calls == 3


def test_non_retryable_exception_is_not_retried():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        raise ValueError("Invalid input")

    with pytest.raises(ValueError):
        retry_call(
            operation,
            attempts=3,
            delay_seconds=0,
            retryable_exceptions=(TimeoutError,),
        )

    assert calls == 1


def test_attempts_must_be_positive():
    with pytest.raises(ValueError, match="at least 1"):
        retry_call(lambda: "success", attempts=0)


def test_negative_delay_is_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        retry_call(lambda: "success", delay_seconds=-1)


def test_retry_call_raises_after_all_attempts():
    calls = 0

    def failing_operation():
        nonlocal calls
        calls += 1
        raise TimeoutError("Service timed out")

    with pytest.raises(TimeoutError):
        retry_call(
            failing_operation,
            attempts=3,
            delay_seconds=0,
        )

    assert calls == 3
