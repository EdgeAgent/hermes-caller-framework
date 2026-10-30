import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.inbound import handle_inbound, twiml_bridge, MOCK_SLOTS
def test_book_success():
    r = handle_inbound("5550101234", "dental", "book", slot="2026-11-02 10:00")
    assert r["action"] == "booked" and r["slot"] == "2026-11-02 10:00"
def test_slot_taken_offers_others():
    r = handle_inbound("5550101234", "walkin_clinic", "book", slot="2026-11-02 10:00", booked=["2026-11-02 10:00"])
    assert r["action"] == "slot_taken" and "2026-11-02 10:00" not in r["available_slots"]
def test_bridge_uses_existing_number():
    r = handle_inbound("5550101234", "dental", "bridge", existing_number="5195550199")
    assert r["action"] == "bridge" and r["to_existing_number"] == "5195550199" and "5195550199" in r["twiml"] and r["dialed"] is False
def test_bridge_without_number_fails_safe():
    r = handle_inbound("5550101234", "dental", "bridge")
    assert r["action"] == "bridge_failed" and r["dialed"] is False
def test_greet_default():
    assert handle_inbound("5550101234", "walkin_clinic", "other")["action"] == "greet"
def test_no_medical_advice_in_booking():
    r = handle_inbound("5550101234", "dental", "book", slot="2026-11-02 09:00")
    assert "diagnosis" in r["confirmation"] and "no diagnosis" in r["confirmation"]
def test_slots_exist():
    assert len(MOCK_SLOTS) >= 4
def test_twiml_is_dial_not_new_number():
    assert "<Dial>" in twiml_bridge("5195550199")
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
