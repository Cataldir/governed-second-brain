# Personal-data catalog

This is the answer to a question a governed second brain must be able to give
out loud: **what types of personal information do the agents use, why do they
need them, and at what sensitivity does each travel?**

The rule is simple and enforced by omission: *if a type of personal data is not
listed here, no agent has licence to rely on it.* Adding a new kind of personal
data to the system means adding a row here first — naming its purpose, its
sensitivity, and the visibility behaviour that follows.

The `Sensitivity` column uses the same vocabulary as every other record
(`public`, `private`, `restricted`), so the
[visibility floor](../../docs/architecture/adr/ADR-004-content-visibility-boundary.md)
governs personal data with no special case: non-public bodies are redacted on
read unless deliberately revealed.

> All values below are **synthetic**. This repository documents the *types* of
> personal data and how they are governed; it never ships a real person's data.

## Catalog

| Data type | What it is | Why an agent uses it | Sensitivity | On read |
| --- | --- | --- | --- | --- |
| Public bio | One-paragraph professional description | Author bylines, talk intros, profile pages | `public` | Body opens |
| Voice & personality | How the person writes and reasons; what they will and will not say | Drafting any first-person content in the person's voice | `public` | Body opens |
| Expertise map | Topics the person can speak to with authority | Routing work, scoping talks, choosing examples | `public` | Body opens |
| Contact details | Email, handles, scheduling links | Addressing outreach, scheduling | `restricted` | Redacted unless revealed |
| Career goals | Role, ambitions, promotion evidence | Prioritising work, framing accomplishments | `private` | Redacted unless revealed |
| Calendar & commitments | Obligations and deadlines | Planning, conflict detection | `private` | Redacted unless revealed |
| Financial projections | Revenue plans, commitments (templates only here) | Modelling decisions, prioritisation | `restricted` | Redacted unless revealed |
| Health context | Anything an agent must handle with the highest care | Pacing work, honouring constraints | `restricted` | Redacted unless revealed |
| Relationships | People referenced in the person's work and life | Disambiguation, respectful reference | `restricted` | Redacted unless revealed |

## How the catalog is enforced

- **Sensitivity drives the floor.** An agent that retrieves a `restricted`
  health or contact record gets a redacted body unless an explicit `reveal` flag
  is passed — a visible, deliberate act, the same mechanism as any other record.
- **The schema carries the label.** Every personal-profile record validates
  against [`../domains/personal-profile.schema.json`](../domains/personal-profile.schema.json),
  which requires a `sensitivity` value from this same vocabulary.
- **The verifier still gates.** Personal records are records: `governed-memory
  verify` checks their citations and index consistency like any other.
- **No semantic side-channel.** Summary vectors are built from navigation text
  only, never bodies, so semantic search over personal data cannot leak a
  redacted body past the floor (see
  [ADR-006](../../docs/architecture/adr/ADR-006-semantic-retrieval.md)).
