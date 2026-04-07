import logging

import pytest

from app.utils.logger import get_logger
from app.utils.retry import retry
from app.utils.serialization import to_pretty_json


def test_to_pretty_json_sorts_keys_and_uses_ascii() -> None:
    payload = {"z": 1, "a": "你好"}

    result = to_pretty_json(payload)

    assert result == '{\n  "a": "\\u4f60\\u597d",\n  "z": 1\n}'


def test_retry_returns_first_successful_result() -> None:
    attempts = {"count": 0}

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise ValueError("try again")
        return "ok"

    assert retry(3, flaky) == "ok"
    assert attempts["count"] == 2


def test_retry_requires_positive_attempt_count() -> None:
    with pytest.raises(RuntimeError, match="at least one attempt"):
        retry(0, lambda: "never called")


def test_get_logger_returns_named_logger() -> None:
    logger = get_logger("browserexplorer.tests")

    assert logger.name == "browserexplorer.tests"
    assert isinstance(logger, logging.Logger)
