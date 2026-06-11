"""Record shape and validation for the governed-memory store.

A record is a single durable artifact. There are two kinds:

- ``source``  — something you ingested (an article, a paper, a transcript);
- ``concept`` — a durable idea that draws on one or more sources.

Concepts cite sources by id. Those citations are the navigation edges the
index uses, and the references the verifier checks. A citation that points at
a record that does not exist is the worst failure mode in a memory system: an
answer that reads as authoritative and is quietly fabricated. The verifier
treats it as a hard error.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

ALLOWED_TYPES = frozenset({"source", "concept"})
ALLOWED_SENSITIVITY = frozenset({"public", "private", "restricted"})
RESTRICTED_SENSITIVITY = frozenset({"restricted"})


class RecordValidationError(ValueError):
    """Raised when a payload violates the record contract."""


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass(slots=True)
class MemoryRecord:
    """A single durable memory artifact.

    ``summary`` is the load-bearing field. It is what the index projects and
    what a reader navigates before paying the token cost of opening ``body``.
    A record with a sloppy summary is a record the index cannot navigate.
    """

    type: str
    title: str
    summary: str
    body: str = ""
    sensitivity: str = "private"
    sources: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    id: str = field(default_factory=_new_id)
    timestamp: str = field(default_factory=_now_iso)

    def validate(self) -> None:
        """Validate the record against the contract. Raise on the first fault."""

        if self.type not in ALLOWED_TYPES:
            raise RecordValidationError(
                f"type must be one of {sorted(ALLOWED_TYPES)}, got {self.type!r}"
            )
        if not self.title.strip():
            raise RecordValidationError("title must not be empty")
        if not self.summary.strip():
            raise RecordValidationError(
                "summary must not be empty — it is the navigation layer"
            )
        if self.sensitivity not in ALLOWED_SENSITIVITY:
            raise RecordValidationError(
                f"sensitivity must be one of {sorted(ALLOWED_SENSITIVITY)}, "
                f"got {self.sensitivity!r}"
            )
        if not isinstance(self.sources, list) or not all(
            isinstance(item, str) for item in self.sources
        ):
            raise RecordValidationError("sources must be a list of record ids")
        if not isinstance(self.tags, list) or not all(
            isinstance(item, str) for item in self.tags
        ):
            raise RecordValidationError("tags must be a list of strings")
        # A source cannot cite other records; only concepts carry edges.
        if self.type == "source" and self.sources:
            raise RecordValidationError("a source record must not declare sources")
        datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))

    @property
    def content_sha256(self) -> str:
        """Stable hash of the durable content, for drift and tamper checks."""

        payload = "\u241f".join(
            [self.type, self.title, self.summary, self.body, self.sensitivity]
            + sorted(self.sources)
            + sorted(self.tags)
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def to_json(self) -> dict[str, Any]:
        """Serialise to a plain dict for JSONL persistence."""

        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type,
            "title": self.title,
            "summary": self.summary,
            "body": self.body,
            "sensitivity": self.sensitivity,
            "sources": list(self.sources),
            "tags": list(self.tags),
            "content_sha256": self.content_sha256,
        }

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> MemoryRecord:
        """Rebuild a record from a persisted dict, ignoring derived fields."""

        return cls(
            id=payload["id"],
            timestamp=payload["timestamp"],
            type=payload["type"],
            title=payload["title"],
            summary=payload["summary"],
            body=payload.get("body", ""),
            sensitivity=payload.get("sensitivity", "private"),
            sources=list(payload.get("sources", [])),
            tags=list(payload.get("tags", [])),
        )
