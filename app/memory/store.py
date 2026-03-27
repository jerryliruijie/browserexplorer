"""State update helpers."""

from __future__ import annotations

from app.agent.models import CriticResult
from app.browser.snapshot import PageSnapshot
from app.memory.history import ActionRecord
from app.memory.state import AgentState
from app.tools.base import ToolResult


class StateStore:
    """Centralized state transitions."""

    def initialize(self, task: str, max_steps: int = 12) -> AgentState:
        return AgentState(task_input=task, max_steps=max_steps)

    def attach_snapshot(self, state: AgentState, snapshot: PageSnapshot) -> None:
        state.latest_snapshot = snapshot
        state.current_url = snapshot.url
        state.page_summary = snapshot.summary
        if snapshot.url and snapshot.url not in state.visited_urls:
            state.visited_urls.append(snapshot.url)

    def record_action(self, state: AgentState, record: ActionRecord) -> None:
        state.step_count = record.step
        state.action_history.append(record)

    def merge_tool_data(self, state: AgentState, result: ToolResult) -> None:
        if result.data:
            state.extracted_data.update(result.data)

    def apply_review(self, state: AgentState, review: CriticResult, snapshot: PageSnapshot) -> None:
        self.attach_snapshot(state, snapshot)
        if review.is_terminal:
            state.done = True
            state.final_report = self.build_report(state)

    @staticmethod
    def build_report(state: AgentState) -> str:
        return (
            f"Task: {state.task_input}\n"
            f"Visited URLs: {len(state.visited_urls)}\n"
            f"Actions: {len(state.action_history)}\n"
            f"Extracted keys: {sorted(state.extracted_data.keys())}"
        )
