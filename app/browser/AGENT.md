# Browser Package Guide

## Responsibility

This package abstracts the browser environment: runtime control, observation, element indexing, and compressed snapshots for planner consumption.

## Out of Scope

- No high-level task planning lives here.
- No business-specific extraction heuristics should be hardcoded into the runtime layer.

## Boundaries

- Snapshots must be compressed, controlled, and LLM-friendly.
- Elements are exposed through internal `element_id` values.
- Raw DOM access should stay local and bounded.

## Rules

- Do not pass unlimited raw HTML to upper layers.
- Keep browser access behind stable runtime and observer interfaces.
- Snapshot builders must be deterministic enough for testing.

## Dependencies

- May depend on Playwright types and local browser-facing models.
- Must not depend on planner, critic, or orchestrator logic.

## Extension Ideas

- Richer structured candidates for commerce or forms.
- Vision-assisted observation that still returns constrained snapshots.

## Prohibited

- Do not expose arbitrary selectors as the main planner interface.
- Do not let page observation mutate agent state directly.

