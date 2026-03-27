# Memory Package Guide

## Responsibility

This package owns runtime state, action history, and helpers that update extracted facts in a traceable way.

## Out of Scope

- Do not embed browser automation or planning logic here.
- Do not let multiple packages maintain competing state copies.

## Boundaries

- `AgentState` is the single mutable source of truth for the main loop.
- History updates should flow through centralized helpers.

## Rules

- Keep state transitions explicit and testable.
- Avoid hidden mutations in unrelated modules.
- Store extracted data in structured fields, not ad-hoc globals.

## Dependencies

- May depend on shared models from agent, browser, and tools packages.
- Must not depend on Playwright details.

## Extension Ideas

- Persistent stores for resumable sessions.
- Trace serialization and replay helpers.

## Prohibited

- Do not let planner or tools each keep their own shadow history.
- Do not bypass store helpers for important state transitions.

