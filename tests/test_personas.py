import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.personas import PERSONAS, list_personas, get_persona, score_persona
def test_six_personas():
    assert set(list_personas()) == {"wholesale", "realtor", "agency", "local_service", "clinic", "dental", "walkin_clinic", "generic_sales"}
def test_every_persona_has_opening_optout_and_close():
    for pid, p in PERSONAS.items():
        assert p["opening"] and p["close"] and p["discovery"] and p["objections"] and p["forbidden"] and p["compliance"]
def test_no_impersonation_in_personas():
    blob = str(PERSONAS); assert "I am Maximilian" not in blob and "I am Josh" not in blob and "I am Aaron" not in blob
def test_realtor_scores_high_on_good_fit():
    r = score_persona("realtor", "high", "<30d", "good", "good"); assert r["verdict"] == "DEAL" and r["score"] >= 80
def test_low_scores_pass():
    assert score_persona("agency", "low", "6mo", "poor", "unknown", "poor")["verdict"] == "PASS"
def test_clinic_has_strictest_compliance():
    assert "patient data" in get_persona("clinic")["compliance"] and "patient data" in str(get_persona("clinic")["forbidden"])
def test_wholesale_forbidden_includes_harvested():
    assert "harvested numbers" in get_persona("wholesale")["forbidden"]
def test_unknown_persona_rejected():
    try: get_persona("nope"); assert False
    except ValueError as e: assert "unknown persona" in str(e)
def test_each_persona_has_distinct_pains():
    pains = [tuple(p["pains"]) for p in PERSONAS.values()]; assert len(set(pains)) == 8
def test_local_service_is_specific_not_generic():
    assert "specific" in get_persona("local_service")["language"].lower()
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
