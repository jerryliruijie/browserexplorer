from app.agent.orchestrator import AgentOrchestrator
from app.browser.observer import BrowserObserver
from app.browser.runtime import BrowserRuntime
from app.memory.store import StateStore
from app.tools.registry import ToolRegistry


def test_orchestrator_runs_minimal_loop_and_builds_report(
    runtime: BrowserRuntime, sample_page: str
) -> None:
    orchestrator = AgentOrchestrator(
        runtime=runtime,
        observer=BrowserObserver(),
        registry=ToolRegistry(),
        store=StateStore(),
    )

    state = orchestrator.run(task=sample_page, max_steps=4)

    assert state.done is True
    assert state.action_history[-1].action_name == "extract_text"
    assert "Fixture Page" in state.extracted_data["texts"]
    assert "Task:" in state.final_report
