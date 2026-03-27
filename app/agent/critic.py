"""Critic interfaces."""

from __future__ import annotations

from app.agent.models import CriticResult, PlannerOutput
from app.browser.snapshot import PageSnapshot
from app.memory.state import AgentState
from app.tools.base import ToolResult


class Critic:
    """Evaluate whether an executed action achieved progress."""

    def assess(
        self,
        state: AgentState,
        plan: PlannerOutput,
        result: ToolResult,
        snapshot: PageSnapshot,
    ) -> CriticResult:
        raise NotImplementedError


class SimpleCritic(Critic):
    """Basic progress checker placeholder."""

    def assess(
        self,
        state: AgentState,
        plan: PlannerOutput,
        result: ToolResult,
        snapshot: PageSnapshot,
    ) -> CriticResult:
        if not result.success:
            return CriticResult(action_succeeded=False, should_replan=True, message=result.message)

        is_terminal = plan.action_name == "extract_text"
        return CriticResult(
            action_succeeded=True,
            should_replan=not is_terminal,
            is_terminal=is_terminal,
            message="Action accepted by placeholder critic.",
        )

