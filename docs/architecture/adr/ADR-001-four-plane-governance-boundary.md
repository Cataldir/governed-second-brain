# ADR-001 — Four-plane governance boundary

- Status: accepted
- Date: 2025

## Context

A knowledge system that mixes "the rules", "the explanation of the rules", "the
data", and "the code that runs" in one undifferentiated pile becomes ungovernable.
Documentation starts asserting requirements nothing enforces. Generated files get
hand-edited. The data and the code that maintains it blur together. Within months
nobody can say which file is authoritative for a given concern.

## Decision

Partition the repository into four planes, each with a root directory and a fixed
edit authority.

| Plane | Root | Responsibility |
| --- | --- | --- |
| Operational | `.github/` | Loadable agent behaviour: instructions, skills, agent personas. |
| Contextual | `docs/` | Rationale and decision records. Explains; never enforces. |
| Authority | `data/` | Canonical records, governed outputs, and derived indexes. |
| Execution | `src/` | Runnable code: validators, index builders, the CLI. |

Two boundaries are load-bearing:

1. **`docs/` may explain a rule but may never be the rule.** Every requirement
   must be enforced in `.github/`, `data/`, or `src/`. A `docs/` page links to
   the enforcement point.
2. **The authority plane is downstream of nothing.** Canonical records are the
   source of truth; everything else is derived from or governed by them.

## Consequences

- A reader can answer "which file wins?" by consulting one map
  ([`governance-map.md`](../../../.github/governance-map.md)).
- Requirements cannot hide in prose. An unenforced "MUST" is, by this ADR,
  aspirational until a schema, test, or check backs it.
- The cost is discipline: new material must be placed in the correct plane, and
  cross-plane shortcuts (e.g. a doc that quietly becomes the operational rule)
  are rejected in review.

## Enforcement

This ADR is backed by
[`governance-boundary.instructions.md`](../../../.github/instructions/governance-boundary.instructions.md),
which every agent loads before editing.
