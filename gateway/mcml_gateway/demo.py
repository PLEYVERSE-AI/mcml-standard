# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""Synthetic clinical environment for the scenarios. Not a real clinical system.

- ClinicalTools: an upstream MCP server with read_vitals and page_rapid_response.
  It accepts calls only with the gateway's credential and signs a receipt for
  every call it executes. With require_credential=False it simulates a
  misconfigured tool that anyone can reach.
- ServingHost: the model-serving host, which attests the hash of the weights it
  is running.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import uuid

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from . import crypto
from .core import CREDENTIAL_ARG


class ClinicalTools:
    def __init__(self, credential: str, require_credential: bool = True):
        self.key = crypto.new_key()
        self.public_key = self.key.public_key()
        self._credential = credential
        self.require_credential = require_credential
        self.receipts: list[dict] = []
        self.access_log: list[dict] = []  # what a conventional tool log would hold
        self.pages_sent: list[dict] = []
        self.server = self._build()

    def _authorize(self, credential: str, tool: str):
        ok = hmac.compare_digest(credential or "", self._credential) if self._credential else False
        self.access_log.append({"ts": dt.datetime.now(dt.timezone.utc).isoformat(), "tool": tool,
                                "status": 200 if (ok or not self.require_credential) else 401})
        if self.require_credential and not ok:
            raise ToolError("401 unauthorized: tool accepts calls only from the MCML gateway")

    def _receipt(self, tool: str, args: dict, result: dict) -> dict:
        body = {"receipt_id": str(uuid.uuid4()), "tool": tool, "args_hash": crypto.digest(args),
                "result_hash": crypto.digest(result),
                "executed_at": dt.datetime.now(dt.timezone.utc).isoformat()}
        receipt = {**body, "signature": crypto.sign(self.key, body)}
        self.receipts.append(receipt)
        return receipt

    def _build(self) -> MCPServer:
        srv = MCPServer("clinical-tools (synthetic)")

        @srv.tool()
        def read_vitals(patient_ref: str, mcml_credential: str = "") -> dict:
            """Read the latest synthetic vital signs for a patient."""
            self._authorize(mcml_credential, "read_vitals")
            seed = int(hashlib.sha256(patient_ref.encode()).hexdigest()[:6], 16)
            result = {"patient_ref": patient_ref, "heart_rate": 90 + seed % 40,
                      "resp_rate": 18 + seed % 10, "systolic_bp": 95 + seed % 30}
            return {"result": result, "receipt": self._receipt("read_vitals", {"patient_ref": patient_ref}, result)}

        @srv.tool()
        def page_rapid_response(patient_ref: str, approval_id: str, message: str, mcml_credential: str = "") -> dict:
            """Page the rapid response team about a patient."""
            self._authorize(mcml_credential, "page_rapid_response")
            args = {"patient_ref": patient_ref, "approval_id": approval_id, "message": message}
            self.pages_sent.append(args)
            result = {"paged": True, "patient_ref": patient_ref}
            return {"result": result, "receipt": self._receipt("page_rapid_response", args, result)}

        return srv


class ServingHost:
    def __init__(self, model_ref: str, weights: bytes):
        self.key = crypto.new_key()
        self.public_key = self.key.public_key()
        self.model_ref = model_ref
        self.weights = weights

    def swap_weights(self, weights: bytes):
        """Simulates an unapproved checkpoint being loaded without updating the card."""
        self.weights = weights

    def attest(self) -> dict:
        body = {"model_ref": self.model_ref, "weights_hash": crypto.sha256(self.weights),
                "attested_at": dt.datetime.now(dt.timezone.utc).isoformat()}
        return {**body, "signature": crypto.sign(self.key, body)}
