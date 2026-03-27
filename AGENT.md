# Root Guide

## Purpose

This repository implements a browser agent skeleton that demonstrates agent design, constrained browser tooling, state management, and testable abstractions.

## MVP Scope

- Support controlled browsing, search, extraction, simple forms, and final reporting.
- Keep the architecture ready for future multi-agent, vision, and evaluation extensions.

## Non-Goals

- Do not implement login, payment, file upload, CAPTCHA, complex iframe handling, drag-and-drop, or default high-risk submissions.
- Do not optimize for broad web coverage before the architecture is stable.

## Architecture Rules

- Do not pass full raw HTML directly to the LLM.
- Do not let the LLM generate arbitrary Playwright scripts.
- Do not bypass the tool registry from planner or orchestrator code.
- Do not enable high-risk actions by default.
- Do not collapse planner, critic, tool logic, and browser runtime into orchestrator.

## Development Priorities

1. Keep module boundaries explicit.
2. Prefer typed interfaces over implicit dictionaries.
3. Preserve the observe -> plan -> act -> reflect loop.
4. Make planner schemas, snapshots, registry behavior, and state transitions easy to test.

## Style

- Use Python 3.11+ with Pydantic models where structured validation matters.
- Keep Markdown and code comments in English, except `README.md`, which may stay in Chinese.
- Write TODO markers where behavior is intentionally deferred.

## Testing

- Add or update tests for planner schemas, snapshot building, registry behavior, and state management.
- Avoid happy-path-only tests when adding new modules.

## Dependency Boundaries

- `app/agent` may depend on browser snapshots, memory state, llm schemas, safety checks, and tools.
- `app/browser` must not depend on planner or critic logic.
- `app/tools` may use browser runtime and safety policies, but must stay decoupled from planner internals.
- `app/memory` is the single source of truth for runtime state and action history.

## Future Evolution

- Real LLM backends and structured output enforcement.
- Multi-agent collaboration.
- Vision-based observation.
- Evaluation datasets, benchmarks, and trace replay.
