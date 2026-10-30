"""doctor — production readiness check. Reports presence only, never key values.
Exit 0 = core ready (mock + dry-run + gates work). Real calls need keys + packet.
"""
from __future__ import annotations
import os, sys
from pathlib import Path
def check() -> dict:
    root = Path(__file__).resolve().parent.parent
    from .personas import list_personas
    from .receipts import verify
    return {
      "python": sys.version.split()[0],
      "personas": list_personas(),
      "scrub_file": (root / "data" / "scrub-list.csv").exists(),
      "env_present_only": {k: bool(os.environ.get(k)) for k in
        ["OPENROUTER_API_KEY", "OPENROUTER_MODEL", "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER", "VAPI_API_KEY", "VAPI_ASSISTANT_ID"]},
      "receipts": verify(root / ".framework"),
      "real_call_ready": bool(os.environ.get("TWILIO_ACCOUNT_SID") or os.environ.get("VAPI_API_KEY")),
      "note": "Real call still needs: provider account + keys + approved packet + scrub passed + your test number first + compliance review.",
    }
