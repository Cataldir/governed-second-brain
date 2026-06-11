"""Summary-first retrieval against the derived index.

A query reads the navigation layer first: it matches against title, summary
and tags, and returns the summary. The body is only fetched when the caller
explicitly asks for it. This is the whole reason the index is cheap to read:
you decide what to open *before* paying for it.

There is a second, editorial boundary layered on top of the summary-first one:
**a body is never returned for a non-public record unless the caller explicitly
reveals it.** Public records open freely; ``private`` and ``restricted`` records
return their summary and are marked ``redacted`` until ``reveal=True`` is passed.
This is the read-path half of the private-to-public rule — it makes leaking a
private body into a public draft an explicit act, not an accident of a smooth
autocomplete.

Three retrieval modes share that same redaction floor:

- ``lexical`` (default) — FTS5 keyword match. Always available, dependency-free.
- ``semantic`` — vector similarity over the summary embeddings. Requires an
  index built with an embedder (``rebuild --embed``).
- ``hybrid`` — both signals fused with reciprocal rank fusion, so a record can
  surface either because it shares words or because it is close in meaning.

Every mode embeds and ranks over navigation text only; bodies are never part of
the vector space, so semantic recall cannot bypass the visibility floor.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from governed_memory.embeddings import (
    Embedder,
    cosine,
    embedder_from_meta,
    unpack_vector,
)

PUBLIC_SENSITIVITY = "public"

Mode = Literal["lexical", "semantic", "hybrid"]

# How many candidates each signal contributes before fusion / truncation.
_POOL_FLOOR = 20
# Reciprocal-rank-fusion constant; the standard dampener that stops rank 1 from
# dominating outright.
_RRF_K = 60


@dataclass(slots=True)
class QueryHit:
    """One retrieval result, summary-first."""

    id: str
    type: str
    title: str
    summary: str
    sensitivity: str
    body: str | None = None
    redacted: bool = False

    def render(self) -> str:
        head = f"[{self.type} · {self.sensitivity}] {self.title}"
        lines = [head, f"  {self.summary}"]
        if self.redacted:
            lines.append("  --- body redacted (non-public; pass reveal to open) ---")
        elif self.body is not None:
            lines.append("  ---")
            lines.extend(f"  {line}" for line in self.body.splitlines())
        return "\n".join(lines)


def _fts_query(text: str) -> str:
    # Quote each term so punctuation in user input cannot break the MATCH syntax.
    terms = [t for t in text.replace('"', " ").split() if t]
    return " OR ".join(f'"{term}"' for term in terms) if terms else '""'


def _lexical_ids(connection: sqlite3.Connection, text: str, pool: int) -> list[str]:
    rows = connection.execute(
        """
        SELECT f.id
        FROM records_fts f
        WHERE records_fts MATCH ?
        ORDER BY bm25(records_fts)
        LIMIT ?
        """,
        (_fts_query(text), pool),
    ).fetchall()
    return [row[0] for row in rows]


def _resolve_embedder(
    connection: sqlite3.Connection, embedder: Embedder | None
) -> Embedder:
    if embedder is not None:
        return embedder
    meta = {
        row[0]: row[1]
        for row in connection.execute("SELECT key, value FROM meta")
    }
    name = meta.get("embedder")
    if name is None:
        raise ValueError(
            "this index has no vectors — run 'governed-memory rebuild --embed' "
            "first, or use mode='lexical'"
        )
    return embedder_from_meta(name, int(meta["embedder_dim"]))


def _semantic_ids(
    connection: sqlite3.Connection,
    text: str,
    pool: int,
    embedder: Embedder | None,
) -> list[str]:
    resolved = _resolve_embedder(connection, embedder)
    query_vector = resolved.embed([text])[0]
    scored: list[tuple[float, str]] = []
    for row in connection.execute("SELECT id, vector FROM vectors"):
        score = cosine(query_vector, unpack_vector(row[1]))
        if score > 0.0:
            scored.append((score, row[0]))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [identifier for _, identifier in scored[:pool]]


def _rrf_fuse(ranked_lists: list[list[str]], limit: int) -> list[str]:
    """Reciprocal rank fusion: combine ranked id lists into one order."""

    scores: dict[str, float] = {}
    for ranked in ranked_lists:
        for rank, identifier in enumerate(ranked):
            scores[identifier] = scores.get(identifier, 0.0) + 1.0 / (_RRF_K + rank + 1)
    ordered = sorted(scores, key=lambda i: scores[i], reverse=True)
    return ordered[:limit]


def _hits_for_ids(
    connection: sqlite3.Connection,
    ids: list[str],
    *,
    open_body: bool,
    reveal: bool,
) -> list[QueryHit]:
    hits: list[QueryHit] = []
    for identifier in ids:
        row = connection.execute(
            "SELECT id, type, title, summary, sensitivity, body "
            "FROM records WHERE id = ?",
            (identifier,),
        ).fetchone()
        if row is None:
            continue
        is_public = row["sensitivity"] == PUBLIC_SENSITIVITY
        body_authorised = open_body and (is_public or reveal)
        redacted = open_body and not is_public and not reveal
        hits.append(
            QueryHit(
                id=row["id"],
                type=row["type"],
                title=row["title"],
                summary=row["summary"],
                sensitivity=row["sensitivity"],
                body=row["body"] if body_authorised else None,
                redacted=redacted,
            )
        )
    return hits


def query(
    db_path: Path,
    text: str,
    *,
    limit: int = 5,
    open_body: bool = False,
    reveal: bool = False,
    mode: Mode = "lexical",
    embedder: Embedder | None = None,
) -> list[QueryHit]:
    """Return up to ``limit`` hits, summary-first, under the chosen ``mode``.

    ``open_body`` asks for bodies. ``reveal`` authorises bodies of non-public
    records. A non-public body is returned only when *both* are true; otherwise
    the hit is marked ``redacted``.

    ``mode`` selects the recall signal: ``lexical`` (FTS, default), ``semantic``
    (vector similarity) or ``hybrid`` (both, fused). ``semantic`` and ``hybrid``
    require an index built with an embedder; otherwise a ``ValueError`` explains
    how to build one.
    """

    if not db_path.exists():
        raise FileNotFoundError(f"index {db_path} does not exist — run rebuild")

    pool = max(limit, _POOL_FLOOR)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        if mode == "lexical":
            ids = _lexical_ids(connection, text, limit)
        elif mode == "semantic":
            ids = _semantic_ids(connection, text, limit, embedder)
        elif mode == "hybrid":
            lexical = _lexical_ids(connection, text, pool)
            semantic = _semantic_ids(connection, text, pool, embedder)
            ids = _rrf_fuse([lexical, semantic], limit)
        else:  # pragma: no cover - guarded by the Mode type
            raise ValueError(f"unknown mode {mode!r}")

        return _hits_for_ids(
            connection, ids, open_body=open_body, reveal=reveal
        )
    finally:
        connection.close()

