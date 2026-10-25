
from typing import Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from refund_agent.agent import handle_customer_message
from refund_agent.health import liveness_check, readiness_check
from refund_agent.metrics import agent_metrics
from refund_agent.models import RefundDecision
from refund_agent.security import require_api_key

app = FastAPI(
    title="Refund Agent API",
    version="0.1.0",
    description="API for processing and evaluating refund requests.",
)


class RefundMessage(BaseModel):
    customer_message: str = Field(
        min_length=1,
        max_length=5000,
        description="The customer's refund-related message.",
    )


class RefundResponse(BaseModel):
    decision: RefundDecision
    customer_response: str


@app.get("/health/live")
def health_live() -> dict[str, str]:
    # Public liveness check for infrastructure monitoring.
    return liveness_check()


@app.get(
    "/health/ready",
    dependencies=[Depends(require_api_key)],
)
def health_ready() -> dict[str, str]:
    return readiness_check()


@app.get(
    "/metrics",
    dependencies=[Depends(require_api_key)],
)
def get_metrics() -> dict[str, Any]:
    return agent_metrics.snapshot()


@app.post(
    "/refunds",
    response_model=RefundResponse,
    dependencies=[Depends(require_api_key)],
)
def create_refund(request: RefundMessage) -> RefundResponse:
    decision, customer_response = handle_customer_message(
        customer_message=request.customer_message,
    )

    return RefundResponse(
        decision=decision,
        customer_response=customer_response,
    )
