---
name: pr-evaluator
description: Use this skill when you need PR architecture review, merge safety checks, or validation that planned work matches repository standards.
argument-hint: Describe the PR, branch, or change scope and the review outcome you need.
user-invocable: true
disable-model-invocation: true
---

# PR Evaluator Skill

Use this skill to run the manual PR review workflow with the installed [PRReviewer](../pr-evaluator.agent.md).

## Load Order

1. Start with the shared [operations skill guide](../_shared/operations/guide.md) and confirm the installed operations agent surface before choosing a review route.
2. Start from the review prompt surface:
   - [pr-review.prompt.md](../../prompts/pr-review.prompt.md)
   - [security-audit.prompt.md](../../prompts/security-audit.prompt.md)
   - [tech-lead-plan.prompt.md](../../prompts/tech-lead-plan.prompt.md)
3. Load the shared instructions:
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [team-mapping.md](../../agents/team-mapping.md)
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
4. Use the portable task-routing and escalation rules in the [operations skill guide](../_shared/operations/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce findings, residual risks, validation gaps, and merge readiness guidance.
- Coordinate with [system-architect.agent.md](../../../architecture/system-architect/system-architect.agent.md) when architecture sign-off is required.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not use it as a substitute for running the relevant tests or validations.
