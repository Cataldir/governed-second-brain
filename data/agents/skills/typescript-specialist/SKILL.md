---
name: typescript-specialist
description: Use this skill when you need repository-aligned TypeScript or React implementation, review, or refactoring workflows.
argument-hint: Describe the TypeScript task, target files, framework, and validation you need.
user-invocable: true
disable-model-invocation: true
---

# TypeScript Specialist Skill

Use this skill to run the manual TypeScript workflow with the installed [TypeScriptDeveloper](../typescript-specialist.agent.md).

## Load Order

1. Start with the shared [engineering skill guide](../_shared/engineering/guide.md) and confirm the installed engineering agent surface before choosing an implementation path.
2. Start from the TypeScript prompt surface:
   - [typescript-implement.prompt.md](../../prompts/typescript-implement.prompt.md)
   - [typescript-review.prompt.md](../../prompts/typescript-review.prompt.md)
   - [ui-design-component.prompt.md](../../prompts/ui-design-component.prompt.md)
   - [codebase-onboarding.prompt.md](../../prompts/codebase-onboarding.prompt.md)
3. Load the shared engineering instructions:
   - [paradigm-priority.instructions.md](../../instructions/paradigm-priority.instructions.md)
   - [pattern-reasoning.instructions.md](../../instructions/pattern-reasoning.instructions.md)
   - [refactoring-techniques.instructions.md](../../instructions/refactoring-techniques.instructions.md)
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
4. Use the portable tool, review, and escalation rules in the [engineering skill guide](../_shared/engineering/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce implementation notes, review findings, or code changes with build, lint, and test validation.
- Escalate accessibility and interaction design to [ui-agent.agent.md](../../ui-agent/ui-agent.agent.md) when the task becomes UI-led.

## Boundaries

- Keep the workflow repo-local and manual-first.
- Do not replace the canonical TypeScript agent or the shared engineering instruction fragments.
