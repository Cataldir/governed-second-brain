"""Tests for the visibility floor on the read path.

These prove the private-to-public boundary is enforced by code, not just by a
label: a non-public body is redacted unless an explicit reveal flag is passed,
while a public body opens freely and summaries always flow.
"""

from __future__ import annotations

from pathlib import Path

from governed_memory.index import rebuild_index
from governed_memory.query import query
from governed_memory.records import MemoryRecord
from governed_memory.store import append_record


def _build(tmp_path: Path) -> Path:
    memory_dir = tmp_path / "memory"
    db_path = tmp_path / "indexes" / "memory.sqlite"
    append_record(
        MemoryRecord(
            type="source",
            title="Public note",
            summary="open summary",
            body="public body text",
            sensitivity="public",
            tags=["visibility"],
        ),
        memory_dir,
    )
    append_record(
        MemoryRecord(
            type="source",
            title="Private note",
            summary="private summary",
            body="private body text",
            sensitivity="private",
            tags=["visibility"],
        ),
        memory_dir,
    )
    rebuild_index(memory_dir, db_path)
    return db_path


def _by_sensitivity(hits, sensitivity):
    return next(h for h in hits if h.sensitivity == sensitivity)


def test_public_body_opens_without_reveal(tmp_path: Path) -> None:
    db_path = _build(tmp_path)
    hits = query(db_path, "visibility", open_body=True)
    public = _by_sensitivity(hits, "public")
    assert public.body == "public body text"
    assert public.redacted is False


def test_private_body_redacted_without_reveal(tmp_path: Path) -> None:
    db_path = _build(tmp_path)
    hits = query(db_path, "visibility", open_body=True)
    private = _by_sensitivity(hits, "private")
    assert private.body is None
    assert private.redacted is True
    # The summary still flows — only the body is withheld.
    assert private.summary == "private summary"


def test_private_body_opens_with_reveal(tmp_path: Path) -> None:
    db_path = _build(tmp_path)
    hits = query(db_path, "visibility", open_body=True, reveal=True)
    private = _by_sensitivity(hits, "private")
    assert private.body == "private body text"
    assert private.redacted is False


def test_reveal_without_open_body_returns_no_body(tmp_path: Path) -> None:
    db_path = _build(tmp_path)
    # reveal authorises a non-public body, but bodies are only fetched at all
    # when open_body is set. No body is leaked by reveal alone.
    hits = query(db_path, "visibility", reveal=True)
    assert all(h.body is None for h in hits)
    assert all(h.redacted is False for h in hits)
