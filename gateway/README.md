# MCML Enforcement Gateway (prototype)

A reference prototype of the runtime layer described in the [MCML Runtime Safety specification](https://mcml-standard.org/docs/runtime-safety.html). It enforces a signed **Agentic Governance Card** on every MCP tool call, from outside the agent's runtime, and records linked, tamper-evident evidence.

> **Status: prototype.** Tested in a synthetic clinical environment (see [RESULTS.md](RESULTS.md)). Not for production use.

## What it does

The agent connects only to the gateway, which is an MCP server to the agent and an MCP client to the real tools. For every call, the gateway checks, in order:

1. **Kill switch.** If active, nothing goes through.
2. **Model provenance.** The serving host's signed attestation of the weight hash must be on the card's approved list. A mismatch can fire the kill switch.
3. **Authorization.** The tool must be declared in the card and must not be a forbidden action. Unknown tools are denied.
4. **Arguments.** They must match the tool's `argument_schema`. Extra or malformed arguments are blocked as security events.
5. **Human approval.** For tools that require it, the approval must exist, cover this tool and patient, not be withdrawn, and not be expired.
6. **Call limits.**

Allowed calls are forwarded with a **credential only the gateway holds**. The tool returns a **signed receipt**, which the gateway verifies against the arguments it sent. Every decision goes into a **hash-chained ledger**. Numeric **kill-switch triggers** from the card are evaluated after every event. When the switch fires, the gateway revokes its own tool credential, so it does not depend on the agent's cooperation.

`reconcile()` compares the tool's receipts with the ledger. Any receipt without a matching gateway decision means something reached the tool another way.

## Run the scenarios

```bash
pip install -r gateway/requirements.txt
cd gateway
python -m mcml_gateway scenarios        # writes RESULTS.md; exits non-zero on any failure
```

Seven scenarios: authorized call, approval withdrawn, kill switch, gateway bypass, model provenance injection, payload injection, and evidence integrity.

## Live demo with a real agent

`demo-serve` runs the gateway over stdio in front of the synthetic clinical tools, so any MCP client (for example Claude Desktop) can act as the agent. Operator commands run in a separate terminal, outside the agent's reach.

MCP client configuration:

```json
{
  "mcpServers": {
    "mcml-gateway": {
      "command": "python3",
      "args": ["-m", "mcml_gateway", "demo-serve", "--state", "/tmp/mcml-demo"],
      "env": { "PYTHONPATH": "/path/to/mcml-standard/gateway" }
    }
  }
}
```

Operator terminal:

```bash
cd gateway
python -m mcml_gateway approve A-100 --state /tmp/mcml-demo          # charge nurse approves a page
python -m mcml_gateway withdraw A-100 --state /tmp/mcml-demo         # ...and withdraws it
python -m mcml_gateway kill --state /tmp/mcml-demo --reason "stop"   # pull the kill switch
python -m mcml_gateway verify-log /tmp/mcml-demo/evidence.jsonl      # check the evidence chain
```

Suggested script: ask the agent to check vitals for `pt-000123` and page the rapid response team. It is blocked until you approve. Approve and it goes through. Withdraw and ask again: blocked. Pull the kill switch: everything stops. Then show `evidence.jsonl`.

## Layout

| File | Role |
|------|------|
| `mcml_gateway/core.py` | Policy engine: checks, approvals, kill switch, provenance, receipts, reconciliation |
| `mcml_gateway/mcp_front.py` | MCP server for the agent; MCP client to the tools |
| `mcml_gateway/card.py` | Load, sign and verify Agentic Governance Cards |
| `mcml_gateway/ledger.py` | Hash-chained evidence log and verification |
| `mcml_gateway/demo.py` | Synthetic clinical tool server and serving host |
| `mcml_gateway/scenarios.py` | Scenario harness and report |

## Limits

- Isolation is simulated with credentials. In production, network or host controls must also stop the agent reaching tools directly.
- Attestation is simulated. Real deployments need hardware- or platform-backed attestation.
- The kill switch blocks every call after activation. It does not abort a call that is already executing.
- It enforces declared limits only. An action the card permits can still cause harm.

## License

GPL-3.0-or-later, with commercial licenses available. See the repository [LICENSE](../LICENSE).
