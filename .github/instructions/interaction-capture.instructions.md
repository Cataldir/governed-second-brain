---
applyTo: '**'
description: How and whether interaction capture happens in this repository.
---
# Interaction capture

This repository has **no hidden capture hook**. There is no background process
that scrapes a transcript, no automatic logging of a conversation, and nothing
an agent should assume is recording its work.

Capture is explicit. If you want a turn, a decision, or an outcome to become a
durable record, you write it through the same path as any other record:

```
governed-memory write --type concept --title "..." --summary "..." \
    --sensitivity private --tag decision
```

An agent runtime may instead reach the store over MCP
(`src/governed_memory/mcp_server.py`). That path is **gated**: the `memory.append`
tool is refused unless write mode has been explicitly enabled with
`GOVERNED_MEMORY_ENABLE_WRITE=true` and `GOVERNED_MEMORY_REQUIRE_APPROVAL=false`.
If the gate is closed, capture did not happen — do not claim it did. See
[ADR-003](../../docs/architecture/adr/ADR-003-governed-write-surface.md).

## Rules

- Do not claim that an interaction was captured unless you actually wrote a
  record and can name its id.
- Keep records compact. Store summaries and references — file paths, command
  names, decision notes — not raw transcripts, raw terminal dumps, secrets,
  tokens, or bulky generated output.
- Respect sensitivity. A record about something private is written with
  `--sensitivity private`; a record about something genuinely sensitive uses
  `restricted`, which the write path will refuse without an explicit
  acknowledgement.
- If you skipped capture, say so plainly. "I did not record this" is an honest
  and acceptable state.
