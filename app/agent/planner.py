"""Planner interfaces."""

from __future__ import annotations

from app.agent.models import PlannerOutput
from app.browser.snapshot import PageSnapshot
from app.memory.state import AgentState


class Planner:
    """Planner abstraction for structured action selection."""

    def plan(self, state: AgentState, snapshot: PageSnapshot) -> PlannerOutput:
        raise NotImplementedError


class HeuristicPlanner(Planner):
    """Minimal placeholder planner for the MVP scaffold."""

    def plan(self, state: AgentState, snapshot: PageSnapshot) -> PlannerOutput:
        if not state.current_url:
            return PlannerOutput(
                thought="Need an initial page before browsing.",
                action_name="open_url",
                action_args={"url": state.task_input},
                expected_outcome="The browser opens the requested page.",
            )

        return PlannerOutput(
            thought="Capture visible content for the report.",
            action_name="extract_text",
            action_args={},
            expected_outcome="Structured visible text is extracted from the current page.",
        )

