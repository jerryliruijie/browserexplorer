"""LLM client abstraction."""

from __future__ import annotations

from app.llm.schemas import PlannerRequest, PlannerResponse


class LLMClient:
    """Abstract structured-output client."""

    def plan(self, request: PlannerRequest) -> PlannerResponse:
        raise NotImplementedError


class StubLLMClient(LLMClient):
    """Placeholder implementation for future provider integration."""

    def plan(self, request: PlannerRequest) -> PlannerResponse:
        raise NotImplementedError("TODO: integrate a real LLM backend.")

