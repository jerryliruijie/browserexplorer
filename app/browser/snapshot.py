"""Compressed page snapshot models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ElementInfo(BaseModel):
    """Compressed representation of an interactive element."""

    element_id: str
    tag: str
    role: str | None = None
    text: str = ""
    aria_label: str | None = None
    placeholder: str | None = None
    is_visible: bool = True
    is_clickable: bool = False


class PageSnapshot(BaseModel):
    """Planner-facing page snapshot."""

    url: str
    title: str
    elements: list[ElementInfo] = Field(default_factory=list)
    visible_texts: list[str] = Field(default_factory=list)
    structured_candidates: list[dict[str, str]] = Field(default_factory=list)
    summary: str = ""

