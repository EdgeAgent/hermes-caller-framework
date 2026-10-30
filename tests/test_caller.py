import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from framework.state import StateStore
from framework import leads as L, scrub as S, gate as G
from framework.dialer import MockDialer

def fresh():
    d = tempfile.mkdtemp(); st = StateStore(d); return st, st.load()

class TestCaller(unittest.TestCase):
    def test_scrub_never_call(self):
        st, s = fresh(); s["scrub_numbers"] = ["5550001111"]
        lead = L.add_lead(s, "A", "555-000-1111", "FSBO", "2026-10-29")
        self.assertTrue(S.is_scrubbed(lead["phone"], s["scrub_numbers"]))
        S.apply_scrub(s); self.assertEqual(lead["status"], "scrubbed")
        with self.assertRaises(ValueError):
            MockDialer().would_call(st, lead)
    def test_gate_blocks_send_call_charge_without_approval(self):
        _, s = fresh()
        for action in ("send", "call", "charge", "close", "delete"):
            self.assertFalse(G.check(s, action, {"to": "x", "msg": "hi"})["allowed"], action)
        self.assertEqual(len(s["blocked_events"]), 5)
    def test_gate_allows_after_exact_approval(self):
        _, s = fresh()
        packet = {"id": "packet-1", "proposed_action_payload": {"action": "send", "to": "closer", "msg": "packet"}}
        G.approve_packet(s, packet)
        self.assertTrue(G.check(s, "send", {"action": "send", "to": "closer", "msg": "packet"})["allowed"])
        self.assertFalse(G.check(s, "send", {"action": "send", "to": "closer", "msg": "different"})["allowed"])
    def test_scoring(self):
        self.assertEqual(L.score_qualification("high", "<30d", "flexible", "poor")["grade"], "A")
        self.assertEqual(L.score_qualification("low", "later", "firm", "average")["grade"], "C")
    def test_booking_packet_contents(self):
        _, s = fresh()
        lead = L.add_lead(s, "Jane", "5551234567", "FSBO", "2026-10-29")
        s["qualifications"].append({"lead_id": lead["id"], "score": 90, "grade": "A"})
        s["bookings"].append({"id": "booking-1", "lead_id": lead["id"], "when": "2026-11-02 14:00"})
        self.assertTrue(lead["source"] and lead["source_date"])
        self.assertEqual(s["qualifications"][0]["grade"], "A")
    def test_sourceless_list_rejected(self):
        _, s = fresh()
        for src, date in (("", "2026-10-29"), ("FSBO", "")):
            with self.assertRaises(ValueError):
                L.add_lead(s, "X", "5551234567", src, date)
    def test_mock_dialer_never_dials(self):
        st, s = fresh()
        lead = L.add_lead(s, "Jane", "5551234567", "FSBO", "2026-10-29")
        rec = MockDialer().would_call(st, lead)
        self.assertFalse(rec["dialed"]); self.assertEqual(rec["action"], "would_call_mock")

if __name__ == "__main__":
    unittest.main()
