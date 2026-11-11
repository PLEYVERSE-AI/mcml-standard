# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Olanrewaju Ogunkunle. Commercial licenses available: lanre@pleyverse.com
"""Canonical hashing and Ed25519 signing helpers."""
from __future__ import annotations

import base64
import hashlib
import json
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def canonical(obj: Any) -> bytes:
    """Deterministic JSON encoding used for every digest and signature."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def digest(obj: Any) -> str:
    return sha256(canonical(obj))


def new_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.generate()


def sign(key: Ed25519PrivateKey, obj: Any) -> str:
    return base64.b64encode(key.sign(canonical(obj))).decode()


def verify(pub: Ed25519PublicKey, obj: Any, signature: str) -> bool:
    try:
        pub.verify(base64.b64decode(signature), canonical(obj))
        return True
    except (InvalidSignature, ValueError):
        return False
