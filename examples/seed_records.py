"""Example records so the store does something on first run.

These are deliberately generic: three sources and two concepts, where the
concepts cite the sources by id. Running ``governed-memory seed`` writes them
to the canonical log; ``rebuild`` then projects them and ``verify`` confirms
every citation resolves.

Nothing here is personal data. It is scaffolding you are meant to delete once
your own records exist.
"""

from __future__ import annotations

from pathlib import Path

from governed_memory.records import MemoryRecord
from governed_memory.store import append_record


def build_records() -> list[MemoryRecord]:
    """Return a small, internally-consistent set of example records."""

    source_a = MemoryRecord(
        type="source",
        title="Append-only logs as a system of record",
        summary=(
            "Write events once and never mutate them; derive every read view "
            "from the log so state is reconstructable and auditable."
        ),
        body=(
            "An append-only log keeps the full history of changes. Read models "
            "are projections you can drop and rebuild without losing truth."
        ),
        sensitivity="public",
        tags=["architecture", "logs", "event-sourcing"],
    )
    source_b = MemoryRecord(
        type="source",
        title="Full-text search with SQLite FTS5",
        summary=(
            "FTS5 gives ranked full-text search in a single embedded file, with "
            "no server and no external dependency."
        ),
        body=(
            "FTS5 is a virtual-table module shipped with SQLite. bm25() ranking "
            "lets you order matches by relevance against indexed columns."
        ),
        sensitivity="public",
        tags=["sqlite", "search", "fts5"],
    )
    source_c = MemoryRecord(
        type="source",
        title="Citations as verifiable edges",
        summary=(
            "Treat a citation as a graph edge that must resolve; an unresolved "
            "edge is an unsupported claim, not a stylistic flaw."
        ),
        body=(
            "When a derived answer cites a source, the source must exist. "
            "Checking that mechanically turns a soft prompt rule into a gate."
        ),
        sensitivity="public",
        tags=["memory", "citations", "integrity"],
    )

    concept_navigation = MemoryRecord(
        type="concept",
        title="Summary-first navigation scales sublinearly",
        summary=(
            "Indexing summaries instead of full bodies lets a reader decide what "
            "to open before paying the token cost, so retrieval cost grows with "
            "the number of summaries, not total content."
        ),
        body=(
            "The index covers title, summary and tags — never body. A query "
            "reads cheap navigation text first and opens a body only on demand."
        ),
        sensitivity="public",
        sources=[source_a.id, source_b.id],
        tags=["memory", "retrieval", "design"],
    )
    concept_gate = MemoryRecord(
        type="concept",
        title="A memory layer earns the word 'memory' only if it verifies",
        summary=(
            "Durable artifacts plus a derived index are necessary but not "
            "sufficient; without a hard verification gate the system produces "
            "confident, rare, and unreviewable failures."
        ),
        body=(
            "Verification checks two things: every citation resolves, and the "
            "derived index matches the canonical log. Both are build-breaking."
        ),
        sensitivity="public",
        sources=[source_c.id, concept_navigation.id],
        tags=["memory", "integrity", "verification"],
    )

    return [source_a, source_b, source_c, concept_navigation, concept_gate]


def seed(memory_dir: Path) -> int:
    """Append the example records to the canonical log. Return the count."""

    records = build_records()
    for record in records:
        append_record(record, memory_dir)
    return len(records)


if __name__ == "__main__":
    written = seed(Path("data/memory"))
    print(f"seeded {written} record(s)")
