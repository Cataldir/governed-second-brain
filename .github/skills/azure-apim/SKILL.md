---
name: azure-apim
description: Use this skill when you need API Management policy design, gateway governance, security, or APIM troubleshooting workflows.
argument-hint: Describe the API surface, policy concern, environment, and the APIM outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure APIM Skill

Use this skill to run the manual APIM workflow with the installed [AzureAPIMSpecialist](../azure-apim.agent.md).

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

- Produce an APIM policy design, troubleshooting plan, or governance recommendation.
- Escalate end-to-end system decomposition to [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md).

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not duplicate canonical APIM policy guidance inside the skill body.
