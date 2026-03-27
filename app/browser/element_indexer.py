"""Element indexing helpers."""

from __future__ import annotations

from app.browser.snapshot import ElementInfo


class ElementIndexer:
    """Assign stable internal ids to observed elements."""

    def build(self, raw_elements: list[dict[str, str | bool | None]]) -> list[ElementInfo]:
        indexed: list[ElementInfo] = []
        for idx, item in enumerate(raw_elements, start=1):
            indexed.append(
                ElementInfo(
                    element_id=f"el-{idx}",
                    tag=str(item.get("tag", "div")),
                    role=self._to_optional_text(item.get("role")),
                    text=str(item.get("text", "")),
                    aria_label=self._to_optional_text(item.get("aria_label")),
                    placeholder=self._to_optional_text(item.get("placeholder")),
                    is_visible=bool(item.get("is_visible", True)),
                    is_clickable=bool(item.get("is_clickable", False)),
                )
            )
        return indexed

    @staticmethod
    def _to_optional_text(value: str | bool | None) -> str | None:
        if value in (None, ""):
            return None
        return str(value)

