from pathlib import Path

from app.config import AppConfig, BrowserConfig, SafetyConfig


def test_browser_config_enforces_non_negative_slow_mo() -> None:
    config = BrowserConfig(slow_mo_ms=25, screenshot_dir=Path("shots"))

    assert config.slow_mo_ms == 25
    assert config.screenshot_dir == Path("shots")


def test_app_config_headless_proxies_browser_setting() -> None:
    config = AppConfig(browser=BrowserConfig(headless=False), safety=SafetyConfig(max_steps=9))

    assert config.headless is False
    assert config.safety.max_steps == 9
