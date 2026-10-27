from dataclasses import dataclass


@dataclass(frozen=True)
class AgentContext:
    """Trusted, per-request data. Set by your API from the authenticated
    session. The model never sees or controls it."""

    customer_id: str
