"""Agent orchestration loop."""

from __future__ import annotations

from app.agent.critic import Critic, SimpleCritic
from app.agent.planner import HeuristicPlanner, Planner
from app.browser.observer import BrowserObserver
from app.browser.runtime import BrowserRuntime
from app.memory.state import ActionRecord, AgentState
from app.memory.store import StateStore
from app.tools.registry import ToolRegistry


class AgentOrchestrator:
    """Coordinates observe -> plan -> act -> reflect."""

    def __init__(
        self,
        runtime: BrowserRuntime,
        observer: BrowserObserver,
        registry: ToolRegistry,
        store: StateStore,
        planner: Planner | None = None,
        critic: Critic | None = None,
    ) -> None:
        self.runtime = runtime
        self.observer = observer
        self.registry = registry
        self.store = store
        self.planner = planner or HeuristicPlanner()
        self.critic = critic or SimpleCritic()

    def run(self, task: str) -> AgentState:
        state = self.store.initialize(task=task)

        while not state.done and state.step_count < state.max_steps:
            snapshot = self.observer.observe(self.runtime)
            self.store.attach_snapshot(state, snapshot)

            plan = self.planner.plan(state, snapshot)
            result = self.registry.execute(plan.action_name, self.runtime, **plan.action_args)

            new_snapshot = self.observer.observe(self.runtime)
            review = self.critic.assess(state, plan, result, new_snapshot)

            self.store.record_action(
                state,
                ActionRecord(
                    step=state.step_count + 1,
                    action_name=plan.action_name,
                    action_args=plan.action_args,
                    before_url=snapshot.url,
                    after_url=new_snapshot.url,
                    success=result.success,
                    error=result.error,
                    message=review.message,
                ),
            )
            self.store.merge_tool_data(state, result)
            self.store.apply_review(state, review, new_snapshot)

        return state
