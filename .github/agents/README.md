# Agents

This directory holds agent definitions: persona files that tell an AI agent how
to behave for a particular role. Each is scoped to a domain and bound to a set
of tools, and each points at the rules under [`../instructions/`](../instructions/)
rather than restating them.

## What ships here

- [`memory-curator.agent.md`](memory-curator.agent.md) — the generic example
  that maintains the governed memory store itself.
- A **portable specialist workbench**: general engineering, architecture, lead,
  business, and Azure agents that reason *from* the memory store. They are
  vendor-neutral and role-neutral; they encode no personal voice or private
  business. See [`team-mapping.md`](team-mapping.md) for the full roster and the
  delegation graph.

The matching prompts live in [`../prompts/`](../prompts/), the colocated skills
in [`../skills/`](../skills/), and the shared engineering/architecture/Azure
instructions in [`../instructions/`](../instructions/).

## What an agent file is for

- a clear **role** and the boundary of what it owns;
- the **tools** it is allowed to use;
- the **rules** it must follow, which always include the governance boundary.

## What an agent file is *not* for

- It is not the source of operational truth. The instructions under
  `../instructions/` are. An agent file points at them; it does not restate them.
- It is not a place for personal identity, voice, or private context. Keep those
  out of a public reference architecture entirely.

## How delegation resolves

The lead agents (system architect, tech lead) delegate by role. They resolve
specialist names from [`team-mapping.md`](team-mapping.md) when it is present; if
it is absent, they continue with whatever agents the runtime exposes and never
hard-fail. The agents are clients of the memory store, never its source of truth.
