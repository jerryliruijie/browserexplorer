"""Structured models for agent decisions."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    """Planner decision for the next controlled action."""

    thought: str
    action_name: str
    action_args: dict[str, Any] = Field(default_factory=dict)
    expected_outcome: str


class CriticResult(BaseModel):
    """Post-action evaluation output."""

    action_succeeded: bool
    should_replan: bool = False
    is_terminal: bool = False
    message: str = ""

