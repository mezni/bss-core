import pytest

from errors import ErrorCategories
from failure import Failure
from retry import RetryPolicy


def test_max_attempts_must_be_at_least_one():
    with pytest.raises(ValueError):
        RetryPolicy(max_attempts=0)


def test_non_retryable_failure_is_not_retried():
    policy = RetryPolicy(max_attempts=3)

    failure = Failure(
        error_type="ValueError",
        category=ErrorCategories.VALIDATION,
        message="Invalid project idea.",
        retryable=False,
    )

    assert policy.should_retry(failure, attempt=1) is False


def test_retryable_failure_is_retried():
    policy = RetryPolicy(max_attempts=3)

    failure = Failure(
        error_type="TimeoutError",
        category=ErrorCategories.TIMEOUT,
        message="LLM request timed out.",
        retryable=True,
    )

    assert policy.should_retry(failure, attempt=1) is True
    assert policy.should_retry(failure, attempt=2) is True


def test_no_retry_after_max_attempts():
    policy = RetryPolicy(max_attempts=3)

    failure = Failure(
        error_type="TimeoutError",
        category=ErrorCategories.TIMEOUT,
        message="LLM request timed out.",
        retryable=True,
    )

    assert policy.should_retry(failure, attempt=3) is False


def test_attempt_must_be_at_least_one():
    policy = RetryPolicy()

    failure = Failure(
        error_type="TimeoutError",
        category=ErrorCategories.TIMEOUT,
        message="LLM request timed out.",
        retryable=True,
    )

    with pytest.raises(ValueError):
        policy.should_retry(failure, attempt=0)


def test_one_attempt_means_no_retry():
    policy = RetryPolicy(max_attempts=1)

    failure = Failure(
        error_type="TimeoutError",
        category=ErrorCategories.TIMEOUT,
        message="LLM request timed out.",
        retryable=True,
    )

    assert policy.should_retry(failure, attempt=1) is False
