from pathlib import Path

from tests.test_runtime_unit import make_runtime


def test_runtime_interactions_update_page_state(monkeypatch, sample_page: str) -> None:
    runtime, _, _, _, _ = make_runtime(monkeypatch)
    runtime.open_url(sample_page)
    runtime.type_text("el-1", "browser explorer")
    runtime.press_enter()

    assert runtime.extract_text() == ["One", "Two"]
    assert runtime.current_url == sample_page


def test_runtime_takes_screenshot(monkeypatch, sample_page: str) -> None:
    runtime, _, _, _, _ = make_runtime(monkeypatch)
    runtime.screenshot_dir = Path("logs-test")
    runtime.open_url(sample_page)

    screenshot_path = Path(runtime.take_screenshot())

    assert screenshot_path.name == "browser-runtime-screenshot.png"
    assert screenshot_path.suffix == ".png"
