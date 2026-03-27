# Test Guide

## Responsibility

Tests validate schemas, snapshots, registry behavior, state transitions, and integration seams.

## Out of Scope

- Do not encode brittle end-to-end flows that depend on uncontrolled public websites.

## Rules

- Prioritize schema, snapshot, registry, and state tests first.
- Cover error paths and invalid inputs, not only happy paths.
- Keep browser-heavy tests layered so unit tests stay fast.

## Dependencies

- Tests may use public interfaces from all `app/*` modules.
- Prefer fixtures and fakes over patching internal private details.

## Extension Ideas

- Add replay-based tests for action traces.
- Add benchmark fixtures for controlled pages.

## Prohibited

- Do not duplicate implementation logic inside tests.
- Do not rely on live sites for core correctness assertions.
