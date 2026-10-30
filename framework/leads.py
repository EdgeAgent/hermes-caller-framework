"""Leads — every lead MUST carry source + source date + verification.
Lists with no source/date are rejected, never imported. No deceptive
'special data nobody ever called' claims are allowed in this framework."""
from __future__ import annotations
from .scrub import normalize_phone

def add_lead(state: dict, name: str, phone: str, source: str, source_date: str, verified: str = "unverified", notes: str = "") -> dict:
    if not source or not source.strip():
        raise ValueError("rejected: lead requires a data source (where it came from)")
    if not source_date or not source_date.strip():
        raise ValueError("rejected: lead requires a source date (when it was pulled)")
    if not phone or not normalize_phone(phone):
        raise ValueError("rejected: lead requires a phone number")
    lead = {"id": f"lead-{len(state['leads'])+1}", "name": name, "phone": phone,
            "source": source, "source_date": source_date, "verified": verified,
            "notes": notes, "status": "new"}
    state["leads"].append(lead)
    return lead

def score_qualification(motivation: str, timeline: str, price: str, condition: str) -> dict:
    score = 0
    score += {"high": 40, "medium": 20, "low": 5}.get(motivation, 0)
    score += 30 if timeline in ("<30d", "immediate", "30d") else 20 if timeline in ("<90d", "90d") else 10
    score += 20 if price in ("flexible", "open") else 5
    score += 10 if condition in ("poor", "needs-work") else 5
    grade = "A" if score >= 80 else "B" if score >= 55 else "C"
    return {"score": score, "grade": grade}
