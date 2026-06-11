---
name: azure-redis
description: Use this skill when you need Redis caching strategy, session design, pub-sub patterns, or Azure Redis troubleshooting workflows.
argument-hint: Describe the workload, latency or caching concern, and the Redis outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Azure Redis Skill

Use this skill to run the manual Redis workflow with the installed [AzureRedisSpecialist](../azure-redis.agent.md).

## Load Order

1. Start with the shared [Azure skill guide](../_shared/azure/guide.md) and confirm the installed Azure agent surface before choosing a service-specific route.
2. Start from the Azure prompt surface:
   - [azure-architecture-review.prompt.md](../../prompts/azure-architecture-review.prompt.md)
   - [azure-cost-optimize.prompt.md](../../prompts/azure-cost-optimize.prompt.md)
   - [azure-troubleshoot.prompt.md](../../prompts/azure-troubleshoot.prompt.md)
3. Load the supporting guidance:
   - [azure-infrastructure.instructions.md](../../instructions/azure-infrastructure.instructions.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
4. Use the Azure MCP tools declared in the installed agent first and keep the portable runtime assumptions from the [Azure skill guide](../_shared/azure/guide.md) in sync with the result.

## Output Contract

- Produce a caching strategy, cost/performance recommendation, or troubleshooting path.
- Make trade-offs around consistency, latency, and cost explicit.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not restate canonical Redis policy or deployment guidance inside the skill.
