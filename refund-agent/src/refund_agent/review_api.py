
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from refund_agent.approval import resolve_human_review
from refund_agent.authorization import Role, require_roles
from refund_agent.models import RefundDecision

router = APIRouter(prefix="/reviews", tags=["reviews"])


class ReviewRequest(BaseModel):
    decision: RefundDecision
    approved: bool
    reason: str = Field(min_length=5, max_length=1000)


class ReviewResponse(BaseModel):
    decision: RefundDecision


@router.post("/{review_id}")
def review_refund(
    review_id: str,
    payload: ReviewRequest,
    reviewer_role: Annotated[
        Role,
        Depends(require_roles(Role.REFUND_REVIEWER, Role.ADMIN)),
    ],
) -> ReviewResponse:
    # Use the authenticated role as part of the audit identity.
    # Replace this with a verified reviewer identity when a real
    # identity provider is introduced.
    reviewer_id = f"{reviewer_role.value}:{review_id}"

    decision = resolve_human_review(
        decision=payload.decision,
        reviewer_id=reviewer_id,
        approved=payload.approved,
        reason=payload.reason,
    )

    return ReviewResponse(decision=decision)
