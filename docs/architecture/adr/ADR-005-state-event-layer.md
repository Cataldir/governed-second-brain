# ADR-005 — State is a separate append-only log from records

- Status: accepted
- Date: 2025

## Context

The blog post this repository implements names four storage shapes, not one:
*source* (what we are producing), *state* (where it is in a process), *index*
(how tools find it), and *evidence* (what happened, when). A plain memory store
usually keeps only the first and the third and quietly folds state into a
free-text field on the record.

That folding is the bug. If a status lives as a mutable field on a record, then
a status correction and a content revision become indistinguishable, and the
question "why is this marked published?" has no durable answer. State changes
*are* events; they deserve the same append-only treatment as the records
themselves.

## Decision

1. **Two logs, two rules.** Records live in `data/memory/*.jsonl` (durable
   artifacts). State transitions live in `data/state/events.jsonl` (transitions).
   Both are append-only; neither rewrites history.

2. **A transition is validated against the current status.** `record_transition`
   reads the entity's latest status, checks the target is reachable from it under
   a declared transition map, and refuses otherwise. A first event must enter at
   the initial status. This is what makes it a governed state machine rather than
   a status field an agent can scribble into.

3. **Every transition carries evidence.** A transition records the entity, the
   from/to statuses, a timestamp, and a list of evidence references (paths, URLs,
   report ids). The recorded event *is* the evidence: it answers which entity,
   what transition, what evidence, whether it was allowed, and where it is stored.

4. **The transition tool is gated like a write.** `memory.record_event` is in the
   set of mutating tools, so it obeys the same default-off, two-flag opt-in as
   `memory.append` (ADR-003).

## Consequences

- "Why is this published?" is answerable by replaying the entity's events.
- An illegal transition (e.g. `drafted -> published`, skipping the audit) is
  refused at write time, not caught later in review.
- The example transition map is a publishing lifecycle, but the engine is
  generic — swap the map for your own workflow.

## Enforcement

- Implemented in `src/governed_memory/events.py` (`record_transition`,
  `current_status`, `PUBLISHING_TRANSITIONS`) and covered by `tests/test_events.py`.
- Surfaced by `src/governed_memory/cli.py` (`state`, `history`) and
  `src/governed_memory/mcp_server.py` (`memory.record_event`).
- Gated by `src/governed_memory/gate.py` (`memory.record_event` ∈ `MUTATING_TOOLS`).
