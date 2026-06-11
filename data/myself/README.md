# Personal context — `data/myself/`

A second brain that holds only notes is a filing cabinet. What makes it a model
of *you* is a governed record of who you are, what you are working toward, and
what an agent is allowed to know about you while it works. That is this plane.

It is part of the **authority plane**: these are source records, edited with
review, validated against a schema, and labelled with a `sensitivity` so the
[visibility floor](../../docs/architecture/adr/ADR-004-content-visibility-boundary.md)
applies to your personal data exactly as it applies to everything else.

## The one rule that makes this safe to publish

**This reference repository ships *types*, *schemas*, and *synthetic templates* —
never a real person's data.** Every file here is a placeholder or an invented
example. The shape is real; the contents are not. In a real deployment you
replace the templates with your own records, and the same governance — schema
validation, sensitivity labels, the visibility floor, the verifier — protects
them.

This mirrors the rule already stated for the record log: *the truth is yours,
not the template's.*

## What lives here

| Area | Purpose | Default sensitivity |
| --- | --- | --- |
| [`identity/`](identity/) | Profile, bio, voice and personality, expertise surfaces | mixed (bio public, contact restricted) |
| [`career/`](career/) | Goals, role, promotion evidence, milestones | private |
| [`knowledge/`](knowledge/) | What you know deeply; teaching and reference surfaces | public |
| [`finances/`](finances/) | Projections, commitments, revenue (templates only) | restricted |
| [`health/`](health/) | Health context an agent must handle with the highest care | restricted |
| [`family/`](family/) | People and relationships referenced in your work | restricted |

A real deployment grows more categories (publishing pipelines, ventures,
monetization, organization). The point is not the list; it is that **each
category declares a default sensitivity**, and an agent reads it through the same
floor as any other record.

## The catalog the agents read

The single most important file here is
[`personal-data-catalog.md`](personal-data-catalog.md). It answers the question a
governed system must be able to answer out loud: *what types of personal
information do the agents actually use, why, and at what sensitivity?* If a type
of personal data is not in the catalog, an agent has no licence to rely on it.

## The contract

A personal-profile record has a formal shape:
[`../domains/personal-profile.schema.json`](../domains/personal-profile.schema.json).
It reuses the same `sensitivity` vocabulary as the memory record, so one
visibility floor covers both. Change the schema and you change the validator in
the same commit — the schema and the code that enforces it must never disagree.
