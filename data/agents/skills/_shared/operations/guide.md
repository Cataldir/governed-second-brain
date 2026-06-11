# Operations Skill Guide

Use this guide when a shared operations skill needs a portable load order.

## Shared Surface

- Prompts:
  - [customization-gap-audit.prompt.md](../../prompts/customization-gap-audit.prompt.md)
  - [workflow-job-orchestrator.prompt.md](../../prompts/workflow-job-orchestrator.prompt.md)
  - [tech-lead-plan.prompt.md](../../../architecture/prompts/tech-lead-plan.prompt.md)
  - [tech-lead-investigate.prompt.md](../../../architecture/prompts/tech-lead-investigate.prompt.md)
  - [tech-lead-issue-execute.prompt.md](../../../architecture/prompts/tech-lead-issue-execute.prompt.md)
  - [tech-lead-issue-correction.prompt.md](../../../architecture/prompts/tech-lead-issue-correction.prompt.md)
  - [platform-cicd-audit.prompt.md](../../prompts/platform-cicd-audit.prompt.md)
  - [platform-dependency-audit.prompt.md](../../prompts/platform-dependency-audit.prompt.md)
  - [platform-quality-evaluation.prompt.md](../../prompts/platform-quality-evaluation.prompt.md)
  - [pr-review.prompt.md](../../prompts/pr-review.prompt.md)
  - [connector-audit.prompt.md](../../../architecture/prompts/connector-audit.prompt.md)
  - [connector-design.prompt.md](../../../architecture/prompts/connector-design.prompt.md)
- Instructions:
  - [tool-usage.instructions.md](../../../instructions/tool-usage.instructions.md)
  - [team-mapping.md](../../../agents/team-mapping.md)
  - [architectural-integration.instructions.md](../../../instructions/architectural-integration.instructions.md)
- Agents:
  - [tech-manager.agent.md](../../tech-manager/tech-manager.agent.md)
  - [platform-quality.agent.md](../../platform-quality/platform-quality.agent.md)
  - [pr-evaluator.agent.md](../../pr-evaluator/pr-evaluator.agent.md)
  - [enterprise-connectors.agent.md](../../enterprise-connectors/enterprise-connectors.agent.md)
- Shared skills:
  - [customization-gap-audit/SKILL.md](customization-gap-audit/SKILL.md)
  - [rubric-based-evaluation/SKILL.md](rubric-based-evaluation/SKILL.md)

## Portable Runtime Notes

- Keep execution order, quality gates, and ownership boundaries explicit.
- Use the workflow orchestrator prompt when the task spans evidence gathering, synthesis, and validation.
- Escalate system-level trade-offs to SystemArchitect when an operational question becomes architectural.
