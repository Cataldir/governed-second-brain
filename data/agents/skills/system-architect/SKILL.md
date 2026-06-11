---
name: system-architect
description: Use this skill when you need architecture reviews, ADR drafts, migration plans, pattern selection, or C4-style Mermaid diagrams in this repository.
argument-hint: Describe the system, constraints, and the architecture artifact you need.
user-invocable: true
disable-model-invocation: true
---

# System Architect Skill

Use this skill to run the manual architecture workflow with the installed [SystemArchitect](../system-architect.agent.md).

## Load Order

1. Start with the shared [architecture skill guide](../_shared/architecture/guide.md) and confirm the installed architecture agent surface before choosing an execution path.
2. Start from the architecture prompt surface:
   - [architecture-evaluate.prompt.md](../../prompts/architecture-evaluate.prompt.md)
   - [architecture-integration.prompt.md](../../prompts/architecture-integration.prompt.md)
   - [migration-plan.prompt.md](../../prompts/migration-plan.prompt.md)
   - [tech-lead-document-architecture.prompt.md](../../prompts/tech-lead-document-architecture.prompt.md)
3. Load the supporting instructions:
   - [architectural-integration.instructions.md](../../instructions/architectural-integration.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Reuse the portable prompts, instructions, and agent links in the [architecture skill guide](../_shared/architecture/guide.md) when the task crosses repository boundaries.

## Output Contract

- Produce an ADR, decision matrix, integration plan, or Mermaid diagram with explicit trade-offs.
- Delegate implementation work to the matching engineering, Azure, or operations agent instead of expanding into code here.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not restate repository policy or replace the canonical agent definition.
