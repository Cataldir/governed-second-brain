---
name: platform-quality
description: Use this skill when you need CI/CD audits, dependency reviews, platform quality checks, or operational remediation plans.
argument-hint: Describe the platform area, pipeline, dependency set, or reliability concern you want assessed.
user-invocable: true
disable-model-invocation: true
---

# Platform Quality Skill

Use this skill to run the manual platform workflow with the installed [PlatformEngineer](../platform-quality.agent.md).

## Load Order

1. Start with the shared [operations skill guide](../_shared/operations/guide.md) and confirm the installed operations agent surface before choosing a platform route.
2. Start from the platform prompt surface:
   - [platform-cicd-audit.prompt.md](../../prompts/platform-cicd-audit.prompt.md)
   - [platform-dependency-audit.prompt.md](../../prompts/platform-dependency-audit.prompt.md)
   - [platform-quality-evaluation.prompt.md](../../prompts/platform-quality-evaluation.prompt.md)
   - [security-audit.prompt.md](../../prompts/security-audit.prompt.md)
   - [ship-deploy-hotfix.prompt.md](../../prompts/ship-deploy-hotfix.prompt.md)
3. Load the shared instructions:
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [team-mapping.md](../../agents/team-mapping.md)
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
4. Use the portable task-routing and escalation rules in the [operations skill guide](../_shared/operations/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce an audit, remediation backlog, rollout check, or quality gate recommendation.
- Escalate language-specific implementation work to the matching engineering specialist.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not use it to bypass the canonical planning or PR-review path.
