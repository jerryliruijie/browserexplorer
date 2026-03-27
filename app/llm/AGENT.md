# LLM Package Guide

## Responsibility

This package owns model-client abstractions, structured schemas, and parsers for constrained LLM interaction.

## Out of Scope

- Do not embed business workflow logic in the client.
- Do not let parsing rules drift away from the exported schemas.

## Boundaries

- Constrain model outputs as much as possible.
- Keep transport, schema, and parser concerns separated.

## Rules

- Planner-facing outputs must validate before use.
- Prefer explicit parse errors over silent coercion.
- Keep provider-specific code behind interfaces.

## Dependencies

- May depend on agent-facing schemas but should not know browser internals.

## Extension Ideas

- Add OpenAI or local-model adapters.
- Add retryable structured-output parsing.

## Prohibited

- Do not hide business rules in prompt transport code.
- Do not return unvalidated raw LLM strings to orchestrator.

