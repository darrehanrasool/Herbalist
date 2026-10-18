"""Tiny demo login for scientists. Replace with SSO later. Not production-grade."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

USERS = Path(__file__).with_name("users.json")


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def seed():
    if USERS.exists():
        return
    USERS.write_text(
        json.dumps(
            {
                "scientist": {"password_sha256": _hash("herbalist"), "role": "scientist"},
                "farmer": {"password_sha256": _hash("herbalist"), "role": "farmer"},
            },
            indent=2,
        )
    )


def verify(username: str, password: str) -> dict | None:
    seed()
    data = json.loads(USERS.read_text())
    rec = data.get(username)
    if rec and rec["password_sha256"] == _hash(password):
        return {"username": username, "role": rec["role"]}
    return None
