from app.browser.runtime import BrowserRuntime
from app.tools.registry import ToolRegistry


def test_registry_executes_known_tool() -> None:
    runtime = BrowserRuntime()
    registry = ToolRegistry()

    result = registry.execute("open_url", runtime, url="https://example.com")

    assert result.success is True
    assert runtime.current_url == "https://example.com"


def test_registry_rejects_unknown_tool() -> None:
    result = ToolRegistry().execute("unknown_tool", BrowserRuntime())

    assert result.success is False
    assert result.error == "unknown_tool"

