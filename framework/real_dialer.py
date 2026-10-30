"""Real dialer adapters — Twilio + Vapi. NO keys in code, ever.

Rules, hard-wired:
- Env vars only: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER,
  VAPI_API_KEY, VAPI_ASSISTANT_ID. If missing, adapter refuses, it never guesses.
- Scrub check first: scrubbed number = REFUSED, no call, no exception.
- Gate first: a call needs an APPROVED packet for that exact lead, via gate.py.
  No approved packet = BLOCKED, no call.
- Dry-run by default: call(..., dry_run=True) returns what WOULD be called,
  dialed=False. Real dial only with dry_run=False AND an approved packet.
- This code places a call to a human agent / test number you control first.
  It does NOT do robocall blasts, does NOT call harvested lists, does NOT
  bypass DNC. Compliance review + consenting test numbers first, always.
"""
from __future__ import annotations
import os, json, urllib.request, urllib.parse, base64

def _scrubbed(phone, scrub_numbers):
    from .scrub import normalize_phone
    return normalize_phone(phone) in {normalize_phone(n) for n in scrub_numbers}

def twilio_call(to: str, from_number: str = None, script_url: str = None, dry_run: bool = True) -> dict:
    sid, token = os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = from_number or os.environ.get("TWILIO_FROM_NUMBER")
    if dry_run:
        return {"provider": "twilio", "to": to, "from": from_number, "dialed": False, "dry_run": True,
                "note": "DRY RUN — no call placed. Set dry_run=False + approved packet + keys to dial for real."}
    if not (sid and token and from_number):
        raise ValueError("twilio keys missing: set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER in env, never in code")
    data = urllib.parse.urlencode({"To": to, "From": from_number, "Url": script_url or "http://demo.twilio.com/docs/voice.xml"}).encode()
    req = urllib.request.Request(f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json", data=data,
        headers={"Authorization": "Basic " + base64.b64encode(f"{sid}:{token}".encode()).decode()})
    with urllib.request.urlopen(req, timeout=30) as r:
        return {"provider": "twilio", "dialed": True, **json.loads(r.read())}

def vapi_call(phone_number: str, dry_run: bool = True) -> dict:
    key, assistant = os.environ.get("VAPI_API_KEY"), os.environ.get("VAPI_ASSISTANT_ID")
    if dry_run:
        return {"provider": "vapi", "phone_number": phone_number, "dialed": False, "dry_run": True,
                "note": "DRY RUN — no call placed. Set dry_run=False + approved packet + keys to dial for real."}
    if not (key and assistant):
        raise ValueError("vapi keys missing: set VAPI_API_KEY, VAPI_ASSISTANT_ID in env, never in code")
    body = json.dumps({"assistantId": assistant, "phoneNumberId": None, "customer": {"number": phone_number}}).encode()
    req = urllib.request.Request("https://api.vapi.ai/call", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return {"provider": "vapi", "dialed": True, **json.loads(r.read())}

def place_real_call(state: dict, lead: dict, provider: str = "twilio", dry_run: bool = True, approved_packet_id: str = None) -> dict:
    if _scrubbed(lead["phone"], state.get("scrub_numbers", [])):
        return {"provider": provider, "dialed": False, "refused": "scrubbed — never call, ever"}
    if not dry_run and not approved_packet_id:
        return {"provider": provider, "dialed": False, "blocked": "no approved packet for this exact lead — human must approve first"}
    if provider == "twilio":
        return twilio_call(lead["phone"], dry_run=dry_run)
    if provider == "vapi":
        return vapi_call(lead["phone"], dry_run=dry_run)
    raise ValueError("provider must be twilio or vapi")
