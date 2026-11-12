---
title: "Our Approach: Governing AI from the Outside, Ready for the Inside"
---

# Our approach

## Governing AI from the outside, ready for the inside

MCML governs AI systems at their boundaries today, treating the model as a black box. The standard and the gateway are designed so that, as interpretability research matures, validated signals from inside the model can feed the same controls without redesigning either.

---

## The black-box gap

Almost every AI governance framework, standard and tool today (NIST AI RMF, ISO/IEC 42001, EU AI Act conformity assessment, commercial guardrails) governs the model from the outside: its training data, its inputs, its outputs and the actions it takes. The internal computation is left alone, for three practical reasons:

- **Access.** Most organizations use models through an API or a hosted inference server. They control prompts, retrieved context, tool calls and outputs, but they cannot read a model's internal activations.
- **Certifiability.** Mechanistic interpretability is making real progress in finding human-understandable features and circuits inside models, but its results are not yet the kind of evidence an auditor or regulator can certify against.
- **Cost.** Monitoring a large model's internal states on every request takes compute and memory that most production latency budgets cannot absorb today.

So governance has settled on the outside. That is a reasonable choice, but it leaves a blind spot.

## Two kinds of governance

| | Extrinsic: governing the system around the model | Intrinsic: governing what happens inside the model |
| --- | --- | --- |
| **What it controls** | Data provenance, inputs and context, tool calls, outputs, audit records | Internal features, activations, the computations behind a decision |
| **Typical mechanisms** | Policy gateways, approvals, kill switches, provenance checks, audit trails | Probes, sparse autoencoder features, activation analysis, steering |
| **Strengths** | Works with any model; deterministic; auditable with today's compliance methods | Could detect problems that never show up in outputs |
| **Limits today** | Sees only what the model does, not why | Research-stage; needs access to the weights; not yet standardized or certifiable |

## The blind spot of black-box governance

When governance only observes behavior, three things stay hidden:

- **Misleading self-reports.** An agent's explanation of why it took an action is more generated text, not a view of the computation that produced the action.
- **Behavior that looks compliant.** A model could produce outputs that pass every outside check while its internal state reflects something else.
- **Unknown routes around filters.** Output filters catch the patterns they were written for, and miss new ones.

Extrinsic enforcement does not solve these. What it does is make sure that, **whatever the model intends, it cannot take an action outside its approved limits**, and that every action is traceable. That is why we build it first.

---

## MCML's three layers

### 1. Zero-trust MCP enforcement gateway

The agent's tool calls go through a gateway outside its runtime. The gateway checks each call against the agent's signed Agentic Governance Card (allowed tools, argument schemas, human approvals, limits) and holds the tool credentials, so the agent cannot go around it. An out-of-band kill switch revokes access without the agent's cooperation, and targeted containment stops only what an upstream change affects.

**Status:** prototype. 7 of 7 attack scenarios pass in a synthetic clinical workflow. [Results](https://mcml-standard.org/gateway/RESULTS.html)

### 2. Provenance and model telemetry

**Today, outside the black box:** the serving host attests the hash of the weights it is running, and the gateway checks it against the Model Card's approved list. A swapped or tampered model fires the kill switch.

**Designed for, inside the black box:** the Model Card has a reserved `intrinsic_telemetry` field. It can declare internal signals, such as a probe for divergence between what a model states and its internal confidence, together with the layer read, the threshold, the validation evidence and which high-consequence actions it applies to. The gateway has a matching extension point: signals feed the same block, escalate and kill-switch logic, and are recorded as evidence.

**Status:** provenance attestation is a prototype (simulated attestation). Intrinsic signals are **designed for, not used.** A mock-provider check confirms the hook works and that unvalidated signals are ignored.

### 3. Verifiable governance chain

Every policy decision, approval, intervention and tool execution produces a record in a hash-chained log, linked to the agent version, the signed card and the tool's own signed receipt. Editing any record breaks the chain. Cards themselves are machine-readable MCML documents with published JSON Schemas.

**Status:** prototype ledger and receipts; schemas published.

---

## Defense in depth

No single control secures an autonomous agent. Prompt filters can be bypassed through indirect injection. Behavioral evaluations can miss latent deception and evaluation awareness. Inspecting weights is too slow and noisy to be the only gate. Safety comes from layers that do not depend on the AI being right.

A November 2026 survey of the field, *Understanding AI from the Inside: The State of Mechanistic Interpretability for AI Safety* (Barez, Bengio, Biderman et al., [arXiv:2611.08438](https://arxiv.org/abs/2611.08438)), reaches the same conclusion for interpretability: it is one component of a layered safety strategy, alongside behavioral evaluation and other safeguards, not a standalone guarantee. MCML is built that way:

| Layer | Where it lives in MCML | Status |
| --- | --- | --- |
| Behavioral evaluation | Model Card evaluation thresholds; `pre-deploy-check` blocks deployment when evaluations miss them | Available |
| Runtime enforcement | Gateway: tool and argument checks, human approval, call limits, provenance attestation, kill switch | Prototype |
| Interpretability signals | Reserved `intrinsic_telemetry` field and `SignalProvider` hook; only validated signals may enforce | Designed for, not used |
| Accountability across every layer | Signed tool receipts, hash-chained ledger, reconciliation to detect bypass | Prototype |

**Deterministic enforcement today. White-box signals tomorrow. Accountable AI throughout.** When interpretability signals mature, they are added as another layer. They never replace the others.

---

## When we would turn on intrinsic signals

We would let an internal signal drive enforcement only when all of these hold:

1. **Access:** the model's weights are self-hosted, so activations can be read.
2. **Validation:** the signal has been evaluated on held-out data, with its detection rate and false-positive rate published and referenced from the Model Card.
3. **Scope:** it applies only to declared high-consequence actions, not every request.
4. **Cost:** its added latency has been measured (see use case P) and fits the deployment's budget.
5. **Fallback:** extrinsic enforcement stays in place regardless. An internal signal can add a reason to stop; it never removes one.

## What we do not claim

- MCML does not read model internals today.
- Probe-based detection of deception or hidden goals is an open research question, not a solved control.
- Extrinsic enforcement constrains what an agent can do, not what it is trying to do.

[Runtime Safety specification](https://mcml-standard.org/docs/runtime-safety.html) · [Use cases](https://mcml-standard.org/docs/use-cases.html) · [Gateway source](https://github.com/PLEYVERSE-AI/mcml-standard/tree/main/gateway)
