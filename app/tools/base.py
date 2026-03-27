"""Base tool interfaces."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.browser.runtime import BrowserRuntime


class ToolResult(BaseModel):
    """Unified tool execution result."""

    success: bool
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class BaseTool:
    """Controlled browser tool."""

    name: str = ""
    high_risk: bool = False

    def execute(self, runtime: BrowserRuntime, **kwargs: Any) -> ToolResult:
        raise NotImplementedError

