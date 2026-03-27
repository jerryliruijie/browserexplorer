# Safety Package Guide

## Responsibility

This package centralizes safe-mode behavior, policy checks, and guardrails for risky actions.

## Out of Scope

- Do not scatter risk checks across unrelated modules.
- Do not encode product-specific workflows here.

## Boundaries

- Define risk levels and default deny rules in one place.
- Keep policy decisions inspectable and testable.

## Rules

- Default-deny high-risk submission behavior.
- Make safety checks explicit at tool-execution boundaries.

## Dependencies

- May depend on tool metadata and configuration models.
- Must stay independent from browser implementation details.

## Extension Ideas

- Domain allowlists and intent-based approval flows.
- Recovery policies for suspected unsafe states.

## Prohibited

- Do not silently downgrade high-risk actions into allowed ones.
- Do not let planner bypass guardrails.

