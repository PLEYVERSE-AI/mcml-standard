# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""Tamper-evident, hash-chained evidence log.

Each record stores the hash of the previous record, so editing, deleting or
reordering any record breaks every hash after it. `verify` recomputes the chain.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import crypto

GENESIS = "sha256:" + "0" * 64


class Ledger:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else None
        self.records: list[dict[str, Any]] = []
        if self.path and self.path.exists():
            self.records = [json.loads(line) for line in self.path.read_text().splitlines() if line]

    @property
    def head(self) -> str:
        return self.records[-1]["record_hash"] if self.records else GENESIS

    def append(self, record: dict[str, Any]) -> dict[str, Any]:
        body = {"seq": len(self.records), "prev_hash": self.head, **record}
        body["record_hash"] = crypto.digest(body)
        self.records.append(body)
        if self.path:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(body, sort_keys=True) + "\n")
        return body


def verify(records: list[dict[str, Any]]) -> tuple[bool, str]:
    prev = GENESIS
    for i, rec in enumerate(records):
        body = {k: v for k, v in rec.items() if k != "record_hash"}
        if rec.get("seq") != i:
            return False, f"record {i}: sequence number is {rec.get('seq')} (record removed or reordered)"
        if rec.get("prev_hash") != prev:
            return False, f"record {i}: does not link to the previous record"
        if crypto.digest(body) != rec.get("record_hash"):
            return False, f"record {i}: contents were altered"
        prev = rec["record_hash"]
    return True, f"{len(records)} records, chain intact"


def verify_file(path: str | Path) -> tuple[bool, str]:
    lines = Path(path).read_text().splitlines()
    return verify([json.loads(line) for line in lines if line])
