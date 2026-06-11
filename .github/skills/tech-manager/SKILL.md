---
name: tech-manager
description: Use this skill when you need technical planning, orchestration, delegation briefs, or cross-domain execution guidance in this repository.
argument-hint: Describe the initiative, scope, constraints, and the planning or orchestration output you need.
user-invocable: true
disable-model-invocation: true
---

# Tech Manager Skill

Use this skill to run the manual orchestration workflow with the installed [TechLeadOrchestrator](../tech-manager.agent.md).

## Load Order

1. Start with the shared [operations skill guide](../_shared/operations/guide.md) and confirm the installed operations agent surface before choosing an orchestration path.
2. Start from the planning prompt surface:
   - [tech-lead-plan.prompt.md](../../prompts/tech-lead-plan.prompt.md)
   - [tech-lead-investigate.prompt.md](../../prompts/tech-lead-investigate.prompt.md)
   - [tech-lead-issue-execute.prompt.md](../../prompts/tech-lead-issue-execute.prompt.md)
   - [tech-lead-issue-correction.prompt.md](../../prompts/tech-lead-issue-correction.prompt.md)
   - [tech-lead-innovation-research.prompt.md](../../prompts/tech-lead-innovation-research.prompt.md)
   - [workflow-job-orchestrator.prompt.md](../../prompts/workflow-job-orchestrator.prompt.md)
3. Load the orchestration instructions:
   - [team-mapping.md](../../agents/team-mapping.md)
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Use the portable task-routing and escalation rules in the [operations skill guide](../_shared/operations/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce a scoped plan, delegation brief, acceptance criteria, risks, and a clear execution order.
- Hand off implementation to the matching specialist instead of turning this skill into a coding surface.

## Boundaries

- This skill is repo-local and manual-first.
- Do not replace canonical planning, governance, or delegation rules.
