from __future__ import annotations

from pathlib import Path

import pytest

from app.browser.runtime import BrowserRuntime


@pytest.fixture
def sample_page() -> str:
    page = Path(__file__).parent / "fixtures" / "sample.html"
    return page.resolve().as_uri()


@pytest.fixture
def runtime() -> BrowserRuntime:
    browser_runtime = BrowserRuntime()
    try:
        yield browser_runtime
    finally:
        browser_runtime.close()
