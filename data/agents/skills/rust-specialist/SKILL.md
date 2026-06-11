---
name: rust-specialist
description: Use this skill when you need repository-aligned Rust implementation, review, refactoring, or safety checks.
argument-hint: Describe the Rust task, target files, crate context, and validation you need.
user-invocable: true
disable-model-invocation: true
---

# Rust Specialist Skill

Use this skill to run the manual Rust workflow with the installed [RustDeveloper](../rust-specialist.agent.md).

## Load Order

1. Start with the shared [engineering skill guide](../_shared/engineering/guide.md) and confirm the installed engineering agent surface before choosing an implementation path.
2. Start from the Rust prompt surface:
   - [rust-implement.prompt.md](../../prompts/rust-implement.prompt.md)
   - [rust-review.prompt.md](../../prompts/rust-review.prompt.md)
   - [codebase-onboarding.prompt.md](../../prompts/codebase-onboarding.prompt.md)
3. Load the shared engineering instructions:
   - [paradigm-priority.instructions.md](../../instructions/paradigm-priority.instructions.md)
   - [pattern-reasoning.instructions.md](../../instructions/pattern-reasoning.instructions.md)
   - [refactoring-techniques.instructions.md](../../instructions/refactoring-techniques.instructions.md)
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
4. Use the portable tool, review, and escalation rules in the [engineering skill guide](../_shared/engineering/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce implementation notes, review findings, or code changes with cargo/test validation steps.
- Escalate architecture to [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md) and pipeline concerns to [platform-quality.agent.md](../../../operations/platform-quality/platform-quality.agent.md).

## Boundaries

- Keep this skill manual-first and repo-local.
- Use the canonical Rust agent and instruction fragments as the source of truth for language behavior.
