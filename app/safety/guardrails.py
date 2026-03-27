"""Guardrail helpers for tool execution."""

from __future__ import annotations

from app.tools.base import BaseTool, ToolResult


def allow_tool(tool: BaseTool, allow_high_risk_actions: bool = False) -> ToolResult | None:
    """Return a denial result when the tool should not execute."""
    if tool.high_risk and not allow_high_risk_actions:
        return ToolResult(
            success=False,
            message="Blocked by safety policy.",
            error="high-risk-action-denied",
        )
    return None
