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

- Keep the architecture clear and easy to reason about as the codebase grows.
- Keep module boundaries explicit and defend them during feature work.
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

## Development Workflow

- Do not try to complete every requested task in one large change.
- Split work into small, reviewable features or fixes whenever practical.
- Test continuously during development instead of waiting until the end.
- Keep each commit focused on one coherent unit of change.
- Aim to keep each commit under 300 added lines of code.
- Keep every `AGENT.md` precise enough that future work can follow its rules without guessing.
- Write detailed commit messages that state where the change happened, what changed, and what behavior or feature it adds or fixes.
- Prefer conventional commit prefixes such as `feat:`, `fix:`, `refactor:`, and `test:` when they fit the change.

## Style

- Use Python 3.11+ with Pydantic models where structured validation matters.
- Keep all files in English, including code, comments, docs, and `AGENT.md`, except `README.md`, which may stay in Chinese.
- When behavior is intentionally deferred, add an explicit `TODO` marker instead of silently omitting the implementation.

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
