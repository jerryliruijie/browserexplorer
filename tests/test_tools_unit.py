from app.config import SafetyConfig
from app.tools.extraction_tools import ExtractListingsTool, ExtractTextTool, TakeScreenshotTool
from app.tools.interaction_tools import ClickElementTool, PressEnterTool, TypeTextTool
from app.tools.navigation_tools import GoBackTool, OpenUrlTool, ScrollDownTool
from app.tools.registry import ToolRegistry


class FakeRuntime:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []
        self.current_url = ""
        self.title = ""
        self.raw_elements = [
            {
                "tag": "button",
                "role": "button",
                "text": "Search",
                "aria_label": "Search",
                "placeholder": None,
                "is_visible": True,
                "is_clickable": True,
            }
        ]
        self.visible_texts = ["visible"]

    def open_url(self, url: str) -> None:
        self.calls.append(("open_url", url))
        self.current_url = url
        self.title = "Opened"

    def click(self, element_id: str) -> None:
        self.calls.append(("click", element_id))

    def type_text(self, element_id: str, text: str) -> None:
        self.calls.append(("type_text", (element_id, text)))

    def press_enter(self) -> None:
        self.calls.append(("press_enter", None))

    def scroll_down(self) -> None:
        self.calls.append(("scroll_down", None))

    def go_back(self) -> None:
        self.calls.append(("go_back", None))

    def extract_text(self) -> list[str]:
        self.calls.append(("extract_text", None))
        return list(self.visible_texts)

    def take_screenshot(self) -> str:
        self.calls.append(("take_screenshot", None))
        return "logs/browser-runtime-screenshot.png"


def test_navigation_and_interaction_tools_delegate_to_runtime() -> None:
    runtime = FakeRuntime()

    assert OpenUrlTool().execute(runtime, url="https://example.com").data == {"url": "https://example.com"}
    assert ClickElementTool().execute(runtime, element_id="el-1").success is True
    assert TypeTextTool().execute(runtime, element_id="el-1", text="browser").message == "Typed text."
    assert PressEnterTool().execute(runtime).message == "Pressed Enter."
    assert ScrollDownTool().execute(runtime).message == "Scrolled down."
    assert GoBackTool().execute(runtime).message == "Navigated back."

    assert runtime.calls == [
        ("open_url", "https://example.com"),
        ("click", "el-1"),
        ("type_text", ("el-1", "browser")),
        ("press_enter", None),
        ("scroll_down", None),
        ("go_back", None),
    ]


def test_extraction_tools_return_structured_payloads() -> None:
    runtime = FakeRuntime()

    assert ExtractTextTool().execute(runtime).data == {"texts": ["visible"]}
    assert ExtractListingsTool().execute(runtime).data == {"listings": []}
    assert TakeScreenshotTool().execute(runtime).data == {"path": "logs/browser-runtime-screenshot.png"}


def test_registry_blocks_high_risk_tool_when_safety_forbids_it() -> None:
    class HighRiskOpenUrlTool(OpenUrlTool):
        high_risk = True

    runtime = FakeRuntime()
    registry = ToolRegistry(safety_config=SafetyConfig(allow_high_risk_actions=False))
    registry._tools["open_url"] = HighRiskOpenUrlTool()

    result = registry.execute("open_url", runtime, url="https://example.com")

    assert result.success is False
    assert result.error == "high-risk-action-denied"
