import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.warrior import objection_response, followup, advance_pipeline, warrior_score, STAGES
def test_known_objection_has_answer():
    r = objection_response("too-expensive"); assert r["known"] and "math" in r["response"]
def test_unknown_objection_defers_to_human():
    r = objection_response("weird-thing"); assert not r["known"] and "human" in r["response"]
def test_followup_cadence_stops_at_14():
    assert followup(3, "contacted")["action"] == "value follow-up"
    assert followup(30, "contacted")["action"] == "STOP"
def test_optout_stops_followup_forever():
    assert followup(3, "optout")["action"] == "STOP"
def test_cannot_jump_to_won():
    assert not advance_pipeline("qualified", "won")["ok"]
def test_human_close_can_win():
    assert advance_pipeline("human-closes", "won")["ok"]
def test_scrubbed_never_advances():
    assert not advance_pipeline("new", "contacted", scrubbed=True)["ok"]
def test_warrior_score():
    assert warrior_score(4, True, True)["grade"] == "WARRIOR"
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
