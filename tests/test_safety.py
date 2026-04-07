from app.safety.guardrails import allow_tool
from app.safety.policies import RiskLevel
from app.tools.base import BaseTool


class HighRiskTool(BaseTool):
    name = "danger"
    high_risk = True


def test_allow_tool_blocks_high_risk_action_by_default() -> None:
    result = allow_tool(HighRiskTool())

    assert result is not None
    assert result.success is False
    assert result.error == "high-risk-action-denied"


def test_allow_tool_allows_high_risk_action_when_enabled() -> None:
    result = allow_tool(HighRiskTool(), allow_high_risk_actions=True)

    assert result is None


def test_risk_level_enum_values_are_stable() -> None:
    assert [level.value for level in RiskLevel] == ["low", "medium", "high"]
