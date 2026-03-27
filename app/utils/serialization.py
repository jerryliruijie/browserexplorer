"""Serialization helpers."""

from __future__ import annotations

import json
from typing import Any


def to_pretty_json(data: dict[str, Any]) -> str:
    """Serialize data in a stable human-readable form."""
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True)
