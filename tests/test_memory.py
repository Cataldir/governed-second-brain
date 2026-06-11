"""Tests for the governed-memory store.

These exercise the parts that matter: validation refuses bad records, the
restricted-sensitivity gate holds, the index round-trips the log, and the
verifier catches a dangling citation. The verifier test is the important one —
it proves the gate actually fails, rather than printing a warning nobody reads.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from governed_memory.index import rebuild_index
from governed_memory.query import query
from governed_memory.records import MemoryRecord, RecordValidationError
from governed_memory.store import append_record, iter_records
from governed_memory.verify import verify
from examples.seed_records import seed


def test_validation_rejects_empty_summary() -> None:
    record = MemoryRecord(type="source", title="x", summary="   ")
    with pytest.raises(RecordValidationError):
        record.validate()


def test_source_cannot_declare_sources() -> None:
    record = MemoryRecord(
        type="source", title="x", summary="y", sources=["some-id"]
    )
    with pytest.raises(RecordValidationError):
        record.validate()


def test_restricted_write_requires_acknowledgement(tmp_path: Path) -> None:
    record = MemoryRecord(
        type="source", title="secret", summary="s", sensitivity="restricted"
    )
    with pytest.raises(RecordValidationError):
        append_record(record, tmp_path / "memory")
    saved = append_record(
        record, tmp_path / "memory", acknowledge_restricted=True
    )
    assert saved.sensitivity == "restricted"
    assert list(iter_records(tmp_path / "memory"))[0].id == saved.id


def test_seed_rebuild_query_roundtrip(tmp_path: Path) -> None:
    memory_dir = tmp_path / "memory"
    db_path = tmp_path / "indexes" / "memory.sqlite"

    written = seed(memory_dir)
    assert written == 5

    count = rebuild_index(memory_dir, db_path)
    assert count == written

    result = verify(memory_dir, db_path)
    assert result.ok, str(result)

    hits = query(db_path, "summary navigation", limit=5)
    assert hits, "expected at least one summary-first hit"
    # The first hit returns a summary, never a body, unless explicitly opened.
    assert hits[0].body is None


def test_verify_catches_dangling_citation(tmp_path: Path) -> None:
    memory_dir = tmp_path / "memory"
    db_path = tmp_path / "indexes" / "memory.sqlite"

    real_source = MemoryRecord(type="source", title="real", summary="exists")
    append_record(real_source, memory_dir)

    # A concept that cites a source id that was never written.
    dangling = MemoryRecord(
        type="concept",
        title="broken",
        summary="cites nothing real",
        sources=["does-not-exist"],
    )
    append_record(dangling, memory_dir)

    rebuild_index(memory_dir, db_path)
    result = verify(memory_dir, db_path)
    assert not result.ok
    assert any("does-not-exist" in error for error in result.errors)
