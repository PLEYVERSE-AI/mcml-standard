# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""Loading, signing and verifying Agentic Governance Cards."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import yaml
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from . import crypto


class CardError(Exception):
    """The card cannot be enforced (missing, unsigned or altered)."""


def load(path: str | Path) -> dict[str, Any]:
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    doc = json.loads(json.dumps(doc, default=str))  # normalise YAML dates
    if "agentic_governance_card" not in doc:
        raise CardError(f"{path}: not an Agentic Governance Card")
    return doc["agentic_governance_card"]


def _unsigned(card: dict) -> dict:
    body = copy.deepcopy(card)
    body.pop("card_signature", None)
    return body


def card_digest(card: dict) -> str:
    """Digest of everything except the signature block."""
    return crypto.digest(_unsigned(card))


def sign_card(card: dict, key: Ed25519PrivateKey, signed_by: str, signed_at: str) -> dict:
    signed = copy.deepcopy(card)
    d = card_digest(card)
    signed["card_signature"] = {
        "algorithm": "ed25519",
        "value": crypto.sign(key, {"card_digest": d}),
        "signed_by": signed_by,
        "signed_at": signed_at,
        "card_digest": d,
    }
    return signed


def verify_card(card: dict, pub: Ed25519PublicKey) -> str:
    """Return the card digest if the signature is valid, else raise CardError."""
    sig = card.get("card_signature")
    if not sig:
        raise CardError("card is unsigned; the gateway only enforces signed cards")
    d = card_digest(card)
    if sig.get("card_digest") != d:
        raise CardError("card was changed after it was signed (digest mismatch)")
    if not crypto.verify(pub, {"card_digest": d}, sig.get("value", "")):
        raise CardError("card signature is invalid")
    return d
