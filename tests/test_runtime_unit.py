from pathlib import Path

import pytest

import app.browser.runtime as runtime_module
from app.browser.runtime import BrowserRuntime


class FakeLocator:
    def __init__(self) -> None:
        self.clicked = False
        self.filled: str | None = None
        self.waited = False

    def click(self) -> None:
        self.clicked = True

    def fill(self, text: str) -> None:
        self.filled = text

    def wait_for(self, state: str) -> None:
        assert state == "visible"
        self.waited = True


class BrokenLocator(FakeLocator):
    def wait_for(self, state: str) -> None:
        raise runtime_module.Error("not visible")


class FakeLocatorCollection:
    def __init__(self, locator: FakeLocator) -> None:
        self.locator = locator
        self.selector: str | None = None
        self.index: int | None = None

    def nth(self, index: int) -> FakeLocator:
        self.index = index
        return self.locator


class FakeKeyboard:
    def __init__(self) -> None:
        self.pressed: list[str] = []

    def press(self, key: str) -> None:
        self.pressed.append(key)


class FakeMouse:
    def __init__(self) -> None:
        self.wheels: list[tuple[int, int]] = []

    def wheel(self, x: int, y: int) -> None:
        self.wheels.append((x, y))


class FakePage:
    def __init__(self, locator: FakeLocator | None = None) -> None:
        self.url = ""
        self._title = "Untitled"
        self.keyboard = FakeKeyboard()
        self.mouse = FakeMouse()
        self.goto_calls: list[tuple[str, str]] = []
        self.load_states: list[str] = []
        self.go_back_calls: list[str] = []
        self.screenshot_calls: list[tuple[str, bool]] = []
        self.evaluate_result = {
            "visibleTexts": ["One", "Two"],
            "rawElements": [
                {
                    "tag": "input",
                    "text": "Search",
                    "role": "textbox",
                    "aria_label": "Search",
                    "placeholder": "Query",
                    "is_visible": True,
                    "is_clickable": True,
                }
            ],
        }
        self.locator_collection = FakeLocatorCollection(locator or FakeLocator())

    def goto(self, url: str, wait_until: str) -> None:
        self.goto_calls.append((url, wait_until))
        self.url = url
        self._title = "Loaded"

    def wait_for_load_state(self, state: str) -> None:
        self.load_states.append(state)

    def title(self) -> str:
        return self._title

    def evaluate(self, script: str):
        assert "interactiveSelector" in script
        return self.evaluate_result

    def locator(self, selector: str) -> FakeLocatorCollection:
        self.locator_collection.selector = selector
        return self.locator_collection

    def screenshot(self, path: str, full_page: bool) -> None:
        self.screenshot_calls.append((path, full_page))

    def go_back(self, wait_until: str) -> None:
        self.go_back_calls.append(wait_until)
        self.url = "https://example.com/previous"


class FakeContext:
    def __init__(self, page: FakePage) -> None:
        self.page = page
        self.closed = False
        self.viewport: dict[str, int] | None = None

    def new_page(self) -> FakePage:
        return self.page

    def close(self) -> None:
        self.closed = True


class FakeBrowser:
    def __init__(self, context: FakeContext) -> None:
        self.context = context
        self.closed = False
        self.headless: bool | None = None

    def new_context(self, viewport: dict[str, int]) -> FakeContext:
        self.context.viewport = viewport
        return self.context

    def close(self) -> None:
        self.closed = True


class FakeChromium:
    def __init__(self, browser: FakeBrowser) -> None:
        self.browser = browser

    def launch(self, headless: bool) -> FakeBrowser:
        self.browser.headless = headless
        return self.browser


class FakePlaywright:
    def __init__(self, browser: FakeBrowser) -> None:
        self.chromium = FakeChromium(browser)
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True


class FakeSyncPlaywrightManager:
    def __init__(self, playwright: FakePlaywright) -> None:
        self.playwright = playwright

    def start(self) -> FakePlaywright:
        return self.playwright


def make_runtime(monkeypatch: pytest.MonkeyPatch, locator: FakeLocator | None = None) -> tuple[BrowserRuntime, FakePage, FakeContext, FakeBrowser, FakePlaywright]:
    page = FakePage(locator=locator)
    context = FakeContext(page)
    browser = FakeBrowser(context)
    playwright = FakePlaywright(browser)
    monkeypatch.setattr(
        runtime_module,
        "sync_playwright",
        lambda: FakeSyncPlaywrightManager(playwright),
    )
    runtime = BrowserRuntime(headless=False, screenshot_dir="test-logs")
    return runtime, page, context, browser, playwright


def test_runtime_open_url_and_interactions_refresh_state(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime, page, _, browser, _ = make_runtime(monkeypatch)

    runtime.open_url("https://example.com")
    runtime.click("el-1")
    runtime.type_text("el-1", "browser explorer")
    runtime.press_enter()
    runtime.scroll_down()
    runtime.go_back()

    assert page.goto_calls == [("https://example.com", "domcontentloaded")]
    assert page.keyboard.pressed == ["Enter"]
    assert page.mouse.wheels == [(0, 900)]
    assert page.go_back_calls == ["domcontentloaded"]
    assert runtime.current_url == "https://example.com/previous"
    assert runtime.title == "Loaded"
    assert runtime.extract_text() == ["One", "Two"]
    assert browser.headless is False


def test_runtime_take_screenshot_creates_expected_path(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime, page, _, _, _ = make_runtime(monkeypatch)
    runtime.screenshot_dir = Path("logs-test")
    runtime.open_url("https://example.com")

    path = runtime.take_screenshot()

    assert path == str(Path("logs-test") / "browser-runtime-screenshot.png")
    assert page.screenshot_calls == [(str(Path("logs-test") / "browser-runtime-screenshot.png"), True)]


def test_runtime_close_releases_resources(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime, _, context, browser, playwright = make_runtime(monkeypatch)
    runtime.open_url("https://example.com")

    runtime.close()

    assert context.closed is True
    assert browser.closed is True
    assert playwright.stopped is True
    assert runtime._page is None


def test_runtime_context_manager_uses_ensure_page(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime, _, _, _, _ = make_runtime(monkeypatch)

    with runtime as active_runtime:
        assert active_runtime is runtime
        assert runtime._page is not None

    assert runtime._page is None


def test_runtime_requires_open_page_for_page_bound_operations() -> None:
    runtime = BrowserRuntime()

    with pytest.raises(RuntimeError, match="open_url first"):
        runtime.press_enter()


def test_runtime_locator_validation_errors_are_clear(monkeypatch: pytest.MonkeyPatch) -> None:
    runtime, _, _, _, _ = make_runtime(monkeypatch, locator=BrokenLocator())
    runtime.open_url("https://example.com")

    with pytest.raises(RuntimeError, match="Element el-1 is not available"):
        runtime._locator_for_element_id("el-1")

    with pytest.raises(ValueError, match="Unsupported element id"):
        runtime._locator_for_element_id("bad-id")


def test_runtime_refresh_state_handles_missing_page() -> None:
    runtime = BrowserRuntime()

    runtime._refresh_state()

    assert runtime.current_url == ""
    assert runtime.title == ""
    assert runtime.visible_texts == []
    assert runtime.raw_elements == []
