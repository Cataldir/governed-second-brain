---
applyTo: '**'
description: The four-plane governance boundary. Load before editing any file.
---
# Governance boundary

This instruction is the operational rule an agent must follow before editing any
path. The rationale lives in the ADRs under `docs/architecture/adr/`; this file
is the checklist.

## The four planes

| Plane | Root | Edit rule |
| --- | --- | --- |
| Operational | `.github/` | The agent personas, prompts, and skills here are **generated mirrors** of `data/agents/`. Edit the canonical source and regenerate; never patch a mirror. Other `.github` files (this instruction, the maps) are canonical — edit with review. |
| Contextual | `docs/` | Edit with review. Never a source of operational authority. |
| Authority | `data/` | Three sub-layers — classify before editing (below). |
| Execution | `src/` | Edit with review and tests. |

## Two surfaces beyond the content planes

A faithful deployment also has two recognised top-level surfaces (see
[ADR-007](../../docs/architecture/adr/ADR-007-personal-context-plane.md)):

| Surface | Root | Edit rule |
| --- | --- | --- |
| Agent memory | `memory/` | Advisory working notes. Prune freely. A note never outranks a verified record. No secrets, no personal data. |
| Infrastructure | `infra/` | Execution-plane deployment surface. Edit with review. Keep the write surface default-off and local-first. |

## Authority-plane sub-layers

Before editing anything under `data/`, classify it:

| Sub-layer | Example | Edit rule |
| --- | --- | --- |
| Source records | `data/domains/*.schema.json`, `data/myself/**`, `data/agents/**` | Edit directly with review. `data/agents/**` is the canonical source for the `.github` operational mirrors. Personal context is sensitivity-labelled; this repo ships templates only. |
| Governed append-only outputs | `data/memory/*.jsonl` | Append only. Never rewrite a past line. Compaction writes a *new* file. |
| Derived indexes | `data/indexes/memory.sqlite` | Never edit by hand. Regenerate from the canonical source. |

If the classification is ambiguous, treat the file as a source record and ask
before any structural change.

## Managed Files

A Managed File is anything automation maintains and a human must not hand-edit.
Before merging a change that touches one, confirm it is declared in
[`../ownership-taxonomy.md`](../ownership-taxonomy.md) with its canonical source,
regeneration entrypoint, drift-check, and failure mode. If it is not declared,
do not edit it — declare it first.

## Drift obligation

Any change affecting a Managed File must:

1. run the declared drift-check (`governed-memory verify` for the index,
   `governed-memory sync-mirrors --check` for the `.github` mirrors);
2. include the result in the change description;
3. regenerate the Managed File if the source is correct and it drifted
   (`governed-memory rebuild` or `governed-memory sync-mirrors`).

## The non-negotiable

Do not merge a change that leaves `governed-memory verify` failing. The verifier
is the contract. A green verifier is the definition of "the memory is intact".
