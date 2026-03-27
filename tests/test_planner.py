from app.agent.planner import HeuristicPlanner
from app.browser.snapshot import PageSnapshot
from app.memory.state import AgentState


def test_planner_opens_initial_url_when_state_is_empty() -> None:
    planner = HeuristicPlanner()
    state = AgentState(task_input="https://example.com")
    snapshot = PageSnapshot(url="", title="", summary="")

    plan = planner.plan(state, snapshot)

    assert plan.action_name == "open_url"
    assert plan.action_args["url"] == "https://example.com"

