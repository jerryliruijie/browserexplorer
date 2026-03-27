# Utils Package Guide

## Responsibility

This package contains stable, truly reusable utilities with no domain-specific browser-agent behavior.

## Out of Scope

- Do not drop temporary experiments or feature logic here.
- Do not turn `utils` into a dumping ground for unresolved design choices.

## Boundaries

- Utilities must stay generic and low-coupling.
- If a helper knows too much about agent workflow, it belongs elsewhere.

## Rules

- Keep interfaces small and dependency-light.
- Prefer pure functions where practical.

## Dependencies

- May depend on standard library modules and neutral helpers.
- Should avoid importing high-level application packages.

## Extension Ideas

- Trace formatting utilities.
- Generic backoff and idempotent retry helpers.

## Prohibited

- Do not hide business policy in utility functions.
- Do not import browser runtime into generic helpers.

