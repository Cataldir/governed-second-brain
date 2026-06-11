---
name: "Business: Go-to-Market Strategy"
description: "Develop a go-to-market plan with positioning, pricing, channel strategy, and competitive differentiation."
agent: "TechLeadOrchestrator"
argument-hint: "Describe the product or service, target audience, and launch timeline. Include competitive context and pricing constraints."
---

Coordinate GTM strategy development:

**Delegation compatibility**: If the workspace has `team-mapping.md`, resolve exact agent names from it before calling `#runSubagent`. Otherwise, use the canonical agent names in this prompt and fall back to current-agent execution if a specialist is unavailable.

1. **Market Positioning** — Invoke `BusinessStrategist` via `#runSubagent` to define:
   - Value proposition (Jobs-to-be-Done framework)
   - Positioning statement (for whom, what, why different)
   - Messaging pillars (3-5 core themes)
   - Go-to-market channels (direct, partner, PLG, enterprise sales)

2. **Competitive Positioning** — Invoke `CompetitiveIntelAnalyst` via `#runSubagent` to identify:
   - Feature comparison matrix vs top 3-5 competitors
   - Pricing landscape analysis
   - Competitor weaknesses we can exploit
   - Market gaps and underserved segments

3. **Pricing & Revenue Model** — Invoke `FinancialModeler` via `#runSubagent` to develop:
   - Pricing tiers (free/starter/pro/enterprise)
   - Revenue model (subscription, usage-based, freemium, one-time)
   - Sensitivity analysis: price elasticity, conversion rate scenarios
   - Break-even timeline under each pricing model

4. **Risk & Compliance** — Invoke `RiskAnalyst` via `#runSubagent` to assess:
   - Launch risks (timing, competitive response, dependency on partners)
   - Regulatory or compliance blockers for the target market
   - Reputation risks from positioning claims

5. **GTM Plan** — Deliver:
   - Launch timeline with milestones
   - Channel-by-channel execution plan
   - Success metrics and measurement cadence (MRR, CAC, activation rate)
   - First 90-day action items
