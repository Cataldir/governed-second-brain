# Architecture

This reference architecture demonstrates one idea: **a memory layer earns the
word "memory" only when it separates canonical records from derived views and
keeps both honest with an executable contract.**

```mermaid
flowchart LR
    subgraph authority["Authority plane (data/)"]
        log["memory/*.jsonl<br/>append-only · canonical"]
        idx["indexes/memory.sqlite<br/>derived · disposable"]
    end
    subgraph execution["Execution plane (src/)"]
        write["store.append"]
        rebuild["index.rebuild"]
        verify["verify (gate)"]
        query["query (summary-first)"]
    end
    write -->|fsync| log
    log -->|project| rebuild --> idx
    log --> verify
    idx --> verify
    idx --> query
```

## The flow

1. **Write** validates a record and appends it to the JSONL log, fsynced before
   returning. The log is the system of record.
2. **Rebuild** projects the entire log into a SQLite/FTS5 index. The index is
   derived: delete it and rebuild, and you have lost nothing.
3. **Verify** is the gate. It fails the build if any citation dangles or if the
   index and the log disagree.
4. **Query** reads the index summary-first, opening a body only on demand.

## Why this shape

The promise of an "AI second brain" usually breaks in one of three places: notes
pile up faster than they can be navigated; a citation rule lives in a prompt and
fails confidently; or a derived view drifts from its source and nobody notices.
This architecture answers each with structure rather than hope — a summary-first
index, a verifier, and a strict append-only/derived split.

## Decision records

- [ADR-001 — Four-plane governance boundary](adr/ADR-001-four-plane-governance-boundary.md)
- [ADR-002 — Authority-plane sub-layers and Managed Files](adr/ADR-002-authority-plane-sublayers-and-managed-files.md)
