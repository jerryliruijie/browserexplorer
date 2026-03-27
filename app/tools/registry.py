"""Tool registry for controlled execution."""

from __future__ import annotations

from app.config import SafetyConfig
from app.browser.runtime import BrowserRuntime
from app.safety.guardrails import allow_tool
from app.tools.base import BaseTool, ToolResult
from app.tools.extraction_tools import ExtractListingsTool, ExtractTextTool, TakeScreenshotTool
from app.tools.interaction_tools import ClickElementTool, PressEnterTool, TypeTextTool
from app.tools.navigation_tools import GoBackTool, OpenUrlTool, ScrollDownTool


class ToolRegistry:
    """Registers and executes named tools."""

    def __init__(self, safety_config: SafetyConfig | None = None) -> None:
        self._tools = {tool.name: tool for tool in self.default_tools()}
        self.safety_config = safety_config or SafetyConfig()

    @staticmethod
    def default_tools() -> list[BaseTool]:
        return [
            OpenUrlTool(),
            ClickElementTool(),
            TypeTextTool(),
            PressEnterTool(),
            ScrollDownTool(),
            GoBackTool(),
            ExtractTextTool(),
            ExtractListingsTool(),
            TakeScreenshotTool(),
        ]

    def execute(self, action_name: str, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        tool = self._tools.get(action_name)
        if tool is None:
            return ToolResult(success=False, message="Unknown tool.", error=action_name)
        blocked = allow_tool(tool, allow_high_risk_actions=self.safety_config.allow_high_risk_actions)
        if blocked is not None:
            return blocked
        return tool.execute(runtime, **kwargs)
