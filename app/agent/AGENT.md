# Agent Package Guide

## Responsibility

This package owns high-level agent control flow: orchestrator, planner interfaces, critic interfaces, prompts, and agent-facing models.

## Out of Scope

- Do not perform raw browser automation here.
- Do not store duplicate mutable runtime state outside the memory package.

## Boundaries

- Keep orchestrator, planner, and critic separated.
- Planner outputs structured action decisions only.
- Critic evaluates outcomes and emits replanning signals.

## Rules

- Planner must not call the browser directly.
- Orchestrator may coordinate modules but should not absorb tool or snapshot logic.
- Models should stay serializable and easy to validate in tests.

## Dependencies

- May depend on browser snapshots, memory state, tool registry interfaces, llm schemas, and safety checks.
- Must not make `app/browser` depend back on agent logic.

## Extension Ideas

- Tree search or multi-candidate planning.
- Critic policies for loop detection and recovery.

## Prohibited

- Do not execute Playwright actions from planner code.
- Do not emit free-form action blobs that bypass tool validation.

