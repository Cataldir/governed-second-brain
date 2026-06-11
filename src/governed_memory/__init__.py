"""governed_memory — an append-only memory store with a derived, verifiable index.

This package is the *execution plane* of the reference architecture. It is the
working part you can run. Everything around it — the governance instructions,
the ADRs, the schema — exists to keep this honest.

The boundary it enforces:

- canonical state is append-only JSONL on disk (the authority plane);
- the SQLite/FTS5 database is a *derived* projection you can delete and rebuild;
- verification is a hard gate, not a prompt suggestion;
- every record carries a sensitivity class.

Nothing here needs a third-party dependency. A memory layer should not fall
over because a pip install did.
"""

from governed_memory.records import (
    ALLOWED_SENSITIVITY,
    RESTRICTED_SENSITIVITY,
    MemoryRecord,
    RecordValidationError,
)

__all__ = [
    "ALLOWED_SENSITIVITY",
    "RESTRICTED_SENSITIVITY",
    "MemoryRecord",
    "RecordValidationError",
]
