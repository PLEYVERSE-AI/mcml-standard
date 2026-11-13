# Model Connect Markup Language (MCML)

**An open, machine-readable standard for AI safety & governance documentation**

[![Spec: CC BY 4.0](https://img.shields.io/badge/spec-CC%20BY%204.0-lightgrey.svg)](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/LICENSE-SPEC) [![Code: GPL-3.0](https://img.shields.io/badge/code-GPL--3.0-blue.svg)](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/LICENSE)
[![Specification](https://img.shields.io/badge/spec-v1.1%20draft-blue)](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/schema/v1.1/)
[![Status](https://img.shields.io/badge/status-draft-orange)]()

> **A unified standard for AI safety & governance documentation — making safety and compliance claims checkable.**

<div class="mcml-mission">
<h2 class="mcml-mission-title">Governed Compute. Enforceable Safety.</h2>
<p class="mcml-mission-sub">“Bridging machine-readable governance documentation with zero-trust runtime policy enforcement.”</p>
<ul class="mcml-stoplight">
<li class="go"><strong>Machine-Readable Traceability:</strong> Standardized schemas that translate static regulations into verifiable system boundaries.</li>
<li class="caution"><strong>Zero-Trust Tool Interception:</strong> Deterministic gateways that inspect, validate, and circuit-break autonomous agent actions before execution.</li>
<li class="stop"><strong>Towards Telemetry Beyond the Black Box:</strong> Fusing runtime provenance checks with targeted latent verification to prevent model self-reporting drift.</li>
</ul>
<p class="mcml-agnostic"><strong>Industry-agnostic by design.</strong> The four cards describe any AI system in any industry. Cross-sector frameworks (NIST AI RMF, EU AI Act) are mapped today; sector rules such as HIPAA, FDA SaMD and banking model-risk guidance are designed to plug in as optional profiles, so one card serves every regime without forking the standard.</p>
</div>

---

## 🛡️ AI Safety: From Declared Controls to Enforced Controls

**Most AI safety controls exist only on paper.** Oversight rules, escalation procedures and shutdown plans are written down, but nothing ensures they bind an AI agent once it is running. When an agent acting through MCP does something harmful, can you prove which version acted, what it was allowed to do at that moment, and what the tool actually executed? When you pull the kill switch, **does the agent actually stop?**

MCML closes that gap in two steps:

| | What it does | Status |
|---|---|---|
| **1. Pre-deployment gate** | Blocks deployment when safety evidence is missing: failure modes, evaluations that missed their thresholds, no human oversight, no tested kill switch, or a configuration that would let the agent bypass enforcement | ✅ **Available** |
| **2. Runtime enforcement gateway** | Enforces the signed Agentic Governance Card on every MCP tool call, from **outside the agent's runtime**, so enforcement does not depend on the agent's cooperation | 🧪 **Prototype**: 7 of 7 scenarios pass in a synthetic environment ([results](https://mcml-standard.org/gateway/RESULTS.html)) |

**The runtime gateway is designed to:**

- 🔒 **Hold the tool credentials** so the agent cannot call tools directly
- ⛔ **Run an out-of-band kill switch**: numeric triggers or a human operator revoke credentials and drop sessions without asking the agent to stop
- ✋ **Enforce human approval in real time**: a withdrawn approval blocks the next call
- 🧬 **Detect model swaps**: the serving host's attested weight hash must match the approved list, or the kill switch fires
- 🧪 **Block payload injection**: tool arguments must match the schema declared in the card
- 🧾 **Record linked evidence**: agent version, card version, gateway decision and the tool's own receipt

The [prototype](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/gateway) passes seven scenarios, including **gateway bypass**, **model provenance injection** and **adversarial payload injection**, in a synthetic clinical workflow, and the tests run on every commit. It has not been tested in production. We publish its limits too: it enforces declared limits, so an action the card permits can still cause harm.

### **[→ Read the MCML AI Safety specification](https://mcml-standard.org/docs/runtime-safety.html)**

---

## What is MCML?

MCML is a **standard language** that formalizes and unifies AI documentation practices into a machine-readable protocol for regulatory compliance. It defines four card types (Model, Dataset, Interface, and Agentic Governance), each with JSON Schema definitions, and the structure needed to validate them automatically.

Documentation that says a model has limitations, requires human review, or is monitored is not enough on its own. MCML requires these claims to be specified in a form tools can check: failure modes with severity and mitigation, evaluation evidence with thresholds, oversight authority, monitoring commitments with actions on breach, recorded risk acceptance, and links to incidents.

MCML is part of the ModelConnect platform, an open-source integration layer for enterprise AI infrastructure.

### Building on Industry Standards

MCML integrates **four documentation standards** from the AI governance community:

1. **Model Cards** (Google, Mitchell et al., 2019): model purpose, performance, limitations
2. **Dataset Cards / Datasheets** (Microsoft, Gebru et al., 2018): data provenance, biases, collection methods
3. **Interface Cards** (emerging from API governance): service endpoints, access control, monitoring
4. **Agentic Governance Cards** (emerging from MCP, A2A, and agent framework communities): agent identity, authority, oversight, enforcement

These four card types are becoming the **de facto industry standards** for AI documentation. MCML provides the integration layer that makes them work together.

### The Compliance Challenge

Organizations must comply with multiple regulatory frameworks and ISO standards:

- **NIST AI Risk Management Framework** (AI RMF)
- **EU AI Act** (Regulation 2024/1689)
- **ISO/IEC 42001** (AI Management System)
- **ISO/IEC 23894** (AI Risk Management)
- **GDPR** (General Data Protection Regulation)
- **FDA** (Medical Device Regulations for AI/ML)
- **Sector-specific regulations** (finance, healthcare, employment)

**The Problem:** Each framework has different documentation requirements, and the four card types exist independently without a unified structure or machine-readable format.

### MCML's Solution: Three Core Contributions

#### 1. Unified Schema

MCML formalizes the structure of all four card types with:
- ✅ Consistent field definitions across card types
- ✅ Required vs. optional field specifications
- ✅ Relationship models (how cards reference each other)
- ✅ Versioning and temporal validity

#### 2. Machine-Readable Protocol

MCML provides JSON/YAML schemas enabling:
- ✅ **Programmatic validation**: automated checking of completeness
- ✅ **Compliance automation**: CI/CD gates that block incomplete deployments
- ✅ **Tool interoperability**: any tool can read and write MCML
- ✅ **Real-time monitoring**: dashboards showing governance status
- ✅ **Instant audit trails**: generate compliance reports in seconds

#### 3. Compliance Framework Mappings

MCML maps card fields to regulatory requirements:

| Framework | MCML Mapping |
|-----------|-------------|
| **NIST AI RMF** | Shows which card fields satisfy GOVERN/MAP/MEASURE/MANAGE functions |
| **EU AI Act** | Maps cards to risk classification, transparency, human oversight requirements |
| **ISO/IEC 42001** | Links cards to AI management system documentation clauses |
| **GDPR** | Demonstrates data provenance, purpose limitation, accountability |
| **FDA** | Provides device traceability and adverse event reporting structure |

**Example:** "To satisfy NIST's MEASURE function, you need `performance_metrics` from Model Card + `quality_metrics` from Dataset Card + `fairness_metrics` from both."

---

## The Problem MCML Solves

### Before MCML

**Manual, Fragmented Compliance:**

```
1. Read Model Card PDF
2. Search wiki for Dataset documentation
3. Check spreadsheet for API governance
4. Manually verify bias assessment exists
5. Write audit report by hand
6. Hope documentation matches production reality

⏱️ Time: Hours to days per audit
❌ No automation
❌ Documentation drifts from deployments
❌ Can't validate before deployment
```

### With MCML

**Automated, Unified Compliance:**

```json
// Single API call returns complete governance lineage
GET /governance/lineage/event_12345

{
  "model": {
    "name": "credit_scorer",
    "version": "3.2.1",
    "governance": {
      "intended_use": "Credit risk assessment for personal loans",
      "performance_metrics": {"auc": 0.87, "f1": 0.82},
      "limitations": ["Not validated for commercial loans"]
    }
  },
  "dataset": {
    "name": "customer_credit_data",
    "version": "2.3",
    "governance": {
      "known_biases": ["geographic_urban", "age_skew_25_45"],
      "quality_score": 0.91,
      "contains_pii": true
    }
  },
  "interface": {
    "governance": {
      "access_control": "oauth2",
      "logging_level": "detailed"
    }
  },
  "agent": {
    "governance": {
      "autonomy_level": "semi_autonomous",
      "escalation_rules": {...}
    }
  },
  "compliance": {
    "nist_rmf": {
      "status": "COMPLIANT",
      "functions": {
        "GOVERN": "✓", "MAP": "✓", "MEASURE": "✓", "MANAGE": "✓"
      }
    },
    "eu_ai_act": {
      "risk_category": "HIGH",
      "status": "COMPLIANT"
    }
  }
}
```

⏱️ **Time: Milliseconds**
✅ **Fully automated**
✅ **Documentation linked to deployments**
✅ **Pre-deployment validation**

---

## Reference Implementation: Patent-Pending Two-Layer Architecture

While MCML is **implementation-agnostic** (you can use any database, file system, or architecture), we describe a **reference architecture**, our **patent-pending two-layer architecture**, that demonstrates the power of machine readability. The schemas, example cards and validator in this repository implement the pre-deployment checks; the two-layer database implementation is described here and is not yet published as code.

### The Architecture

```
┌────────────────────────────────────────────────────────────┐
│              GOVERNANCE LAYER (Documentation)              │
│                                                            │
│  ┌─────────────┐ ┌─────────────┐ ┌───────────────┐        │
│  │ Model Cards │ │Dataset Cards│ │Interface Cards│        │
│  └──────┬──────┘ └──────┬──────┘ └──────┬────────┘        │
│         │               │               │                 │
│  ┌──────┴───────────────┴───────────────┴──┐              │
│  │             Agentic Cards               │              │
│  └──────┬──────────────────────────────────┘              │
└─────────┼──────────┼──────────┼──────────┼─────────────────┘
          │   Foreign Key Relationships    │
┌─────────┼──────────┼──────────┼──────────┼─────────────────┐
│         ▼          ▼          ▼          ▼                 │
│  ┌──────────────┐ ┌───────────┐ ┌──────────────────┐      │
│  │Model Registry│ │  Dataset  │ │Interface Registry│      │
│  └──────────────┘ │  Registry │ └──────────────────┘      │
│                   └───────────┘                           │
│  ┌─────────────────┐  ┌───────────────────────┐           │
│  │ Agent Registry  │  │   Inference Events    │           │
│  └─────────────────┘  └───────────────────────┘           │
│                                                            │
│            OPERATIONAL LAYER (Deployments)                 │
└────────────────────────────────────────────────────────────┘
```

### Key Innovation: Foreign Keys Linking Layers

**Governance Layer (Documentation):**
- Model Cards: document model purpose, performance, limitations, ethical considerations
- Dataset Cards: document data provenance, biases, quality, legal basis
- Interface Cards: document API governance, access control, monitoring requirements
- Agentic Governance Cards: document agent identity, autonomy, oversight rules, tool permissions, enforcement

**Operational Layer (Deployed Systems):**
- Model Registry: actual deployed model instances
- Dataset Registry: actual data sources in use
- Interface Registry: live API endpoints and services
- Agent Registry: running agent instances (MCP servers, LangGraph graphs, A2A agents, etc.)
- Inference Events: every prediction or decision with full context

**Foreign Keys** create enforceable relationships:
- Can't deploy a model without a complete Model Card (database constraint)
- Can't reference a non-existent Dataset Card (referential integrity)
- Every inference event links to all four card types via operational registries

### Benefits of This Architecture

| Capability | How Foreign Keys Enable It | Time Saved |
|------------|---------------------------|------------|
| **Pre-deployment validation** | FK constraint blocks deployment if card missing | Catches issues before production |
| **Single-query audit trails** | One SQL JOIN traverses entire governance graph | Hours → Milliseconds |
| **Guaranteed completeness** | Database enforces all required cards exist | No manual verification |
| **Automatic compliance checks** | Query card fields to validate regulatory requirements | Days → Seconds |
| **Drift prevention** | Documentation can't get out of sync with deployments | Eliminates documentation debt |
| **Incident investigation** | Trace from prediction → model → biased training data | Hours → Minutes |

### Example: Single-Query Traceability

```sql
-- PostgreSQL implementation: Complete lineage in one query
SELECT
    ie.event_id,
    ie.prediction,
    ie.timestamp,

    -- Model governance
    mc.intended_use,
    mc.performance_metrics,
    mc.limitations,

    -- Dataset governance
    dc.known_biases,
    dc.collection_method,
    dc.quality_score,

    -- Interface governance
    ic.access_control_policy,
    ic.logging_level,

    -- Agent governance
    ac.identity,
    ac.autonomy,
    ac.enforcement

FROM inference_events ie
JOIN model_registry mr        ON ie.model_fk = mr.id
JOIN model_cards mc           ON mr.model_card_fk = mc.id
JOIN dataset_cards dc         ON mc.training_dataset_fk = dc.id
JOIN interface_registry ir    ON ie.interface_fk = ir.id
JOIN interface_cards ic       ON ir.interface_card_fk = ic.id
LEFT JOIN agent_registry ar   ON ie.agent_fk = ar.id
LEFT JOIN agentic_governance_cards ac ON ar.agent_card_fk = ac.id

WHERE ie.event_id = '550e8400-e29b-41d4-a716-446655440000';
```

⏱️ **Query time: <100ms** for complete governance lineage across all four card types

### This is ONE Way to Implement MCML

The two-layer architecture with foreign keys is our **patent-pending reference implementation**, but MCML can be implemented in other ways:

- **Graph databases** (Neo4j): relationships as first-class citizens
- **Document stores** (MongoDB): embedded cards with URI references
- **File-based** (Git repositories): YAML files with linked references
- **Hybrid** (cards in Git, events in TimescaleDB)

The MCML **standard** is implementation-agnostic. Our reference implementation demonstrates the benefits of machine readability plus relational integrity.

---

## The Four Card Types (Detailed)

### 1. Model Card (extends Google Model Cards)

Documents the **governance metadata** for ML models.

**Core Fields:**
```yaml
model_card:
  model_name: credit_risk_scorer
  version: 3.2.1

  # Purpose and scope
  intended_use: "Credit risk assessment for personal loans up to $50K"
  out_of_scope_uses:
    - "Commercial loan assessment"
    - "International credit scoring"

  # Relationships to other cards
  training_dataset_ref: "dataset://customer_credit_data/v2.3"
  validation_dataset_ref: "dataset://holdout_data/v1.0"

  # Performance documentation
  performance_metrics:
    primary_metric: auc
    auc: 0.87
    f1_score: 0.82
    precision: 0.85
    recall: 0.79

  # Fairness and bias
  fairness_metrics:
    demographic_parity: 0.92
    equal_opportunity: 0.94
    disparate_impact: 0.88

  # Transparency
  limitations:
    - "Performance degrades for recent immigrants (limited training data)"
    - "Not validated for loan amounts above $50K"
    - "Requires annual retraining to maintain accuracy"

  ethical_considerations:
    high_risk_groups:
      - recent_immigrants
      - first_time_borrowers
    mitigation_strategies:
      - "Manual review required for confidence < 0.85"
      - "Quarterly fairness audits by external auditor"

  # Accountability
  responsible_team: "ML Engineering - Credit Models"
  contact_email: "ml-credit@example.com"

  # Compliance mapping
  nist_rmf_alignment:
    GOVERN: "Responsible team designated, approval workflow documented"
    MAP: "Risk categorized as HIGH, context fully documented"
    MEASURE: "Performance and fairness metrics tracked continuously"
    MANAGE: "Monitoring commitments and risk acceptance recorded"
```

**Safety Extension (v1.1):**

```yaml
model_card:
  # ...core fields above

  failure_modes:
    - id: FM-01
      description: "Reduced accuracy for applicants with thin credit files"
      severity: high
      detection: "Subgroup AUC and population stability index monitoring"
      mitigation_ref: MIT-03
      residual_risk: medium

  evaluation_evidence:
    evaluation_date: 2026-01-10
    test_dataset_ref: "dataset://holdout_data/v1.0"
    metrics:
      - metric: auc
        threshold: 0.85
        observed: 0.87
        passed: true
    report_uri: "https://example.com/evals/credit_scorer_3.2.1.pdf"

  human_oversight:
    oversight_model: human_on_the_loop   # or human_in_the_loop, human_in_command
    reviewer_role: senior_underwriter
    override_authority: "Reviewer may overturn any automated decision"
    review_triggers:
      - "Confidence below 0.85"
      - "Applicant requests explanation"
    reviewer_training: "Bias-awareness training completed before assignment"

  monitoring_commitments:
    - metric: population_stability_index
      threshold: 0.25
      frequency: daily
      action_on_breach: "Suspend automated decisions and route to manual review"
      owner: "ML Monitoring Team"

  risk_acceptance:
    risk_category: high
    accepted_residual_risk: medium
    accepted_by: "Chief Risk Officer"
    accepted_on: 2026-02-01
    review_due: 2026-08-01

  incident_refs: []   # Incident Card planned for v1.2
```

**MCML Extensions for Machine Readability:**
- `training_dataset_ref`: URI reference to Dataset Card (enables automated lineage)
- `performance_metrics`: structured numbers (enables automated threshold checks)
- `fairness_metrics`: quantitative bias measures (enables drift detection)
- `nist_rmf_alignment`: direct mapping to compliance framework
- `failure_modes`, `evaluation_evidence`, `human_oversight`, `monitoring_commitments`, `risk_acceptance`: safety fields (v1.1)

---

### 2. Dataset Card (extends Microsoft Datasheets for Datasets)

Documents the **governance metadata** for training/evaluation datasets.

**Core Fields:**
```yaml
dataset_card:
  dataset_name: customer_credit_data
  version: 2.3

  # Provenance
  collection_method: "Production credit applications 2023-2024 + synthetic augmentation"
  collection_date_start: 2023-01-01
  collection_date_end: 2024-12-31
  data_owner: "Data Governance Office"

  # Bias documentation
  known_biases:
    - bias_type: geographic
      description: "Urban areas over-represented (65% vs 45% national population)"
      impact: "May underperform for rural applicants"
      mitigation: "Synthetic rural data augmentation + stratified validation"

    - bias_type: demographic
      description: "Age distribution skewed toward 25-45 (68% vs 52% population)"
      impact: "May underperform for applicants <25 or >60"
      mitigation: "Age-based fairness constraints in training"

  # Quality metrics
  quality_metrics:
    completeness: 0.94
    consistency_score: 0.89
    accuracy_sample_validated: 0.97
    missing_value_rate: 0.06

  # Preprocessing
  preprocessing_steps:
    - step: "Remove duplicate applications"
      description: "Deduplicated on national_id + application_date"

    - step: "Impute missing income"
      description: "Median imputation by ZIP code + job category"

    - step: "Outlier removal"
      description: "Remove income >$500K or <$5K (0.3% of data)"

  # Legal and compliance
  contains_pii: true
  pii_fields:
    - national_id
    - full_name
    - address
    - date_of_birth

  legal_basis: "Customer consent for credit assessment (GDPR Art. 6.1.b)"
  retention_policy: "7 years from application date per banking regulations"

  # GDPR compliance
  gdpr_compliance:
    lawful_basis: "Contract necessity"
    data_minimization: "Only credit-relevant fields collected"
    purpose_limitation: "Used only for credit risk assessment"
    subject_rights: "Deletion requests processed within 30 days"
```

**MCML Extensions for Machine Readability:**
- `known_biases`: structured list (enables automated fairness validation)
- `quality_metrics`: quantitative scores (enables data quality gates)
- `preprocessing_steps`: reproducible transformations (enables lineage tracking)
- `pii_fields`: explicit PII listing (enables GDPR compliance checks)

---

### 3. Interface Card (extends OpenAPI governance patterns)

Documents the **governance metadata** for API endpoints and services.

**Core Fields:**
```yaml
interface_card:
  service_name: credit_scoring_api
  description: "Production credit scoring endpoint for loan origination system"

  # API specification
  api_specification_url: "https://api.example.com/docs/credit/v2/openapi.json"
  supported_protocols:
    - REST
    - gRPC
  base_url: "https://api.example.com/v2/credit"

  # Access control
  authentication_method: oauth2
  access_control_policy:
    authorized_roles:
      - loan_officer
      - underwriter
      - risk_analyst
    ip_whitelist:
      - "10.0.0.0/8"  # Internal network only

  rate_limits:
    requests_per_minute: 100
    requests_per_hour: 5000
    burst_allowance: 150

  # Data governance
  data_classification: confidential
  pii_handling_policy: "All requests/responses encrypted in transit and at rest"

  # Monitoring and logging
  logging_level: detailed
  log_retention_days: 365
  audit_requirements:
    - "Log all access attempts (success and failure)"
    - "Log all prediction inputs and outputs"
    - "Alert on unusual access patterns"

  # Compliance
  compliance_frameworks:
    - GDPR
    - CCPA
    - SOC2
    - PCI-DSS

  data_residency_requirements:
    allowed_regions:
      - us-east
      - eu-west
    prohibited_regions:
      - china
      - russia

  # Ownership
  service_owner: "Platform Engineering - APIs"
  contact_email: "api-team@example.com"
```

**MCML Extensions for Machine Readability:**
- `rate_limits`: structured throttling (enables automated enforcement)
- `access_control_policy`: machine-readable permissions (enables IAM integration)
- `compliance_frameworks`: explicit framework list (enables compliance validation)
- `data_residency_requirements`: geographic constraints (enables deployment validation)

---

### 4. Agentic Governance Card (v1.1; replaces `agentic_card`)

Documents the **governance metadata** for AI agents and autonomous components. The v1.0 `agentic_card` name remains as a deprecated alias for one minor version.

```yaml
agentic_governance_card:
  schema_version: "1.1"
  agent_name: loan_approval_agent
  agent_version: "1.3.0"
  description: "Semi-autonomous agent supporting personal loan decisions"
  last_verified: 2026-11-01

  # Identity: who the agent is and how it authenticates
  identity:
    agent_id: "agent://lending/loan-approval/1.3.0"
    authentication: "OAuth 2.1 client credentials, workload-attested via SPIFFE ID"
    credential_rotation: "Every 24 hours; revocable immediately"
    owner: "Risk Management - Lending Operations"

  # Autonomy and decision authority
  autonomy:
    level: semi_autonomous
    decision_authority:
      max_loan_amount: 25000
      max_approval_without_review: 15000
      requires_human_approval_above: 25000

  # Authorization: scoped, time-limited permissions per tool
  authorization:
    tools:
      - name: credit_bureau_lookup
        scopes: ["credit:read"]
        max_calls_per_application: 3
        permission_ttl: "PT30M"
      - name: fraud_check
        scopes: ["fraud:read"]
        max_calls_per_application: 1
        permission_ttl: "PT30M"
    standing_access: none
    forbidden_actions:
      - modify_credit_score
      - approve_loan_above_authority
      - disable_fraud_check
      - access_competitor_data

  # Delegation: who acted on whose authority
  delegation:
    max_hops: 2
    requires_origin_user: true
    chain_recorded: true
    permitted_downstream_agents:
      - fraud_detection_agent
    prohibited_downstream_agents:
      - external_third_party_agents

  # Interoperability: protocols and spec versions as ranges
  interoperability:
    mcp:
      supported: true
      spec_version_range: "[verify against current MCP specification]"
      auth_profile: "OAuth 2.1 resource server"
    a2a:
      supported: true
      spec_version_range: "[verify against current A2A specification]"
      agent_card_signed: true
    upstream_spec_links:
      - "https://modelcontextprotocol.io/specification"
      - "https://a2a-protocol.org"

  # Runtime enforcement: how rules are applied, not only declared
  enforcement:
    policy_engine: "[name the policy decision point]"
    enforcement_point: "Tool gateway, before each tool call"
    violation_behavior: "Block action, log event, escalate"
    audit_log:
      captures: [identity, origin_user, tool, arguments_hash, decision, timestamp]
      retention_days: 365
      tamper_evident: true

  # Kill switch and rollback
  kill_switch:
    trigger_conditions:
      - "error_rate > 10% over 5 minutes"
      - "approval_rate > 95% over 1 hour"
      - "tool_call_failure_rate > 20%"
    action: "Revoke credentials and route requests to manual review queue"
    tested: [test date]
    tested_by: "[owning team]"
    rollback_procedure_ref: "[runbook location]"

  # Oversight: reference the Model Card, do not duplicate it
  human_oversight:
    model_card_ref: "model://credit_risk_scorer/3.2.1#human_oversight"
    escalation_rules:
      - condition: "confidence_score < 0.85"
        action: escalate_to_senior_underwriter
        sla: "4 hours"
      - condition: "fraud_score > 0.7"
        action: immediate_escalation_to_fraud_team
        sla: "1 hour"

  # Monitoring: reference the Model Card's commitments
  monitoring:
    model_card_ref: "model://credit_risk_scorer/3.2.1#monitoring_commitments"
    action_logging_level: all

  # Threat coverage
  threat_coverage:
    framework: "OWASP Top 10 for Agentic Applications"
    reviewed_categories:
      - "Insecure inter-agent communication"
      - "Identity and privilege abuse"
      - "Tool misuse"
    last_reviewed: [review date]

  incident_refs: []
```

**MCML Extensions for Machine Readability:**
- `identity` and `delegation`: who acted and on whose authority (enables attribution across agent chains)
- `authorization.tools` with `permission_ttl`: scoped, time-limited permissions (enables least-privilege enforcement)
- `forbidden_actions`: blocklist (enables runtime enforcement)
- `escalation_rules`: structured conditions (enables automated routing)
- `kill_switch.trigger_conditions`: quantitative thresholds (enables automatic shutdown)
- `enforcement`: how rules are applied at runtime (enables verification)
- Runtime safety extension (draft): `card_signature`, `enforcement.gateway_isolation`, per-tool `argument_schema`, structured kill-switch triggers and actions, `provenance_verification`, `adversarial_defenses`. See the [AI Safety specification](https://mcml-standard.org/docs/runtime-safety.html).

### How the Four Card Types Relate

- Model Card → Dataset Card (training data)
- Model Card → Interface Card (deployment)
- Interface Card → Agentic Governance Card (where agents are used)
- Agentic Governance Card → Model Card (oversight and monitoring)

---

## Compliance Framework Mappings

MCML provides **direct mappings** from card fields to regulatory and framework requirements, enabling automated compliance checking. Mappings show where evidence can be found. They do not guarantee compliance.

### NIST AI Risk Management Framework

| NIST Function | Required MCML Fields | Validation Check |
|---------------|---------------------|------------------|
| **GOVERN** | `model_card.responsible_team`<br>`agentic_governance_card.identity.owner`<br>`dataset_card.data_owner` | ✅ All ownership fields populated |
| **MAP** | `model_card.intended_use`<br>`model_card.limitations`<br>`model_card.failure_modes`<br>`agentic_governance_card.autonomy.decision_authority` | ✅ Purpose, constraints, and failure modes documented |
| **MEASURE** | `model_card.performance_metrics`<br>`model_card.fairness_metrics`<br>`model_card.evaluation_evidence`<br>`dataset_card.quality_metrics`<br>`dataset_card.known_biases` | ✅ Quantitative assessments present |
| **MANAGE** | `interface_card.logging_level = 'detailed'`<br>`model_card.monitoring_commitments`<br>`model_card.risk_acceptance`<br>`agentic_governance_card.kill_switch` | ✅ Monitoring, response, and risk acceptance mechanisms present |

**Automated Validation Example:**
```python
def validate_nist_compliance(model_card, dataset_card, interface_card, agentic_card):
    results = {
        "GOVERN": bool(
            model_card.responsible_team and
            dataset_card.data_owner
        ),
        "MAP": bool(
            model_card.intended_use and
            model_card.limitations and
            model_card.failure_modes
        ),
        "MEASURE": bool(
            model_card.performance_metrics and
            model_card.fairness_metrics and
            model_card.evaluation_evidence and
            dataset_card.quality_metrics
        ),
        "MANAGE": (
            interface_card.logging_level == "detailed" and
            bool(model_card.monitoring_commitments) and
            bool(model_card.risk_acceptance) and
            bool(agentic_card.kill_switch)
        ),
    }

    return {
        "compliant": all(results.values()),
        "function_status": results,
    }
```

### EU AI Act

| Article | Requirement | MCML Fields | Validation |
|---------|------------|-------------|------------|
| **Art. 6** | Risk Classification | `model_card.risk_acceptance.risk_category` | ✅ Must be: `minimal`, `limited`, `high`, `unacceptable` |
| **Art. 11** | Technical Documentation | All four card types complete | ✅ All required fields present |
| **Art. 13** | Transparency | `model_card.intended_use`<br>`model_card.limitations`<br>`dataset_card.known_biases` | ✅ Clear purpose and constraints |
| **Art. 14** | Human Oversight | `model_card.human_oversight`<br>`agentic_governance_card.kill_switch`<br>`agentic_governance_card.human_oversight.escalation_rules` | ✅ Oversight mechanisms defined for high-risk systems |
| **Art. 15** | Accuracy Requirements | `model_card.evaluation_evidence`<br>`model_card.performance_metrics`<br>`dataset_card.quality_metrics` | ✅ Metrics meet thresholds |

### ISO/IEC 42001 (AI Management System)

| Clause | Requirement | MCML Fields |
|--------|-------------|-------------|
| **6.1** | Risk Assessment | `model_card.failure_modes`<br>`model_card.ethical_considerations`<br>`model_card.risk_acceptance` |
| **7.2** | Competence | `model_card.responsible_team`<br>`agentic_governance_card.identity.owner` |
| **7.5** | Documented Information | All four card types |
| **8.1** | Operational Planning | `model_card.intended_use`<br>`agentic_governance_card.autonomy.decision_authority` |
| **9.1** | Monitoring | `model_card.monitoring_commitments`<br>`agentic_governance_card.enforcement.audit_log` |

### GDPR (Data Protection)

| Principle | Requirement | MCML Fields | Validation |
|-----------|------------|-------------|------------|
| **Art. 5.1.b** | Purpose Limitation | `model_card.intended_use`<br>`model_card.out_of_scope_uses` | ✅ Explicit boundaries |
| **Art. 5.1.c** | Data Minimization | `dataset_card.collection_method`<br>`dataset_card.pii_fields` | ✅ Only necessary data |
| **Art. 5.1.e** | Storage Limitation | `dataset_card.retention_policy` | ✅ Retention period defined |
| **Art. 13** | Transparency | `model_card.limitations`<br>`dataset_card.known_biases` | ✅ Explainability |
| **Art. 24** | Accountability | All cards: ownership fields | ✅ Controllers identified |

### Agentic Systems

| Reference | Relevant MCML Fields |
|-----------|---------------------|
| NIST AI Agent Standards Initiative (CAISI, launched February 2026) | `identity`, `authorization`, `delegation`, `enforcement` |
| OWASP Top 10 for Agentic Applications | `threat_coverage`, `delegation`, `authorization` |

MCML maps to these references by topic. It does not claim endorsement by NIST, OWASP, or any other body.

---

## Getting Started

This repository contains the MCML v1.1 JSON Schemas, example cards, and a reference validator (`tools/mcml.py`) that checks cards and acts as a pre-deployment gate. A pip-installable package and Python SDK are planned (see [Roadmap](#roadmap)).

### 1. Install

```bash
git clone https://github.com/PLEYVERSE-AI/mcml-standard
cd mcml-standard
pip install -r requirements.txt
```

### 2. Validate cards against the schemas

```bash
python tools/mcml.py validate examples/credit-scoring/*.yaml
```

```
PASS examples/credit-scoring/agentic-governance-card.yaml (agentic_governance_card)
PASS examples/credit-scoring/dataset-card.yaml (dataset_card)
PASS examples/credit-scoring/interface-card.yaml (interface_card)
PASS examples/credit-scoring/model-card.yaml (model_card)
```

Cards are YAML or JSON files whose top-level key names the card type: `model_card`, `dataset_card`, `interface_card` or `agentic_governance_card`. The schemas are in [`schema/v1.1/`](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/schema/v1.1/) and can be used with any JSON Schema (draft 2020-12) validator.

### 3. Report framework evidence

```bash
python tools/mcml.py compliance-check examples/credit-scoring --framework nist       # or eu-ai-act
```

```
PASS  GOVERN
PASS  MAP
PASS  MEASURE
PASS  MANAGE

nist: evidence present for all requirements
Note: this reports documentation evidence, not legal compliance.
```

### 4. Gate deployment

`pre-deploy-check` exits non-zero, blocking the pipeline, when:

- a required card (Model, Dataset, Interface; Agentic Governance with `--require-agent`) is missing or fails its schema
- a card reference (for example `training_dataset_ref`) does not resolve to a card in the stack
- the Model Card lacks safety evidence (failure modes, evaluation evidence, human oversight, monitoring commitments, risk acceptance), an evaluation metric missed its threshold, the risk category is `unacceptable`, or the risk-acceptance review is overdue
- an Agentic Governance Card has no kill switch, no recorded kill-switch test, or an audit log that is not tamper-evident
- an Agentic Governance Card declares a setup the agent could bypass: enforcement inside the agent runtime, tool credentials held by the agent, an in-band kill switch, or a model provenance mismatch that is only logged

```bash
python tools/mcml.py pre-deploy-check examples/blocked-deployment --require-agent
```

```
DEPLOYMENT BLOCKED
  - examples/blocked-deployment/agentic-governance-card.yaml: agentic_governance_card: 'kill_switch' is a required property
  - missing required dataset_card
  - missing required interface_card
  - examples/blocked-deployment/model-card.yaml: safety field 'failure_modes' is missing
  ...
```

### 5. Add the gate to CI/CD

[`.github/workflows/validate.yml`](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/.github/workflows/validate.yml) runs the gate on every push. To use it in your own pipeline:

```yaml
- run: pip install -r requirements.txt
- run: python tools/mcml.py pre-deploy-check governance/ --require-agent
```

### Examples

| Folder | What it shows |
|--------|---------------|
| [`examples/credit-scoring/`](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/examples/credit-scoring/) | Complete four-card stack for a credit model and a loan agent; passes the gate |
| [`examples/clinical-alert-agent/`](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/examples/clinical-alert-agent/) | Synthetic healthcare stack: an agent that may page a rapid response team only after charge-nurse approval; passes the gate |
| [`examples/blocked-deployment/`](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/examples/blocked-deployment/) | Incomplete stack the gate refuses |

---

## Use Cases

The validator above implements use case 1. Use cases 2 to 5 describe planned SDK capabilities; the code shown is illustrative and not yet released.

### 1. Pre-Deployment Validation (available)

**Block incomplete deployments** with `python tools/mcml.py pre-deploy-check <dir>`. See [Getting Started](#4-gate-deployment).

### 2. Automated Compliance Reporting (planned)

```python
from mcml import ComplianceReporter   # planned API

reporter = ComplianceReporter()
nist_report = reporter.generate_report(
    inference_event_id="evt_12345",
    framework="nist_rmf",
    output_format="pdf"
)
```

### 3. Governance Monitoring (planned)

```python
from mcml import GovernanceDashboard   # planned API

status = GovernanceDashboard().get_production_status()
# {'total_models': ..., 'fully_documented': ..., 'missing_cards': ...}
```

### 4. Incident Investigation (planned)

```python
from mcml import IncidentInvestigator   # planned API

analysis = IncidentInvestigator().analyze_incident(
    inference_event_id="incident_789",
    include_full_lineage=True
)
# Returns the event, the model and dataset cards in force, and the matching known limitations and biases
```

### 5. Runtime Enforcement and Kill Switch for Agents (prototype)

A gateway outside the agent's runtime enforces the signed Agentic Governance Card on every MCP tool call: it holds tool credentials, runs an out-of-band kill switch, checks model attestation, validates tool arguments, and links each decision to the tool's own receipt. See the **[MCML AI Safety specification](https://mcml-standard.org/docs/runtime-safety.html)** for the architecture, card fields, six-scenario threat model and known limits.

---

## Documentation

- **Specification overview**: this README
- **Detailed specification draft**: [`docs/mcml-spec.md`](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/docs/mcml-spec.md)
- **JSON Schemas**: [`schema/v1.1/`](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/schema/v1.1/)
- **Example cards**: [`examples/`](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/examples/)
- **Validator**: [`tools/mcml.py`](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/tools/mcml.py)
- **Website**: [mcml-standard.org](https://mcml-standard.org)

---

## Schema Downloads

### MCML v1.1 Schemas (JSON Schema, draft 2020-12)

- **[Model Card Schema](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/schema/v1.1/model-card.schema.json)**
- **[Dataset Card Schema](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/schema/v1.1/dataset-card.schema.json)**
- **[Interface Card Schema](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/schema/v1.1/interface-card.schema.json)**
- **[Agentic Governance Card Schema](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/schema/v1.1/agentic-governance-card.schema.json)**

Schemas allow additional properties, so organizations can add their own fields while staying valid.

---

## Community and Ecosystem

### Contributing

MCML is an **open standard**. Contributions are welcome through [GitHub issues](https://github.com/PLEYVERSE-AI/mcml-standard/issues) and pull requests:

- **Schema enhancements**: new fields, relationships, or card types
- **Compliance mappings**: additional frameworks (ISO 27001, SOC 2, sector-specific)
- **Implementation patterns**: architectures and lessons learned
- **Tooling**: validators, generators, visualizers, IDE extensions
- **Documentation**: guides, examples, translations

### Tooling

**Available in this repository:**
- **MCML validator** (`tools/mcml.py`): schema validation, framework evidence reports, pre-deployment gate
- **CI workflow** (`.github/workflows/validate.yml`): runs the gate on every push

**Planned:**
- pip package and Python SDK
- MCP runtime enforcement gateway
- MLflow, Great Expectations, Weights & Biases and LangChain integrations
- VS Code extension and pre-commit linter
- Governance dashboard

---

## Roadmap

### v1.0 (January 2026)

✅ **Core Specification**
- Four card types formalized (Model, Dataset, Interface, Agentic)
- URI-based relationship model
- Versioning and temporal validity

✅ **Compliance Mappings**
- NIST AI Risk Management Framework
- EU AI Act
- ISO/IEC 42001
- GDPR (high-level)

✅ **Reference Architecture**
- Two-layer architecture (patent pending), described above

### v1.1 (draft, current)

✅ **Published in this repository**
- JSON Schemas for all four card types
- Agentic Governance Card replacing `agentic_card`: identity, scoped and time-limited authorization, delegation chains, runtime enforcement, kill switch
- Model safety extension: failure modes, evaluation evidence, human oversight, monitoring commitments, risk acceptance
- Reference validator with framework evidence reports and a pre-deployment gate
- Example stacks, including a synthetic clinical alert agent

✅ **Runtime safety fields** in the Agentic Governance Card schema, with gate checks that block configurations an agent could bypass

🔲 **In development**
- Runtime enforcement gateway for MCP tool calls: prototype published in `gateway/` with out-of-band kill switch, model provenance checks, payload validation, signed tool receipts and hash-chained evidence; 7 of 7 synthetic scenarios pass
- Production pilot with a partner organization
- Mappings to NIST AI Agent Standards Initiative and OWASP Top 10 for Agentic Applications

🔲 **Planned**
- pip package and Python SDK
- Detailed GDPR, FDA, ISO/IEC 23894 and SR 11-7 mappings
- Protobuf and GraphQL schema definitions; OpenAPI specification for MCML REST APIs
- Additional SDKs (TypeScript, Go, Java, Rust)
- Governance graph explorer, card generation from code, card diff tools

### v1.2 (planned)

🔲 **Incident Card**: link post-deployment incidents to cards
🔲 **Proposed MCP extension** for agent governance evidence, if runtime testing supports it

### Future Exploration

🔮 **Federated Learning Governance**
- Multi-party Model Cards
- Distributed dataset provenance
- Cross-organizational compliance

🔮 **Real-Time Governance Monitoring**
- Standard APIs for governance telemetry
- Drift detection protocols
- Automated remediation triggers

🔮 **Blockchain Integration**
- Immutable audit trails
- Smart contracts for governance enforcement
- Decentralized card verification

🔮 **Extended Card Types**
- Evaluation Card (benchmarking and testing)
- Deployment Card (infrastructure and operations)

---

## FAQ

**Q: What is MCML?**
A: MCML is a standard language that formalizes four documentation practices (Model, Dataset, Interface, and Agentic Governance cards) into a unified, machine-readable protocol for regulatory compliance.

**Q: Did MCML invent Model Cards and Dataset Cards?**
A: No. Model Cards were created by Google (Mitchell et al., 2019) and Dataset Cards/Datasheets by Microsoft (Gebru et al., 2018). MCML formalizes these existing standards and adds machine readability.

**Q: What problem does MCML solve?**
A: MCML enables **automated compliance** by making AI governance documentation machine-readable. Instead of manually reconstructing audit trails from PDFs and spreadsheets, you can programmatically validate completeness, generate compliance reports, and enforce governance requirements in CI/CD.

**Q: Do I need to use the two-layer architecture?**
A: No. The two-layer architecture with foreign keys is our **patent-pending reference implementation** that demonstrates the benefits of MCML. You can implement MCML using any database, file system, or architecture. The standard is implementation-agnostic.

**Q: What makes MCML "machine-readable"?**
A: MCML provides JSON Schemas with formal validation rules and structured field definitions, plus a reference validator. This allows tools to parse, validate, and query governance documentation automatically.

**Q: How does MCML relate to NIST AI RMF / EU AI Act / GDPR?**
A: MCML provides **mappings** from card fields to regulatory requirements. It helps you demonstrate compliance but doesn't guarantee it. You still need to satisfy the actual regulatory requirements. MCML makes it easier to document and prove.

**Q: Can I extend MCML with custom fields?**
A: Yes. MCML schemas support `additionalProperties` for organization-specific extensions. You can add custom fields while maintaining compatibility with the core standard.

**Q: How do the four card types relate?**
A: Cards reference each other via URIs:
- Model Card → references Dataset Card (training data)
- Model Card → references Interface Card (deployment)
- Interface Card → may reference Agentic Governance Card (if using agents)
- Agentic Governance Card → references Model Cards (models the agent uses)

**Q: What if my organization doesn't use AI agents?**
A: Agentic Governance Cards are optional. If you're not deploying autonomous agents, you only need Model, Dataset, and Interface cards.

**Q: Is MCML only for ML models, or can it document traditional software?**
A: MCML is designed for AI/ML systems. For traditional software, use standard documentation practices (OpenAPI, README, etc.). However, Interface Cards can document any API.

**Q: How do I migrate existing documentation to MCML?**
A: Migration tooling is planned. Today, copy the relevant fields from your existing Model Card or Datasheet into the YAML structure shown in [`examples/`](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/examples/) and run `python tools/mcml.py validate` until it passes.

**Q: What if I'm already using MLflow / Weights & Biases / other MLOps tools?**
A: MCML is designed to sit alongside existing tools. Cards are plain YAML or JSON, so they can be generated from MLOps metadata by your own scripts; official MLflow and W&B integrations are planned.

**Q: How often should cards be updated?**
A:
- **Model Cards**: update with each model version or when performance or fairness characteristics change
- **Dataset Cards**: update when data sources, preprocessing, or quality metrics change
- **Interface Cards**: update when API contracts, access control, or compliance requirements change
- **Agentic Governance Cards**: update when autonomy level, tools, or oversight rules change

**Q: Can MCML be used for open source models?**
A: Yes. MCML is well suited to documenting open source models. Publish Model and Dataset Cards alongside your model releases to provide transparency and enable responsible use.

**Q: How does MCML handle model versioning?**
A: Each card includes a `version` field (semantic versioning recommended: `1.0.0`, `1.1.0`, `2.0.0`). Cards can reference specific versions of other cards via URIs like `dataset://customer_data/v2.3`.

**Q: What about models trained on proprietary data?**
A: Dataset Cards can document data characteristics (biases, quality) without exposing proprietary details. Use `collection_method: "Proprietary customer data"` and document known biases and limitations without revealing specifics.

---

## Presentations

- "MCML: A Universal Schema for AI Traceability & Lifecycle Governance," co-presented with Alex Olaniyan (PLEYVERSE AI), virtual Day 1 session, 6th annual MLOps World | GenAI Summit, October 2025. [Recording](https://www.youtube.com/watch?v=BKLwwvKk0DE)

---

## Patents

The two-layer architecture with foreign key relationships for AI governance is **patent pending**. Implementing the MCML specification and schemas does not require a patent license.

---

## License

MCML is open in the way Linux is: free to use and build on, with changes to the code shared back, and commercial licenses available.

### Specification, schemas and documentation: CC BY 4.0

The MCML specification, JSON Schemas, compliance mappings, example cards and documentation are licensed under **[Creative Commons Attribution 4.0 International](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/LICENSE-SPEC)**. Anyone, including commercial vendors, may use, adapt and implement the standard, provided they give credit and indicate changes.

### Code: GPL-3.0, or a commercial license

The code in this repository (`tools/` and any future SDKs, gateway and reference implementation code) is licensed under the **[GNU General Public License v3.0 or later](https://github.com/PLEYVERSE-AI/mcml-standard/blob/main/LICENSE)**. You may use it for any purpose, including commercially. If you distribute modified versions, you must release them under the same license.

Organizations that want to embed or distribute the code in proprietary products without GPL obligations can obtain a **commercial license**: contact [lanre@pleyverse.com](mailto:lanre@pleyverse.com).

Contributions are accepted under the same terms, so the project can continue to offer both licenses.

---

## Contact and Support

- 🌐 **Website**: [https://mcml-standard.org](https://mcml-standard.org)
- 🐛 **Issues and proposals**: [GitHub issues](https://github.com/PLEYVERSE-AI/mcml-standard/issues)
- 📧 **Author**: Dr. Olanrewaju Ogunkunle, [lanre@pleyverse.com](mailto:lanre@pleyverse.com)

---

## Acknowledgments

MCML builds on pioneering work by:

- **Google Research**: Model Cards for Model Reporting (Mitchell et al., 2019)
- **Microsoft Research**: Datasheets for Datasets (Gebru et al., 2018)
- **NIST**: AI Risk Management Framework and AI Agent Standards Initiative
- **European Commission**: EU AI Act
- **ISO/IEC JTC 1/SC 42**: AI standardization
- **Model Context Protocol and Agent2Agent communities**: agent interoperability patterns
- **OWASP GenAI Security Project**: Top 10 for Agentic Applications
- **LangChain Community**: agent framework governance patterns

We are grateful to the AI governance research community, open source contributors, and early adopters who shaped this standard.

---

## Star ⭐ This Repo

If MCML helps your AI governance work, please **star this repository** to show support and help others discover the standard.

---

## Citation

If you use MCML in research or production, please cite:

```bibtex
@misc{mcml_standard,
  title  = {Model Connect Markup Language (MCML): A Machine-Readable Standard for AI Governance},
  author = {Ogunkunle, Olanrewaju},
  year   = {2026},
  url    = {https://mcml-standard.org}
}
```

**For the reference implementation:**
```bibtex
@misc{mcml_two_layer_2026,
  title  = {Two-Layer Architecture for AI Governance Traceability},
  author = {Ogunkunle, Olanrewaju},
  year   = {2026},
  note   = {Patent pending. Reference implementation of the MCML standard.},
  url    = {https://mcml-standard.org}
}
```

---

**Model Connect Markup Language (MCML): From documentation to automation. Making AI governance machine-readable, compliant, and auditable.**

**Version 1.1 (draft) | Last updated: 2026-11-10**
