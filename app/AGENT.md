# App Layer Guide

## Responsibility

`app/` contains the runtime entry points and the main bounded contexts for the browser agent.

## Out of Scope

- This directory is not the place for ad-hoc experiments or one-off scripts.
- Do not place raw benchmark datasets or browser traces here.

## Boundaries

- Keep each subpackage focused on a single concern.
- Cross-package wiring should happen at clear integration points, not through circular imports.

## Rules

- Preserve typed interfaces between packages.
- Keep the CLI thin; orchestration belongs in `app/agent`.
- New shared behavior belongs in a dedicated module, not in package `__init__` files.

## Dependencies

- `app/main.py` may depend on configuration and orchestrator entry points.
- Subpackages should depend inward on shared models, not sideways on implementation details.

## Extension Ideas

- Environment-based configuration loading.
- Dependency injection for LLM clients and browser runtimes.

## Prohibited

- Do not hide core behavior behind package import side effects.
- Do not turn `app/main.py` into the main business-logic module.

