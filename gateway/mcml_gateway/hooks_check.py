# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""Check the intrinsic-signal extension point with a MOCK provider.

    python -m mcml_gateway.hooks_check

This is not a result about any real model. MCML treats models as black boxes
today; this only confirms that, when a Model Card declares a validated internal
signal and a provider is attached, the gateway routes it into the same
block / escalate / kill-switch logic and records it as evidence, and that
unvalidated signals are ignored.
"""
from __future__ import annotations

import sys

import anyio

from .scenarios import PATIENT, call, make_env, page_args

MODEL_CARD = {
    "model_name": "deterioration_risk_model",
    "version": "1.0.0",
    "intrinsic_telemetry": {
        "status": "validated",
        "access": "self_hosted_weights",
        "signals": [{
            "id": "confidence_divergence",
            "purpose": "stated confidence diverges from internal confidence",
            "method": "linear_probe",
            "layer": 18,
            "threshold": 0.8,
            "validation_evidence_ref": "MOCK: no real validation",
            "applies_to_tools": ["page_rapid_response"],
            "on_trigger": "activate_kill_switch",
        }],
    },
}


class MockProvider:
    def __init__(self, value: float):
        self.value = value

    def signals(self, tool, arguments, signal_ids):
        return {sid: self.value for sid in signal_ids}


async def run() -> list[tuple[str, bool]]:
    checks = []

    env = make_env()
    env.gateway.model_card, env.gateway.signal_provider = MODEL_CARD, MockProvider(0.95)
    env.gateway.grant_approval("A-H1", "page_rapid_response", "charge_nurse", PATIENT)
    r = await call(env.server, "page_rapid_response", page_args("A-H1"))
    rec = [x for x in env.gateway.ledger.records if x.get("rule") == "intrinsic_signal"]
    checks.append(("signal above threshold blocks an approved high-consequence call", r["decision"] == "BLOCK"))
    checks.append(("card's on_trigger action fires the kill switch", env.gateway.kill.active))
    checks.append(("signal recorded in the evidence chain", bool(rec) and rec[0]["intrinsic_signal"]["value"] == 0.95))

    env = make_env()
    env.gateway.model_card, env.gateway.signal_provider = MODEL_CARD, MockProvider(0.95)
    v = await call(env.server, "read_vitals", {"patient_ref": PATIENT})
    checks.append(("signal not consulted for tools outside applies_to_tools", v["decision"] == "ALLOW"))

    env = make_env()
    research = {**MODEL_CARD, "intrinsic_telemetry": {**MODEL_CARD["intrinsic_telemetry"], "status": "research"}}
    env.gateway.model_card, env.gateway.signal_provider = research, MockProvider(0.95)
    env.gateway.grant_approval("A-H2", "page_rapid_response", "charge_nurse", PATIENT)
    r = await call(env.server, "page_rapid_response", page_args("A-H2"))
    checks.append(("unvalidated ('research') signals never drive enforcement", r["decision"] == "ALLOW"))

    env = make_env()
    env.gateway.grant_approval("A-H3", "page_rapid_response", "charge_nurse", PATIENT)
    r = await call(env.server, "page_rapid_response", page_args("A-H3"))
    checks.append(("default black-box mode is unchanged", r["decision"] == "ALLOW"))
    return checks


def main() -> int:
    checks = anyio.run(run)
    for label, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {label}")
    print("\nExtension point only, with a mock provider. Not a result about any real model.")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
