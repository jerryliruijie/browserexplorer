from app.browser.element_indexer import ElementIndexer
from app.browser.observer import BrowserObserver
from tests.test_observer_indexer import FakeRuntime


def test_snapshot_contains_compressed_summary_and_internal_ids(
    sample_page: str,
) -> None:
    runtime = FakeRuntime()
    runtime.current_url = sample_page

    snapshot = BrowserObserver(ElementIndexer()).observe(runtime)

    assert snapshot.url == sample_page
    assert snapshot.elements[0].element_id == "el-1"
    assert snapshot.elements[0].tag == "button"
    assert snapshot.elements[0].text == "Search"
    assert "interactive_elements=1" in snapshot.summary
