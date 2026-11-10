#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""MCML reference validator (v1.1 draft).

Commands:
  validate <file>...                 Check card files against the MCML v1.1 JSON Schemas.
  compliance-check <dir> [--framework nist|eu-ai-act]
                                     Report which framework requirements have evidence in the cards.
  pre-deploy-check <dir> [--require-agent]
                                     Deployment gate: exits non-zero if required cards are missing,
                                     invalid, unlinked, or lack required safety evidence.

Cards are YAML or JSON files whose top-level key names the card type
(model_card, dataset_card, interface_card, agentic_governance_card).
Compliance mappings show where evidence exists; they do not establish legal compliance.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("Missing dependencies. Run: pip install -r requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema" / "v1.1"
CARD_TYPES = {
    "model_card": "model-card.schema.json",
    "dataset_card": "dataset-card.schema.json",
    "interface_card": "interface-card.schema.json",
    "agentic_governance_card": "agentic-governance-card.schema.json",
}
DEPRECATED = {"agentic_card": "agentic_governance_card"}


# ---------------------------------------------------------------- loading

def load_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    # Normalise YAML dates and other scalars to JSON types.
    return json.loads(json.dumps(data, default=str))


def card_type(doc) -> str | None:
    if not isinstance(doc, dict):
        return None
    for key in doc:
        if key in CARD_TYPES or key in DEPRECATED:
            return key
    return None


def schema_errors(doc: dict, ctype: str) -> list[str]:
    schema = json.loads((SCHEMA_DIR / CARD_TYPES[ctype]).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    return [f"{'.'.join(str(p) for p in e.path) or '(root)'}: {e.message}" for e in errors]


def collect(directory: Path) -> tuple[dict[str, list[tuple[Path, dict]]], list[str]]:
    cards: dict[str, list[tuple[Path, dict]]] = {t: [] for t in CARD_TYPES}
    problems: list[str] = []
    files = sorted(p for p in directory.rglob("*") if p.suffix in {".yaml", ".yml", ".json"})
    for path in files:
        try:
            doc = load_card(path)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{path}: cannot parse ({exc})")
            continue
        ctype = card_type(doc)
        if ctype is None:
            continue
        if ctype in DEPRECATED:
            problems.append(f"{path}: '{ctype}' is deprecated; rename the top-level key to '{DEPRECATED[ctype]}'")
            continue
        for err in schema_errors(doc, ctype):
            problems.append(f"{path}: {err}")
        cards[ctype].append((path, doc[ctype]))
    return cards, problems


# ---------------------------------------------------------------- references

def _norm_version(v) -> str:
    s = str(v)
    return s[1:] if s.lower().startswith("v") else s


def parse_ref(ref: str) -> tuple[str, str, str]:
    scheme, rest = ref.split("://", 1)
    rest = rest.split("#", 1)[0]
    name, _, version = rest.rpartition("/")
    return scheme, name, _norm_version(version)


def index(cards) -> dict[tuple[str, str, str], dict]:
    idx = {}
    for _, m in cards["model_card"]:
        idx[("model", m["model_name"], _norm_version(m["version"]))] = m
    for _, d in cards["dataset_card"]:
        idx[("dataset", d["dataset_name"], _norm_version(d["version"]))] = d
    return idx


def unresolved_refs(cards) -> list[str]:
    idx = index(cards)
    issues = []

    def check(path, field, ref):
        if not ref:
            return
        try:
            key = parse_ref(ref)
        except ValueError:
            issues.append(f"{path}: {field} '{ref}' is not a valid card reference")
            return
        if key[0] in {"model", "dataset"} and key not in idx:
            issues.append(f"{path}: {field} '{ref}' does not match any card in this directory")

    for path, m in cards["model_card"]:
        for field in ("training_dataset_ref", "validation_dataset_ref"):
            check(path, field, m.get(field))
    for path, i in cards["interface_card"]:
        check(path, "model_ref", i.get("model_ref"))
    for path, a in cards["agentic_governance_card"]:
        check(path, "model_ref", a.get("model_ref"))
        check(path, "human_oversight.model_card_ref", a.get("human_oversight", {}).get("model_card_ref"))
    return issues


# ---------------------------------------------------------------- compliance

def _first(cards, ctype) -> dict:
    return cards[ctype][0][1] if cards[ctype] else {}


def nist_rmf(cards) -> dict[str, bool]:
    m, d = _first(cards, "model_card"), _first(cards, "dataset_card")
    i, a = _first(cards, "interface_card"), _first(cards, "agentic_governance_card")
    agent_present = bool(cards["agentic_governance_card"])
    return {
        "GOVERN": bool(m.get("responsible_team") and d.get("data_owner")
                       and (not agent_present or a.get("identity", {}).get("owner"))),
        "MAP": bool(m.get("intended_use") and m.get("limitations") and m.get("failure_modes")
                    and (not agent_present or a.get("autonomy", {}).get("decision_authority"))),
        "MEASURE": bool(m.get("performance_metrics") and m.get("fairness_metrics")
                        and m.get("evaluation_evidence") and d.get("quality_metrics")
                        and d.get("known_biases")),
        "MANAGE": bool(i.get("logging_level") == "detailed" and m.get("monitoring_commitments")
                       and m.get("risk_acceptance") and (not agent_present or a.get("kill_switch"))),
    }


def eu_ai_act(cards) -> dict[str, bool]:
    m, d = _first(cards, "model_card"), _first(cards, "dataset_card")
    a = _first(cards, "agentic_governance_card")
    agent_present = bool(cards["agentic_governance_card"])
    evidence = m.get("evaluation_evidence", {})
    return {
        "Art. 6 risk classification": bool(m.get("risk_acceptance", {}).get("risk_category")),
        "Art. 11 technical documentation": all(cards[t] for t in ("model_card", "dataset_card", "interface_card")),
        "Art. 13 transparency": bool(m.get("intended_use") and m.get("limitations") and d.get("known_biases")),
        "Art. 14 human oversight": bool(m.get("human_oversight") and (not agent_present or (
            a.get("kill_switch") and a.get("human_oversight", {}).get("escalation_rules")))),
        "Art. 15 accuracy": bool(evidence.get("metrics") and all(x.get("passed") for x in evidence["metrics"])
                                 and d.get("quality_metrics")),
    }


FRAMEWORKS = {"nist": nist_rmf, "eu-ai-act": eu_ai_act}


# ---------------------------------------------------------------- deployment gate

def safety_gate(cards, require_agent: bool) -> list[str]:
    issues = []
    for ctype in ("model_card", "dataset_card", "interface_card"):
        if not cards[ctype]:
            issues.append(f"missing required {ctype}")
    if require_agent and not cards["agentic_governance_card"]:
        issues.append("missing required agentic_governance_card (--require-agent)")

    today = dt.date.today().isoformat()
    for path, m in cards["model_card"]:
        for field in ("failure_modes", "evaluation_evidence", "human_oversight",
                      "monitoring_commitments", "risk_acceptance"):
            if not m.get(field):
                issues.append(f"{path}: safety field '{field}' is missing")
        for metric in m.get("evaluation_evidence", {}).get("metrics", []):
            if not metric.get("passed"):
                issues.append(f"{path}: evaluation metric '{metric.get('metric')}' did not meet its threshold")
        risk = m.get("risk_acceptance", {})
        if risk.get("risk_category") == "unacceptable":
            issues.append(f"{path}: risk_category is 'unacceptable'; deployment is not permitted")
        if risk.get("review_due") and str(risk["review_due"]) < today:
            issues.append(f"{path}: risk acceptance review was due {risk['review_due']}")

    for path, a in cards["agentic_governance_card"]:
        if not a.get("enforcement", {}).get("audit_log", {}).get("tamper_evident"):
            issues.append(f"{path}: enforcement.audit_log.tamper_evident must be true")
        if not a.get("kill_switch", {}).get("tested"):
            issues.append(f"{path}: kill_switch has no recorded test date")
    return issues


# ---------------------------------------------------------------- CLI

def cmd_validate(args) -> int:
    failed = False
    for name in args.files:
        path = Path(name)
        doc = load_card(path)
        ctype = card_type(doc)
        if ctype is None:
            print(f"FAIL {path}: no recognised card type")
            failed = True
            continue
        if ctype in DEPRECATED:
            print(f"FAIL {path}: '{ctype}' is deprecated; use '{DEPRECATED[ctype]}'")
            failed = True
            continue
        errors = schema_errors(doc, ctype)
        print(f"{'FAIL' if errors else 'PASS'} {path} ({ctype})")
        for e in errors:
            print(f"     - {e}")
        failed |= bool(errors)
    return 1 if failed else 0


def cmd_compliance(args) -> int:
    cards, problems = collect(Path(args.directory))
    for p in problems:
        print(f"WARN {p}")
    results = FRAMEWORKS[args.framework](cards)
    for req, ok in results.items():
        print(f"{'PASS' if ok else 'MISSING'}  {req}")
    overall = all(results.values())
    print(f"\n{args.framework}: {'evidence present for all requirements' if overall else 'evidence incomplete'}")
    print("Note: this reports documentation evidence, not legal compliance.")
    return 0 if overall else 1


def cmd_predeploy(args) -> int:
    cards, problems = collect(Path(args.directory))
    issues = problems + unresolved_refs(cards) + safety_gate(cards, args.require_agent)
    if issues:
        print("DEPLOYMENT BLOCKED")
        for i in issues:
            print(f"  - {i}")
        return 1
    counts = ", ".join(f"{len(v)} {k}" for k, v in cards.items() if v)
    print(f"DEPLOYMENT ALLOWED ({counts})")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="mcml", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("validate", help="validate card files against the schemas")
    p.add_argument("files", nargs="+")
    p.set_defaults(func=cmd_validate)
    p = sub.add_parser("compliance-check", help="report framework evidence coverage")
    p.add_argument("directory")
    p.add_argument("--framework", choices=sorted(FRAMEWORKS), default="nist")
    p.set_defaults(func=cmd_compliance)
    p = sub.add_parser("pre-deploy-check", help="deployment gate; non-zero exit blocks deployment")
    p.add_argument("directory")
    p.add_argument("--require-agent", action="store_true")
    p.set_defaults(func=cmd_predeploy)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
