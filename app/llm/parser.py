"""Helpers for structured output parsing."""

from __future__ import annotations

import json

from app.llm.schemas import PlannerResponse


def parse_planner_response(raw_text: str) -> PlannerResponse:
    """Parse a JSON planner response."""
    payload = json.loads(raw_text)
    return PlannerResponse.model_validate(payload)

