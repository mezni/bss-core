
import hmac
from enum import StrEnum
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from refund_agent.config import get_settings


class Role(StrEnum):
    CUSTOMER_SERVICE = "customer_service"
    REFUND_REVIEWER = "refund_reviewer"
    ADMIN = "admin"


role_api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def get_current_role(
    api_key: Annotated[
        str | None,
        Security(role_api_key_header),
    ],
) -> Role:
    settings = get_settings()

    role_keys = {
        Role.CUSTOMER_SERVICE: settings.customer_service_api_key,
        Role.REFUND_REVIEWER: settings.refund_reviewer_api_key,
        Role.ADMIN: settings.admin_api_key,
    }

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key.",
        )

    for role, secret in role_keys.items():
        if secret and hmac.compare_digest(
            api_key,
            secret.get_secret_value(),
        ):
            return role

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key.",
    )


def require_roles(*allowed_roles: Role):
    def dependency(
        current_role: Annotated[Role, Depends(get_current_role)],
    ) -> Role:
        if current_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action.",
            )

        return current_role

    return dependency
