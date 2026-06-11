"""The hard gate.

Most "AI second brain" setups put the citation rule in a prompt and hope the
model follows it. It follows it most of the time, which is worse than never,
because the failures are confident and rare. This module makes the rule a
check that either passes or fails the build.

Two classes of error are fatal:

1. **Dangling citation** — a concept cites a source id that does not exist.
   This is the hallucinated-citation failure made mechanical: if the edge does
   not resolve, the answer that relies on it is unsupported.
2. **Index drift** — the derived SQLite index and the canonical JSONL log
   disagree about which records exist. A projection that has silently diverged
   from its source is a lie the query path will trust.

``verify`` returns a result; the CLI turns a non-empty error list into a
non-zero exit code so it can sit in a hook or a CI step.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from governed_memory.store import iter_records


@dataclass(slots=True)
class VerifyResult:
    """Outcome of a verification pass."""

    ok: bool
    errors: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        if self.ok:
            return "OK — every citation resolves and the index matches the log."
        lines = [f"FAILED with {len(self.errors)} error(s):"]
        lines.extend(f"  - {message}" for message in self.errors)
        return "\n".join(lines)


def verify(memory_dir: Path, db_path: Path) -> VerifyResult:
    """Check referential integrity and index/log consistency."""

    errors: list[str] = []

    records = list(iter_records(memory_dir))
    log_ids = {record.id for record in records}

    # 1. Referential integrity: every cited source must exist.
    for record in records:
        for source_id in record.sources:
            if source_id not in log_ids:
                errors.append(
                    f"{record.type} {record.id} ({record.title!r}) cites "
                    f"missing record {source_id}"
                )

    # 2. Drift: the derived index must match the canonical log exactly.
    if not db_path.exists():
        errors.append(f"index {db_path} does not exist — run rebuild")
    else:
        connection = sqlite3.connect(db_path)
        try:
            index_ids = {
                row[0] for row in connection.execute("SELECT id FROM records")
            }
        finally:
            connection.close()
        for missing in sorted(log_ids - index_ids):
            errors.append(f"record {missing} is in the log but not in the index")
        for orphan in sorted(index_ids - log_ids):
            errors.append(f"record {orphan} is in the index but not in the log")

    return VerifyResult(ok=not errors, errors=errors)
