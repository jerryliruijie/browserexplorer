"""Structured LLM request and response schemas."""

from __future__ import annotations

from pydantic import BaseModel

from app.agent.models import PlannerOutput


class PlannerRequest(BaseModel):
    """Input payload for planner-style model calls."""

    task: str
    current_url: str
    snapshot_summary: str


class PlannerResponse(BaseModel):
    """Validated planner response."""

    decision: PlannerOutput

