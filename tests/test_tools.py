from app.tools.registry import ToolRegistry
from tests.test_tools_unit import FakeRuntime


def test_registry_executes_known_tool(sample_page: str) -> None:
    registry = ToolRegistry()
    runtime = FakeRuntime()

    result = registry.execute("open_url", runtime, url=sample_page)

    assert result.success is True
    assert runtime.current_url == sample_page
    assert runtime.title == "Opened"


def test_registry_rejects_unknown_tool() -> None:
    result = ToolRegistry().execute("unknown_tool", FakeRuntime())

    assert result.success is False
    assert result.error == "unknown_tool"
