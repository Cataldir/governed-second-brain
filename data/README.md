# Authority plane — `data/`

This plane holds the truth. It has three sub-layers, and they are **not** edited
the same way. Read
[ADR-002](../docs/architecture/adr/ADR-002-authority-plane-sublayers-and-managed-files.md)
before changing anything here.

| Directory | Sub-layer | Edit rule |
| --- | --- | --- |
| [`domains/`](domains/) | Source records (the contract) | Edit with review. |
| `memory/` | Governed append-only output | Append only. Never rewrite a past line. |
| `indexes/` | Derived index (Managed File) | Never hand-edit. Regenerate with `governed-memory rebuild`. |

## `memory/` — the canonical log

Records are stored as JSON Lines, one record per line, in monthly files
(`YYYY-MM.jsonl`). This directory ships empty: the truth is *yours*, not the
template's. Run `governed-memory seed` to populate it with example records, or
`governed-memory write` to add your own.

## `indexes/` — derived, disposable

The SQLite/FTS5 index lives here. It is **git-ignored** on purpose: it is never
the source of truth and is always reconstructable. Delete it and run
`governed-memory rebuild` to get it back, byte-faithful to the log.

## `domains/` — the contract

[`memory-record.schema.json`](domains/memory-record.schema.json) is the formal
shape of a record. If you change it, change the validator in
`src/governed_memory/records.py` in the same commit. The schema and the code that
enforces it must never disagree.
