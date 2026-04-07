from typer.testing import CliRunner

import app.main as main_module


class FakeState:
    def __init__(self, final_report: str = "", page_summary: str = "") -> None:
        self.final_report = final_report
        self.page_summary = page_summary


class FakeOrchestrator:
    last_task: str | None = None
    last_max_steps: int | None = None

    def __init__(self, **_: object) -> None:
        pass

    def run(self, task: str, max_steps: int) -> FakeState:
        FakeOrchestrator.last_task = task
        FakeOrchestrator.last_max_steps = max_steps
        return FakeState(final_report="done")


def test_cli_run_invokes_orchestrator(monkeypatch) -> None:
    monkeypatch.setattr(main_module, "AgentOrchestrator", FakeOrchestrator)
    runner = CliRunner()

    result = runner.invoke(main_module.app, ["https://example.com"])

    assert result.exit_code == 0
    assert "done" in result.output
    assert FakeOrchestrator.last_task == "https://example.com"
    assert FakeOrchestrator.last_max_steps == 12
