# Azure Skill Guide

Use this guide when a shared Azure skill needs a portable load order.

## Shared Surface

- Prompts:
  - [azure-architecture-review.prompt.md](../../prompts/azure-architecture-review.prompt.md)
  - [azure-cost-optimize.prompt.md](../../prompts/azure-cost-optimize.prompt.md)
  - [azure-migrate.prompt.md](../../prompts/azure-migrate.prompt.md)
  - [azure-troubleshoot.prompt.md](../../prompts/azure-troubleshoot.prompt.md)
  - [tech-lead-innovation-research.prompt.md](../../../architecture/prompts/tech-lead-innovation-research.prompt.md)
- Instructions:
  - [tool-usage.instructions.md](../../../instructions/tool-usage.instructions.md)
  - [azure-infrastructure.instructions.md](../../../instructions/azure-infrastructure.instructions.md)
- Agents:
  - [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md)
  - [platform-quality.agent.md](../../../operations/platform-quality/platform-quality.agent.md)

## Portable Runtime Notes

- Use the Azure MCP tools declared in the installed Azure specialist agent first.
- Keep results explicit about subscription, region, quota, identity, and cost assumptions.
- Escalate broader architecture or platform trade-offs when the request crosses service boundaries.
