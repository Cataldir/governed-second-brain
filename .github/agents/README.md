# Agents

This directory holds agent definitions: persona files that tell an AI agent how
to behave for a particular role. In a full system there are many, each scoped to
a domain and bound to a set of tools.

This reference architecture ships **one** generic example —
[`memory-curator.agent.md`](memory-curator.agent.md) — to show the shape without
encoding anyone's personal roles, voice, or business.

## What an agent file is for

- a clear **role** and the boundary of what it owns;
- the **tools** it is allowed to use;
- the **rules** it must follow, which always include the governance boundary.

## What an agent file is *not* for

- It is not the source of operational truth. The instructions under
  `instructions/` are. An agent file points at them; it does not restate them.
- It is not a place for personal identity, voice, or private context. Keep those
  out of a public reference architecture entirely.
