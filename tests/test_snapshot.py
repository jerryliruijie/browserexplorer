from app.browser.element_indexer import ElementIndexer
from app.browser.observer import BrowserObserver
from app.browser.runtime import BrowserRuntime


def test_snapshot_contains_compressed_summary_and_internal_ids() -> None:
    runtime = BrowserRuntime()
    runtime.open_url("https://example.com")
    runtime.raw_elements = [
        {"tag": "button", "text": "Search", "role": "button", "is_clickable": True},
        {"tag": "input", "placeholder": "keywords", "role": "textbox", "is_clickable": True},
    ]

    snapshot = BrowserObserver(ElementIndexer()).observe(runtime)

    assert snapshot.url == "https://example.com"
    assert snapshot.elements[0].element_id == "el-1"
    assert "interactive_elements=2" in snapshot.summary

