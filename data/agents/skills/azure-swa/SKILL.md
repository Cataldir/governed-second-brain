---
name: azure-swa
description: Use this skill when you need Static Web Apps scaffolding, configuration, deployment, or troubleshooting workflows.
argument-hint: Describe the app, hosting model, API integration, and the Static Web Apps outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure SWA Skill

Use this skill to run the manual Static Web Apps workflow with the installed [AzureStaticWebAppsSpecialist](../azure-swa.agent.md).

## Load Order

1. Start with the shared [Azure skill guide](../_shared/azure/guide.md) and confirm the installed Azure agent surface before choosing a service-specific route.
2. Start from the Azure prompt surface:
   - [azure-migrate.prompt.md](../../prompts/azure-migrate.prompt.md)
   - [azure-troubleshoot.prompt.md](../../prompts/azure-troubleshoot.prompt.md)
   - [azure-architecture-review.prompt.md](../../prompts/azure-architecture-review.prompt.md)
3. Load the supporting guidance:
   - [azure-infrastructure.instructions.md](../../instructions/azure-infrastructure.instructions.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
4. Use the Azure MCP tools declared in the installed agent first and keep the portable runtime assumptions from the [Azure skill guide](../_shared/azure/guide.md) in sync with the result.

## Output Contract

- Produce a SWA design note, deployment plan, configuration review, or troubleshooting path.
- Escalate frontend design work to [ui-agent.agent.md](../../../engineering/ui-agent/ui-agent.agent.md) when the task becomes UI-led.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not use the skill to replace the canonical SWA agent or Azure rules.
