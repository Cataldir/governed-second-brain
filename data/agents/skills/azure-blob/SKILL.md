---
name: azure-blob
description: Use this skill when you need Blob Storage architecture, lifecycle policy, event-driven storage design, or migration workflows.
argument-hint: Describe the storage workload, access pattern, compliance needs, and the Blob outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure Blob Skill

Use this skill to run the manual Blob workflow with the installed [AzureBlobStorageSpecialist](../azure-blob.agent.md).

## Load Order

1. Start with the shared [Azure skill guide](../_shared/azure/guide.md) and confirm the installed Azure agent surface before choosing a service-specific route.
2. Start from the Azure prompt surface:
   - [azure-architecture-review.prompt.md](../../prompts/azure-architecture-review.prompt.md)
   - [azure-migrate.prompt.md](../../prompts/azure-migrate.prompt.md)
   - [azure-troubleshoot.prompt.md](../../prompts/azure-troubleshoot.prompt.md)
3. Load the supporting guidance:
   - [azure-infrastructure.instructions.md](../../instructions/azure-infrastructure.instructions.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
4. Use the Azure MCP tools declared in the installed agent first and keep the portable runtime assumptions from the [Azure skill guide](../_shared/azure/guide.md) in sync with the result.

## Output Contract

- Produce a storage design, lifecycle policy recommendation, migration plan, or troubleshooting path.
- Call out access, cost, and retention trade-offs explicitly.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not turn the skill into a canonical storage design standard.
