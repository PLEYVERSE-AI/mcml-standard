# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""MCP adapter: the gateway is an MCP server to the agent and an MCP client to the tools.

The agent connects only to the gateway. Every tools/call goes through
Gateway.handle(); allowed calls are forwarded to the upstream MCP server with a
credential that only the gateway holds.
"""
from __future__ import annotations

import json
from typing import Any

from mcp import Client, types
from mcp.server.lowlevel import Server

from .core import CREDENTIAL_ARG, Gateway, UpstreamRefused


class MCPUpstream:
    """Forward calls to an upstream MCP server (an MCPServer object, a URL, or stdio parameters)."""

    def __init__(self, target: Any):
        self.target = target

    async def call(self, tool: str, arguments: dict, credential: str) -> dict:
        async with Client(self.target) as client:
            res = await client.call_tool(tool, {**arguments, CREDENTIAL_ARG: credential})
        text = "".join(getattr(c, "text", "") for c in res.content)
        if res.is_error:
            raise UpstreamRefused(text)
        return json.loads(text)


def build_server(gateway: Gateway, name: str = "mcml-gateway") -> Server:
    async def on_list_tools(ctx, params) -> types.ListToolsResult:
        tools = []
        for tname, spec in gateway.tools.items():
            schema = spec.get("argument_schema") or {"type": "object"}
            note = " Requires human approval (pass approval_id)." if spec.get("requires_human_approval") else ""
            tools.append(types.Tool(name=tname, description=f"Governed by MCML card {gateway.card_digest[:19]}.{note}",
                                    input_schema=schema))
        return types.ListToolsResult(tools=tools)

    async def on_call_tool(ctx, params: types.CallToolRequestParams) -> types.CallToolResult:
        decision = await gateway.handle(params.name, params.arguments or {})
        payload = ({"decision": "ALLOW", "result": decision.result, "evidence_id": decision.record["record_hash"]}
                   if decision.allowed else
                   {"decision": "BLOCK", "reason": decision.reason, "evidence_id": decision.record["record_hash"]})
        return types.CallToolResult(content=[types.TextContent(type="text", text=json.dumps(payload))],
                                    is_error=not decision.allowed)

    return Server(name, on_list_tools=on_list_tools, on_call_tool=on_call_tool)
