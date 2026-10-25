
import pytest
from fastapi import HTTPException

from refund_agent.authorization import Role, get_current_role, require_roles


def test_unknown_api_key_is_rejected(monkeypatch):
    from refund_agent.config import get_settings

    monkeypatch.setenv("REFUND_AGENT_CUSTOMER_API_KEY", "customer-test")
    monkeypatch.setenv("REFUND_AGENT_REVIEWER_API_KEY", "reviewer-test")
    monkeypatch.setenv("REFUND_AGENT_ADMIN_API_KEY", "admin-test")
    get_settings.cache_clear()

    try:
        with pytest.raises(HTTPException) as error:
            get_current_role("invalid-key")

        assert error.value.status_code == 401
    finally:
        get_settings.cache_clear()


def test_reviewer_key_resolves_to_reviewer_role(monkeypatch):
    from refund_agent.config import get_settings

    monkeypatch.setenv("REFUND_AGENT_CUSTOMER_API_KEY", "customer-test")
    monkeypatch.setenv("REFUND_AGENT_REVIEWER_API_KEY", "reviewer-test")
    monkeypatch.setenv("REFUND_AGENT_ADMIN_API_KEY", "admin-test")
    get_settings.cache_clear()

    try:
        assert get_current_role("reviewer-test") == Role.REFUND_REVIEWER
    finally:
        get_settings.cache_clear()


def test_customer_cannot_access_reviewer_action():
    dependency = require_roles(Role.REFUND_REVIEWER)

    with pytest.raises(HTTPException) as error:
        dependency(Role.CUSTOMER_SERVICE)

    assert error.value.status_code == 403


def test_admin_can_access_reviewer_action():
    dependency = require_roles(Role.REFUND_REVIEWER, Role.ADMIN)

    assert dependency(Role.ADMIN) == Role.ADMIN
