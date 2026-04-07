from app.browser.element_indexer import ElementIndexer
from app.browser.observer import BrowserObserver


class FakeRuntime:
    def __init__(self) -> None:
        self.current_url = "https://example.com"
        self.title = "Example"
        self.raw_elements = [
            {
                "tag": "button",
                "role": "button",
                "text": "Search",
                "aria_label": "",
                "placeholder": None,
                "is_visible": True,
                "is_clickable": True,
            }
        ]

    def extract_text(self) -> list[str]:
        return ["Alpha", "Beta"]


def test_element_indexer_normalizes_optional_text_values() -> None:
    indexed = ElementIndexer().build(
        [
            {
                "tag": "input",
                "role": "",
                "text": "Query",
                "aria_label": None,
                "placeholder": False,
                "is_visible": True,
                "is_clickable": True,
            }
        ]
    )

    assert indexed[0].element_id == "el-1"
    assert indexed[0].role is None
    assert indexed[0].aria_label is None
    assert indexed[0].placeholder == "False"


def test_browser_observer_builds_summary_from_runtime_state() -> None:
    snapshot = BrowserObserver(ElementIndexer()).observe(FakeRuntime())

    assert snapshot.url == "https://example.com"
    assert snapshot.title == "Example"
    assert snapshot.visible_texts == ["Alpha", "Beta"]
    assert snapshot.elements[0].element_id == "el-1"
    assert "texts=2" in snapshot.summary
    assert "interactive_elements=1" in snapshot.summary
