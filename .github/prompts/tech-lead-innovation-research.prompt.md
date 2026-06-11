---
name: "Tech Lead: Innovation Research"
description: "Research innovative solutions by coordinating business strategy agents for opportunity framing and technical agents for feasibility analysis."
agent: "TechLeadOrchestrator"
argument-hint: "Describe the problem space or opportunity to explore. Include business constraints, current limitations, and desired outcomes."
---

Coordinate a concise multi-agent innovation research cycle.

If `team-mapping.md` exists, resolve exact agent names from it before calling `#runSubagent`. Otherwise, use the canonical names below and fall back to current-agent execution only when a specialist is unavailable.

1. Frame the opportunity with `BusinessStrategist`, `CompetitiveIntelAnalyst`, `FinancialModeler`, and `RiskAnalyst`. Focus on strategic fit, competitive differentiation, ROI, and key risks.
2. Survey the state of the art with workspace and web research. Cover recent papers, active frameworks, adoption trends, and credible open-source implementations.
3. Validate technical feasibility with `SystemArchitect`, the relevant language specialist or specialists, and `PlatformEngineer`. Focus on architectural fit, migration path, prototype viability, and operational burden.
4. Synthesize the findings into a decision matrix scoring business value, technical feasibility, time-to-value, operational cost, and risk.
5. Recommend the top one or two options and define a time-boxed proof of concept. If the user approves, delegate implementation to the appropriate specialists.

Deliver a concise innovation brief with:

- opportunity summary
- candidate comparison matrix
- recommended approach and rationale
- proof-of-concept scope, success criteria, and main risks
