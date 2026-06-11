---
mode: agent
description: Run a weekly review loop over the governed memory store — surface what changed, decide what to keep, record the transitions with evidence.
---
# Weekly review

You are running the weekly review loop for the governed memory store. The loop
turns a week of loose notes into durable, cited records and moves work forward
through its lifecycle with evidence. Follow it in order; do not skip the gate.

## Inputs

- The canonical record log under `data/memory/`.
- The state event log under `data/state/`.
- The derived index at `data/indexes/memory.sqlite`.

## Loop

1. **Rebuild and verify.** Run `governed-memory rebuild` then
   `governed-memory verify`. If verify fails, stop and fix referential integrity
   before anything else — a review built on a broken index is theatre.

2. **Survey the week, summary-first.** Use `governed-memory query` to pull the
   themes you worked on. Read summaries, not bodies. For non-public hits, do
   **not** pass `--reveal` — you are surveying, not extracting.

3. **Decide what graduates.** For each loose idea worth keeping, write it as a
   record with `governed-memory write`, citing the public sources behind it.
   Concept records must cite at least one source. Keep sensitivity honest:
   default to `private`; mark `public` only what you would publish.

4. **Advance the work, with evidence.** For each entity that moved this week,
   record the transition with `governed-memory state --entity ... --to-status ...
   --evidence ...`. The transition is refused if it is not allowed from the
   current status — that refusal is a feature, not an error to work around.

5. **Carry forward.** List anything still in flight with
   `governed-memory history --entity ...` and note what evidence the next
   transition will need.

## Gate

- Never copy a non-public body into a public artifact. Restate the idea in your
  own words and cite public sources. See
  [`content-visibility.instructions.md`](../instructions/content-visibility.instructions.md).
- Never force an illegal transition by editing the state log by hand. If a
  transition is refused, either supply the missing intermediate step or fix the
  declared transition map in `events.py` deliberately.
- Rebuild and re-verify at the end. The review is done when `verify` is green.
