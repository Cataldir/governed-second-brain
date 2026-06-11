# Infrastructure — `infra/`

The deployment surface: how the store and its optional MCP server are run, from
a laptop to a cloud. It is part of the **execution plane** — edited with review,
never a source of authority over content.

The default deployment is *no deployment*: the store is local files and the CLI
runs against them. You only need anything here when you want the governed write
surface reachable by an agent runtime.

## What ships here

| Path | Purpose |
| --- | --- |
| [`local/Containerfile`](local/Containerfile) | Run the MCP server in a container, read-only by default |
| `cloud/` | Placeholder for cloud IaC (Bicep/Terraform) in a real deployment |

## The one rule infra must honour

The write surface is **default-off and local-first**. Any deployment here keeps
that posture: the MCP server starts read-only, and writes require the explicit
two-flag opt-in described in
[ADR-003](../docs/architecture/adr/ADR-003-governed-write-surface.md). Exposing
the server over anything other than local stdio is a deliberate decision the
deployment author owns — the default never does it for you.

> A real deployment (the kind this architecture mirrors) adds cloud IaC under
> `cloud/` — a resource group, an identity, a small always-on host for the index
> and server. That is intentionally left as a stub here: the reference repo
> demonstrates the *shape* and the safe default, not a specific cloud bill.
