---
name: risk-analysis-agent
description: Use this skill when you need scenario planning, risk quantification, compliance mapping, or mitigation design across business and delivery decisions.
argument-hint: Describe the scenario, risk horizon, constraints, and the risk artifact you need.
user-invocable: true
disable-model-invocation: true
---

# Risk Analysis Skill

Use this skill to run the manual risk workflow with the installed [RiskAnalyst](../risk-analysis-agent.agent.md).

## Load Order

1. Start with the shared [business-acumen skill guide](../_shared/business-acumen/guide.md) and confirm the installed business agent surface before choosing a risk route.
2. Start from the risk prompt surface:
   - [business-risk-assessment.prompt.md](../../prompts/business-risk-assessment.prompt.md)
   - [tech-lead-innovation-research.prompt.md](../../prompts/tech-lead-innovation-research.prompt.md)
   - [security-audit.prompt.md](../../prompts/security-audit.prompt.md)
3. Load the supporting guidance:
   - [tool-usage.instructions.md](../../instructions/tool-usage.instructions.md)
   - [mermaid-theme.instructions.md](../../instructions/mermaid-theme.instructions.md)
4. Use the portable evidence and escalation rules in the [business-acumen skill guide](../_shared/business-acumen/guide.md) when the workflow crosses repository boundaries.

## Output Contract

- Produce a risk register, mitigation plan, scenario matrix, or quantified exposure assessment.
- Call out where compliance or architecture input is still missing rather than guessing.

## Boundaries

- Keep this skill repo-local and manual-first.
- Do not let the skill become the authoritative policy source for controls or compliance.
