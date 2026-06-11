---
name: "Business: Competitive Intelligence"
description: "Build a market and competitor intelligence brief with positioning, pricing, and differentiation evidence."
agent: "TechLeadOrchestrator"
argument-hint: "Describe the market, competitor set, and the strategic question to answer. Include region, segment, and any assumptions already in play."
---

Coordinate a focused competitive-intelligence pass:

1. **Market Scope** — Invoke `BusinessStrategist` via `#runSubagent` to define:
   - The target segment, buyer, and adjacent markets in scope
   - The strategic question this analysis must answer
   - The evaluation criteria for differentiation

2. **Competitor Mapping** — Invoke `CompetitiveIntelAnalyst` via `#runSubagent` to research:
   - Direct, indirect, and emerging competitors
   - Positioning and feature narratives for the top competitors
   - Pricing models, packaging, and commercial signals
   - Recent moves, launches, or partnership signals that affect the space

3. **Commercial Impact** — Invoke `FinancialModeler` via `#runSubagent` when pricing or investment choices matter:
   - Relative price-to-value positioning
   - Margin or revenue sensitivity implied by the competitive landscape
   - Likely monetization trade-offs for each positioning option

4. **Decision Brief** — Deliver:
   - Competitor map with categories and threat level
   - Pricing and packaging comparison table
   - Differentiation vectors we can credibly sustain
   - Key unknowns, weak assumptions, and recommended next evidence to gather
