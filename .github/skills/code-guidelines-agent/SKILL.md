---
name: code-guidelines-agent
description: Use this skill when you need educational code review, sample quality checks, or language-specific guidance for book, paper, course, and notebook code.
argument-hint: Describe the code sample, target language, and the review or rewrite outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Code Guidelines Skill

Use this skill to run the manual review workflow with the installed [CodeReviewer](../code-guidelines-agent.agent.md).

## Load Order

1. Start with the shared [engineering skill guide](../_shared/engineering/guide.md) and confirm the installed engineering agent surface before choosing a review route.
2. Start from the nearest review prompt surface:
   - [code-sample-review.prompt.md](../../prompts/code-sample-review.prompt.md)
   - [python-review.prompt.md](../../prompts/python-review.prompt.md)
   - [rust-review.prompt.md](../../prompts/rust-review.prompt.md)
   - [typescript-review.prompt.md](../../prompts/typescript-review.prompt.md)
   - [codebase-onboarding.prompt.md](../../prompts/codebase-onboarding.prompt.md)
3. Load the shared engineering instructions:
   - [paradigm-priority.instructions.md](../../instructions/paradigm-priority.instructions.md)
   - [pattern-reasoning.instructions.md](../../instructions/pattern-reasoning.instructions.md)
   - [refactoring-techniques.instructions.md](../../instructions/refactoring-techniques.instructions.md)
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
4. Use the portable validation and escalation rules in the [engineering skill guide](../_shared/engineering/guide.md) whenever the review crosses repository boundaries or tool surfaces.

## Output Contract

- Return findings, requested rewrites, or quality gates for educational code samples.
- Escalate full implementation to the matching language specialist and architecture questions to [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md).

## Boundaries

- This skill complements the canonical code-review agent; it does not replace language-specific specialists.
- Keep the workflow manual-first and repo-local.
