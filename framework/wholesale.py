"""Wholesale mode — Dier-workflow model, in Kevin's own name, NOT Dier/Assigns.

Style/workflow model only: never claim to be Maximilian Dier, affiliated
with Assigns.com, or using his results. No harvested-numbers tactic.
Probate: authority first, respectful timing, opt-out, open math.
Ontario: assignment model needs a lawyer / RECO check before use.
"""
from __future__ import annotations

SCRIPT = {
 "opening": "Hi, I'm calling about [property]. I'm a local buyer looking at off-market properties — is now an okay time for a quick 2-minute chat, or would another time be better? If you'd rather not get calls, just say so and I'll remove you, no problem.",
 "motivation": "What's making you think about selling right now — timing, repairs, tenants, or just testing the number? No pressure, I just want to know if this is even a fit.",
 "open_math": "Here's my math in the open: purchase [price], repairs [repairs], after-repair value [arv], my assignment fee [fee]. That leaves [buyer_profit] for the end buyer. If the buyer can't profit, it's not a deal — I won't pretend it is.",
 "probate": "I know this may be a difficult time, and there's no rush from me. Are you the person authorised to make decisions for the property — estate trustee or executor? If not, I'm happy to speak with whoever is, at a time that suits them. If you'd rather I not call again, say so and I stop.",
 "close_human": "Thanks — I'll pass this exact packet to a human to review. Nothing is agreed, signed, or sent until a human checks it and you agree in writing. Would a follow-up call at [time] work, or would you rather I leave it?",
}

def deal_math(price: float, repairs: float, arv: float, fee: float) -> dict:
    buyer_profit = arv - price - repairs - fee
    return {"price": price, "repairs": repairs, "arv": arv, "assignment_fee": fee,
            "buyer_profit": buyer_profit, "buyer_profit_ok": buyer_profit > 0}

def qualify_wholesale(motivation: str, timeline: str, authority: str,
                      probate: bool, price: float, repairs: float, arv: float, fee: float) -> dict:
    """Returns verdict DEAL / FOLLOW-UP / PASS / HOLD-probate, with open math."""
    math = deal_math(price, repairs, arv, fee)
    # Probate gate: no authority confirmed = HOLD, never a pitch
    if probate and authority not in ("trustee", "executor", "estate-trustee", "owner"):
        return {"verdict": "HOLD-probate", "reason": "probate + authority not confirmed — respectful follow-up only, no offer pitch",
                "script": SCRIPT["probate"], **math, "score": 0}
    score = 0
    score += {"high": 40, "medium": 20, "low": 5}.get(motivation, 0)
    score += 30 if timeline in ("<30d", "immediate") else 20 if timeline == "<90d" else 10
    score += 20 if math["buyer_profit_ok"] else -20
    score += 10 if authority in ("trustee", "executor", "estate-trustee", "owner") else 0
    if not math["buyer_profit_ok"]:
        verdict, reason = "PASS", "buyer profit <= 0 — deal only works if buyer overpays, so it's not a deal"
    elif score >= 80:
        verdict, reason = "DEAL", "high motivation + fast timeline + buyer profit + authority confirmed"
    elif score >= 50:
        verdict, reason = "FOLLOW-UP", "partial fit — follow up, re-check numbers, human reviews"
    else:
        verdict, reason = "PASS", "low fit on motivation / timeline / numbers"
    return {"verdict": verdict, "reason": reason, "score": score, "script": SCRIPT["open_math"], **math}
