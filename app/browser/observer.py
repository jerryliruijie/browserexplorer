"""Browser observation and snapshot construction."""

from __future__ import annotations

from app.browser.element_indexer import ElementIndexer
from app.browser.runtime import BrowserRuntime
from app.browser.snapshot import PageSnapshot


class BrowserObserver:
    """Build planner-facing snapshots from runtime state."""

    def __init__(self, indexer: ElementIndexer | None = None) -> None:
        self.indexer = indexer or ElementIndexer()

    def observe(self, runtime: BrowserRuntime) -> PageSnapshot:
        elements = self.indexer.build(runtime.raw_elements)
        visible_texts = runtime.extract_text()
        summary = self._summarize(runtime.current_url, runtime.title, visible_texts, elements)
        return PageSnapshot(
            url=runtime.current_url,
            title=runtime.title,
            elements=elements,
            visible_texts=visible_texts[:20],
            structured_candidates=[],
            summary=summary,
        )

    @staticmethod
    def _summarize(url: str, title: str, visible_texts: list[str], elements: list[object]) -> str:
        return (
            f"url={url or 'unknown'}; title={title or 'unknown'}; "
            f"texts={len(visible_texts)}; interactive_elements={len(elements)}"
        )

