from app.agent.orchestrator import AgentOrchestrator
from app.browser.observer import BrowserObserver
from app.browser.runtime import BrowserRuntime
from app.memory.store import StateStore
from app.tools.registry import ToolRegistry


def test_orchestrator_runs_minimal_loop_and_builds_report() -> None:
    orchestrator = AgentOrchestrator(
        runtime=BrowserRuntime(),
        observer=BrowserObserver(),
        registry=ToolRegistry(),
        store=StateStore(),
    )

    state = orchestrator.run(task="https://example.com", max_steps=4)

    assert state.done is True
    assert state.action_history[-1].action_name == "extract_text"
    assert "texts" in state.extracted_data
    assert "Task:" in state.final_report
