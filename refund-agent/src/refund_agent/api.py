
from fastapi import FastAPI
from pydantic import BaseModel, Field

from refund_agent.agent import handle_customer_message
from refund_agent.health import liveness_check, readiness_check
from refund_agent.metrics import agent_metrics
from refund_agent.models import RefundDecision


app = FastAPI(
    title="Refund Agent API",
    version="0.1.0",
    description="API for processing and evaluating refund requests.",
)


class RefundMessage(BaseModel):
    customer_message: str = Field(
        min_length=1,
        max_length=5000,
        description="The customer's message about their refund request.",
    )


class RefundResponse(BaseModel):
    decision: RefundDecision
    customer_response: str


@app.get("/health/live")
def health_live() -> dict[str, str]:
    return liveness_check()


@app.get("/health/ready")
def health_ready() -> dict[str, str]:
    return readiness_check()


@app.get("/metrics")
def get_metrics() -> dict:
    return agent_metrics.snapshot()


@app.post("/refunds", response_model=RefundResponse)
def create_refund(
    request: RefundMessage,
) -> RefundResponse:
    decision, customer_response = handle_customer_message(
        customer_message=request.customer_message,
    )

    return RefundResponse(
        decision=decision,
        customer_response=customer_response,
    )
