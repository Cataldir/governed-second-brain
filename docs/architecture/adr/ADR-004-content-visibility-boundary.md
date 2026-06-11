# ADR-004 — Visibility is a read-path boundary, not a label

- Status: accepted
- Date: 2025

## Context

Every record declares a `sensitivity`: `public`, `private`, or `restricted`.
Until now that field was honest about *intent* but inert at *read time* — the
query path returned any record's body when asked, regardless of sensitivity.
That is the exact gap where a "second brain" leaks: a private note is retrieved,
its full text lands in the context window, and it is reused verbatim in a public
draft because nothing in the read path objected.

A label that nothing enforces is, by this repository's own standard (see the
governance map's chain of responsibility), aspirational. The visibility rule had
to be backed by code or downgraded.

## Decision

1. **Bodies of non-public records are redacted by default.** `query()` returns a
   `public` body when `open_body` is set, but returns a `private` or
   `restricted` body only when an additional, explicit `reveal` flag is also set.
   Without it, the hit is returned with its summary and marked `redacted=True`.

2. **Reveal is a deliberate, visible act.** The flag is surfaced as `--reveal`
   on the CLI and `reveal: true` over MCP. Revealing a private body is therefore
   an event you can point at in a command line or a tool call, not a silent
   default.

3. **The summary always flows.** Redaction never hides a record's existence or
   its summary — only its body. Navigation stays cheap; it is verbatim reuse of
   sensitive text that becomes explicit.

## Consequences

- The common path (find the idea, read the summary) is unchanged. The privileged
  path (pull the full private text) now requires intent.
- This is the read-path twin of ADR-003's write gate: writes of sensitive
  material are opt-in at write time; reads of sensitive bodies are opt-in at read
  time. Both make the consequential action explicit while leaving the common
  action frictionless.
- An operator who genuinely wants a private body must ask for it by name. That
  friction is the point.

## Enforcement

- Implemented in `src/governed_memory/query.py` (`query(..., reveal=...)` and the
  `QueryHit.redacted` field) and covered by `tests/test_visibility.py`.
- Surfaced by `src/governed_memory/cli.py` (`--reveal`) and
  `src/governed_memory/mcp_server.py` (`reveal` on `memory.query`).
- The operational rule agents must follow is
  [`content-visibility.instructions.md`](../../../.github/instructions/content-visibility.instructions.md).
