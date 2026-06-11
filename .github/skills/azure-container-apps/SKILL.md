---
name: azure-container-apps
description: Use this skill when you need Container Apps architecture, scaling, revision strategy, or troubleshooting workflows.
argument-hint: Describe the service topology, scaling concern, and the Container Apps outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure Container Apps Skill

Use this skill to run the manual Container Apps workflow with the installed [AzureContainerAppsSpecialist](../azure-container-apps.agent.md).

## Load Order

1. Start with the shared [Azure skill guide](../_shared/azure/guide.md) and confirm the installed Azure agent surface before choosing a service-specific route.
2. Start from the Azure prompt surface:
   - [azure-architecture-review.prompt.md](../../prompts/azure-architecture-review.prompt.md)
   - [azure-troubleshoot.prompt.md](../../prompts/azure-troubleshoot.prompt.md)
   - [azure-migrate.prompt.md](../../prompts/azure-migrate.prompt.md)
3. Load the supporting guidance:
   - [azure-infrastructure.instructions.md](../../instructions/azure-infrastructure.instructions.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
4. Use the Azure MCP tools declared in the installed agent first and keep the portable runtime assumptions from the [Azure skill guide](../_shared/azure/guide.md) in sync with the result.

## Output Contract

- Produce a Container Apps design, scaling plan, revision strategy, or troubleshooting path.
- Escalate broader platform or CI/CD issues to [platform-quality.agent.md](../../../operations/platform-quality/platform-quality.agent.md).

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not duplicate canonical deployment or infrastructure policy inside the skill.
