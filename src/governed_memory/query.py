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
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

PUBLIC_SENSITIVITY = "public"


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


def query(
    db_path: Path,
    text: str,
    *,
    limit: int = 5,
    open_body: bool = False,
    reveal: bool = False,
) -> list[QueryHit]:
    """Return up to ``limit`` hits, summary-first, ordered by FTS relevance.

    ``open_body`` asks for bodies. ``reveal`` authorises bodies of non-public
    records. A non-public body is returned only when *both* are true; otherwise
    the hit is marked ``redacted``.
    """

    if not db_path.exists():
        raise FileNotFoundError(f"index {db_path} does not exist — run rebuild")

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT r.id, r.type, r.title, r.summary, r.sensitivity, r.body
            FROM records_fts f
            JOIN records r ON r.id = f.id
            WHERE records_fts MATCH ?
            ORDER BY bm25(records_fts)
            LIMIT ?
            """,
            (_fts_query(text), limit),
        ).fetchall()
    finally:
        connection.close()

    hits: list[QueryHit] = []
    for row in rows:
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
