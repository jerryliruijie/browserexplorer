from app.agent.critic import Critic, SimpleCritic
from app.agent.models import CriticResult, PlannerOutput
from app.agent.prompts import CRITIC_SYSTEM_PROMPT, PLANNER_SYSTEM_PROMPT
from app.agent.planner import HeuristicPlanner
from app.browser.snapshot import PageSnapshot
from app.memory.state import AgentState
from app.tools.base import ToolResult


def test_heuristic_planner_extracts_text_after_navigation() -> None:
    planner = HeuristicPlanner()
    state = AgentState(task_input="https://example.com", current_url="https://example.com")
    snapshot = PageSnapshot(url="https://example.com", title="Example", summary="loaded")

    plan = planner.plan(state, snapshot)

    assert plan.action_name == "extract_text"
    assert plan.action_args == {}


def test_simple_critic_requests_replan_on_failure() -> None:
    critic = SimpleCritic()
    result = critic.assess(
        state=AgentState(task_input="task"),
        plan=PlannerOutput(
            thought="try",
            action_name="open_url",
            action_args={},
            expected_outcome="open",
        ),
        result=ToolResult(success=False, message="boom", error="broken"),
        snapshot=PageSnapshot(url="", title="", summary=""),
    )

    assert result == CriticResult(action_succeeded=False, should_replan=True, message="boom")


def test_simple_critic_marks_extract_text_as_terminal() -> None:
    critic = SimpleCritic()
    result = critic.assess(
        state=AgentState(task_input="task"),
        plan=PlannerOutput(
            thought="extract",
            action_name="extract_text",
            action_args={},
            expected_outcome="done",
        ),
        result=ToolResult(success=True, message="ok"),
        snapshot=PageSnapshot(url="https://example.com", title="Example", summary=""),
    )

    assert result.action_succeeded is True
    assert result.should_replan is False
    assert result.is_terminal is True


def test_critic_interface_is_abstract_placeholder() -> None:
    critic = Critic()

    try:
        critic.assess(
            state=AgentState(task_input="task"),
            plan=PlannerOutput(
                thought="t",
                action_name="extract_text",
                action_args={},
                expected_outcome="e",
            ),
            result=ToolResult(success=True, message="ok"),
            snapshot=PageSnapshot(url="", title="", summary=""),
        )
    except NotImplementedError:
        pass
    else:
        raise AssertionError("Critic.assess should raise NotImplementedError")


def test_prompts_include_expected_contract_language() -> None:
    assert "registered tool set" in PLANNER_SYSTEM_PROMPT
    assert "structured schemas" in CRITIC_SYSTEM_PROMPT
