"""CLI entry point."""

from __future__ import annotations

import typer

from app.config import AppConfig
from app.agent.orchestrator import AgentOrchestrator
from app.browser.observer import BrowserObserver
from app.browser.runtime import BrowserRuntime
from app.memory.store import StateStore
from app.tools.registry import ToolRegistry

app = typer.Typer(help="Browser agent CLI.")


@app.command()
def run(task: str) -> None:
    """Run the agent for a task."""
    config = AppConfig()
    orchestrator = AgentOrchestrator(
        runtime=BrowserRuntime(),
        observer=BrowserObserver(),
        registry=ToolRegistry(safety_config=config.safety),
        store=StateStore(),
    )
    state = orchestrator.run(task=task, max_steps=config.safety.max_steps)
    typer.echo(state.final_report or state.page_summary)


if __name__ == "__main__":
    app()
