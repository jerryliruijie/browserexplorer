from app.agent.orchestrator import AgentOrchestrator
from app.browser.observer import BrowserObserver
from app.memory.store import StateStore
from app.tools.registry import ToolRegistry
from tests.test_tools_unit import FakeRuntime


def test_orchestrator_runs_minimal_loop_and_builds_report(
    sample_page: str,
) -> None:
    runtime = FakeRuntime()
    runtime.current_url = sample_page
    runtime.title = "Fixture Page"
    orchestrator = AgentOrchestrator(
        runtime=runtime,
        observer=BrowserObserver(),
        registry=ToolRegistry(),
        store=StateStore(),
    )

    state = orchestrator.run(task=sample_page, max_steps=4)

    assert state.done is True
    assert state.action_history[-1].action_name == "extract_text"
    assert "visible" in state.extracted_data["texts"]
    assert "Task:" in state.final_report
