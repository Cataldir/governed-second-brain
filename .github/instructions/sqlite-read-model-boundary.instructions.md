---
applyTo: 'data/memory/**,data/indexes/**,src/governed_memory/**,src/governed_memory/mcp_server.py,src/governed_memory/gate.py'
description: Operational boundary for the governed SQLite read model and its MCP write surface.
---
# SQLite read-model boundary

The SQLite database under `data/indexes/` is a **read model**: a derived
projection of the canonical JSONL log. This instruction governs how it may be
created, read, and rebuilt.

## Rules

1. **The log is the truth.** `data/memory/*.jsonl` is append-only and canonical.
   The database is downstream of it, always.
2. **Write order is fixed.** A record is appended and fsynced to JSONL *before*
   it is projected into SQLite. If the process dies in between, a rebuild
   repairs the index. The reverse order can lose the source of truth — forbidden.
3. **Rebuilds are total.** `rebuild` drops and recreates the index from the log.
   There is no incremental in-place mutation that a human is allowed to perform.
4. **No hand edits.** Never open the database and `UPDATE`/`INSERT`/`DELETE` to
   "fix" something. Fix the log, then rebuild.
5. **Drift is a bug.** If `verify` reports the index and the log disagree, the
   index is wrong by definition. Rebuild it.

## Why FTS5 covers summaries, not bodies

The full-text index covers `title`, `summary`, and `tags` — never `body`. This
is deliberate: retrieval reads the cheap navigation layer first and opens a body
only on demand. Indexing bodies would defeat the summary-first design and make
retrieval cost grow with total content instead of with the number of summaries.

## The MCP write surface

The store is also reachable over the Model Context Protocol via
`src/governed_memory/mcp_server.py`. The same rules apply, plus a gate:

- The server is **local stdio only**. It binds no socket and ships no record off
  the machine.
- Mutating tools (`memory.append`, `memory.rebuild`) are **refused by default**.
  They run only when *both* `GOVERNED_MEMORY_ENABLE_WRITE=true` and
  `GOVERNED_MEMORY_REQUIRE_APPROVAL=false` — a deliberate two-flag opt-in.
- The read tool (`memory.query`) is never gated.
- A `restricted` write requires `acknowledge_restricted=true`, enforced by the
  store. See [ADR-003](../../docs/architecture/adr/ADR-003-governed-write-surface.md).
