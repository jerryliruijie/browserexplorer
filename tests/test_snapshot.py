from app.browser.element_indexer import ElementIndexer
from app.browser.observer import BrowserObserver
from app.browser.runtime import BrowserRuntime


def test_snapshot_contains_compressed_summary_and_internal_ids(
    runtime: BrowserRuntime, sample_page: str
) -> None:
    runtime.open_url(sample_page)

    snapshot = BrowserObserver(ElementIndexer()).observe(runtime)

    assert snapshot.url == sample_page
    assert snapshot.elements[0].element_id == "el-1"
    assert snapshot.elements[0].tag == "input"
    assert snapshot.elements[1].text == "Search"
    assert "interactive_elements=2" in snapshot.summary
