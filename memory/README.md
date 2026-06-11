# Agent memory — `memory/`

This is the agent's own working memory: short notes it keeps *across* sessions
so it does not relearn the same thing every time. It is deliberately **not** the
same as the canonical record log in [`data/memory/`](../data/memory/).

The distinction is the point:

| | `data/memory/` | `memory/` (this folder) |
| --- | --- | --- |
| What | Canonical records about the world | The agent's notes to itself |
| Shape | Schema-validated JSON Lines | Free-form Markdown |
| Authority | Source of truth, verified | Working memory, advisory |
| Lifecycle | Append-only, never rewritten | Updated or pruned as it goes stale |

Keeping them separate stops the agent's scratch notes from masquerading as
verified truth. A note here is a hint; a record there is a fact with a citation.

## Scopes

| Scope | Lifetime | Use for |
| --- | --- | --- |
| [`repo/`](repo/) | Persists with the repository | Conventions, build commands, verified facts about this codebase |
| [`session/`](session/) | The current task | In-progress plans, temporary working state |

## Rules

- **No secrets, no personal data.** Working notes are not a place for
  credentials, tokens, or anything that belongs behind the visibility floor.
  Personal context belongs in [`data/myself/`](../data/myself/), governed by its
  sensitivity label.
- **Notes are advisory.** If a note and a verified record disagree, the record
  wins. Update or delete the stale note.
- **Prune freely.** Unlike the canonical log, working memory is meant to be
  edited and trimmed.
