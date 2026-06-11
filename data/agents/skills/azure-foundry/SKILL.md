---
name: azure-foundry
description: Use this skill when you need Azure AI Foundry model deployment, agent evaluation, RAG, or AI project infrastructure workflows.
argument-hint: Describe the project, model or agent goal, environment, and the Foundry outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure Foundry Skill

Use this skill to run the manual Foundry workflow with the installed [AzureAIFoundrySpecialist](../azure-foundry.agent.md).

## Load Order

1. Start with the shared [Azure skill guide](../_shared/azure/guide.md) and confirm the installed Azure agent surface before choosing a service-specific route.
2. Start from the Azure prompt surface:
   - [azure-architecture-review.prompt.md](../../prompts/azure-architecture-review.prompt.md)
   - [azure-troubleshoot.prompt.md](../../prompts/azure-troubleshoot.prompt.md)
   - [tech-lead-innovation-research.prompt.md](../../prompts/tech-lead-innovation-research.prompt.md)
3. Load the supporting guidance:
   - [azure-infrastructure.instructions.md](../../instructions/azure-infrastructure.instructions.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
4. Use the Azure MCP tools declared in the installed agent first and keep the portable runtime assumptions from the [Azure skill guide](../_shared/azure/guide.md) in sync with the result.

## Output Contract

- Produce a Foundry deployment plan, evaluation workflow, RAG design note, or troubleshooting path.
- Keep cost, quota, and evaluation implications explicit in the result.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not replace the canonical Foundry agent or the future MCP-backed runtime direction.
