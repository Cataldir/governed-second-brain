---
name: azure-aks
description: Use this skill when you need AKS architecture, networking, security, troubleshooting, or capacity-planning workflows.
argument-hint: Describe the cluster, environment, region, and the AKS outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure AKS Skill

Use this skill to run the manual AKS workflow with the installed [AzureKubernetesSpecialist](../azure-aks.agent.md).

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

- Produce an AKS plan, troubleshooting path, or remediation recommendation with cost and operational trade-offs.
- Escalate broader system design to [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md).

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not treat local MCP runtime docs as a substitute for Azure service guidance.
