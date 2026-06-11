"""Tests for semantic and hybrid retrieval over the index.

These prove that an embedded index serves semantic and hybrid modes, that those
modes still honour the redaction floor, that a vector index stays consistent
under verify, and that asking for semantic recall without vectors fails loudly
rather than silently returning lexical results.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from governed_memory.index import rebuild_index
from governed_memory.embeddings import default_embedder
from governed_memory.query import query
from governed_memory.records import MemoryRecord
from governed_memory.store import append_record
from governed_memory.verify import verify


def _seed(memory_dir: Path) -> None:
    append_record(
        MemoryRecord(
            type="source",
            title="Append-only change log",
            summary="Record every change as an event and never rewrite history.",
            body="public body",
            sensitivity="public",
            tags=["log", "audit"],
        ),
        memory_dir,
    )
    append_record(
        MemoryRecord(
            type="source",
            title="Private retrospective",
            summary="Internal notes on the change log audit cadence.",
            body="private body text",
            sensitivity="private",
            tags=["audit"],
        ),
        memory_dir,
    )


def _build(tmp_path: Path, *, embed: bool) -> Path:
    memory_dir = tmp_path / "memory"
    db_path = tmp_path / "indexes" / "memory.sqlite"
    _seed(memory_dir)
    embedder = default_embedder() if embed else None
    rebuild_index(memory_dir, db_path, embedder=embedder)
    return db_path


def test_embedded_index_verifies(tmp_path: Path) -> None:
    db_path = _build(tmp_path, embed=True)
    result = verify(tmp_path / "memory", db_path)
    assert result.ok, str(result)


def test_semantic_mode_returns_hits(tmp_path: Path) -> None:
    db_path = _build(tmp_path, embed=True)
    hits = query(db_path, "change log audit", mode="semantic")
    assert hits, "expected semantic hits from an embedded index"


def test_hybrid_mode_returns_hits(tmp_path: Path) -> None:
    db_path = _build(tmp_path, embed=True)
    hits = query(db_path, "change log audit", mode="hybrid")
    assert hits


def test_semantic_mode_honours_redaction(tmp_path: Path) -> None:
    db_path = _build(tmp_path, embed=True)
    hits = query(db_path, "change log audit", mode="semantic", open_body=True)
    private = next(h for h in hits if h.sensitivity == "private")
    assert private.body is None
    assert private.redacted is True
    # And it opens only with an explicit reveal.
    revealed = query(
        db_path, "change log audit", mode="semantic", open_body=True, reveal=True
    )
    private_revealed = next(h for h in revealed if h.sensitivity == "private")
    assert private_revealed.body == "private body text"


def test_semantic_without_vectors_fails_loudly(tmp_path: Path) -> None:
    db_path = _build(tmp_path, embed=False)
    with pytest.raises(ValueError, match="no vectors"):
        query(db_path, "anything", mode="semantic")


def test_verify_catches_vector_drift(tmp_path: Path) -> None:
    import sqlite3

    db_path = _build(tmp_path, embed=True)
    # Simulate a half-embedded index by deleting one record's vector.
    connection = sqlite3.connect(db_path)
    try:
        ids = [row[0] for row in connection.execute("SELECT id FROM vectors")]
        connection.execute("DELETE FROM vectors WHERE id = ?", (ids[0],))
        connection.commit()
    finally:
        connection.close()
    result = verify(tmp_path / "memory", db_path)
    assert not result.ok
    assert any("vector" in error for error in result.errors)
