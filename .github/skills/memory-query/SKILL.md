---
name: memory-query
description: Retrieve from the governed memory store summary-first, opening bodies only on demand.
---
# Skill: memory-query

Use this skill to recall what the store knows about a topic. Retrieval is
summary-first by design: you read cheap navigation text before paying the token
cost of a full body.

## When to use

- Before answering a question that the store may already hold an answer to.
- Before writing a new concept, to check whether one already exists (avoid
  duplicates; prefer citing or superseding).

## Steps

1. Query with the navigation layer:

   ```
   governed-memory query "summary first navigation"
   ```

   You get titles and summaries, ranked by relevance. No bodies yet.

2. Decide which records are worth opening. Only then pay for the body:

   ```
   governed-memory query "summary first navigation" --open-body
   ```

## Why summary-first

The full-text index covers `title`, `summary`, and `tags` — never `body`. This
keeps retrieval cost tied to the number of summaries, not the total volume of
content. If you find yourself always passing `--open-body`, your summaries are
too weak to navigate — fix the summaries, not the query.
