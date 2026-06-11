"""A worked weekly-review loop, runnable end to end.

This is the proof that the pieces compose: an active plan becomes daily notes,
notes become cited records, the index makes them findable, a review decides what
graduates, and the work advances through its lifecycle with evidence — all
without rewriting history.

Run it against a throwaway directory so it never touches your real store:

    python -m examples.weekly_review

It prints each step. Nothing here is personal data; delete it once your own
loop exists.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from governed_memory.events import current_status, record_transition
from governed_memory.index import rebuild_index
from governed_memory.query import query
from governed_memory.records import MemoryRecord
from governed_memory.store import append_record
from governed_memory.verify import verify


def run(base: Path) -> None:
    memory_dir = base / "memory"
    state_dir = base / "state"
    db_path = base / "indexes" / "memory.sqlite"

    # 1. The week produced two notes. One is a public source we can cite; the
    #    other is a private working note that must not be quoted in public.
    print("== step 1: capture the week's notes ==")
    source = append_record(
        MemoryRecord(
            type="source",
            title="Append-only state logs",
            summary="Record transitions as events so 'why is this published?' is answerable.",
            body="Public reference text, safe to quote.",
            sensitivity="public",
            tags=["state", "event-sourcing"],
        ),
        memory_dir,
    )
    append_record(
        MemoryRecord(
            type="concept",
            title="Our review cadence works because the gate is cheap",
            summary="Weekly rebuild+verify keeps the index honest at low cost.",
            body="Private working note — restate the idea, never paste this verbatim.",
            sensitivity="private",
            sources=[source.id],
            tags=["process", "review"],
        ),
        memory_dir,
    )
    print(f"  wrote source {source.id} and one private concept")

    # 2. Project and verify. A review on a broken index is theatre.
    print("== step 2: rebuild and verify ==")
    count = rebuild_index(memory_dir, db_path)
    result = verify(memory_dir, db_path)
    print(f"  indexed {count} record(s); verify ok={result.ok}")
    assert result.ok, result.errors

    # 3. Survey summary-first. The private body stays redacted unless revealed.
    print("== step 3: survey, summary-first, no reveal ==")
    for hit in query(db_path, "state review", open_body=True):
        flag = " (redacted)" if hit.redacted else ""
        print(f"  [{hit.sensitivity}] {hit.title}{flag}")

    # 4. Advance the work, with evidence. Illegal jumps are refused.
    print("== step 4: advance the work with evidence ==")
    entity = "post:weekly-review"
    record_transition(entity, "drafted", state_dir, evidence=["data/memory"])
    record_transition(
        entity, "audited", state_dir, evidence=["verify: ok"], note="index green"
    )
    try:
        # Skipping straight to published (no submission) must be refused.
        record_transition(entity, "published", state_dir)
    except Exception as exc:  # noqa: BLE001 — demonstrating the guardrail
        print(f"  refused illegal jump: {exc}")
    record_transition(entity, "submitted", state_dir, evidence=["sent: 2025"])
    record_transition(entity, "published", state_dir, evidence=["url: example"])
    print(f"  current status of {entity}: {current_status(state_dir, entity)}")


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        run(Path(tmp))
    print("\ndone — throwaway store discarded.")


if __name__ == "__main__":
    main()
