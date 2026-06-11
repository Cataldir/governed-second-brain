# Governance map

This file answers one question: **for a given concern, which file is
authoritative?** When two sources disagree, the one named here wins.

## Authority matrix

| Concern | Authoritative source | Plane |
| --- | --- | --- |
| What an agent may edit, and how | [`instructions/governance-boundary.instructions.md`](instructions/governance-boundary.instructions.md) | Operational |
| Which files are machine-maintained | [`ownership-taxonomy.md`](ownership-taxonomy.md) | Operational |
| How derived read models must behave | [`instructions/sqlite-read-model-boundary.instructions.md`](instructions/sqlite-read-model-boundary.instructions.md) | Operational |
| Whether a non-public body may cross into a public artifact | [`instructions/content-visibility.instructions.md`](instructions/content-visibility.instructions.md) | Operational |
| Whether/how interaction capture happens | [`instructions/interaction-capture.instructions.md`](instructions/interaction-capture.instructions.md) | Operational |
| The shape of a memory record | [`../data/domains/memory-record.schema.json`](../data/domains/memory-record.schema.json) | Authority |
| The canonical record log | `../data/memory/*.jsonl` | Authority |
| The canonical state event log | `../data/state/events.jsonl` | Authority |
| The derived search index | `../data/indexes/memory.sqlite` (regenerated) | Authority |
| How the store actually works | [`../src/governed_memory/`](../src/README.md) | Execution |
| How the store is reached over MCP, and its gate | [`../src/governed_memory/mcp_server.py`](../src/README.md) + [`gate.py`](../src/README.md) | Execution |
| How workflow state transitions are validated | [`../src/governed_memory/events.py`](../src/README.md) | Execution |
| How semantic/hybrid retrieval and embeddings work | [`../src/governed_memory/embeddings.py`](../src/README.md) + [`query.py`](../src/README.md) | Execution |
| Why the architecture is shaped this way | [`../docs/architecture/adr/`](../docs/architecture/README.md) | Contextual |

## Chain of responsibility

1. **Schema** defines the contract.
2. **Validator** (`src/governed_memory/records.py`) enforces the contract on write.
3. **State machine** (`src/governed_memory/events.py`) refuses a transition that
   is not allowed from the entity's current status, and records evidence with it.
4. **Visibility floor** (`src/governed_memory/query.py`) redacts non-public bodies
   on read unless an explicit reveal flag is passed. Vectors are built from
   navigation text only (`src/governed_memory/embeddings.py`), so semantic recall
   never bypasses that floor.
5. **Verifier** (`src/governed_memory/verify.py`) enforces referential integrity,
   index/log consistency, and vector drift as a build-breaking gate.
6. **ADRs** record *why* these boundaries exist, and may assert requirements —
   but a requirement is only real once a schema, a test, or a check enforces it.

If you find an ADR asserting a "MUST" that nothing enforces, the requirement is
aspirational. Either back it with an executable check or downgrade it.
