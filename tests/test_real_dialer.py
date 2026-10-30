import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.real_dialer import place_real_call, twilio_call, vapi_call
def test_dry_run_never_dials():
    assert twilio_call("+15550101234")["dialed"] is False
    assert vapi_call("+15550101234")["dialed"] is False
def test_scrubbed_refused_even_dry():
    r = place_real_call({"scrub_numbers": ["5550101234"]}, {"phone": "5550101234"})
    assert r["dialed"] is False and "scrubbed" in r["refused"]
def test_real_without_packet_blocked():
    r = place_real_call({"scrub_numbers": []}, {"phone": "+15550101234"}, dry_run=False)
    assert r["dialed"] is False and "approved packet" in r["blocked"]
def test_missing_keys_raise_on_real():
    try:
        twilio_call("+15550101234", dry_run=False); assert False
    except ValueError as e: assert "keys missing" in str(e)
def test_bad_provider_rejected():
    try:
        place_real_call({"scrub_numbers": []}, {"phone": "+15550101234"}, provider="nope"); assert False
    except ValueError: pass
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
