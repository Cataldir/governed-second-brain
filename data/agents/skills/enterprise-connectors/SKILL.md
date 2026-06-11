---
name: enterprise-connectors
description: Use this skill when you need enterprise connector design, adapter audits, or integration boundary planning for external systems.
argument-hint: Describe the target platform, integration pattern, data flow, and the connector outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Enterprise Connectors Skill

Use this skill to run the manual connector workflow with the installed [ConnectorEngineer](../enterprise-connectors.agent.md).

## Load Order

1. Start with the shared [operations skill guide](../_shared/operations/guide.md) and confirm the installed operations agent surface before choosing a connector route.
2. Start from the connector prompt surface:
   - [connector-design.prompt.md](../../prompts/connector-design.prompt.md)
   - [connector-audit.prompt.md](../../prompts/connector-audit.prompt.md)
   - [codebase-onboarding.prompt.md](../../prompts/codebase-onboarding.prompt.md)
3. Load the most relevant instructions:
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
   - [pattern-reasoning.instructions.md](../../instructions/pattern-reasoning.instructions.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
4. Use the portable task-routing and escalation rules in the [operations skill guide](../_shared/operations/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce an adapter design, audit checklist, boundary contract, or remediation plan.
- Escalate deep architecture trade-offs to [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md).

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not turn connector guidance into repository policy or runtime configuration truth.
