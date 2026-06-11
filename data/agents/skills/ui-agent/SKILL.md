---
name: ui-agent
description: Use this skill when you need repository-aligned UI design, accessibility, responsive layout, or interface quality workflows.
argument-hint: Describe the UI problem, target surface, constraints, and audit or design outcome you need.
user-invocable: true
disable-model-invocation: true
---

# UI Agent Skill

Use this skill to run the manual interface workflow with the installed [UIDesigner](../ui-agent.agent.md).

## Load Order

1. Start with the shared [engineering skill guide](../_shared/engineering/guide.md) and confirm the installed engineering agent surface before choosing a design route.
2. Start from the UI prompt surface:
   - [ui-design-component.prompt.md](../../prompts/ui-design-component.prompt.md)
   - [ui-accessibility-audit.prompt.md](../../prompts/ui-accessibility-audit.prompt.md)
   - [typescript-implement.prompt.md](../../prompts/typescript-implement.prompt.md)
3. Load the shared guidance that affects UI work:
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Use the portable tool, review, and escalation rules in the [engineering skill guide](../_shared/engineering/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce interface recommendations, accessibility findings, component plans, or implementation-ready UI notes.
- Hand off TypeScript-heavy coding work to [typescript-specialist.agent.md](../../typescript-specialist/typescript-specialist.agent.md) when the task shifts from design to implementation.

## Boundaries

- Keep this skill repo-local and manual-first.
- Use the canonical UI agent as the primary source of behavior and standards.
