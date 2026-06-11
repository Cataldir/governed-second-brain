# ADR-002 — Authority-plane sub-layers and Managed Files

- Status: accepted
- Date: 2025

## Context

"Put the data in `data/`" is not enough. Inside the authority plane, three kinds
of file behave very differently and must not be edited the same way:

- a **schema** is a contract you revise deliberately;
- the **record log** is history you must never rewrite;
- the **search index** is a projection you must never hand-edit.

Treating them uniformly leads to the two classic failures: someone rewrites
history to "fix" a typo, or someone edits the derived index directly and it
silently diverges from the log.

## Decision

Split the authority plane into three sub-layers, each with its own edit rule.

| Sub-layer | Example | Edit rule |
| --- | --- | --- |
| Source records | `data/domains/memory-record.schema.json` | Edit directly, with review. |
| Governed append-only outputs | `data/memory/*.jsonl` | Append only. Never rewrite. Compaction writes a new file. |
| Derived indexes | `data/indexes/memory.sqlite` | Never hand-edit. Regenerate from the source. |

Define a **Managed File**: any file automation maintains and a human must not
hand-edit. Every Managed File must be declared in
[`ownership-taxonomy.md`](../../../.github/ownership-taxonomy.md) with four
fields: canonical source, regeneration entrypoint, drift-check, and failure mode.
A change that touches a Managed File must run its drift-check and regenerate it
if it drifted.

## Consequences

- The append-only rule makes history auditable and makes the log a trustworthy
  source for rebuilding any derived view.
- The "derived files are regenerated, never patched" rule, plus a drift-check
  (`verify`), means divergence between the index and the log is caught
  mechanically instead of discovered later as a wrong answer.
- The cost is that fixing a mistake in the log is done by *appending a
  correction*, not by editing the past — which is the point.

## Enforcement

Backed by the write path in `src/governed_memory/store.py` (append-only, fsync
ordering, restricted gate), the rebuild in `index.py`, and the drift-check in
`verify.py`. The
[`sqlite-read-model-boundary.instructions.md`](../../../.github/instructions/sqlite-read-model-boundary.instructions.md)
states the operational rule for agents.
