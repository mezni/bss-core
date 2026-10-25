
import hmac

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from refund_agent.config import get_settings

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def require_api_key(
    api_key: str | None = Security(api_key_header),
) -> None:
    settings = get_settings()
    configured_secret = settings.refund_agent_api_key

    if configured_secret is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API authentication is not configured.",
        )

    expected_key = configured_secret.get_secret_value()

    if api_key is None or not hmac.compare_digest(
        api_key,
        expected_key,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
