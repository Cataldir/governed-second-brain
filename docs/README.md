# Contextual plane — `docs/`

This plane explains *why*. It holds rationale, architecture notes, and decision
records.

It has one hard rule: **`docs/` may explain a rule, but it may never be the
rule.** If a behaviour is required, that requirement must already be enforced in
`.github/` (instructions), `data/` (a schema), or `src/` (a validator or test).
A `docs/` page links to where the rule actually lives.

This keeps documentation from drifting into a second, unenforced source of truth
— the most common way a "governed" system quietly stops being governed.

## Contents

- [`architecture/`](architecture/README.md) — the architecture overview and the
  Architecture Decision Records (ADRs) that explain the boundaries.
