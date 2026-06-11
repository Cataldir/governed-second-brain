---
applyTo: '**'
description: The private-to-public visibility boundary. Loaded before any content is read for reuse in a public draft.
---
# Content visibility

A record carries a `sensitivity`: `public`, `private`, or `restricted`. That
field is not decoration. It governs whether a record's **body** may cross into a
public artifact.

## The rule

- A `public` body may be quoted, summarised, and reused freely.
- A `private` or `restricted` body must **never** be copied verbatim into a
  public draft, message, or commit. Use its summary, or the conclusion it
  supports, in your own words — not its text.
- The read path enforces the floor: `governed-memory query` returns the body of
  a non-public record only when the caller passes an explicit reveal flag
  (`--reveal` on the CLI, `reveal: true` over MCP). Without it, the hit is marked
  `redacted` and only the summary is returned.

## Why the floor is in the read path, not just in a person's head

The failure mode is mundane: an agent retrieves a private record, the body is
right there in the context window, and it gets pasted into a public draft
because nothing said "stop". Redaction by default means revealing a private body
is a deliberate act with a flag attached to it — an event you can see in a
command, not an accident of a smooth autocomplete.

## Obligations for an agent

1. Before reusing retrieved text in anything public, check the `sensitivity`
   of every hit you are drawing from.
2. Do not pass `--reveal` / `reveal: true` to pull a non-public body unless the
   user has asked for that specific record and the destination is not public.
3. If you need the *idea* from a private record in a public artifact, restate it
   in your own words and cite the public sources behind it — never the private
   body.
4. When in doubt about whether a destination is public, treat it as public.

## Cross-references

- Rationale: [`../../docs/architecture/adr/ADR-004-content-visibility-boundary.md`](../../docs/architecture/adr/ADR-004-content-visibility-boundary.md).
- The read path that enforces the floor: `src/governed_memory/query.py`.
- The record contract: [`../../data/domains/memory-record.schema.json`](../../data/domains/memory-record.schema.json).
