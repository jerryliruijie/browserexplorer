from app.browser.runtime import BrowserRuntime
from app.tools.registry import ToolRegistry


def test_registry_executes_known_tool(runtime: BrowserRuntime, sample_page: str) -> None:
    registry = ToolRegistry()

    result = registry.execute("open_url", runtime, url=sample_page)

    assert result.success is True
    assert runtime.current_url == sample_page
    assert runtime.title == "Fixture Page"


def test_registry_rejects_unknown_tool() -> None:
    result = ToolRegistry().execute("unknown_tool", BrowserRuntime())

    assert result.success is False
    assert result.error == "unknown_tool"
