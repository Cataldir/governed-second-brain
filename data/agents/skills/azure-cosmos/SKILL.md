---
name: azure-cosmos
description: Use this skill when you need Cosmos DB data modeling, partitioning, consistency, RU optimization, or retrieval-pattern workflows.
argument-hint: Describe the data model, access pattern, scale needs, and the Cosmos DB outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure Cosmos Skill

Use this skill to run the manual Cosmos workflow with the installed [AzureCosmosDBSpecialist](../azure-cosmos.agent.md).

## Load Order

1. Start with the shared [Azure skill guide](../_shared/azure/guide.md) and confirm the installed Azure agent surface before choosing a service-specific route.
2. Start from the Azure prompt surface:
   - [azure-architecture-review.prompt.md](../../prompts/azure-architecture-review.prompt.md)
   - [azure-troubleshoot.prompt.md](../../prompts/azure-troubleshoot.prompt.md)
   - [azure-cost-optimize.prompt.md](../../prompts/azure-cost-optimize.prompt.md)
3. Load the supporting guidance:
   - [azure-infrastructure.instructions.md](../../instructions/azure-infrastructure.instructions.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
4. Use the Azure MCP tools declared in the installed agent first and keep the portable runtime assumptions from the [Azure skill guide](../_shared/azure/guide.md) in sync with the result.

## Output Contract

- Produce a Cosmos data-model recommendation, partition strategy, optimization plan, or troubleshooting path.
- Keep access-pattern assumptions explicit and escalate application architecture trade-offs when needed.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not convert this skill into the authoritative data-model contract.
