---
name: process-management-agent
description: Use this skill when you need BPMN-style process mapping, operational bottleneck analysis, or workflow redesign guidance.
argument-hint: Describe the process, bottleneck, cadence, or operational improvement target you want analyzed.
user-invocable: true
disable-model-invocation: true
---

# Process Management Skill

Use this skill to run the manual process workflow with the installed [ProcessImprover](../process-management-agent.agent.md).

## Load Order

1. Start with the shared [business-acumen skill guide](../_shared/business-acumen/guide.md) and confirm the installed business agent surface before choosing a process route.
2. Start from the process prompt surface:
   - [business-process-audit.prompt.md](../../prompts/business-process-audit.prompt.md)
   - [workflow-job-orchestrator.prompt.md](../../../operations/prompts/workflow-job-orchestrator.prompt.md)
   - [tech-lead-plan.prompt.md](../../prompts/tech-lead-plan.prompt.md)
3. Load the supporting guidance:
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Use the portable evidence and escalation rules in the [business-acumen skill guide](../_shared/business-acumen/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce a process map, bottleneck analysis, or prioritized improvement plan.
- Escalate governance or architecture issues to [tech-manager.agent.md](../../../operations/tech-manager/tech-manager.agent.md) or [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md) when the scope stops being process-local.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not convert process guidance into canonical workflow policy without an explicit repository decision.
