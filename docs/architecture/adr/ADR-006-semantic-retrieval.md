# ADR-006 — Semantic retrieval is optional, summary-only, derived, and pluggable

- Status: accepted
- Date: 2026

## Context

The README was honest that the store shipped with no embeddings: full-text
search over good summaries goes a long way, and vector retrieval is the upgrade
you want *later* — once the corpus is large enough that keyword matching misses
a paraphrase. "Later" has arrived. The risk in adding embeddings is that the
naive version quietly breaks three things this architecture cares about:

1. **The dependency-free promise.** A memory layer should not fall over because
   of a model download.
2. **The visibility floor (ADR-004).** If you embed bodies, the vector index
   becomes a semantic side channel: a nearest-neighbour search over a private
   body returns its meaning even though the read path redacts its text.
3. **The source/derived split (ADR-002).** Vectors are not truth; treating them
   as a second source of record would let them drift.

## Decision

1. **Summaries only, never bodies.** Vectors are built from the same navigation
   text the FTS index covers — `title`, `summary`, `tags`. A body, public or
   private, is never embedded. This keeps the visibility floor intact: there is
   no semantic representation of a private body to retrieve.

2. **Derived and disposable.** Vectors live in a `vectors` table inside the
   derived `memory.sqlite`, written at `rebuild --embed` and reconciled by
   `verify` (vector drift is fatal). Delete the index and rebuild; nothing is
   lost. They are never a source of truth.

3. **Default-off.** A plain `rebuild` produces a vector-free index and is
   behaviour-identical to before. Vectors exist only when explicitly requested,
   and `query` defaults to `mode="lexical"`. Semantic and hybrid modes raise a
   clear error if the index has no vectors.

4. **Pluggable, dependency-free default.** Retrieval depends on a small
   `Embedder` protocol, not a model. The built-in `HashingEmbedder` is
   stdlib-only and deterministic — it exercises the full vector path (recall +
   reciprocal-rank fusion) without a dependency. It is lexical at heart, so it
   does not, on its own, catch true synonyms. A deployment that wants genuine
   paraphrase recall plugs a real embedding model in behind the same protocol;
   nothing else in the pipeline changes.

5. **Hybrid uses rank fusion, not score mixing.** `hybrid` mode fuses the FTS
   ranking and the cosine ranking with reciprocal rank fusion, which avoids the
   trap of comparing a bm25 score to a cosine score on incompatible scales.

## Consequences

- The common path is unchanged and dependency-free; semantic recall is an
  opt-in that a single environment variable's worth of effort (one `--embed`)
  turns on.
- Honesty is preserved: the built-in encoder demonstrates the mechanism but
  does not overclaim semantic understanding. The README says so.
- A half-embedded index cannot return silently incomplete results, because
  `verify` fails on vector drift.

## Enforcement

- Implemented in `src/governed_memory/embeddings.py` (`Embedder`,
  `HashingEmbedder`, `embedding_text`, `cosine`, pack/unpack),
  `src/governed_memory/index.py` (`rebuild_index(..., embedder=...)`, `vectors`
  and `meta` tables), and `src/governed_memory/query.py` (`mode`, RRF fusion).
- Vector drift is checked in `src/governed_memory/verify.py`.
- Covered by `tests/test_embeddings.py` and `tests/test_semantic.py`, including
  the summary-only invariant (a private body's text never enters the vector).
- Surfaced by `cli.py` (`rebuild --embed`, `query --mode`) and `mcp_server.py`
  (`embed` on `memory.rebuild`, `mode` on `memory.query`).
