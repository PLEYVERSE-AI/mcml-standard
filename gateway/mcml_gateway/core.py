# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""MCML enforcement gateway core (prototype).

Enforces a signed Agentic Governance Card on every tool call, from outside the
agent's runtime. Transport-agnostic: the MCP adapter lives in mcp_front.py.

Checks, in order, for every call:
  1. kill switch not active
  2. model provenance: the serving host's attested weight hash is approved
  3. tool is declared in the card and not a forbidden action
  4. arguments match the tool's argument_schema
  5. human approval is valid (exists, matches, not withdrawn, not expired)
  6. per-tool call limits
then forwards with a credential only the gateway holds, verifies the tool's
signed receipt, and records everything in a hash-chained ledger. Numeric
kill-switch triggers are evaluated after every event.
"""
from __future__ import annotations

import datetime as dt
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator

from . import card as cardmod
from . import crypto
from .ledger import Ledger

Clock = Callable[[], dt.datetime]
INTERNAL_PREFIXES = ("_mcml", "mcml_")  # reserved for the gateway; stripped from agent input
CREDENTIAL_ARG = "mcml_credential"


def _internal(key: str) -> bool:
    return key.startswith(INTERNAL_PREFIXES)


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_duration(text: str | None) -> dt.timedelta | None:
    if not text:
        return None
    m = re.fullmatch(r"P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?", text)
    if not m:
        raise ValueError(f"unsupported ISO 8601 duration: {text}")
    d, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return dt.timedelta(days=d, hours=h, minutes=mi, seconds=s)


class Upstream(Protocol):
    async def call(self, tool: str, arguments: dict, credential: str) -> dict: ...


class Attestor(Protocol):
    def attest(self) -> dict: ...


class UpstreamRefused(Exception):
    pass


@dataclass
class Approval:
    approval_id: str
    tool: str
    patient_ref: str | None
    approver_role: str
    granted_at: dt.datetime
    withdrawn_at: dt.datetime | None = None


@dataclass
class Decision:
    allowed: bool
    reason: str
    record: dict
    result: Any = None


@dataclass
class KillSwitch:
    active: bool = False
    activated_at: str | None = None
    trigger: str | None = None


@dataclass
class Gateway:
    card: dict
    card_public_key: Ed25519PublicKey
    upstream: Upstream
    upstream_credential: str
    tool_public_key: Ed25519PublicKey
    attestor: Attestor | None = None
    host_public_key: Ed25519PublicKey | None = None
    ledger: Ledger = field(default_factory=Ledger)
    clock: Clock = utcnow
    origin_user: str = "unknown"

    def __post_init__(self):
        # Refuse to start on an unsigned or altered card.
        self.card_digest = cardmod.verify_card(self.card, self.card_public_key)
        auth = self.card.get("authorization", {})
        self.tools = {t["name"]: t for t in auth.get("tools", [])}
        self.forbidden = set(auth.get("forbidden_actions", []))
        self.unknown_tool_policy = auth.get("unknown_tool_policy", "deny")
        self.schemas = {n: Draft202012Validator(t["argument_schema"])
                        for n, t in self.tools.items() if t.get("argument_schema")}
        ks = self.card.get("kill_switch", {})
        self.triggers = ks.get("numeric_triggers", [])
        self.manual_roles = set(ks.get("manual_activation", {}).get("authorized_roles", []))
        self.kill_actions = ks.get("enforcement_actions", [])
        self.provenance = self.card.get("provenance_verification")
        self.kill = KillSwitch()
        self.approvals: dict[str, Approval] = {}
        self.calls_per_tool: dict[str, int] = defaultdict(int)
        self.events: dict[str, deque] = defaultdict(deque)  # metric -> timestamps
        self.ledger.append(self._base("gateway_started", detail={
            "card_signed_by": self.card["card_signature"].get("signed_by"),
            "enforcement_point": self.card.get("enforcement", {}).get("enforcement_point")}))

    # ------------------------------------------------------------ records

    def _now(self) -> dt.datetime:
        return self.clock()

    def _base(self, event: str, **extra) -> dict:
        return {
            "ts": self._now().isoformat(),
            "event": event,
            "agent_id": self.card.get("identity", {}).get("agent_id"),
            "agent_version": self.card.get("agent_version"),
            "card_digest": self.card_digest,
            "origin_user": self.origin_user,
            "kill_switch_active": self.kill.active,
            **extra,
        }

    # ------------------------------------------------------------ approvals (human side)

    def grant_approval(self, approval_id: str, tool: str, approver_role: str, patient_ref: str | None = None):
        self.approvals[approval_id] = Approval(approval_id, tool, patient_ref, approver_role, self._now())
        self.ledger.append(self._base("approval_granted", approval_id=approval_id, tool=tool,
                                      patient_ref=patient_ref, approver_role=approver_role))

    def withdraw_approval(self, approval_id: str, by_role: str):
        appr = self.approvals.get(approval_id)
        if appr and not appr.withdrawn_at:
            appr.withdrawn_at = self._now()
            self.ledger.append(self._base("approval_withdrawn", approval_id=approval_id, by_role=by_role))

    # ------------------------------------------------------------ kill switch

    def activate_kill_switch(self, trigger: str, by_role: str | None = None) -> bool:
        if by_role is not None and by_role not in self.manual_roles:
            self.ledger.append(self._base("kill_switch_refused", by_role=by_role,
                                          reason="role not authorized for manual activation"))
            return False
        if self.kill.active:
            return True
        self.kill = KillSwitch(True, self._now().isoformat(), trigger)
        # Out-of-band: the gateway acts without the agent's participation.
        if "revoke_credentials" in self.kill_actions:
            self.upstream_credential = ""
        self.ledger.append(self._base("kill_switch_activated", trigger=trigger, by_role=by_role,
                                      actions=self.kill_actions))
        return True

    def _record_metric(self, metric: str):
        self.events[metric].append(self._now())
        self._evaluate_triggers()

    def _evaluate_triggers(self):
        now = self._now()
        for t in self.triggers:
            window = parse_duration(t.get("window"))
            stamps = self.events.get(t["metric"], deque())
            while window and stamps and now - stamps[0] > window:
                stamps.popleft()
            value = len(stamps)
            op, thr = t["operator"], t["threshold"]
            hit = {">": value > thr, ">=": value >= thr, "<": value < thr,
                   "<=": value <= thr, "==": value == thr}[op]
            if hit and not self.kill.active:
                self.activate_kill_switch(f"{t['metric']} {op} {thr} (observed {value})")

    # ------------------------------------------------------------ provenance

    def _check_provenance(self) -> tuple[bool, str, str | None]:
        if not self.provenance:
            return True, "no provenance policy", None
        if not (self.attestor and self.host_public_key):
            return False, "no attestation available from the serving host", None
        att = self.attestor.attest()
        body = {k: v for k, v in att.items() if k != "signature"}
        if not crypto.verify(self.host_public_key, body, att.get("signature", "")):
            return False, "serving host attestation signature is invalid", att.get("weights_hash")
        if att.get("weights_hash") not in self.provenance.get("allowed_model_hashes", []):
            return False, "attested model hash is not on the approved list", att.get("weights_hash")
        return True, "attested model hash approved", att.get("weights_hash")

    # ------------------------------------------------------------ the decision

    async def handle(self, tool: str, arguments: dict | None) -> Decision:
        args = {k: v for k, v in (arguments or {}).items()}
        args_hash = crypto.digest({k: v for k, v in args.items() if not _internal(k)})
        approval_id = args.get("approval_id")

        def block(rule: str, reason: str, metrics=(), security=False, **extra) -> Decision:
            rec = self.ledger.append(self._base(
                "tool_call", tool=tool, args_hash=args_hash, decision="BLOCK", rule=rule,
                reason=reason, approval_id=approval_id, security_event=security, **extra))
            for m in metrics:
                self._record_metric(m)
            return Decision(False, reason, rec)

        # 1. kill switch
        if self.kill.active:
            return block("kill_switch", f"kill switch active since {self.kill.activated_at} ({self.kill.trigger})")

        # 2. provenance
        ok, why, attested = self._check_provenance()
        if not ok:
            action = (self.provenance or {}).get("on_mismatch", "block_and_escalate")
            dec = block("provenance_verification", why, security=True, attested_model_hash=attested)
            if action == "activate_kill_switch":
                self.activate_kill_switch(f"provenance: {why}")
            return dec

        # 3. declared tool, not forbidden
        if tool in self.forbidden or tool not in self.tools:
            kind = "forbidden action" if tool in self.forbidden else "tool not declared in card"
            return block("authorization", f"{kind}: {tool}", security=True,
                         metrics=("unauthorized_scope_attempts", "blocked_calls"), attested_model_hash=attested)

        # 4. argument schema
        validator = self.schemas.get(tool)
        if validator:
            errors = [e.message for e in validator.iter_errors(args)]
            if errors:
                return block("argument_schema", "arguments rejected: " + "; ".join(errors[:3]),
                             security=True, metrics=("blocked_calls",), attested_model_hash=attested)

        spec = self.tools[tool]
        # 5. human approval
        approval_state = None
        if spec.get("requires_human_approval"):
            appr = self.approvals.get(approval_id or "")
            ttl = parse_duration(spec.get("permission_ttl"))
            if not appr:
                return block("human_approval", "no valid approval for this call", metrics=("blocked_calls",),
                             attested_model_hash=attested)
            if appr.withdrawn_at:
                return block("human_approval", f"approval {approval_id} was withdrawn at {appr.withdrawn_at.isoformat()}",
                             metrics=("blocked_calls",), approval_state="withdrawn", attested_model_hash=attested)
            if appr.tool != tool or (appr.patient_ref and appr.patient_ref != args.get("patient_ref")):
                return block("human_approval", "approval does not cover this tool or patient",
                             metrics=("blocked_calls",), approval_state="mismatch", attested_model_hash=attested)
            if ttl and self._now() - appr.granted_at > ttl:
                return block("human_approval", "approval expired", metrics=("blocked_calls",),
                             approval_state="expired", attested_model_hash=attested)
            approval_state = {"state": "valid", "approver_role": appr.approver_role,
                              "granted_at": appr.granted_at.isoformat()}

        # 6. call limits
        limit = spec.get("max_calls_per_application")
        if limit is not None and self.calls_per_tool[tool] >= limit:
            return block("call_limit", f"{tool} limited to {limit} call(s)", metrics=("blocked_calls",),
                         attested_model_hash=attested)

        # Forward with the gateway-held credential; the agent never sees it.
        forwarded = {k: v for k, v in args.items() if not _internal(k)}
        try:
            out = await self.upstream.call(tool, forwarded, self.upstream_credential)
        except UpstreamRefused as exc:
            return block("upstream", f"tool refused the call: {exc}", attested_model_hash=attested)

        receipt = out.get("receipt") or {}
        rbody = {k: v for k, v in receipt.items() if k != "signature"}
        receipt_ok = (crypto.verify(self.tool_public_key, rbody, receipt.get("signature", ""))
                      and receipt.get("args_hash") == crypto.digest(forwarded))
        self.calls_per_tool[tool] += 1
        rec = self.ledger.append(self._base(
            "tool_call", tool=tool, args_hash=args_hash, decision="ALLOW", rule="all checks passed",
            reason="forwarded", approval_id=approval_id, approval=approval_state,
            attested_model_hash=attested, tool_receipt=receipt, receipt_verified=receipt_ok))
        if tool == "page_rapid_response":
            self._record_metric("alerts_per_hour")
        return Decision(True, "forwarded", rec, out.get("result"))


def reconcile(ledger_records: list[dict], tool_receipts: list[dict]) -> list[dict]:
    """Receipts the tool issued that have no matching ALLOW decision in the ledger.

    A non-empty result means something reached the tool without going through
    the gateway."""
    allowed = {r["tool_receipt"]["receipt_id"] for r in ledger_records
               if r.get("decision") == "ALLOW" and r.get("tool_receipt")}
    return [rc for rc in tool_receipts if rc["receipt_id"] not in allowed]
