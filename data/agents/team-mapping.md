# Team Mapping

This is the delegation registry for the specialist workbench. Lead agents (the
system architect and the tech lead) resolve specialist names from this file
before delegating. If a mapped agent is not available in the current runtime,
they fall back to the available agents and tools and never hard-fail.

These agents are **portable and general**. They encode no personal role, voice,
or private business. Each is a client of the governed memory store, never its
source of truth.

## Roster

### Engineering

| Agent name | File | Owns |
| --- | --- | --- |
| `PythonDeveloper` | [`python-specialist.agent.md`](python-specialist.agent.md) | Idiomatic, typed Python; async patterns; pytest coverage |
| `RustDeveloper` | [`rust-specialist.agent.md`](rust-specialist.agent.md) | Safe, performant Rust; ownership; structured concurrency |
| `TypeScriptDeveloper` | [`typescript-specialist.agent.md`](typescript-specialist.agent.md) | Type-safe TypeScript/React; strict mode; server state |
| `UIDesigner` | [`ui-agent.agent.md`](ui-agent.agent.md) | Accessible, responsive interfaces; WCAG 2.2; Core Web Vitals |
| `CodeReviewer` | [`code-guidelines-agent.agent.md`](code-guidelines-agent.agent.md) | Code quality, decomposition, and clarity review |

### Architecture and lead

| Agent name | File | Owns |
| --- | --- | --- |
| `SystemArchitect` | [`system-architect.agent.md`](system-architect.agent.md) | System design, trade-offs, ADRs, integration patterns |
| `TechLeadOrchestrator` | [`tech-manager.agent.md`](tech-manager.agent.md) | Planning, decomposition, delegation, review |
| `ConnectorEngineer` | [`enterprise-connectors.agent.md`](enterprise-connectors.agent.md) | Production connector adapters (REST/GraphQL/OData) |
| `PlatformEngineer` | [`platform-quality.agent.md`](platform-quality.agent.md) | CI/CD reliability, infrastructure, cross-cutting quality |
| `PRReviewer` | [`pr-evaluator.agent.md`](pr-evaluator.agent.md) | PR architecture review and safe merge |

### Business

| Agent name | File | Owns |
| --- | --- | --- |
| `BusinessStrategist` | [`business-strategy-agent.agent.md`](business-strategy-agent.agent.md) | Market strategy, go-to-market, business model design |
| `CompetitiveIntelAnalyst` | [`competitive-intelligence-agent.agent.md`](competitive-intelligence-agent.agent.md) | Win/loss analysis, positioning, market sizing |
| `FinancialModeler` | [`financial-modeling-agent.agent.md`](financial-modeling-agent.agent.md) | Unit economics, P&L projections, pricing, ROI/NPV |
| `ProcessImprover` | [`process-management-agent.agent.md`](process-management-agent.agent.md) | BPMN modelling, Lean/Six Sigma, capacity planning |
| `RiskAnalyst` | [`risk-analysis-agent.agent.md`](risk-analysis-agent.agent.md) | Scenario planning, compliance mapping, risk quantification |

### Azure

| Agent name | File | Owns |
| --- | --- | --- |
| `AzureKubernetesSpecialist` | [`azure-aks.agent.md`](azure-aks.agent.md) | AKS clusters, networking, security, workloads |
| `AzureAPIMSpecialist` | [`azure-apim.agent.md`](azure-apim.agent.md) | API Management facades, policies, governance |
| `AzureBlobStorageSpecialist` | [`azure-blob.agent.md`](azure-blob.agent.md) | Blob storage architecture, tiers, lifecycle |
| `AzureContainerAppsSpecialist` | [`azure-container-apps.agent.md`](azure-container-apps.agent.md) | Container Apps, Dapr, revisions, scaling |
| `AzureCosmosDBSpecialist` | [`azure-cosmos.agent.md`](azure-cosmos.agent.md) | Cosmos DB data modelling, partitioning, RU tuning |
| `AzureAIFoundrySpecialist` | [`azure-foundry.agent.md`](azure-foundry.agent.md) | Microsoft Foundry model and agent deployment |
| `AzurePostgreSQLSpecialist` | [`azure-postgres.agent.md`](azure-postgres.agent.md) | PostgreSQL schemas, extensions, HA/backup |
| `AzureRedisSpecialist` | [`azure-redis.agent.md`](azure-redis.agent.md) | Redis caching, session stores, pub/sub |
| `AzureStaticWebAppsSpecialist` | [`azure-swa.agent.md`](azure-swa.agent.md) | Static Web Apps scaffolding, deployment, config |

### Memory

| Agent name | File | Owns |
| --- | --- | --- |
| `MemoryCurator` | [`memory-curator.agent.md`](memory-curator.agent.md) | Maintains the governed memory store; keeps the index honest |

## Delegation rules

| Trigger | Specialist |
| --- | --- |
| System design, integration, migration path | `SystemArchitect` |
| Multi-step planning and coordination | `TechLeadOrchestrator` |
| Python implementation | `PythonDeveloper` |
| Rust implementation | `RustDeveloper` |
| TypeScript or frontend implementation | `TypeScriptDeveloper` |
| UI, accessibility, responsive design | `UIDesigner` |
| Connector adapters | `ConnectorEngineer` |
| CI/CD, infrastructure, operational quality | `PlatformEngineer` |
| PR evaluation and merge safety | `PRReviewer` |
| Business framing, ROI, risk, market analysis | Matching business specialist |
| Azure-specific operations | Matching Azure specialist |
| Memory curation and index integrity | `MemoryCurator` |

Resolve canonical names from the roster above. Do not invent agent names that
are absent from this registry. If the intended specialist is unavailable in the
runtime, stay in the current agent, use the available tools, and explain the
fallback.
