---
name: "Business: Financial Modeling"
description: "Build a decision-ready financial model with explicit assumptions, scenarios, and sensitivity analysis."
agent: "TechLeadOrchestrator"
argument-hint: "Describe the business scenario, decision horizon, major assumptions, and the model output you need. Include cost, revenue, and pricing inputs when available."
---

Coordinate a financial-modeling workflow:

1. **Model Framing** — Invoke `BusinessStrategist` via `#runSubagent` when the decision context needs clarification:
   - What business decision the model must support
   - The target segment, offer shape, and decision horizon
   - The operating assumptions that materially affect the model

2. **Financial Model** — Invoke `FinancialModeler` via `#runSubagent` to build:
   - Assumptions table with source quality and confidence level
   - Base, optimistic, and downside scenarios
   - ROI, NPV, payback, breakeven, or unit-economics analysis as appropriate
   - Sensitivity analysis for the most fragile inputs

3. **Market Inputs** — Invoke `CompetitiveIntelAnalyst` via `#runSubagent` when price or demand depends on market context:
   - Reference pricing and packaging ranges
   - Comparable commercial motions
   - Market signals that support or weaken the assumptions

4. **Risk Overlay** — Invoke `RiskAnalyst` via `#runSubagent` when exposure needs explicit treatment:
   - Assumption failure modes
   - Cost-overrun and schedule-risk implications
   - Monitoring triggers for the most important risks

5. **Decision Package** — Deliver:
   - Final model summary and scenario comparison
   - Assumptions that matter most and their evidence strength
   - Recommended decision with financial caveats
   - Follow-up data required to improve model confidence
