"""Action history models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ActionRecord(BaseModel):
    """Audit record for one tool execution."""

    step: int
    action_name: str
    action_args: dict[str, Any] = Field(default_factory=dict)
    before_url: str = ""
    after_url: str = ""
    success: bool
    error: str | None = None
    message: str = ""

