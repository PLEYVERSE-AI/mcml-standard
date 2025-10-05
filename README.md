# MCML Standard

**Machine-Readable Card Markup Language for AI Governance**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Specification](https://img.shields.io/badge/spec-v1.0-blue)](https://mcml-standard.org/spec/v1.0)
[![Status](https://img.shields.io/badge/status-draft-orange)]()

> **A unified standard for AI governance documentation — making compliance automatable**

---

## What is MCML?

MCML is a **standard language** that formalizes and unifies emerging AI documentation practices into a machine-readable protocol for regulatory compliance.

### Building on Industry Standards

MCML integrates **four emerging documentation standards** from the AI governance community:

1. **Model Cards** (Google, Mitchell et al., 2019) — Model purpose, performance, limitations
2. **Dataset Cards / Datasheets** (Microsoft, Gebru et al., 2018) — Data provenance, biases, collection methods  
3. **Interface Cards** (emerging from API governance) — Service endpoints, access control, monitoring
4. **Agentic Cards** (emerging from MCP, LangGraph communities) — Agent autonomy, oversight, tool permissions

These four Card types are becoming the **de facto industry standards** for AI documentation. MCML provides the integration layer that makes them work together.

### The Compliance Challenge

Organizations must comply with multiple regulatory frameworks and ISO standards:

- **NIST AI Risk Management Framework** (AI RMF)
- **EU AI Act** (Regulation 2024/1689)
- **ISO/IEC 42001** (AI Management System)
- **ISO/IEC 23894** (AI Risk Management)
- **GDPR** (General Data Protection Regulation)
- **FDA** (Medical Device Regulations for AI/ML)
- **Sector-specific regulations** (finance, healthcare, employment)

**The Problem:** Each framework has different documentation requirements, and the four Card types exist independently without a unified structure or machine-readable format.

### MCML's Solution: Three Core Contributions

#### 1. Unified Schema

MCML formalizes the structure of all four Card types with:
- ✅ Consistent field definitions across Card types
- ✅ Required vs. optional field specifications
- ✅ Relationship models (how Cards reference each other)
- ✅ Versioning and temporal validity

#### 2. Machine-Readable Protocol

MCML provides JSON/YAML schemas enabling:
- ✅ **Programmatic validation** — Automated checking of completeness
- ✅ **Compliance automation** — CI/CD gates that block incomplete deployments
- ✅ **Tool interoperability** — Any tool can read/write MCML format
- ✅ **Real-time monitoring** — Dashboards showing governance status
- ✅ **Instant audit trails** — Generate compliance reports in seconds

#### 3. Compliance Framework Mappings

MCML maps Card fields to regulatory requirements:

| Framework | MCML Mapping |
|-----------|-------------|
| **NIST AI RMF** | Shows which Card fields satisfy GOVERN/MAP/MEASURE/MANAGE functions |
| **EU AI Act** | Maps Cards to risk classification, transparency, human oversight requirements |
| **ISO/IEC 42001** | Links Cards to AI management system documentation clauses |
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

## Reference Implementation: Patented Two-Layer Architecture

While MCML is **implementation-agnostic** (you can use any database, file system, or architecture), we provide a **reference implementation** that demonstrates the power of machine readability through our **patented two-layer architecture**.

### The Architecture

```
┌────────────────────────────────────────────────────────────┐
│              GOVERNANCE LAYER (Documentation)              │
│                                                            │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐       │
│  │ Model Cards │ │Dataset Cards│ │Interface Cards│       │
│  └──────┬──────┘ └──────┬──────┘ └──────┬───────┘       │
│         │                │                │                │
│  ┌──────┴──────────────────────────────────┐             │
│  │        Agentic Cards                      │             │
│  └──────┬──────────────────────────────────┘             │
└─────────┼──────────┼──────────┼──────────┼────────────────┘
          │          │          │          │
          │   Foreign Key Relationships    │
          │          │          │          │
┌─────────┼──────────┼──────────┼──────────┼────────────────┐
│         ▼          ▼          ▼          ▼                │
│  ┌──────────────┐ ┌───────────┐ ┌─────────────────┐     │
│  │Model Registry│ │  Dataset  │ │Interface Registry│     │
│  └──────────────┘ │  Registry │ └─────────────────┘     │
│                   └───────────┘                           │
│  ┌─────────────────┐      ┌───────────────────────┐     │
│  │ Agent Registry  │      │  Inference Events     │     │
│  └─────────────────┘      └───────────────────────┘     │
│                                                           │
│            OPERATIONAL LAYER (Deployments)                │
└───────────────────────────────────────────────────────────┘
```

### Key Innovation: Foreign Keys Linking Layers

**Governance Layer (Documentation):**
- Model Cards — Document model purpose, performance, limitations, ethical considerations
- Dataset Cards — Document data provenance, biases, quality, legal basis
- Interface Cards — Document API governance, access control, monitoring requirements
- Agentic Cards — Document agent autonomy, oversight rules, tool permissions

**Operational Layer (Deployed Systems):**
- Model Registry — Actual deployed model instances
- Dataset Registry — Actual data sources in use
- Interface Registry — Live API endpoints and services
- Agent Registry — Running agent instances (MCP servers, LangGraph graphs, etc.)
- Inference Events — Every prediction/decision with full context

**Foreign Keys** create enforceable relationships:
- Can't deploy a model without a complete Model Card (database constraint)
- Can't reference a non-existent Dataset Card (referential integrity)
- Every inference event links to all four Card types via operational registries

### Benefits of This Architecture

| Capability | How Foreign Keys Enable It | Time Saved |
|------------|---------------------------|------------|
| **Pre-deployment validation** | FK constraint blocks deployment if Card missing | Catches issues before production |
| **Single-query audit trails** | One SQL JOIN traverses entire governance graph | Hours → Milliseconds |
| **Guaranteed completeness** | Database enforces all required Cards exist | No manual verification |
| **Automatic compliance checks** | Query Card fields to validate regulatory requirements | Days → Seconds |
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
    ac.autonomy_level,
    ac.escalation_rules
    
FROM inference_events ie
JOIN model_registry mr ON ie.model_fk = mr.id
JOIN model_cards mc ON mr.model_card_fk = mc.id
JOIN dataset_cards dc ON mc.training_dataset_fk = dc.id
JOIN interface_registry ir ON ie.interface_fk = ir.id
JOIN interface_cards ic ON ir.interface_card_fk = ic.id
LEFT JOIN agent_registry ar ON ie.agent_fk = ar.id
LEFT JOIN agentic_cards ac ON ar.agent_card_fk = ac.id

WHERE ie.event_id = '550e8400-e29b-41d4-a716-446655440000';
```

⏱️ **Query time: <100ms** for complete governance lineage across all four Card types

### This is ONE Way to Implement MCML

The two-layer architecture with foreign keys is our **patented reference implementation**, but MCML can be implemented in other ways:

- **Graph databases** (Neo4j) — Relationships as first-class citizens
- **Document stores** (MongoDB) — Embedded Cards with URI references  
- **File-based** (Git repositories) — YAML files with linked references
- **Hybrid** (Cards in Git, events in TimescaleDB)

The MCML **standard** is implementation-agnostic. Our reference implementation demonstrates the benefits of machine readability + relational integrity.

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
  
  # Relationships to other Cards
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
    MANAGE: "Monthly revalidation, automated drift detection"
```

**MCML Extensions for Machine Readability:**
- `training_dataset_ref` — URI reference to Dataset Card (enables automated lineage)
- `performance_metrics` — Structured numbers (enables automated threshold checks)
- `fairness_metrics` — Quantitative bias measures (enables drift detection)
- `nist_rmf_alignment` — Direct mapping to compliance framework

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
      description: "Deduplicated on SSN + application_date"
      
    - step: "Impute missing income"
      description: "Median imputation by ZIP code + job category"
      
    - step: "Outlier removal"
      description: "Remove income >$500K or <$5K (0.3% of data)"
  
  # Legal and compliance
  contains_pii: true
  pii_fields:
    - ssn
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
- `known_biases` — Structured list (enables automated fairness validation)
- `quality_metrics` — Quantitative scores (enables data quality gates)
- `preprocessing_steps` — Reproducible transformations (enables lineage tracking)
- `pii_fields` — Explicit PII listing (enables GDPR compliance checks)

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
- `rate_limits` — Structured throttling (enables automated enforcement)
- `access_control_policy` — Machine-readable permissions (enables IAM integration)
- `compliance_frameworks` — Explicit framework list (enables compliance validation)
- `data_residency_requirements` — Geographic constraints (enables deployment validation)

---

### 4. Agentic Card (emerging standard for autonomous systems)

Documents the **governance metadata** for AI agents and autonomous components.

**Core Fields:**
```yaml
agentic_card:
  agent_name: loan_approval_agent
  agent_type: task_executor
  description: "Semi-autonomous agent for personal loan approval decisions"
  
  # Autonomy level
  autonomy_level: semi_autonomous
  
  decision_authority:
    max_loan_amount: 25000
    max_approval_without_review: 15000
    requires_human_approval_above: 25000
    
  # Tool and function access
  allowed_tools:
    - credit_bureau_lookup
    - income_verification
    - fraud_check
    - employment_verification
    
  forbidden_actions:
    - modify_credit_score
    - approve_loan_above_authority
    - disable_fraud_check
    - access_competitor_data
    
  tool_call_limits:
    credit_bureau_lookup:
      max_calls_per_application: 3
      cost_per_call: 2.50
    fraud_check:
      max_calls_per_application: 1
      
  # Human oversight
  escalation_rules:
    - condition: "confidence_score < 0.85"
      action: "escalate_to_senior_underwriter"
      sla: "4 hours"
      
    - condition: "loan_amount > 25000"
      action: "require_manual_approval"
      sla: "24 hours"
      
    - condition: "fraud_score > 0.7"
      action: "immediate_escalation_to_fraud_team"
      sla: "1 hour"
      
    - condition: "applicant_in_high_risk_group"
      action: "require_fairness_review"
      sla: "8 hours"
  
  human_review_triggers:
    - "Confidence below threshold"
    - "Applicant requests explanation"
    - "Contradicting data sources"
    - "High-value transaction"
  
  # Safety guardrails
  circuit_breaker_conditions:
    - "error_rate > 10% over 5 minutes"
    - "approval_rate > 95% over 1 hour"  # Anomaly detection
    - "average_confidence < 0.7 over 30 minutes"
    - "tool_call_failure_rate > 20%"
    
  rollback_procedures: |
    1. Disable agent immediately
    2. Route all requests to manual review queue
    3. Alert on-call engineer
    4. Investigate root cause
    5. Require manual approval to re-enable
    
  safety_protocols:
    - "Sandbox testing required before production deployment"
    - "A/B test at 1% traffic for 48 hours"
    - "Weekly fairness audits"
    - "Monthly capability reviews"
  
  # Agent framework integration
  framework: mcp  # Model Context Protocol
  framework_version: "0.9.0"
  framework_compatibility:
    - mcp
    - langgraph
  
  mcp_server_config:
    server_url: "mcp://agents.example.com/loan-approval"
    protocol_version: "0.9"
    
  # Inter-agent communication
  can_communicate_with:
    - fraud_detection_agent
    - customer_service_agent
  prohibited_communication:
    - competitor_agents
    - external_third_party_agents
  
  # Monitoring
  action_logging_level: all  # Log every decision and tool call
  audit_trail_retention_days: 365
  
  # Accountability
  responsible_party: "Risk Management - Lending Operations"
  escalation_contact: "risk-team@example.com"
  approval_workflow: "Requires VP Risk approval for autonomy changes"
```

**MCML Extensions for Machine Readability:**
- `allowed_tools` / `forbidden_actions` — Whitelist/blacklist (enables runtime enforcement)
- `escalation_rules` — Structured conditions (enables automated routing)
- `circuit_breaker_conditions` — Quantitative thresholds (enables automatic shutdown)
- `framework` — Explicit framework identifier (enables deployment validation)

---

## Compliance Framework Mappings

MCML provides **direct mappings** from Card fields to regulatory requirements, enabling automated compliance checking.

### NIST AI Risk Management Framework

| NIST Function | Required MCML Fields | Validation Check |
|---------------|---------------------|------------------|
| **GOVERN** | `model_card.responsible_team`<br>`agentic_card.responsible_party`<br>`dataset_card.data_owner` | ✅ All ownership fields populated |
| **MAP** | `model_card.intended_use`<br>`model_card.limitations`<br>`model_card.risk_category`<br>`agentic_card.decision_authority` | ✅ Purpose and constraints documented |
| **MEASURE** | `model_card.performance_metrics`<br>`model_card.fairness_metrics`<br>`dataset_card.quality_metrics`<br>`dataset_card.known_biases` | ✅ Quantitative assessments present |
| **MANAGE** | `interface_card.logging_level = 'detailed'`<br>`agentic_card.escalation_rules`<br>`agentic_card.circuit_breaker_conditions` | ✅ Monitoring and response mechanisms |

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
            model_card.limitations
        ),
        "MEASURE": bool(
            model_card.performance_metrics and
            model_card.fairness_metrics and
            dataset_card.quality_metrics
        ),
        "MANAGE": (
            interface_card.logging_level == "detailed" and
            bool(agentic_card.escalation_rules)
        )
    }
    
    return {
        "compliant": all(results.values()),
        "function_status": results
    }
```

### EU AI Act

| Article | Requirement | MCML Fields | Validation |
|---------|------------|-------------|------------|
| **Art. 6** | Risk Classification | `model_card.risk_category` | ✅ Must be: `minimal`, `limited`, `high`, `unacceptable` |
| **Art. 11** | Technical Documentation | All four Card types complete | ✅ All required fields present |
| **Art. 14** | Human Oversight | `agentic_card.autonomy_level`<br>`agentic_card.escalation_rules`<br>`agentic_card.human_review_triggers` | ✅ Oversight mechanisms defined for high-risk |
| **Art. 13** | Transparency | `model_card.intended_use`<br>`model_card.limitations`<br>`dataset_card.known_biases` | ✅ Clear purpose and constraints |
| **Art. 15** | Accuracy Requirements | `model_card.performance_metrics`<br>`dataset_card.quality_metrics` | ✅ Metrics meet thresholds |

### ISO/IEC 42001 (AI Management System)

| Clause | Requirement | MCML Fields |
|--------|-------------|-------------|
| **6.1** | Risk Assessment | `model_card.risk_category`<br>`model_card.ethical_considerations` |
| **7.2** | Competence | `model_card.responsible_team`<br>`agentic_card.responsible_party` |
| **7.5** | Documented Information | All four Card types |
| **8.1** | Operational Planning | `model_card.intended_use`<br>`agentic_card.decision_authority` |
| **9.1** | Monitoring | `interface_card.logging_level`<br>`agentic_card.circuit_breaker_conditions` |

### GDPR (Data Protection)

| Principle | Requirement | MCML Fields | Validation |
|-----------|------------|-------------|------------|
| **Art. 5.1.b** | Purpose Limitation | `model_card.intended_use`<br>`model_card.out_of_scope_uses` | ✅ Explicit boundaries |
| **Art. 5.1.c** | Data Minimization | `dataset_card.collection_method`<br>`dataset_card.pii_fields` | ✅ Only necessary data |
| **Art. 5.1.e** | Storage Limitation | `dataset_card.retention_policy` | ✅ Retention period defined |
| **Art. 13** | Transparency | `model_card.limitations`<br>`dataset_card.known_biases` | ✅ Explainability |
| **Art. 24** | Accountability | All Cards: ownership fields | ✅ Controllers identified |

---

## Getting Started

### 1. Install MCML Tools

```bash
pip install mcml-standard
```

### 2. Create Your First Model Card

```python
from mcml import ModelCard

# Create Model Card following MCML schema
model_card = ModelCard(
    model_name="credit_risk_scorer",
    version="3.2.1",
    intended_use="Credit risk assessment for personal loans up to $50K",
    training_dataset_ref="dataset://customer_credit_data/v2.3",
    performance_metrics={
        "auc": 0.87,
        "f1_score": 0.82
    },
    fairness_metrics={
        "demographic_parity": 0.92,
        "equal_opportunity": 0.94
    },
    limitations=[
        "Not validated for commercial loans",
        "Performance degrades for recent immigrants"
    ],
    responsible_team="ML Engineering - Credit Models"
)

# Validate against MCML schema
validation_result = model_card.validate()
print(validation_result)  # {'valid': True, 'errors': []}

# Check compliance with NIST AI RMF
nist_compliance = model_card.check_compliance(framework="nist_rmf")
print(nist_compliance)
# {
#   'GOVERN': True,
#   'MAP': True, 
#   'MEASURE': True,
#   'MANAGE': False,  # Missing interface/agent cards
#   'overall': False
# }

# Export to YAML
model_card.save("model_cards/credit_scorer_v3.2.1.yaml")
```

### 3. Create Dataset Card

```python
from mcml import DatasetCard

dataset_card = DatasetCard(
    dataset_name="customer_credit_data",
    version="2.3",
    collection_method="Production credit applications 2023-2024",
    known_biases=[
        {
            "bias_type": "geographic",
            "description": "Urban areas over-represented",
            "mitigation": "Synthetic rural data augmentation"
        }
    ],
    quality_metrics={
        "completeness": 0.94,
        "consistency_score": 0.89
    },
    contains_pii=True,
    pii_fields=["ssn", "full_name", "address"],
    legal_basis="Customer consent (GDPR Art. 6.1.b)",
    data_owner="Data Governance Office"
)

dataset_card.save("dataset_cards/customer_credit_data_v2.3.yaml")
```

### 4. Validate Complete Governance Stack

```python
from mcml import GovernanceValidator

# Validate all four Card types together
validator = GovernanceValidator()

result = validator.validate_complete_stack(
    model_card="model_cards/credit_scorer_v3.2.1.yaml",
    dataset_card="dataset_cards/customer_credit_data_v2.3.yaml",
    interface_card="interface_cards/credit_api_v2.1.0.yaml",
    agentic_card="agentic_cards/loan_agent_v1.3.0.yaml",
    framework="nist_rmf"
)

print(result)
# {
#   'valid': True,
#   'all_cards_present': True,
#   'relationships_valid': True,
#   'nist_compliance': {
#     'GOVERN': True,
#     'MAP': True,
#     'MEASURE': True,
#     'MANAGE': True,
#     'overall': True
#   }
# }
```

### 5. Integrate with CI/CD

```yaml
# .github/workflows/validate-governance.yml
name: MCML Governance Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Install MCML
        run: pip install mcml-standard
      
      - name: Validate Model Cards
        run: |
          mcml validate \
            --card-type model \
            --directory model_cards/ \
            --schema-version 1.0
      
      - name: Validate Dataset Cards
        run: |
          mcml validate \
            --card-type dataset \
            --directory dataset_cards/ \
            --schema-version 1.0
      
      - name: Check NIST AI RMF Compliance
        run: |
          mcml compliance-check \
            --framework nist_rmf \
            --model-card model_cards/credit_scorer_v3.2.1.yaml \
            --dataset-card dataset_cards/customer_credit_data_v2.3.yaml \
            --interface-card interface_cards/credit_api_v2.1.0.yaml
          
          # Exit with error if not compliant
          if [ $? -ne 0 ]; then
            echo "❌ NIST AI RMF compliance failed"
            exit 1
          fi
```

### 6. Deploy with Reference Implementation

If using the patented two-layer architecture:

```python
from mcml.reference_implementation import TwoLayerArchitecture

# Initialize reference implementation (PostgreSQL + foreign keys)
architecture = TwoLayerArchitecture(database_url="postgresql://...")

# Deploy model with governance
deployment = architecture.deploy_model(
    model_card_path="model_cards/credit_scorer_v3.2.1.yaml",
    dataset_card_path="dataset_cards/customer_credit_data_v2.3.yaml",
    interface_card_path="interface_cards/credit_api_v2.1.0.yaml",
    model_artifact_uri="s3://models/credit_scorer/v3.2.1/",
    environment="production"
)

# Foreign key constraints ensure all Cards exist before deployment
print(deployment)
# {
#   'model_registry_id': '550e8400-...',
#   'governance_complete': True,
#   'deployed_at': '2025-01-15T10:00:00Z',
#   'status': 'active'
# }

# Query complete lineage
lineage = architecture.get_lineage(inference_event_id="evt_12345")
print(lineage.model_card.intended_use)
print(lineage.dataset_card.known_biases)
```

---

## Use Cases

### 1. Pre-Deployment Validation

**Block incomplete deployments:**

```bash
$ mcml pre-deploy-check \
    --model-card credit_scorer_v3.2.1.yaml \
    --dataset-card customer_data_v2.3.yaml \
    --framework eu_ai_act

❌ Deployment blocked: Missing required fields
  - model_card.fairness_metrics (required for HIGH risk)
  - agentic_card missing (required for autonomous decisions)
  
Fix these issues before deploying to production.
```

### 2. Automated Compliance Reporting

**Generate regulatory reports instantly:**

```python
from mcml import ComplianceReporter

reporter = ComplianceReporter()

# Generate NIST AI RMF report
nist_report = reporter.generate_report(
    inference_event_id="evt_12345",
    framework="nist_rmf",
    output_format="pdf"
)

# Generates complete audit trail:
# - Executive summary
# - GOVERN function evidence
# - MAP function evidence  
# - MEASURE function evidence
# - MANAGE function evidence
# - Recommendations

nist_report.save("reports/nist_compliance_evt_12345.pdf")
```

### 3. Real-Time Governance Monitoring

**Dashboard showing live compliance status:**

```python
from mcml import GovernanceDashboard

dashboard = GovernanceDashboard()

status = dashboard.get_production_status()

print(status)
# {
#   'total_models': 47,
#   'fully_documented': 44,
#   'missing_cards': 3,
#   'compliance_status': {
#     'nist_rmf_compliant': 42,
#     'eu_ai_act_compliant': 40,
#     'gdpr_compliant': 47
#   },
#   'at_risk_models': [
#     {
#       'model': 'fraud_detector_v2.1',
#       'issue': 'Missing fairness_metrics',
#       'deadline': '2025-02-01'
#     }
#   ]
# }
```

### 4. Incident Investigation

**Instant root cause analysis:**

```python
from mcml import IncidentInvestigator

investigator = IncidentInvestigator()

# Investigate biased prediction
analysis = investigator.analyze_incident(
    inference_event_id="incident_789",
    include_full_lineage=True
)

print(analysis)
# {
#   'event': {
#     'timestamp': '2025-01-15T14:23:45Z',
#     'prediction': 'DENY',
#     'confidence': 0.62
#   },
#   'model': {
#     'name': 'credit_scorer',
#     'version': '3.2.1',
#     'known_limitations': [
#       'Performance degrades for recent immigrants'
#     ]
#   },
#   'dataset': {
#     'known_biases': [
#       {
#         'type': 'demographic',
#         'description': 'Limited recent immigrant data',
#         'impact': 'May underperform for this group'
#       }
#     ]
#   },
#   'root_cause': 'Applicant in known high-risk group with limited training data',
#   'recommendation': 'Manual review required per escalation rules'
# }
```

### 5. Agent Governance and Safety

**Monitor autonomous agent behavior:**

```python
from mcml import AgentMonitor

monitor = AgentMonitor()

# Check if agent action complies with governance
action_check = monitor.validate_action(
    agent_id="loan_approval_agent",
    proposed_action={
        'type': 'approve_loan',
        'loan_amount': 30000,
        'confidence': 0.82
    }
)

print(action_check)
# {
#   'allowed': False,
#   'reason': 'Exceeds decision authority (max: $25,000)',
#   'required_action': 'escalate_to_senior_underwriter',
#   'escalation_sla': '24 hours',
#   'agentic_card_ref': 'agent://loan_approval_agent/v1.3.0'
# }
```

---

## Documentation

📖 **[Complete Specification](https://mcml-standard.org/spec/v1.0)**

### Core Documentation
- [MCML Standard Overview](https://mcml-standard.org/)
- [Card Schema Specifications](https://mcml-standard.org/schemas/)
- [Compliance Framework Mappings](https://mcml-standard.org/compliance/)
- [Machine-Readable Protocol](https://mcml-standard.org/protocol/)

### Implementation Guides
- [Reference Implementation (Two-Layer Architecture)](https://mcml-standard.org/reference-implementation/)
- [PostgreSQL Setup Guide](https://mcml-standard.org/guides/postgresql/)
- [Alternative Implementations](https://mcml-standard.org/guides/alternatives/)
- [MLflow Integration](https://mcml-standard.org/integrations/mlflow/)
- [CI/CD Integration](https://mcml-standard.org/integrations/cicd/)

### Compliance Guides
- [NIST AI RMF Compliance](https://mcml-standard.org/compliance/nist-rmf/)
- [EU AI Act Compliance](https://mcml-standard.org/compliance/eu-ai-act/)
- [ISO/IEC 42001 Compliance](https://mcml-standard.org/compliance/iso-42001/)
- [GDPR Compliance](https://mcml-standard.org/compliance/gdpr/)
- [FDA Medical Device Compliance](https://mcml-standard.org/compliance/fda/)

### API Reference
- [Python SDK](https://mcml-standard.org/sdk/python/)
- [REST API](https://mcml-standard.org/api/rest/)
- [CLI Tools](https://mcml-standard.org/cli/)

---

## Schema Downloads

### MCML v1.0 Schemas (JSON Schema)

- **[Model Card Schema](https://mcml-standard.org/schemas/v1.0/model-card.schema.json)** — Machine-readable Model Card specification
- **[Dataset Card Schema](https://mcml-standard.org/schemas/v1.0/dataset-card.schema.json)** — Machine-readable Dataset Card specification  
- **[Interface Card Schema](https://mcml-standard.org/schemas/v1.0/interface-card.schema.json)** — Machine-readable Interface Card specification
- **[Agentic Card Schema](https://mcml-standard.org/schemas/v1.0/agentic-card.schema.json)** — Machine-readable Agentic Card specification

### Example Cards

- **[Model Card Example (YAML)](https://mcml-standard.org/examples/model-card.yaml)**
- **[Dataset Card Example (YAML)](https://mcml-standard.org/examples/dataset-card.yaml)**
- **[Interface Card Example (YAML)](https://mcml-standard.org/examples/interface-card.yaml)**
- **[Agentic Card Example (YAML)](https://mcml-standard.org/examples/agentic-card.yaml)**
- **[Complete Governance Stack](https://mcml-standard.org/examples/complete-stack/)**

### Compliance Templates

- **[NIST AI RMF Template](https://mcml-standard.org/templates/nist-rmf/)**
- **[EU AI Act Template](https://mcml-standard.org/templates/eu-ai-act/)**
- **[ISO 42001 Template](https://mcml-standard.org/templates/iso-42001/)**

---

## Community and Ecosystem

### Contributing

MCML is an **open standard**. We welcome contributions:

- **Schema Enhancements** — Propose new fields, relationships, or Card types
- **Compliance Mappings** — Add frameworks (ISO 27001, SOC2, sector-specific)
- **Implementation Patterns** — Share your architecture and learnings
- **Tooling** — Build validators, generators, visualizers, IDE extensions
- **Documentation** — Improve guides, add examples, translate content

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for detailed guidelines.

### Governance

MCML is governed by the **AI Governance Standards Working Group**, with representation from:
- Industry practitioners (AI/ML engineers, compliance officers)
- Academic researchers (AI ethics, governance)
- Regulatory experts
- Open source community

### Adopters

Organizations using MCML in production:
- *(List will grow as ecosystem develops)*

### Complementary Tools

**Integrations:**
- **MLflow MCML Plugin** — Auto-generate Model Cards from experiments
- **Great Expectations Bridge** — Link data tests to Dataset Cards
- **Weights & Biases Integration** — Export W&B metadata to MCML
- **LangChain MCML** — Document LangChain applications with Agentic Cards

**IDE Extensions:**
- **VS Code MCML Extension** — Syntax highlighting, validation, auto-complete
- **IntelliJ MCML Plugin** — Schema validation, reference navigation
- **Jupyter MCML Widget** — Interactive Card creation in notebooks

**Validation Tools:**
- **MCML CLI** — Command-line validation and compliance checking
- **MCML Linter** — Pre-commit hooks for Card validation
- **MCML Dashboard** — Web UI for governance monitoring

---

## Roadmap

### Current: v1.0 (January 2025)

✅ **Core Specification**
- Four Card types formalized (Model, Dataset, Interface, Agentic)
- JSON Schema definitions for all Cards
- URI-based relationship model
- Versioning and temporal validity

✅ **Compliance Mappings**
- NIST AI Risk Management Framework
- EU AI Act
- ISO/IEC 42001
- GDPR (high-level)

✅ **Reference Implementation**
- Two-layer architecture (patented)
- PostgreSQL/TimescaleDB schema
- Python SDK
- CLI tools

### Planned: v1.1 (Q2 2025)

🔲 **Enhanced Compliance**
- Detailed GDPR mapping (all Articles)
- FDA medical device regulations
- ISO/IEC 23894 (AI risk management)
- Financial services regulations (SR 11-7, model risk management)

🔲 **Additional Schemas**
- Protobuf schema definitions (in addition to JSON Schema)
- GraphQL schema for API implementations
- OpenAPI specification for MCML REST APIs

🔲 **Multi-Language SDKs**
- JavaScript/TypeScript SDK
- Go SDK
- Java SDK
- Rust SDK

🔲 **Advanced Tooling**
- MCML visualization tools (governance graph explorer)
- Automated Card generation from code
- Diff tools for Card versioning

### Future Exploration (2025-2026)

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
- Decentralized Card verification

🔮 **Extended Card Types**
- Evaluation Card (benchmarking and testing)
- Deployment Card (infrastructure and operations)
- Incident Card (post-deployment issues)

---

## FAQ

**Q: What is MCML?**  
A: MCML is a standard language that formalizes four emerging AI documentation practices (Model Cards, Dataset Cards, Interface Cards, Agentic Cards) into a unified, machine-readable protocol for regulatory compliance.

**Q: Did MCML invent Model Cards and Dataset Cards?**  
A: No. Model Cards were created by Google (Mitchell et al., 2019) and Dataset Cards/Datasheets by Microsoft (Gebru et al., 2018). MCML formalizes these existing standards and adds machine readability.

**Q: What problem does MCML solve?**  
A: MCML enables **automated compliance** by making AI governance documentation machine-readable. Instead of manually reconstructing audit trails from PDFs and spreadsheets, you can programmatically validate completeness, generate compliance reports, and enforce governance requirements in CI/CD.

**Q: Do I need to use the two-layer architecture?**  
A: No. The two-layer architecture with foreign keys is our **patented reference implementation** that demonstrates the benefits of MCML. You can implement MCML using any database, file system, or architecture. The standard is implementation-agnostic.

**Q: What makes MCML "machine-readable"?**  
A: MCML provides JSON/YAML schemas with formal validation rules, structured field definitions, and programmatic APIs. This allows tools to parse, validate, and query governance documentation automatically.

**Q: How does MCML relate to NIST AI RMF / EU AI Act / GDPR?**  
A: MCML provides **mappings** from Card fields to regulatory requirements. It helps you demonstrate compliance but doesn't guarantee it. You still need to satisfy the actual regulatory requirements—MCML just makes it easier to document and prove.

**Q: Can I extend MCML with custom fields?**  
A: Yes. MCML schemas support `additionalProperties` for organization-specific extensions. You can add custom fields while maintaining compatibility with the core standard.

**Q: How do the four Card types relate?**  
A: Cards reference each other via URIs:
- Model Card → references Dataset Card (training data)
- Model Card → references Interface Card (deployment)
- Interface Card → may reference Agentic Card (if using agents)
- Agentic Card → references Model Cards (models the agent uses)

**Q: What if my organization doesn't use AI agents?**  
A: Agentic Cards are optional. If you're not deploying autonomous agents, you only need Model Cards, Dataset Cards, and Interface Cards.

**Q: Is MCML only for ML models, or can it document traditional software?**  
A: MCML is designed for AI/ML systems. For traditional software, use standard documentation practices (OpenAPI, README, etc.). However, Interface Cards can document any API.

**Q: How do I migrate existing documentation to MCML?**  
A: Use the MCML migration tools:
```bash
mcml migrate --from google-model-card --input existing_card.md --output model_card.yaml
```

**Q: What if I'm already using MLflow / Weights & Biases / other MLOps tools?**  
A: MCML integrates with existing tools. Use plugins to auto-generate MCML Cards from your MLOps metadata, then add governance-specific fields (intended use, limitations, etc.).

**Q: How often should Cards be updated?**  
A: 
- **Model Cards** — Update with each model version or when performance/fairness characteristics change
- **Dataset Cards** — Update when data sources, preprocessing, or quality metrics change
- **Interface Cards** — Update when API contracts, access control, or compliance requirements change
- **Agentic Cards** — Update when autonomy level, tools, or oversight rules change

**Q: Can MCML be used for open source models?**  
A: Yes! MCML is perfect for documenting open source models. Publish Model Cards and Dataset Cards alongside your model releases to provide transparency and enable responsible use.

**Q: How does MCML handle model versioning?**  
A: Each Card includes a `version` field (semantic versioning recommended: `1.0.0`, `1.1.0`, `2.0.0`). Cards can reference specific versions of other Cards via URIs like `dataset://customer_data/v2.3`.

**Q: What about models trained on proprietary data?**  
A: Dataset Cards can document data characteristics (biases, quality) without exposing proprietary details. Use `collection_method: "Proprietary customer data"` and document known biases/limitations without revealing specifics.

---

## Citation

If you use MCML in research or production, please cite:

```bibtex
@techreport{mcml2025,
  title={MCML: Machine-Readable Card Markup Language for AI Governance},
  author={MCML Working Group},
  year={2025},
  institution={AI Governance Standards Consortium},
  url={https://mcml.ai/spec/v1.0},
  note={Standard for unified, machine-readable AI documentation}
}
```

**For the two-layer architecture reference implementation:**
```bibtex
@misc{mcml_two_layer_2025,
  title={Two-Layer Architecture for AI Governance Traceability},
  author={[Your Organization]},
  year={2025},
  note={Patent pending. Reference implementation of MCML standard.},
  url={https://mcml.ai/reference-implementation}
}
```

---

## License

### MCML Specification
The MCML standard specification (schemas, documentation, compliance mappings) is released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

You are free to:
- Use MCML in commercial and non-commercial projects
- Modify and extend MCML schemas
- Create tools and implementations

You must:
- Give appropriate credit to MCML
- Indicate if changes were made

### Reference Implementation Code
The reference implementation code (two-layer architecture, SDKs, tools) is dual-licensed:

- **Open Source License**: MIT License (for non-commercial use and evaluation)
- **Commercial License**: Contact [licensing@mcml.ai](mailto:licensing@mcml.ai) for production use of patented two-layer architecture

### Patents
The two-layer architecture with foreign key relationships for AI governance is patent pending. Commercial use requires a license. Academic and non-profit use is permitted under the MIT License.

---

## Contact and Support

### General Inquiries
- 📧 **Email**: [info@mcml-standard.org](mailto:info@mcml-standard.org)
- 🌐 **Website**: [https://mcml-standard.org](https://mcml-standard.org)

### Technical Support
- 💬 **GitHub Discussions**: [github.com/mcml-standard.org/mcml/discussions](https://github.com/mcml-standard.org/mcml/discussions)
- 🐛 **Bug Reports**: [github.com/mcml-standard.org/mcml/issues](https://github.com/mcml-standard.org/mcml/issues)
- 📚 **Documentation**: [https://mcml-standard.org/docs](https://mcml-standard.org/docs)

### Standards Working Group
- 📝 **Proposals**: [github.com/mcml-standard.org/proposals](https://github.com/mcml-standard.org/proposals)
- 📅 **Meeting Schedule**: Monthly public calls (see [mcml-standard.org/meetings](https://mcml-standard.org/meetings))
- 👥 **Join the Working Group**: [mcml-standard.org/join](https://mcml-standard.org/join)

### Commercial Licensing (Reference Implementation)
- 💼 **Licensing**: [licensing@mcml-standard.org](mailto:licensing@mcml-standard.org)
- 🤝 **Enterprise Support**: [enterprise@mcml-standard.org](mailto:enterprise@mcml-standard.org)

### Social Media
- 🐦 **Twitter/X**: [@mcml-standard.org](https://twitter.com/mcml-standard)
- 💼 **LinkedIn**: [MCML Standard](https://linkedin.com/company/mcml-standard)
- 📺 **YouTube**: [MCML Tutorials](https://youtube.com/@mcml-standard)

---

## Acknowledgments

MCML builds on pioneering work by:

- **Google Research** — Model Cards for Model Reporting (Mitchell et al., 2019)
- **Microsoft Research** — Datasheets for Datasets (Gebru et al., 2018)
- **NIST** — AI Risk Management Framework
- **European Commission** — EU AI Act development
- **ISO/IEC JTC 1/SC 42** — AI standardization
- **Anthropic** — Model Context Protocol (MCP)
- **LangChain Community** — Agent framework governance patterns

We are grateful to the AI governance research community, open source contributors, and early adopters who shaped this standard.

---

## Star ⭐ This Repo

If MCML helps your AI governance, please **star this repository** to show support and help others discover the standard!

---

**MCML: From documentation to automation. Making AI governance machine-readable, compliant, and auditable.**

**Version 1.0 | January 2025**
