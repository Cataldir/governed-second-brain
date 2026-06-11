---
name: "Business: Evaluate Opportunity"
description: "Full opportunity analysis combining strategy, competitive intelligence, financial modeling, and risk assessment."
agent: "TechLeadOrchestrator"
argument-hint: "Describe the opportunity: market, problem being solved, target customer, and any initial hypotheses. Include budget constraints and timeline."
---

Coordinate a comprehensive opportunity evaluation across all business acumen agents:

**Delegation compatibility**: If the workspace has `team-mapping.md`, resolve exact agent names from it before calling `#runSubagent`. Otherwise, use the canonical agent names in this prompt and fall back to current-agent execution if a specialist is unavailable.

1. **Strategic Fit** — Invoke `BusinessStrategist` via `#runSubagent` to assess:
   - Porter's Five Forces analysis for the target market
   - SWOT assessment of our position relative to the opportunity
   - Business Model Canvas for the proposed approach
   - Strategic alignment with existing capabilities and roadmap

2. **Competitive Landscape** — Invoke `CompetitiveIntelAnalyst` via `#runSubagent` to research:
   - TAM/SAM/SOM sizing for the opportunity
   - Competitor mapping (direct, indirect, emerging)
   - Win/loss patterns in the space — what works, what fails
   - Differentiation vectors available to us

3. **Financial Viability** — Invoke `FinancialModeler` via `#runSubagent` to model:
   - Unit economics (CAC, LTV, payback period)
   - P&L projection (12-month, 36-month)
   - Pricing strategy options with revenue sensitivity analysis
   - ROI/NPV under optimistic, base, and pessimistic scenarios

4. **Risk Matrix** — Invoke `RiskAnalyst` via `#runSubagent` to evaluate:
   - Technical risk (can we build it? do we have the skills?)
   - Market risk (will customers pay? is the timing right?)
   - Regulatory risk (compliance, data privacy, industry regulations)
   - Execution risk (team bandwidth, competing priorities, dependencies)

5. **Process Feasibility** — Invoke `ProcessImprover` via `#runSubagent` to assess:
   - Operational readiness (do we have the processes to support this?)
   - Capacity requirements vs current capacity
   - Bottlenecks in delivery pipeline

6. **Decision Package** — Synthesize into a go/no-go recommendation:
   - Opportunity score (weighted across all dimensions)
   - Key assumptions that must hold true
   - Minimum viable scope to validate the opportunity
   - Investment required vs expected return timeline
