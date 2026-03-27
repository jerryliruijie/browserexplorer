"""Playwright runtime abstraction."""

from __future__ import annotations

from typing import Any


class BrowserRuntime:
    """Thin wrapper for controlled browser operations."""

    def __init__(self) -> None:
        self.current_url = ""
        self.title = ""
        self.visible_texts: list[str] = []
        self.raw_elements: list[dict[str, Any]] = []

    def open_url(self, url: str) -> None:
        self.current_url = url
        self.title = f"Page: {url}"

    def click(self, element_id: str) -> None:
        self.visible_texts.append(f"clicked:{element_id}")

    def type_text(self, element_id: str, text: str) -> None:
        self.visible_texts.append(f"typed:{element_id}:{text}")

    def press_enter(self) -> None:
        self.visible_texts.append("pressed:enter")

    def scroll_down(self) -> None:
        self.visible_texts.append("scrolled:down")

    def go_back(self) -> None:
        self.visible_texts.append("navigated:back")

    def extract_text(self) -> list[str]:
        return list(self.visible_texts)

    def take_screenshot(self) -> str:
        return "logs/todo-screenshot.png"

