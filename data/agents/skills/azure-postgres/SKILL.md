---
name: azure-postgres
description: Use this skill when you need PostgreSQL schema design, extension planning, migration guidance, or Azure Database for PostgreSQL troubleshooting workflows.
argument-hint: Describe the workload, schema or migration concern, and the PostgreSQL outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure PostgreSQL Skill

Use this skill to run the manual PostgreSQL workflow with the installed [AzurePostgreSQLSpecialist](../azure-postgres.agent.md).

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

- Produce a PostgreSQL design note, migration plan, performance recommendation, or troubleshooting path.
- Escalate application data ownership questions to [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md).

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not treat this skill as the canonical schema or migration authority.
