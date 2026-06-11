# Execution plane — `src/`

This is the part you can run. Everything else in the repository exists to keep
this code honest.

The only package here is [`governed_memory`](governed_memory/), a dependency-free
memory store:

| Module | Responsibility |
| --- | --- |
| `records.py` | The record contract and validation. |
| `store.py` | Append-only JSONL write path (authority plane in code). |
| `index.py` | Rebuilds the derived SQLite/FTS5 index from the log. |
| `verify.py` | The hard gate: dangling-citation and index-drift checks. |
| `query.py` | Summary-first retrieval against the index. |
| `cli.py` | The `write / rebuild / verify / query / seed` verbs. |

## Rules for this plane

- Code reads from and projects the authority plane (`data/`). It never *is* the
  authority plane. Delete `data/indexes/` and a rebuild restores it; delete
  `data/memory/` and the data is gone.
- Read-model outputs are **derived**. They are regenerated, never hand-edited.
- The verifier is the contract made executable. If you change the record shape,
  change the verifier in the same commit.
