# ADR-007 — A personal-context plane: types over contents

- Status: accepted
- Date: 2026

## Context

A store of well-governed records is a filing cabinet, not a *second brain*. What
makes a memory layer model a person is a governed record of who they are, what
they are working toward, and what an agent is licensed to know about them while
it works. Without that, an agent acts as a generic assistant that happens to
have good notes.

But personal context is the most sensitive data in the system, and this is a
*public reference repository*. The naive approaches both fail:

1. **Ship a real person's data** — impossible; it is a public repo, and the
   point is to be copied.
2. **Omit personal context entirely** — then the architecture is not a faithful
   model of a second brain, and it gives no guidance on the hardest governance
   question: how should an agent handle personal data?

The architecture also has surfaces beyond the four content planes that a faithful
deployment needs: the agent's own working memory, and the infrastructure that
runs the store. Pretending the four planes are the whole repository would make
the reference structure diverge from any real deployment.

## Decision

1. **Model the person as a governed authority-plane sub-tree.** `data/myself/`
   holds personal context as source records: identity, voice, career, knowledge,
   and the categories a real deployment adds. Each record validates against
   [`data/domains/personal-profile.schema.json`](../../../data/domains/personal-profile.schema.json)
   and carries a `sensitivity` from the same vocabulary as every other record.

2. **One visibility floor, no special case.** Personal data is governed by the
   read-path redaction of [ADR-004](ADR-004-content-visibility-boundary.md): a
   `restricted` contact, health, or financial body is redacted unless explicitly
   revealed. Personal data is not privileged or exempted; it rides the same
   mechanism, which is why that mechanism had to exist first.

3. **Publish types, not contents.** The reference repository ships *types,
   schemas, and synthetic templates only* — never a real person's data. The
   shape is real; every value is a placeholder. A deployment replaces the
   templates with real records and inherits the governance unchanged.

4. **Name the personal-data types out loud.** The governance artifact is
   [`data/myself/personal-data-catalog.md`](../../../data/myself/personal-data-catalog.md):
   it enumerates every type of personal information the agents use, why they use
   it, and at what sensitivity. The rule is enforced by omission — *if a type is
   not in the catalog, no agent has licence to rely on it.*

5. **Recognise the two surfaces beyond the content planes.** A faithful
   deployment has more than `.github/ docs/ data/ src/`:
   - `memory/` — the agent's own working memory (repo- and session-scoped
     Markdown notes). It is advisory, prunable, and explicitly *not* the
     canonical record log; a note never outranks a verified record.
   - `infra/` — the execution-plane deployment surface (how the gated MCP server
     runs). It honours the default-off, local-first posture of
     [ADR-003](ADR-003-governed-write-surface.md).

## Consequences

- The repository is now a faithful structural mirror of a real deployment: the
  personal-context plane, agent memory, and infrastructure surface all exist,
  with the same governance, and no real personal data is exposed.
- The hardest governance question — how an agent handles personal data — has a
  concrete, enforced answer: schema-validated, sensitivity-labelled, redacted by
  the same floor, catalogued by type.
- A reader can copy the structure and drop in their own records without
  re-deriving the privacy model.
- `memory/` and `infra/` are documented as recognised surfaces, so an agent does
  not mistake working notes for canonical truth, nor treat infra as authority
  over content.

## Enforcement

- The `sensitivity` field is required by `personal-profile.schema.json`.
- The visibility floor (`src/governed_memory/query.py`) redacts non-public
  bodies on read, personal or not.
- Summary vectors are built from navigation text only (ADR-006), so semantic
  search over personal data cannot leak a redacted body.
- The personal-data catalog is the declared source for which personal types are
  in use; adding a type means adding a catalog row first.
