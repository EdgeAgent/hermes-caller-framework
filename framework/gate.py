"""Approval gate — IMMUTABLE CORE. Never bypassed by any other module.

Dangerous actions (send, call, charge, close, delete) are BLOCKED unless
an exact approval exists for that exact payload. Approval is granted only
by `approve --confirm <packet_id>` after the packet/message is shown.
There is no auto-send, auto-dial, auto-charge, or auto-close path.
"""
from __future__ import annotations
import hashlib, json

DANGEROUS = {"send", "call", "charge", "close", "delete"}

def payload_hash(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]

def check(state: dict, action: str, payload) -> dict:
    if action not in DANGEROUS:
        return {"allowed": True, "reason": "not a dangerous action"}
    h = payload_hash(payload)
    if h in state.get("approvals", []):
        return {"allowed": True, "reason": "exact approval on file", "hash": h}
    state.setdefault("blocked_events", []).append({"action": action, "hash": h, "payload": payload})
    return {"allowed": False, "reason": "blocked: no exact approval — run packet, review it, then approve --confirm <packet_id>", "hash": h}

def approve_packet(state: dict, packet: dict) -> dict:
    """Record approval for this packet's exact proposed payload. Callers
    must have shown the packet to the human before calling this."""
    payload = packet.get("proposed_action_payload") or packet
    h = payload_hash(payload)
    if h not in state["approvals"]:
        state["approvals"].append(h)
    return {"approved": True, "packet_id": packet.get("id"), "hash": h}
