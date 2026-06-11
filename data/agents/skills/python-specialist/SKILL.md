---
name: python-specialist
description: Use this skill when you need repository-aligned Python implementation, review, refactoring, testing, or async design workflows.
argument-hint: Describe the Python task, target files, framework, and validation you need.
user-invocable: true
disable-model-invocation: true
---

# Python Specialist Skill

Use this skill to run the manual Python workflow with the installed [PythonDeveloper](../python-specialist.agent.md).

## Load Order

1. Start with the shared [engineering skill guide](../_shared/engineering/guide.md) and confirm the installed engineering agent surface before choosing an implementation path.
2. Start from the Python prompt surface:
   - [python-implement.prompt.md](../../prompts/python-implement.prompt.md)
   - [python-refactor.prompt.md](../../prompts/python-refactor.prompt.md)
   - [python-review.prompt.md](../../prompts/python-review.prompt.md)
   - [codebase-onboarding.prompt.md](../../prompts/codebase-onboarding.prompt.md)
3. Load the shared engineering instructions:
   - [paradigm-priority.instructions.md](../../instructions/paradigm-priority.instructions.md)
   - [pattern-reasoning.instructions.md](../../instructions/pattern-reasoning.instructions.md)
   - [refactoring-techniques.instructions.md](../../instructions/refactoring-techniques.instructions.md)
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
4. Use the portable tool, review, and escalation rules in the [engineering skill guide](../_shared/engineering/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce implementation notes, review findings, or code changes with tests or explicit validation steps.
- Escalate architecture to [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md) and CI/CD concerns to [platform-quality.agent.md](../../../operations/platform-quality/platform-quality.agent.md).

## Boundaries

- Keep the workflow repo-local and manual-first.
- Do not restate Python policy that already lives in the canonical agent file or instruction fragments.
