# Engineering Skill Guide

Use this guide when a shared engineering skill needs a portable load order.

## Shared Surface

- Prompts:
  - [python-implement.prompt.md](../../prompts/python-implement.prompt.md)
  - [python-refactor.prompt.md](../../prompts/python-refactor.prompt.md)
  - [python-review.prompt.md](../../prompts/python-review.prompt.md)
  - [rust-implement.prompt.md](../../prompts/rust-implement.prompt.md)
  - [rust-review.prompt.md](../../prompts/rust-review.prompt.md)
  - [typescript-implement.prompt.md](../../prompts/typescript-implement.prompt.md)
  - [typescript-review.prompt.md](../../prompts/typescript-review.prompt.md)
  - [ui-design-component.prompt.md](../../prompts/ui-design-component.prompt.md)
  - [ui-accessibility-audit.prompt.md](../../prompts/ui-accessibility-audit.prompt.md)
  - [code-sample-review.prompt.md](../../prompts/code-sample-review.prompt.md)
- Instructions:
  - [paradigm-priority.instructions.md](../../../instructions/paradigm-priority.instructions.md)
  - [pattern-reasoning.instructions.md](../../../instructions/pattern-reasoning.instructions.md)
  - [refactoring-techniques.instructions.md](../../../instructions/refactoring-techniques.instructions.md)
  - [architectural-integration.instructions.md](../../../instructions/architectural-integration.instructions.md)
  - [tool-usage.instructions.md](../../../instructions/tool-usage.instructions.md)
- Agents:
  - [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md)
  - [platform-quality.agent.md](../../../operations/platform-quality/platform-quality.agent.md)
  - [ui-agent.agent.md](../../ui-agent/ui-agent.agent.md)

## Portable Runtime Notes

- Read the installed code and tests before changing anything.
- Keep findings first when the task is a review, and keep validation explicit when the task is an implementation.
- Escalate architecture to SystemArchitect and CI/CD or rollout issues to PlatformEngineer.
