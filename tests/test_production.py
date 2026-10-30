import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch, MagicMock
from framework.model import _parse, qualify_with_model
from framework.receipts import append, verify
from framework.doctor import check
import tempfile
from pathlib import Path
def test_parse_valid_json():
    r = _parse('{"motivation": "high", "timeline": "<30d", "authority": "owner", "summary": "wants cash fast"}')
    assert r["motivation"] == "high" and r["model_ran"] is True
def test_parse_rejects_garbage():
    try: _parse("not json"); assert False
    except ValueError: pass
def test_parse_rejects_bad_motivation():
    try: _parse('{"motivation": "huge", "authority": "owner"}'); assert False
    except ValueError: pass
def test_model_missing_key_raises_not_mock():
    os.environ.pop("OPENROUTER_API_KEY", None)
    try: qualify_with_model("openrouter", "test"); assert False
    except ValueError as e: assert "missing" in str(e)
def test_model_bad_provider_rejected():
    try: qualify_with_model("nope", "x"); assert False
    except ValueError: pass
def test_receipt_chain_verifies_and_breaks_on_tamper():
    with tempfile.TemporaryDirectory() as d:
        append(Path(d), "qualify", {"lead": "lead-1"}); append(Path(d), "call", {"lead": "lead-1", "dialed": False})
        assert verify(Path(d)) == {"ok": True, "count": 2}
        p = Path(d) / "receipts.jsonl"; lines = p.read_text().splitlines(); lines[0] = lines[0].replace("lead-1", "lead-9"); p.write_text("\n".join(lines) + "\n")
        assert verify(Path(d))["ok"] is False
def test_doctor_reports_presence_not_values():
    r = check(); assert "OPENROUTER_API_KEY" in r["env_present_only"] and isinstance(r["env_present_only"]["OPENROUTER_API_KEY"], bool)
    assert len(r["personas"]) == 8
def test_doctor_real_call_ready_false_without_keys():
    for k in ["TWILIO_ACCOUNT_SID", "VAPI_API_KEY"]: os.environ.pop(k, None)
    assert check()["real_call_ready"] is False
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
