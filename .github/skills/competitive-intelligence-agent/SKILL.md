---
name: competitive-intelligence-agent
description: Use this skill when you need competitor mapping, win-loss interpretation, TAM/SAM/SOM framing, or adjacent-market intelligence.
argument-hint: Describe the market, competitor set, and the intelligence output you need.
user-invocable: true
disable-model-invocation: true
---

# Competitive Intelligence Skill

Use this skill to run the manual intelligence workflow with the installed [CompetitiveIntelAnalyst](../competitive-intelligence-agent.agent.md).

## Load Order

1. Start with the shared [business-acumen skill guide](../_shared/business-acumen/guide.md) and confirm the installed business agent surface before choosing an intelligence route.
2. Start from the nearest prompt surface:
   - [business-competitive-intelligence.prompt.md](../../prompts/business-competitive-intelligence.prompt.md)
   - [business-evaluate-opportunity.prompt.md](../../prompts/business-evaluate-opportunity.prompt.md)
   - [tech-lead-innovation-research.prompt.md](../../prompts/tech-lead-innovation-research.prompt.md)
3. Load the shared guidance that affects evidence gathering:
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Use the portable evidence and escalation rules in the [business-acumen skill guide](../_shared/business-acumen/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce a competitor map, market-positioning brief, or evidence-backed win-loss narrative.
- Keep publishing-book competition separate and hand that work to the repo-local publishing-competition workflow when it is available.

## Boundaries

- Keep this skill repo-local and manual-first.
