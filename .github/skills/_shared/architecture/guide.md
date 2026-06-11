# Architecture Skill Guide

Use this guide when a shared architecture skill needs a portable load order.

## Shared Surface

- Prompts:
  - [architecture-evaluate.prompt.md](../../prompts/architecture-evaluate.prompt.md)
  - [architecture-integration.prompt.md](../../prompts/architecture-integration.prompt.md)
  - [migration-plan.prompt.md](../../prompts/migration-plan.prompt.md)
  - [tech-lead-document-architecture.prompt.md](../../prompts/tech-lead-document-architecture.prompt.md)
- Instructions:
  - [architectural-integration.instructions.md](../../../instructions/architectural-integration.instructions.md)
  - [mermaid-theme.instructions.md](../../../instructions/mermaid-theme.instructions.md)
  - [tool-usage.instructions.md](../../../instructions/tool-usage.instructions.md)
- Agents:
  - [system-architect.agent.md](../../system-architect/system-architect.agent.md)
  - [tech-manager.agent.md](../../../operations/tech-manager/tech-manager.agent.md)

## Portable Runtime Notes

- Treat the installed prompt, instruction, and agent surfaces as the authoritative local context.
- Keep outputs architecture-only: ADRs, diagrams, trade-off matrices, and migration plans.
- Hand off implementation to engineering, Azure, or operations agents instead of embedding code in the architecture skill.
