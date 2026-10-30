"""Real persistent calendar — not mock slots.

Bookings live in .framework/calendar.json, not hardcoded MOCK_SLOTS.
Book = check conflict, write, return confirmation. Cancel = remove.
Google Calendar sync is the NEXT integration (OAuth, your account) — this
file calendar is the real booking system a single clinic can use TODAY,
and its export format is designed to import into Google/CRM later.
"""
from __future__ import annotations
import json
from pathlib import Path

def _path(root: Path) -> Path: return Path(root) / "calendar.json"
def _load(root: Path) -> list:
    p = _path(root)
    return json.loads(p.read_text()) if p.exists() else []
def _save(root: Path, data: list): _path(root).write_text(json.dumps(data, indent=2))

def book(root: Path, caller: str, persona: str, slot: str) -> dict:
    data = _load(root)
    if any(b["slot"] == slot for b in data):
        return {"ok": False, "action": "slot_taken", "slot": slot, "available": [b["slot"] for b in data]}
    rec = {"caller": caller, "persona": persona, "slot": slot, "status": "booked-pending-staff-confirmation"}
    data.append(rec); _save(root, data)
    return {"ok": True, "action": "booked", **rec}

def list_bookings(root: Path) -> list: return _load(root)
def cancel(root: Path, slot: str, caller: str) -> dict:
    data = _load(root); before = len(data); data = [b for b in data if not (b["slot"] == slot and b["caller"] == caller)]
    _save(root, data); return {"ok": len(data) < before, "cancelled": len(data) < before, "slot": slot}
