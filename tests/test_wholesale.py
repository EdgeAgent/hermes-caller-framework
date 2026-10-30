import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from framework.wholesale import qualify_wholesale, deal_math, SCRIPT

def test_good_deal_is_deal():
    r = qualify_wholesale("high", "<30d", "owner", False, 200000, 30000, 300000, 10000)
    assert r["verdict"] == "DEAL" and r["buyer_profit"] == 60000 and r["buyer_profit_ok"]
def test_no_buyer_profit_is_pass():
    r = qualify_wholesale("high", "<30d", "owner", False, 290000, 30000, 300000, 10000)
    assert r["verdict"] == "PASS" and not r["buyer_profit_ok"]
def test_probate_without_authority_holds():
    r = qualify_wholesale("high", "<30d", "relative", True, 200000, 30000, 300000, 10000)
    assert r["verdict"] == "HOLD-probate" and "no offer pitch" in r["reason"]
def test_probate_with_trustee_can_deal():
    r = qualify_wholesale("high", "<30d", "trustee", True, 200000, 30000, 300000, 10000)
    assert r["verdict"] == "DEAL"
def test_low_motivation_passes():
    r = qualify_wholesale("low", "6mo", "owner", False, 200000, 30000, 300000, 10000)
    assert r["verdict"] in ("PASS", "FOLLOW-UP")
def test_math_is_open():
    m = deal_math(200000, 30000, 300000, 10000); assert m["buyer_profit"] == 60000 and m["assignment_fee"] == 10000
def test_script_has_optout_and_no_impersonation():
    assert "remove you" in SCRIPT["opening"] and "Maximilian" not in " ".join(SCRIPT.values())
def test_script_has_probate_respect():
    assert "difficult time" in SCRIPT["probate"] and "no rush" in SCRIPT["probate"]
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
