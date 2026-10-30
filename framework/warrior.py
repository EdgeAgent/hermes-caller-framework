"""Sales Rep WARRIOR mode — strong, not pushy.

Warrior means: prepared, persistent, objection-ready, follow-up disciplined.
It does NOT mean: pressure closes, harassment, ignoring opt-outs, or
closing without a human. Those are forbidden, and the code enforces them.

Pipeline: new -> contacted -> qualified -> booked -> human-closes -> won|lost
Terminal states: optout, lost, won. Once optout, NOTHING advances, ever.
Follow-up cadence: day 0 (first contact), 3, 7, 14 — then STOP and hand to
human. No more than 4 touches, business hours only (enforced by policy,
not by clock in this local module — see COMPLIANCE.md).
"""
from __future__ import annotations

STAGES = ["new", "contacted", "qualified", "booked", "human-closes", "won", "lost", "optout"]
CADENCE = {0: "first contact", 3: "value follow-up", 7: "specific proof follow-up", 14: "final check-in, then hand to human"}

OBJECTIONS = {
 "too-expensive": "I hear you — let's do the math, not a pitch. What does one closed deal / booked job pay you, versus what this costs? If the math doesn't work, I'll say so.",
 "not-interested": "Totally fair — is it not a problem right now, or just bad timing? Either way, I'll leave it there unless you tell me otherwise.",
 "send-info": "Happy to — what part is actually relevant to you, so I don't send a generic deck you'll never read?",
 "already-have-someone": "What part are they not covering — leads, fulfillment, or follow-up? If they're covering it all, you don't need me.",
 "need-to-think": "Take the time — what specifically do you need to think through, price, fit, or timing? I can get you that one answer, no pressure.",
 "bad-experience-before": "Fair — what specifically went wrong last time? I'll show you how this is different on that one point, or I'll tell you it's not.",
 "no-time": "That's exactly why this exists — you only take qualified calls, the system does the prospecting. Want me to show you the one workflow that saves time?",
 "not-the-decision-maker": "No problem — who is the right person, and would you be okay with me reaching them directly, or would you rather pass this on?",
}

def objection_response(objection: str) -> dict:
    key = objection.lower().replace(" ", "-")
    if key not in OBJECTIONS:
        return {"objection": objection, "response": "Good question — let me get you the exact answer, not a guess. A human will follow up on this one.", "known": False}
    return {"objection": key, "response": OBJECTIONS[key], "known": True}

def followup(day: int, stage: str) -> dict:
    if stage == "optout":
        return {"day": day, "action": "STOP", "reason": "opted out — no further follow-up, ever"}
    if day not in CADENCE:
        return {"day": day, "action": "STOP", "reason": "cadence ended at day 14 — hand to human, do not keep chasing"}
    return {"day": day, "action": CADENCE[day], "stage": stage, "max_touches": 4}

def advance_pipeline(current: str, target: str, scrubbed: bool = False) -> dict:
    if scrubbed: return {"ok": False, "reason": "scrubbed — never advance, never call"}
    if current == "optout": return {"ok": False, "reason": "opted out — terminal, no advance"}
    if target not in STAGES: return {"ok": False, "reason": f"unknown stage {target}"}
    if target == "won" and current != "human-closes":
        return {"ok": False, "reason": "cannot jump to won — human must close first (stage human-closes)"}
    if STAGES.index(target) < STAGES.index(current) and target != "optout":
        return {"ok": False, "reason": "cannot move pipeline backwards (except optout)"}
    return {"ok": True, "from": current, "to": target}

def warrior_score(activities: int, qualified: bool, booked: bool) -> dict:
    score = min(activities, 4) * 10 + (30 if qualified else 0) + (30 if booked else 0)
    grade = "WARRIOR" if score >= 80 else "GRINDING" if score >= 40 else "WARMING-UP"
    return {"score": score, "grade": grade, "note": "Activity + qualification + booking. Score never overrides scrub, gate, or human-close."}
