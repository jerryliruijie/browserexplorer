from pathlib import Path

from app.browser.runtime import BrowserRuntime


def test_runtime_interactions_update_page_state(runtime: BrowserRuntime, sample_page: str) -> None:
    runtime.open_url(sample_page)
    runtime.type_text("el-1", "browser explorer")
    runtime.press_enter()

    assert "Submitted:browser explorer" in runtime.extract_text()

    runtime.click("el-2")

    assert "browser explorer" in runtime.extract_text()


def test_runtime_takes_screenshot(runtime: BrowserRuntime, sample_page: str) -> None:
    runtime.open_url(sample_page)

    screenshot_path = Path(runtime.take_screenshot())

    assert screenshot_path.exists()
    assert screenshot_path.suffix == ".png"
