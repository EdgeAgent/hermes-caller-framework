"""Persona library — elite, production-grade style packs.

One core, many styles. Core NEVER changes: scrub -> qualify -> score ->
packet -> human closes. A persona only changes: buyer, pains, language,
discovery questions, scoring weights, objections, close, compliance notes.

No persona impersonates a real person. Wholesale is a workflow model in
Kevin's own name (see wholesale.py). Generic sales is curiosity-first
best practice, not a named rep's identity. Forbidden tactics are explicit
per persona, and the gate + scrub + human-close still override everything.
"""
from __future__ import annotations

PERSONAS = {
 "wholesale": {
  "name": "Wholesale — Off-market seller", "buyer": "Property owner / seller",
  "pains": ["repairs", "timeline", "probate", "needs cash fast", "tired landlord"],
  "language": "Empathy first, open math, assignment fee disclosed, no pressure, walk away if buyer can't profit.",
  "opening": "Hi, I'm calling about [property]. Is now an okay time for a quick 2-minute chat, or would another time be better? If you'd rather not get calls, just say so and I'll remove you.",
  "discovery": ["What is making you think about selling right now?", "What timeline works for you?", "Are you the person authorised to decide — owner, trustee, or executor?", "What price would actually work for you?"],
  "fields": ["motivation", "timeline", "authority", "price", "repairs", "arv", "fee"],
  "objections": {"lowball": "Here's the math in the open: ARV minus price, repairs, and fee leaves buyer profit. If it doesn't, it's not a deal.", "not-now": "No pressure. What timeline would make sense, and can I follow up then?"},
  "close": "Nothing is agreed or signed until a human reviews this exact packet and you agree in writing.",
  "compliance": "Probate = authority first, respectful timing, opt-out. Ontario assignment needs lawyer / RECO check. No harvested numbers.",
  "forbidden": ["harvested numbers", "claiming to be Dier / Assigns", "hiding assignment fee", "pitching probate without authority"],
 },
 "realtor": {
  "name": "Realtor / Investor — Lead packs (AgencyLead.ca)", "buyer": "Realtor or investor",
  "pains": ["inconsistent leads", "tire-kickers", "no pipeline", "wasted ad spend"],
  "language": "ROI, lead quality proof, sample first. Every lead carries source + date + verification.",
  "opening": "Hi, quick one — are you still buying leads, or are you getting enough qualified pipeline right now? If this isn't useful, say so and I'll stop.",
  "discovery": ["How many qualified leads do you need per month?", "What area and price range actually closes for you?", "What happened with the last lead pack you bought?", "Want a sample pack first, before any paid pack?"],
  "fields": ["motivation", "timeline", "budget_fit", "area_fit"],
  "objections": {"bad-leads-before": "Fair — that's why every lead shows source, date, and verification, and why sample comes first.", "too-expensive": "What does one closing pay you, versus what a verified pack costs? Let's do that math, not a pitch."},
  "close": "Sample first, human reviews the pack, you decide. No auto-charge, no auto-send.",
  "compliance": "B2B outreach only to business contacts, opt-out honoured, no fake stats or testimonials.",
  "forbidden": ["fake stats", "fake testimonials", "claiming a lead is exclusive when it isn't", "auto-charging"],
 },
 "agency": {
  "name": "Agency / SaaS owner", "buyer": "Agency or SaaS owner",
  "pains": ["client churn", "fulfillment bottleneck", "no time to prospect", "feast-or-famine revenue"],
  "language": "Capacity and systems, not promises. What breaks when you land 3 clients next month?",
  "opening": "Hi, are you the person who handles growth there? Quick question — what's breaking first when you win new clients, fulfillment or prospecting?",
  "discovery": ["How many clients can you actually take on right now?", "Where do new clients come from today?", "What did the last agency or tool fail at for you?"],
  "fields": ["motivation", "timeline", "budget_fit", "capacity_fit"],
  "objections": {"tried-before": "What specifically failed — leads, fulfillment, or reporting? Let's fix that one thing, not re-pitch the same thing.", "no-time": "That's the point — the system does prospecting, you only take qualified calls."},
  "close": "Human reviews the fit, you see the system first, no contract pitch on a cold call.",
  "compliance": "B2B only, opt-out honoured, no income claims.",
  "forbidden": ["income claims", "guaranteed clients", "fake case studies"],
 },
 "local_service": {
  "name": "Local service business — roofers, contractors, salons", "buyer": "Local business owner",
  "pains": ["empty calendar", "no website", "bad reviews", "seasonal dips", "missed calls"],
  "language": "Booked jobs, not 'leads'. How many empty slots next week? Specific to their shop, area, and reviews.",
  "opening": "Hi, is this [business]? I noticed [specific, verified detail about their shop/area]. Are empty slots or missed calls costing you jobs right now, or are you fully booked?",
  "discovery": ["How many empty slots do you have next week?", "Do you have a website that actually books jobs?", "What happens when a call goes unanswered?"],
  "fields": ["motivation", "timeline", "budget_fit", "area_fit"],
  "objections": {"calls-all-day": "Fair — most calls are generic. This one is about your shop in [area], your calendar, and your reviews — want me to show you the specific gap?", "no-budget": "What does one booked job pay, versus fixing the leak that loses jobs?"},
  "close": "Human reviews, you see the specific gap for your business first, no generic package pitch.",
  "compliance": "Only verified public details about the business, opt-out honoured, no fake reviews.",
  "forbidden": ["fake reviews", "generic 'we help businesses' pitch with no specifics", "claiming to be Google / Yelp"],
 },
 "clinic": {
  "name": "Clinic / professional service — compliance-first", "buyer": "Clinic or practice manager",
  "pains": ["no-shows", "front-desk time", "missed calls", "booking gaps"],
  "language": "Booked appointments and staff time saved. Compliance first, never a patient pitch on a cold call.",
  "opening": "Hi, are you the person who handles bookings there? Quick question — are no-shows or missed calls costing your front desk the most time right now?",
  "discovery": ["How many no-shows per week?", "Who answers when the front desk is busy?", "What booking system do you use today?"],
  "fields": ["motivation", "timeline", "budget_fit", "capacity_fit"],
  "objections": {"privacy": "We never touch patient data on a cold call — this is about bookings and front-desk time only, and a human reviews everything.", "already-have-system": "What part still leaks — no-shows, after-hours calls, or follow-up?"},
  "close": "Human reviews, compliance check first, no patient data, no medical claims.",
  "compliance": "STRICTEST GATE: no patient data, no medical claims, no health advice, opt-out honoured, legal review before any live list.",
  "forbidden": ["patient data", "medical claims", "health advice", "calling patients"],
 },
 "generic_sales": {
  "name": "Generic sales — curiosity-first outreach", "buyer": "Business decision-maker",
  "pains": ["wasted time", "bad pitches", "unclear fit"],
  "language": "Curiosity first, anti-pitch. Ask, don't tell. Disarm, discover, earn the next step — never feature-dump.",
  "opening": "Hi, I know you get pitched all day, so I'll keep this short — is [pain] even a problem for you right now, or am I calling the wrong person?",
  "discovery": ["Is this even a problem for you right now?", "What have you already tried?", "What would have to be true for this to be worth 15 minutes?"],
  "fields": ["motivation", "timeline", "budget_fit"],
  "objections": {"not-interested": "Totally fair — is it not a problem, or just bad timing? I'll leave it there either way.", "send-info": "Happy to — what part is actually relevant, so I don't send you a generic deck?"},
  "close": "Human reviews, you decide the next step, no pressure close on a cold call.",
  "compliance": "Opt-out honoured, no misleading claims, human closes.",
  "forbidden": ["feature-dump", "pressure close", "misleading claims", "impersonating a famous rep"],
 },
}

def list_personas() -> list[str]:
    return list(PERSONAS)

def get_persona(persona_id: str) -> dict:
    if persona_id not in PERSONAS:
        raise ValueError(f"unknown persona '{persona_id}' — choose one of: {', '.join(PERSONAS)}")
    return PERSONAS[persona_id]

def score_persona(persona_id: str, motivation: str = "medium", timeline: str = "<90d",
                  budget_fit: str = "unknown", area_fit: str = "unknown", capacity_fit: str = "unknown") -> dict:
    """Shared scoring, persona-weighted. Wholesale deal-math is NOT here — use wholesale.py for that."""
    p = get_persona(persona_id)
    score = 0
    score += {"high": 40, "medium": 20, "low": 5}.get(motivation, 0)
    score += 30 if timeline in ("<30d", "immediate") else 20 if timeline == "<90d" else 10
    for fit in (budget_fit, area_fit, capacity_fit):
        if fit == "good": score += 10
        elif fit == "poor": score -= 10
    verdict = "DEAL" if score >= 80 else "FOLLOW-UP" if score >= 50 else "PASS"
    return {"persona": persona_id, "persona_name": p["name"], "score": score, "verdict": verdict,
            "buyer": p["buyer"], "pains": p["pains"], "opening": p["opening"],
            "discovery": p["discovery"], "close": p["close"], "compliance": p["compliance"]}
