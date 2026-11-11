---
title: "MCML Use Cases"
---

# MCML Use Cases

Each use case shows MCML cards driving runtime controls for AI agents, tested as automated scenarios. Together they show what it takes to make an agent's safety controls enforceable rather than documented: from the data a model was trained on, through the model and its interface, to every action the agent takes.

We publish the full roadmap openly. A use case is marked **Done** only when it is built and its results are reproducible from this repository.

## Roadmap

| ID | Use case | What it demonstrates | Cards involved | Status |
| --- | --- | --- | --- | --- |
| K | Kill switch in an MCP agentic workflow | Approvals, payload checks, bypass detection and an out-of-band kill switch | Agentic, Interface | **Done** (prototype) |
| M | MCP alone vs MCP with MCML | Which attacks succeed when MCP has no governance data, and how MCML closes each gap | All four | Planned |
| P | Performance and cost | Added latency, throughput and cost of enforcement, against the incident and audit costs it avoids | All four | Planned |
| A | Poisoned training data under an XGBoost sepsis model | Dataset and model integrity checks firing the kill switch, on public PhysioNet data | Dataset, Model, Interface | Planned |
| B | Backdoored LLM agent | Action enforcement holds even when the model is compromised; canary prompts expose the backdoor | All four | Planned |
| C | Patient consent revoked mid-workflow | An upstream consent change stops in-flight actions and flags affected data and models | Dataset, Model, Agentic | Planned |
| D | An agent changes a function of certified medical device software | An out-of-scope change suspends clinical use, opens an audit and rolls back | Model, Interface, Agentic | Planned |
| E | Upstream lab data changes | The input contract catches the change; outputs made since are flagged | Dataset, Interface, Model | Planned |

## Done

### K. Kill switch in an MCP agentic workflow

**Status:** prototype, synthetic clinical environment. 7 of 7 scenarios pass on every commit.

A clinical alert agent may page a rapid response team only after a charge nurse approves. The [MCML gateway](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/gateway) sits between the agent and its MCP tools and enforces the signed Agentic Governance Card on every call.

| Scenario | What is attempted | Result |
| --- | --- | --- |
| Authorized call | Page with a valid nurse approval | Forwarded; signed tool receipt verified |
| Approval withdrawn | Page after the nurse withdraws approval | Blocked; record shows the withdrawal |
| Kill switch | Operator stops the agent mid-workflow; a forbidden action trips a numeric trigger | Gateway revokes its own credentials; every later call refused |
| Gateway bypass | Agent calls the tool directly | Refused; with isolation misconfigured, reconciliation flags the bypass |
| Model provenance injection | Unapproved checkpoint swapped in | Attestation fails; kill switch fires |
| Payload injection | Extra recipient, malformed ID, forged credential | Blocked as security events |
| Evidence integrity | Log record edited; card altered after signing | Edit detected; altered card refused |

[Full results](https://mcml-standard.org/gateway/RESULTS.html) · [Runtime Safety specification](https://mcml-standard.org/docs/runtime-safety.html) · [Run it yourself](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/gateway)

**Limits:** synthetic environment; tool isolation and model attestation are simulated; not yet tested in production.

## Planned

### M. MCP alone vs MCP with MCML

MCP standardizes how agents connect to tools and authorize against them. It carries no governance data: nothing about which model is approved, what data trained it, whether a patient still consents, or whether software is still within its certification. We will run every attack twice, once with only MCP-level token checks and once with MCML enforcement, and publish which attacks succeed in each mode.

### P. Performance and cost

Enterprises need to know what enforcement costs. We will measure the latency MCML adds per call (p50, p95, p99), throughput per CPU core and across instances, and evidence storage per million calls, comparing MCP alone with MCP plus MCML on the same hardware. A cost model will set infrastructure cost against the incident investigation, audit and downtime costs that enforcement avoids. We will publish only measured numbers, with the hardware stated.

### A. Poisoned training data under an XGBoost sepsis model

An XGBoost model trained on the public [PhysioNet/CinC Challenge 2019 sepsis dataset](https://physionet.org/challenge/2019/) (CC BY 4.0). Attacks include injected or relabeled training rows, a planted backdoor that suppresses alerts, and a swapped model file. The Dataset and Model cards (data hash, signer, baseline statistics, canary probes, weight hash) must catch each one and fire the kill switch.

### B. Backdoored LLM agent

The agent's own language model is fine-tuned on poisoned data that plants a trigger phrase to page without approval. The gateway must block the action regardless, while canary prompts in the Dataset and Model cards expose the backdoor so the model is no longer trusted anywhere.

### C. Patient consent revoked mid-workflow

A patient withdraws consent while the agent is working on their case. The gateway must refuse further calls about that patient, void a pending approval, and flag the patient's records and the models trained on them, without stopping care for anyone else.

### D. An agent changes a function of certified medical device software

An automated agent changes an alert threshold or adds an input outside the change envelope recorded in the Model Card. MCML must mark the version as not authorized for clinical use, roll back, flag outputs produced since the change, and open an audit for the regulatory owner. MCML enforces the envelope the regulatory team declares; it does not decide what needs regulatory review.

### E. Upstream lab data changes

A lab system starts reporting a value in different units. The input contract in the Dataset and Interface cards must reject out-of-contract inputs, flag scores produced since the change, and hold alerts for a human.

**Want to pilot one of these with us, or attack the gateway?** Open an [issue](https://github.com/PLEYVERSE-AI/mcml-standard/issues) or contact [lanre@pleyverse.com](mailto:lanre@pleyverse.com).
