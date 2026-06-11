---
name: financial-modeling-agent
description: Use this skill when you need ROI, NPV, unit economics, pricing, or scenario-modeling workflows grounded in repository evidence.
argument-hint: Describe the business scenario, time horizon, assumptions, and the financial model you need.
user-invocable: true
disable-model-invocation: true
---

# Financial Modeling Skill

Use this skill to run the manual finance-model workflow with the installed [FinancialModeler](../financial-modeling-agent.agent.md).

## Load Order

1. Start with the shared [business-acumen skill guide](../_shared/business-acumen/guide.md) and confirm the installed business agent surface before choosing a modeling route.
2. Start from the nearest prompt surface:
   - [business-financial-modeling.prompt.md](../../prompts/business-financial-modeling.prompt.md)
   - [business-go-to-market.prompt.md](../../prompts/business-go-to-market.prompt.md)
   - [business-evaluate-opportunity.prompt.md](../../prompts/business-evaluate-opportunity.prompt.md)
3. Load the shared guidance that affects analysis quality:
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Use the portable evidence and escalation rules in the [business-acumen skill guide](../_shared/business-acumen/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce a financial model, assumptions table, scenario comparison, or ROI recommendation.
- Mark assumptions explicitly when canonical repository evidence is incomplete.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not treat prompt text or intermediate calculations as the authoritative financial record.
