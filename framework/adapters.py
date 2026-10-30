"""Provider adapters — see framework/real_dialer.py for the real gated adapters.

This file is kept only so old imports do not break. Do NOT add a second
dialer here. Twilio / Vapi: bring your own keys in env, never in code.
"""
from .real_dialer import twilio_call, vapi_call, place_real_call
TWILIO_STUB = {"provider": "twilio", "configured": False, "note": "Use real_dialer.twilio_call with TWILIO_* in env; never commit keys."}
VAPI_STUB = {"provider": "vapi", "configured": False, "note": "Use real_dialer.vapi_call with VAPI_* in env; never commit keys."}
