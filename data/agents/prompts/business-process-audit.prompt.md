---
name: "Business: Process Audit"
description: "Identify bottlenecks, waste, and improvement opportunities in technical and operational workflows."
agent: "TechLeadOrchestrator"
argument-hint: "Describe the process or workflow to audit. Include current pain points, cycle times, and stakeholders involved."
---

Coordinate a multi-agent process audit:

1. **Process Mapping** — Invoke `ProcessImprover` via `#runSubagent` to:
   - Map the current process as BPMN (swimlane diagram via Mermaid)
   - Identify all handoffs, wait states, and decision points
   - Measure cycle time per stage (actual vs expected)
   - Classify steps as value-add, necessary non-value-add, or waste

2. **Bottleneck Analysis** — Invoke `ProcessImprover` via `#runSubagent` to:
   - Apply Theory of Constraints to identify the binding constraint
   - Calculate throughput at each stage
   - Quantify queue times and batch sizes
   - Map dependencies that create blocking

3. **Risk Assessment** — Invoke `RiskAnalyst` via `#runSubagent` to evaluate:
   - Failure modes at each process step (FMEA)
   - Single points of failure (bus factor, manual steps, tribal knowledge)
   - Compliance gaps in the current process

4. **Technical Automation Opportunities** — Invoke `PlatformEngineer` via `#runSubagent` to assess:
   - Which manual steps can be automated (CI/CD, scripts, integrations)
   - Tool gaps (missing monitoring, alerting, or reporting)
   - Infrastructure bottlenecks affecting process throughput

5. **Financial Impact** — Invoke `FinancialModeler` via `#runSubagent` to quantify:
   - Cost of current inefficiencies (time × hourly rate × frequency)
   - Investment required for each improvement
   - ROI and payback period per improvement

6. **Improvement Plan** — Deliver:
   - Current-state vs future-state process maps
   - Ranked improvement opportunities (quick wins → structural changes)
   - Implementation timeline with owners
   - KPIs to track improvement effectiveness
