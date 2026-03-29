"""Playwright runtime abstraction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Error, Page, Playwright, sync_playwright


class BrowserRuntime:
    """Thin wrapper for controlled browser operations."""

    def __init__(self, headless: bool = True, screenshot_dir: str | Path = "logs") -> None:
        self.headless = headless
        self.screenshot_dir = Path(screenshot_dir)
        self.current_url = ""
        self.title = ""
        self.visible_texts: list[str] = []
        self.raw_elements: list[dict[str, Any]] = []
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    def open_url(self, url: str) -> None:
        page = self._ensure_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        self._refresh_state()

    def click(self, element_id: str) -> None:
        locator = self._locator_for_element_id(element_id)
        locator.click()
        self._refresh_state()

    def type_text(self, element_id: str, text: str) -> None:
        locator = self._locator_for_element_id(element_id)
        locator.fill(text)
        self._refresh_state()

    def press_enter(self) -> None:
        page = self._require_page()
        page.keyboard.press("Enter")
        self._refresh_state()

    def scroll_down(self) -> None:
        page = self._require_page()
        page.mouse.wheel(0, 900)
        self._refresh_state()

    def go_back(self) -> None:
        page = self._require_page()
        page.go_back(wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        self._refresh_state()

    def extract_text(self) -> list[str]:
        if self._page is not None:
            self._refresh_state()
        return list(self.visible_texts)

    def take_screenshot(self) -> str:
        page = self._require_page()
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = self.screenshot_dir / "browser-runtime-screenshot.png"
        page.screenshot(path=str(path), full_page=True)
        self._refresh_state()
        return str(path)

    def close(self) -> None:
        if self._context is not None:
            self._context.close()
            self._context = None
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None
        self._page = None

    def __enter__(self) -> BrowserRuntime:
        self._ensure_page()
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _ensure_page(self) -> Page:
        if self._page is not None:
            return self._page
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context(viewport={"width": 1440, "height": 1200})
        self._page = self._context.new_page()
        return self._page

    def _require_page(self) -> Page:
        page = self._page
        if page is None:
            raise RuntimeError("Browser page has not been initialized. Call open_url first.")
        return page

    def _refresh_state(self) -> None:
        if self._page is None:
            self.current_url = ""
            self.title = ""
            self.visible_texts = []
            self.raw_elements = []
            return
        page = self._page
        self.current_url = page.url
        self.title = page.title()
        state = page.evaluate(
            """
            () => {
              const clean = (value) => (value || "").replace(/\\s+/g, " ").trim();
              const interactiveSelector = [
                "a[href]",
                "button",
                "input",
                "select",
                "textarea",
                "[role=button]",
                "[role=link]",
                "[role=textbox]",
                "[tabindex]"
              ].join(",");
              const isVisible = (element) => {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();
                return style.visibility !== "hidden" && style.display !== "none" && rect.width > 0 && rect.height > 0;
              };
              const visibleTexts = Array.from(document.querySelectorAll("body *"))
                .filter((element) => element.children.length === 0 && isVisible(element))
                .map((element) => clean(element.textContent))
                .filter(Boolean)
                .slice(0, 100);
              const rawElements = Array.from(document.querySelectorAll(interactiveSelector))
                .filter((element) => isVisible(element))
                .map((element) => ({
                  tag: element.tagName.toLowerCase(),
                  text: clean(element.innerText || element.textContent),
                  role: clean(element.getAttribute("role")),
                  aria_label: clean(element.getAttribute("aria-label")),
                  placeholder: clean(element.getAttribute("placeholder")),
                  is_visible: true,
                  is_clickable: ["a", "button"].includes(element.tagName.toLowerCase())
                    || element.getAttribute("role") === "button"
                    || element.getAttribute("role") === "link"
                    || element.tagName.toLowerCase() === "input"
                    || element.tagName.toLowerCase() === "textarea"
                    || element.tagName.toLowerCase() === "select",
                }));
              return { visibleTexts, rawElements };
            }
            """
        )
        self.visible_texts = [str(text) for text in state["visibleTexts"]]
        self.raw_elements = [dict(item) for item in state["rawElements"]]

    def _locator_for_element_id(self, element_id: str):
        index = self._element_index(element_id)
        page = self._require_page()
        locator = page.locator(
            ",".join(
                [
                    "a[href]",
                    "button",
                    "input",
                    "select",
                    "textarea",
                    "[role=button]",
                    "[role=link]",
                    "[role=textbox]",
                    "[tabindex]",
                ]
            )
        ).nth(index)
        try:
            locator.wait_for(state="visible")
        except Error as exc:
            raise RuntimeError(f"Element {element_id} is not available.") from exc
        return locator

    @staticmethod
    def _element_index(element_id: str) -> int:
        prefix = "el-"
        if not element_id.startswith(prefix):
            raise ValueError(f"Unsupported element id: {element_id}")
        return int(element_id[len(prefix) :]) - 1
