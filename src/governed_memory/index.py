"""Rebuild the derived SQLite/FTS5 index from the canonical JSONL log.

This module never invents data. It reads the append-only log and projects it
into a database optimised for summary-first navigation. The full-text index
covers ``title``, ``summary`` and ``tags`` — deliberately *not* ``body``, so a
query reads cheap navigation text before deciding whether to open a body.

The index is disposable. Delete the file, run ``rebuild_index`` and you are
back to a faithful projection of the log.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from governed_memory.store import iter_records

SCHEMA = """
CREATE TABLE records (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    body TEXT NOT NULL,
    sensitivity TEXT NOT NULL,
    sources_json TEXT NOT NULL,
    tags_json TEXT NOT NULL,
    content_sha256 TEXT NOT NULL
);

CREATE VIRTUAL TABLE records_fts USING fts5(
    id UNINDEXED,
    title,
    summary,
    tags
);
"""


def _connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA busy_timeout = 5000")
    connection.row_factory = sqlite3.Row
    return connection


def rebuild_index(memory_dir: Path, db_path: Path) -> int:
    """Rebuild the SQLite index from scratch. Return the number of records."""

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    connection = _connect(db_path)
    try:
        connection.executescript(SCHEMA)
        count = 0
        for record in iter_records(memory_dir):
            payload = record.to_json()
            connection.execute(
                """
                INSERT INTO records (
                    id, timestamp, type, title, summary, body,
                    sensitivity, sources_json, tags_json, content_sha256
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["id"],
                    payload["timestamp"],
                    payload["type"],
                    payload["title"],
                    payload["summary"],
                    payload["body"],
                    payload["sensitivity"],
                    json.dumps(payload["sources"]),
                    json.dumps(payload["tags"]),
                    payload["content_sha256"],
                ),
            )
            connection.execute(
                "INSERT INTO records_fts (id, title, summary, tags) VALUES (?, ?, ?, ?)",
                (
                    payload["id"],
                    payload["title"],
                    payload["summary"],
                    " ".join(payload["tags"]),
                ),
            )
            count += 1
        connection.commit()
        return count
    finally:
        connection.close()
