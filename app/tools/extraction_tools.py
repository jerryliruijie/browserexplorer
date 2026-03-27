"""Extraction tools."""

from __future__ import annotations

from app.browser.runtime import BrowserRuntime
from app.tools.base import BaseTool, ToolResult


class ExtractTextTool(BaseTool):
    name = "extract_text"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        texts = runtime.extract_text()
        return ToolResult(success=True, message="Extracted visible text.", data={"texts": texts})


class ExtractListingsTool(BaseTool):
    name = "extract_listings"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        return ToolResult(
            success=True,
            message="TODO: implement listing extraction heuristics.",
            data={"listings": []},
        )


class TakeScreenshotTool(BaseTool):
    name = "take_screenshot"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        path = runtime.take_screenshot()
        return ToolResult(success=True, message="Captured screenshot.", data={"path": path})

