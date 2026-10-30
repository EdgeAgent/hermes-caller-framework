"""Inbound calls + booking + BridgeConnect.

Inbound is the OPPOSITE direction from cold calling: the patient / customer
calls YOU. The agent greets, books a slot from a mock calendar, confirms,
or bridges the caller to the business's EXISTING number.

BridgeConnect: --existing-number is the number the business ALREADY has.
If the agent cannot book / caller asks for a human / urgent flag, the call
is bridged to that number — NOT to a new number, NOT to a personal phone.
In mock mode bridge returns dialed=False + the TwiML / transfer config that
WOULD be used. Real bridging happens only inside a real Twilio/Vapi call,
with an approved packet, same gate as outbound.

Compliance, clinic/dental: booking only — name, phone, slot, general reason
category (e.g. "checkup", "walk-in"). NO diagnosis, NO medical advice,
NO patient history, NO health data stored beyond the booking itself.
"""
from __future__ import annotations
import re

MOCK_SLOTS = ["2026-11-02 09:00", "2026-11-02 10:00", "2026-11-02 11:00", "2026-11-03 09:00"]

def twiml_bridge(existing_number: str) -> str:
    n = re.sub(r"\D", "", existing_number)
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Say>Connecting you to the clinic now.</Say><Dial>+{n}</Dial></Response>'

def handle_inbound(caller_phone: str, persona: str, intent: str, slot: str = None,
                   existing_number: str = None, booked: list = None) -> dict:
    booked = booked if booked is not None else []
    if intent == "bridge" or intent == "human":
        if not existing_number:
            return {"direction": "inbound", "action": "bridge_failed", "reason": "no existing number supplied — BridgeConnect needs the business's existing number", "dialed": False}
        return {"direction": "inbound", "action": "bridge", "to_existing_number": existing_number,
                "twiml": twiml_bridge(existing_number), "dialed": False,
                "note": "MOCK: in a real Twilio call this TwiML bridges the caller to the existing number."}
    if intent == "book":
        # Real calendar is the source of truth now; MOCK_SLOTS is only the
        # suggested list when no slot is given. A slot not in the suggestion
        # list is NOT invalid — it is booked if free in the real calendar.
        if not slot: return {"direction": "inbound", "action": "ask_slot", "available_slots": MOCK_SLOTS}
        if slot in booked: return {"direction": "inbound", "action": "slot_taken", "slot": slot, "available_slots": [s for s in MOCK_SLOTS if s not in booked]}
        return {"direction": "inbound", "action": "booked", "caller": caller_phone, "persona": persona, "slot": slot,
                "confirmation": f"Booked {slot} for {caller_phone} ({persona}). Human staff confirm by callback — no diagnosis or medical advice given."}
    return {"direction": "inbound", "action": "greet", "persona": persona,
            "greeting": f"Thanks for calling. Are you looking to book, or would you like to be connected to the clinic directly?"}
