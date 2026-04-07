import pytest
from pydantic import ValidationError

from app.agent.models import PlannerOutput
from app.llm.client import StubLLMClient
from app.llm.parser import parse_planner_response
from app.llm.schemas import PlannerRequest, PlannerResponse


def test_parse_planner_response_validates_json_payload() -> None:
    response = parse_planner_response(
        """
        {
          "decision": {
            "thought": "Open the page first.",
            "action_name": "open_url",
            "action_args": {"url": "https://example.com"},
            "expected_outcome": "The page loads."
          }
        }
        """
    )

    assert isinstance(response, PlannerResponse)
    assert response.decision == PlannerOutput(
        thought="Open the page first.",
        action_name="open_url",
        action_args={"url": "https://example.com"},
        expected_outcome="The page loads.",
    )


def test_parse_planner_response_rejects_invalid_payload() -> None:
    with pytest.raises(ValidationError):
        parse_planner_response('{"decision": {"thought": "missing fields"}}')


def test_stub_llm_client_is_explicitly_unimplemented() -> None:
    request = PlannerRequest(task="task", current_url="", snapshot_summary="")

    with pytest.raises(NotImplementedError, match="real LLM backend"):
        StubLLMClient().plan(request)
