---
name: business-strategy-agent
description: Use this skill when you need opportunity framing, go-to-market design, competitive positioning, or strategic recommendation workflows.
argument-hint: Describe the market, product, or strategic question and the business outcome you need.
user-invocable: true
disable-model-invocation: true
---

# Business Strategy Skill

Use this skill to run the manual strategy workflow with the installed [BusinessStrategist](../business-strategy-agent.agent.md).

## Load Order

1. Start with the shared [business-acumen skill guide](../_shared/business-acumen/guide.md) and confirm the installed business agent surface before choosing a strategy route.
2. Start from the business prompt surface:
   - [business-go-to-market.prompt.md](../../prompts/business-go-to-market.prompt.md)
   - [business-evaluate-opportunity.prompt.md](../../prompts/business-evaluate-opportunity.prompt.md)
   - [business-competitive-intelligence.prompt.md](../../prompts/business-competitive-intelligence.prompt.md)
3. Load the shared guidance that affects decision framing:
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Use the portable evidence and escalation rules in the [business-acumen skill guide](../_shared/business-acumen/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce a strategy brief, decision matrix, or go-to-market recommendation with explicit trade-offs.
- Hand off financial depth, competitive signals, and risk analysis to the matching business specialists.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not let the skill become a new source of policy or market truth.
