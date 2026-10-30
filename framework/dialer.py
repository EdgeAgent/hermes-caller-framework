"""Mock dialer — logs 'would call' and NEVER dials a real number.

A real Twilio/Vapi adapter lives in real_dialer.py (gated): no keys in code,
dry-run default. Real calling needs keys + compliance + approval.
"""
from __future__ import annotations
from .scrub import is_scrubbed, normalize_phone

class MockDialer:
    def would_call(self, store, lead: dict) -> dict:
        state = store.load()
        if lead.get("status") == "scrubbed" or is_scrubbed(lead.get("phone", ""), state.get("scrub_numbers", [])):
            raise ValueError(f"REFUSED: {lead.get('id')} is scrubbed — never call, ever")
        rec = {"lead_id": lead.get("id"), "phone": lead.get("phone"), "action": "would_call_mock", "dialed": False}
        state.setdefault("calls", []).append(rec)
        store.save(state)
        return rec

# Real dialing lives in framework/real_dialer.py (gated, dry-run default).
# Nothing in this file dials.
