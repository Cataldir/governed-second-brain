"""The changing-workflow-state layer.

This is the third storage shape the blog's vocabulary insists on, and the one a
plain memory store usually omits:

    source   — what we are producing or deciding (records.py / memory log)
    state    — where it is in a process (this module / state log)
    index    — how tools find it fast (index.py)
    evidence — what happened, when, by which path (the event itself)

A *record* is a durable artifact. A *state event* is a transition: an entity
moving from one status to the next, at a time, with evidence. Collapsing the two
is the classic mistake — it turns a status correction into something
indistinguishable from a content revision. Here they are different files with
different rules:

- memory records live in ``data/memory/`` (append-only canonical artifacts);
- state events live in ``data/state/`` (append-only transitions).

A transition is only recorded if it is *allowed from the current status*. That
single check is what separates a governed state machine from a free-text status
field an agent can scribble anything into.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

# A deliberately small, example-grounded workflow: the publishing lifecycle the
# blog post uses. Replace the map with your own; the engine is generic.
#
# Keys are statuses; values are the statuses you may transition *to*.
PUBLISHING_TRANSITIONS: dict[str, frozenset[str]] = {
    "drafted": frozenset({"audited", "abandoned"}),
    "audited": frozenset({"submitted", "drafted"}),
    "submitted": frozenset({"published", "rejected"}),
    "rejected": frozenset({"drafted", "abandoned"}),
    "published": frozenset(),  # terminal
    "abandoned": frozenset(),  # terminal
}
INITIAL_STATUS = "drafted"


class TransitionError(ValueError):
    """Raised when a transition is not allowed from the current status."""


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class StateEvent:
    """One transition of one entity, with evidence.

    ``evidence`` is a free-form list of references — file paths, URLs, message
    ids, audit-report paths — that justify the transition. It is the answer to
    the question future-you asks with mild irritation: "why is this marked this
    way?"
    """

    entity: str
    to_status: str
    from_status: str | None = None
    evidence: list[str] = field(default_factory=list)
    note: str = ""
    timestamp: str = field(default_factory=_now_iso)

    def to_json(self) -> dict[str, object]:
        return {
            "timestamp": self.timestamp,
            "entity": self.entity,
            "from_status": self.from_status,
            "to_status": self.to_status,
            "evidence": list(self.evidence),
            "note": self.note,
        }

    @classmethod
    def from_json(cls, payload: dict[str, object]) -> StateEvent:
        return cls(
            timestamp=str(payload["timestamp"]),
            entity=str(payload["entity"]),
            from_status=(
                str(payload["from_status"])
                if payload.get("from_status") is not None
                else None
            ),
            to_status=str(payload["to_status"]),
            evidence=list(payload.get("evidence", [])),  # type: ignore[arg-type]
            note=str(payload.get("note", "")),
        )


def _state_path(state_dir: Path) -> Path:
    return state_dir / "events.jsonl"


def iter_events(state_dir: Path) -> Iterator[StateEvent]:
    """Yield every state event in append order."""

    path = _state_path(state_dir)
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if raw:
                yield StateEvent.from_json(json.loads(raw))


def current_status(state_dir: Path, entity: str) -> str | None:
    """Return the latest status of an entity, or None if it has no events."""

    status: str | None = None
    for event in iter_events(state_dir):
        if event.entity == entity:
            status = event.to_status
    return status


def record_transition(
    entity: str,
    to_status: str,
    state_dir: Path,
    *,
    evidence: list[str] | None = None,
    note: str = "",
    transitions: dict[str, frozenset[str]] | None = None,
) -> StateEvent:
    """Validate and append one transition. Return the recorded event.

    Answers the five questions a transition tool must answer before it writes:
    which entity, what transition, what evidence, is it allowed from the current
    status, and where is it stored. The append is fsynced before returning.
    """

    transitions = transitions or PUBLISHING_TRANSITIONS

    if to_status not in transitions:
        raise TransitionError(
            f"unknown status {to_status!r}; known: {sorted(transitions)}"
        )

    from_status = current_status(state_dir, entity)

    if from_status is None:
        # First event for this entity. It must enter at the initial status.
        if to_status != INITIAL_STATUS:
            raise TransitionError(
                f"{entity!r} has no history; first status must be "
                f"{INITIAL_STATUS!r}, not {to_status!r}"
            )
    else:
        allowed = transitions.get(from_status, frozenset())
        if to_status not in allowed:
            raise TransitionError(
                f"{entity!r} cannot move {from_status!r} -> {to_status!r}; "
                f"allowed from {from_status!r}: {sorted(allowed) or 'none (terminal)'}"
            )

    event = StateEvent(
        entity=entity,
        to_status=to_status,
        from_status=from_status,
        evidence=list(evidence or []),
        note=note,
    )

    state_dir.mkdir(parents=True, exist_ok=True)
    path = _state_path(state_dir)
    line = json.dumps(event.to_json(), ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return event
