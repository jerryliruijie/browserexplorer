# Tools Package Guide

## Responsibility

This package defines all controlled browser actions and the registry that exposes them to the agent.

## Out of Scope

- Do not place planning logic here.
- Do not mutate global state directly from tool implementations.

## Boundaries

- All browser actions must go through the tool registry.
- Every tool returns the shared `ToolResult` model.
- High-risk actions must be explicitly marked and policy-checked.

## Rules

- Keep tool inputs narrow and validated.
- Prefer `element_id` over arbitrary selectors.
- Tools should be easy to log and test in isolation.

## Dependencies

- May depend on browser runtime and safety policies.
- Must not depend on planner internals beyond action names and args.

## Extension Ideas

- Richer extraction tools for product cards and form fields.
- Retry wrappers for flaky page interactions.

## Prohibited

- Do not call Playwright directly from orchestrator when a tool exists.
- Do not return untyped dictionaries as the public tool interface.

