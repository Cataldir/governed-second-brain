---
name: "Business: Risk Assessment"
description: "Build a risk matrix for a specific decision combining technical, financial, market, and regulatory perspectives."
agent: "TechLeadOrchestrator"
argument-hint: "Describe the decision or initiative to assess. Include the options under consideration and known constraints."
---

Coordinate a multi-dimensional risk assessment:

1. **Risk Identification** — Invoke `RiskAnalyst` via `#runSubagent` to:
   - Catalog all risk categories: technical, market, financial, regulatory, operational, reputational
   - For each category, identify specific risk events with trigger conditions
   - Map risk interdependencies (which risks cascade to others)

2. **Technical Risk** — Invoke `SystemArchitect` via `#runSubagent` to assess:
   - Architecture complexity and failure mode analysis
   - Technology maturity and community support trajectory
   - Integration risk with existing systems
   - Scalability limits and performance cliffs

3. **Financial Risk** — Invoke `FinancialModeler` via `#runSubagent` to quantify:
   - Cost overrun scenarios (1.5x, 2x, 3x budget)
   - Revenue impact of delay (opportunity cost per month)
   - Sunk cost exposure at each project stage
   - Break-even sensitivity to key assumptions

4. **Market & Competitive Risk** — Invoke `CompetitiveIntelAnalyst` via `#runSubagent` to evaluate:
   - Competitive response probability and impact
   - Market timing risk (too early, too late, disruption)
   - Customer adoption risk (willingness to switch, change management)

5. **Process & Execution Risk** — Invoke `ProcessImprover` via `#runSubagent` to assess:
   - Team capacity and skill gaps
   - Process maturity for the type of work required
   - Dependency chain fragility (critical path analysis)

6. **Risk Matrix & Mitigation** — Deliver:
   - Risk matrix (likelihood × impact) with heat map
   - Top 5 risks with detailed mitigation strategies
   - Risk-adjusted decision recommendation per option
   - Monitoring triggers (early warning signals for each major risk)
   - Contingency plans for the top 3 risks
