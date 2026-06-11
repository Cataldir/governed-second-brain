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
