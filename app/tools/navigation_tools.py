"""Navigation tools."""

from __future__ import annotations

from app.browser.runtime import BrowserRuntime
from app.tools.base import BaseTool, ToolResult


class OpenUrlTool(BaseTool):
    name = "open_url"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        url = kwargs["url"]
        runtime.open_url(url)
        return ToolResult(success=True, message=f"Opened {url}.", data={"url": url})


class ScrollDownTool(BaseTool):
    name = "scroll_down"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        runtime.scroll_down()
        return ToolResult(success=True, message="Scrolled down.")


class GoBackTool(BaseTool):
    name = "go_back"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        runtime.go_back()
        return ToolResult(success=True, message="Navigated back.")

