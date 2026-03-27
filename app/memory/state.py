"""Agent runtime state."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.browser.snapshot import PageSnapshot
from app.memory.history import ActionRecord


class AgentState(BaseModel):
    """Mutable state for a browser-agent run."""

    task_input: str
    step_count: int = 0
    max_steps: int = 12
    current_url: str = ""
    page_summary: str = ""
    visited_urls: list[str] = Field(default_factory=list)
    extracted_data: dict[str, Any] = Field(default_factory=dict)
    action_history: list[ActionRecord] = Field(default_factory=list)
    latest_snapshot: PageSnapshot | None = None
    done: bool = False
    final_report: str = ""

