"""CLI entry point."""

from __future__ import annotations

import typer

from app.config import AppConfig

app = typer.Typer(help="Browser agent CLI.")


@app.command()
def run(task: str) -> None:
    """Run the agent for a task."""
    config = AppConfig()
    typer.echo(f"TODO: wire orchestrator for task={task!r} with headless={config.headless}")


if __name__ == "__main__":
    app()

