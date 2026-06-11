"""Tests for the state event layer.

These prove the three properties that make a state log more than a status field:

1. an entity must enter at the initial status;
2. a transition not allowed from the current status is refused;
3. evidence and history are recorded append-only and replayable.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from governed_memory.events import (
    TransitionError,
    current_status,
    iter_events,
    record_transition,
)


def test_first_event_must_be_initial_status(tmp_path: Path) -> None:
    state_dir = tmp_path / "state"
    with pytest.raises(TransitionError):
        record_transition("post:x", "published", state_dir)
    # Entering at the initial status is allowed.
    event = record_transition("post:x", "drafted", state_dir)
    assert event.from_status is None
    assert event.to_status == "drafted"


def test_illegal_transition_is_refused(tmp_path: Path) -> None:
    state_dir = tmp_path / "state"
    record_transition("post:x", "drafted", state_dir)
    # drafted -> published skips the audit and submission steps.
    with pytest.raises(TransitionError):
        record_transition("post:x", "published", state_dir)
    assert current_status(state_dir, "post:x") == "drafted"


def test_legal_lifecycle_records_evidence(tmp_path: Path) -> None:
    state_dir = tmp_path / "state"
    record_transition("post:x", "drafted", state_dir)
    record_transition("post:x", "audited", state_dir, evidence=["verify: ok"])
    record_transition("post:x", "submitted", state_dir, evidence=["sent"])
    final = record_transition("post:x", "published", state_dir, evidence=["url"])

    assert final.to_status == "published"
    assert current_status(state_dir, "post:x") == "published"

    events = list(iter_events(state_dir))
    assert len(events) == 4
    assert events[1].evidence == ["verify: ok"]
    # The log is append-only: every transition is preserved in order.
    assert [e.to_status for e in events] == [
        "drafted",
        "audited",
        "submitted",
        "published",
    ]


def test_unknown_status_is_refused(tmp_path: Path) -> None:
    state_dir = tmp_path / "state"
    with pytest.raises(TransitionError):
        record_transition("post:x", "nonsense", state_dir)
