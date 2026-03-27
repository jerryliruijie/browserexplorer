"""Generic retry helper."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry(times: int, func: Callable[[], T]) -> T:
    """Retry a callback a fixed number of times."""
    last_error: Exception | None = None
    for _ in range(times):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    if last_error is None:
        raise RuntimeError("retry() requires at least one attempt.")
    raise last_error

