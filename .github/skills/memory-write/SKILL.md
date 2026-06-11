---
name: memory-write
description: Append a durable record (source or concept) to the governed memory log, then rebuild and verify.
---
# Skill: memory-write

Use this skill when you need to persist something durable — a source you
ingested, or a concept you derived. Writing is append-only and always followed by
a rebuild and a verify.

## When to use

- You read a source worth keeping → write a `source`.
- A durable idea emerged across sources → write a `concept` that cites them.

## When *not* to use

- For scratch thinking that does not need to survive the session. Not everything
  is memory. Over-writing pollutes the index with noise.

## Steps

1. Draft a one-paragraph `summary`. This is the navigation layer — make it stand
   on its own. If a reader cannot tell from the summary whether to open the body,
   rewrite it.
2. For a concept, collect the ids of the sources it relies on.
3. Write the record:

   ```
   governed-memory write \
       --type concept \
       --title "Summary-first navigation scales sublinearly" \
       --summary "Indexing summaries instead of bodies lets a reader decide what to open before paying the token cost." \
       --source <source-id> \
       --tag retrieval --tag design \
       --sensitivity public
   ```

4. Rebuild and verify:

   ```
   governed-memory rebuild
   governed-memory verify     # must print OK before you stop
   ```

## Guardrails

- A `source` record must not declare `--source`.
- `--sensitivity restricted` requires `--acknowledge-restricted` and explicit
  user consent.
- If `verify` fails, fix the log (not the index) and rebuild.
