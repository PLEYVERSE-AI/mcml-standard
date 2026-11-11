# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""MCML gateway command line.

  python -m mcml_gateway scenarios               run the safety scenarios and write RESULTS.md
  python -m mcml_gateway demo-serve --state DIR  run the gateway over stdio for a real MCP agent
                                                 (synthetic clinical tools, for live demos)
  python -m mcml_gateway approve ID --state DIR [--role charge_nurse] [--patient pt-000123]
  python -m mcml_gateway withdraw ID --state DIR [--role charge_nurse]
  python -m mcml_gateway kill --state DIR [--role charge_nurse] [--reason TEXT]
  python -m mcml_gateway verify-log FILE         check the evidence log's hash chain

In demo-serve mode the operator commands write to the state directory, and the
gateway picks them up before every tool call. The agent cannot reach them.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import anyio


def _control(state: Path) -> Path:
    state.mkdir(parents=True, exist_ok=True)
    return state / "control.json"


def _read_control(state: Path) -> dict:
    p = _control(state)
    return json.loads(p.read_text()) if p.exists() else {"approvals": {}, "withdrawn": {}, "kill": None}


def _write_control(state: Path, data: dict):
    _control(state).write_text(json.dumps(data, indent=2))


def cmd_approve(a):
    c = _read_control(Path(a.state))
    c["approvals"][a.id] = {"tool": "page_rapid_response", "role": a.role, "patient_ref": a.patient}
    _write_control(Path(a.state), c)
    print(f"approval {a.id} granted by {a.role} for {a.patient}")


def cmd_withdraw(a):
    c = _read_control(Path(a.state))
    c["withdrawn"][a.id] = a.role
    _write_control(Path(a.state), c)
    print(f"approval {a.id} withdrawn by {a.role}")


def cmd_kill(a):
    c = _read_control(Path(a.state))
    c["kill"] = {"role": a.role, "reason": a.reason}
    _write_control(Path(a.state), c)
    print(f"kill switch requested by {a.role}: {a.reason}")


def cmd_verify_log(a):
    from .ledger import verify_file
    ok, msg = verify_file(a.file)
    print(("OK  " if ok else "FAIL ") + msg)
    return 0 if ok else 1


def cmd_demo_serve(a):
    from mcp.server.stdio import stdio_server

    from .ledger import Ledger
    from .mcp_front import build_server
    from .scenarios import make_env

    state = Path(a.state)
    state.mkdir(parents=True, exist_ok=True)
    env = make_env()
    gw = env.gateway
    gw.ledger = Ledger(state / "evidence.jsonl")
    gw.ledger.append(gw._base("gateway_started", detail={"mode": "demo-serve (synthetic tools)"}))
    applied = {"approvals": set(), "withdrawn": set(), "kill": False}

    def sync():
        c = _read_control(state)
        for aid, spec in c.get("approvals", {}).items():
            if aid not in applied["approvals"]:
                gw.grant_approval(aid, spec["tool"], spec["role"], spec.get("patient_ref"))
                applied["approvals"].add(aid)
        for aid, role in c.get("withdrawn", {}).items():
            if aid not in applied["withdrawn"]:
                gw.withdraw_approval(aid, role)
                applied["withdrawn"].add(aid)
        if c.get("kill") and not applied["kill"]:
            gw.activate_kill_switch(c["kill"].get("reason", "manual"), by_role=c["kill"].get("role"))
            applied["kill"] = True

    original = gw.handle

    async def handle(tool, arguments):
        sync()
        return await original(tool, arguments)

    gw.handle = handle
    server = build_server(gw)

    async def run():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    anyio.run(run)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="mcml_gateway", description="MCML enforcement gateway (prototype)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scenarios", add_help=False)
    p = sub.add_parser("demo-serve"); p.add_argument("--state", required=True); p.set_defaults(func=cmd_demo_serve)
    p = sub.add_parser("approve"); p.add_argument("id"); p.add_argument("--state", required=True)
    p.add_argument("--role", default="charge_nurse"); p.add_argument("--patient", default="pt-000123")
    p.set_defaults(func=cmd_approve)
    p = sub.add_parser("withdraw"); p.add_argument("id"); p.add_argument("--state", required=True)
    p.add_argument("--role", default="charge_nurse"); p.set_defaults(func=cmd_withdraw)
    p = sub.add_parser("kill"); p.add_argument("--state", required=True)
    p.add_argument("--role", default="charge_nurse"); p.add_argument("--reason", default="manual activation")
    p.set_defaults(func=cmd_kill)
    p = sub.add_parser("verify-log"); p.add_argument("file"); p.set_defaults(func=cmd_verify_log)

    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "scenarios":
        from .scenarios import main as scenarios_main
        return scenarios_main(argv[1:])
    a = ap.parse_args(argv)
    return a.func(a) or 0


if __name__ == "__main__":
    sys.exit(main())
