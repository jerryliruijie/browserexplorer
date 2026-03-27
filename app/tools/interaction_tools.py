"""Interaction tools."""

from __future__ import annotations

from app.browser.runtime import BrowserRuntime
from app.tools.base import BaseTool, ToolResult


class ClickElementTool(BaseTool):
    name = "click_element"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        element_id = kwargs["element_id"]
        runtime.click(element_id)
        return ToolResult(success=True, message=f"Clicked {element_id}.")


class TypeTextTool(BaseTool):
    name = "type_text"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        runtime.type_text(kwargs["element_id"], kwargs["text"])
        return ToolResult(success=True, message="Typed text.")


class PressEnterTool(BaseTool):
    name = "press_enter"

    def execute(self, runtime: BrowserRuntime, **kwargs: str) -> ToolResult:
        runtime.press_enter()
        return ToolResult(success=True, message="Pressed Enter.")

