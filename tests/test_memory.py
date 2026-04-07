from app.agent.models import CriticResult
from app.browser.snapshot import PageSnapshot
from app.memory.history import ActionRecord
from app.memory.store import StateStore
from app.tools.base import ToolResult


def test_state_store_tracks_snapshot_actions_and_report() -> None:
    store = StateStore()
    state = store.initialize(task="https://example.com", max_steps=3)
    snapshot = PageSnapshot(url="https://example.com", title="Example", summary="ready")

    store.attach_snapshot(state, snapshot)
    store.record_action(
        state,
        ActionRecord(
            step=1,
            action_name="open_url",
            action_args={"url": "https://example.com"},
            before_url="",
            after_url="https://example.com",
            success=True,
            message="opened",
        ),
    )
    store.merge_tool_data(state, ToolResult(success=True, message="ok", data={"texts": ["hello"]}))
    store.apply_review(
        state,
        CriticResult(action_succeeded=True, is_terminal=True, message="done"),
        snapshot,
    )

    assert state.current_url == "https://example.com"
    assert state.visited_urls == ["https://example.com"]
    assert state.step_count == 1
    assert state.extracted_data == {"texts": ["hello"]}
    assert state.done is True
    assert "Task: https://example.com" in state.final_report
    assert "Extracted keys: ['texts']" in state.final_report


def test_state_store_does_not_duplicate_visited_urls_or_empty_data() -> None:
    store = StateStore()
    state = store.initialize(task="task")
    snapshot = PageSnapshot(url="https://example.com", title="", summary="")

    store.attach_snapshot(state, snapshot)
    store.attach_snapshot(state, snapshot)
    store.merge_tool_data(state, ToolResult(success=True, message="ok"))

    assert state.visited_urls == ["https://example.com"]
    assert state.extracted_data == {}
