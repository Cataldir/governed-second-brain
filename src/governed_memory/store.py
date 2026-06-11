"""Append-only JSONL write path — the canonical source of truth.

This is the *authority plane* in code. Records are appended, never rewritten.
History is the point. The SQLite index is derived from these files and can be
deleted at any time; these files cannot.

The write path enforces two things the index cannot:

1. validation — a malformed record never reaches disk;
2. the restricted-sensitivity gate — a ``restricted`` record requires an
   explicit acknowledgement, so sensitive material is never written by accident.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path

from governed_memory.records import (
    RESTRICTED_SENSITIVITY,
    MemoryRecord,
    RecordValidationError,
)


def _monthly_path(memory_dir: Path, record: MemoryRecord) -> Path:
    month = record.timestamp[:7]  # YYYY-MM
    return memory_dir / f"{month}.jsonl"


def append_record(
    record: MemoryRecord,
    memory_dir: Path,
    *,
    acknowledge_restricted: bool = False,
) -> MemoryRecord:
    """Validate, gate, and append one record to the canonical JSONL log.

    The bytes are flushed and fsynced before the function returns. If the
    process dies after this call, the record is durable; the index is repaired
    by a rebuild, not by hand.
    """

    record.validate()
    if record.sensitivity in RESTRICTED_SENSITIVITY and not acknowledge_restricted:
        raise RecordValidationError(
            "writing a 'restricted' record requires acknowledge_restricted=True"
        )

    memory_dir.mkdir(parents=True, exist_ok=True)
    target = _monthly_path(memory_dir, record)
    line = json.dumps(record.to_json(), ensure_ascii=False, sort_keys=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return record


def iter_records(memory_dir: Path) -> Iterator[MemoryRecord]:
    """Yield every record from the canonical log, in file then line order."""

    if not memory_dir.exists():
        return
    for path in sorted(memory_dir.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for raw in handle:
                raw = raw.strip()
                if not raw:
                    continue
                yield MemoryRecord.from_json(json.loads(raw))
