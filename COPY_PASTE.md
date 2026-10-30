# LEGACY — v0 bootstrap only. DO NOT use this file to rebuild the current repo.
# Current version is v1.1 (51 tests, personas, wholesale, real model, real gated dialer, inbound + BridgeConnect).
# To get the current version, clone https://github.com/EdgeAgent/hermes-caller-framework — do not re-run the v0 bootstrap below, it recreates only the skeleton.

# Copy-paste start here — Hermes Caller Framework

**How to use this file in ONE paste:** copy this whole file and paste it
into your Hermes agent chat, or into a new GitHub repo's first issue /
new chat, and say: "Build this exactly, run the tests, do not change
the safety rules." Everything below is self-contained: the brief, the
file list, and the bootstrap script that recreates the whole framework
with no manual edits. No keys, no pricing, no real calls.

## 1. Project brief, in plain words

Build a RunItRemote-style cold-calling lead service framework, in
Python, no dependencies, local-first, mock/free first, that Kevin can
hand to his Hermes agent. It is NOT a real dialer and NOT a sales
machine that closes deals by itself.

Core loop: a lead list goes in (CSV / `lead add`) -> scrub / DNC /
opt-out filter -> call script (motivation, timeline, price, condition)
-> score (A/B/C) -> book an appointment -> handoff packet for the
human closer -> follow-up drafts. Each stage is a skill/playbook in
`skills/` (qualify, objection-handling, booking, follow-up).

Selling, honestly autonomous up to the gate: the agent CAN autonomously
research, prepare a dial list, mock-qualify, score, draft outreach /
booking messages, and prepare a sales packet. It can NEVER autonomously
send an email/SMS, place a real call, charge, close a deal, or delete
data without explicit human approval. That is the immutable core.

Free stack: local file-based state, free models via Ollama local /
OpenRouter free tier only (router.yaml, free-only filter, never
silently upgrade to paid), mock dialer that logs "would call" and
never dials a real number, Twilio/Vapi as STUBS only (config, no keys,
no real calls, "bring your own keys, compliance is yours").

Compliance: business hours only, DNC/scrub absolute, opt-out on first
request, identify yourself, no robocall / pre-recorded sales calls
without consent, Canada/US basics in plain language, "this is not
legal advice, check your jurisdiction". No deceptive "special data
nobody ever called" claims — every lead must carry source + source
date + verification, and lists with no source/date are rejected.

Hermes handoff: see HERMES.md in the generated folder. Hermes runs
the commands in section 4 below, in order.

## 2. Folder / file list (created by the script below)

```
hermes-caller-framework/
  run.py, framework.yaml, router.yaml, README.md, COMPLIANCE.md,
  HERMES.md, COPY_PASTE.md, LICENSE, .gitignore
  framework/__init__.py, __main__.py, cli.py, state.py, scrub.py,
    leads.py, gate.py, dialer.py, adapters.py
  skills/qualify.md, objection-handling.md, booking.md, follow-up.md
  data/scrub-list.csv
  tests/__init__.py, test_caller.py
```

## 3. Bootstrap script — paste this into a terminal (or give it to Hermes)

```bash
#!/bin/bash
# Hermes Caller Framework bootstrap — paste this whole script into a terminal, or paste COPY_PASTE.md into Hermes/a new repo and ask it to run it.
# Creates hermes-caller-framework/ in the current directory. No keys, no pricing, mock dialer only.
set -e
mkdir -p hermes-caller-framework
cd hermes-caller-framework
# root
cat > .gitignore << 'EOF_HCF'
__pycache__/
.framework/
*.pyc
EOF_HCF
# root
cat > COMPLIANCE.md << 'EOF_HCF'
# Compliance — plain language, not legal advice

Check your jurisdiction before any real call. This framework does not
make you compliant; it makes the safe defaults easy and the unsafe
actions hard.

- **Business hours only.** Call only during local business hours for
  the person you are calling. No late-night or early-morning calls.
- **Do Not Call / scrub, absolute.** Never call a scrubbed, DNC, or
  opted-out number, ever. Opt-out on first request, immediately, no
  argument, no callback to confirm.
- **Identify yourself.** Say who you are, who you represent, and why
  you are calling, at the start of the call.
- **No robocalls / pre-recorded sales calls without consent.** Do not
  use automated dialing or pre-recorded sales messages without the
  consent your jurisdiction requires.
- **Canada / US basics.** Respect national and state/provincial DNC
  registries, consent rules, and calling-hour rules in both countries.
  Rules differ by place and by call type — check yours.
- **Honest data claims.** Label every lead with source, source date,
  and verification. Never claim data is "special", "exclusive", or
  "never called" unless you can prove it for that exact list.
- **No auto-send, auto-dial, auto-charge, auto-close.** Those need
  explicit human approval of the exact message/recipients/packet, every
  time. See gate.py.

This is not legal advice. If you are unsure, get advice for your
jurisdiction before placing a real call or sending a real message.
EOF_HCF
# root
cat > HERMES.md << 'EOF_HCF'
# Hermes handoff — how to hand this to Hermes

Hermes (Kevin's lead-gen agent) can run this framework as-is, locally,
with no new service. Copy this whole folder into Hermes's workspace,
or point Hermes at this repo folder. It is Python, no dependencies.

## Folder layout
- `run.py` — entry point: `python run.py <command>`
- `framework/` — state, scrub, gate, leads, dialer, cli
- `skills/` — qualify, objection-handling, booking, follow-up playbooks
- `data/scrub-list.csv` — scrub numbers (add opt-outs here, never remove)
- `framework.yaml` / `router.yaml` — config, free-only models
- `.framework/state.json` — local state, created on first run

## Commands Hermes runs, in order
```bash
python run.py lead add "Jane Seller" --phone 5551234567 --source "FSBO list" --source-date 2026-10-29
python run.py scrub
python run.py dial-prep --lead lead-1        # mock only, never dials
python run.py qualify --mock --lead lead-1 --motivation high --timeline "<30d" --price flexible --condition poor
python run.py book --lead lead-1 --when "2026-11-02 14:00 America/Toronto"
python run.py packet --lead lead-1           # READ this exact packet first
python run.py approve --confirm packet-1     # only after review; approves this exact payload only
python run.py status
```

## What Hermes must NOT do
- Never send, call, charge, close, or delete without the gate.
- Never call a scrubbed number, for any reason.
- Never import a lead with no source/date.
- Never claim data is "never called" without proof.
- Never add keys to this repo. Twilio/Vapi keys live in Hermes's own
  environment, never committed, and real calling needs a compliance
  review first (see COMPLIANCE.md).
EOF_HCF
# root
cat > LICENSE << 'EOF_HCF'
MIT License — see https://opensource.org/licenses/MIT
EOF_HCF
# root
cat > README.md << 'EOF_HCF'
# Hermes Caller — RunItRemote-style cold-calling lead service, as a framework

Parallel to Battle Court, built for Hermes: a lead list goes in, scrub
filter runs, qualification scores it, booking is drafted, and a handoff
packet goes to the human closer. The human closes. The agent prepares,
scores, and drafts — autonomously, up to a hard gate.

## What it does (skeleton)
1. Lead list in (CSV / `lead add`) — source + source date required
2. Scrub / DNC / opt-out filter — scrubbed numbers are NEVER called
3. Call script — motivation, timeline, price, condition (skills/)
4. Score — A / B / C from answers given, never invented
5. Book appointment — pending human confirmation
6. Handoff packet — for the human closer
7. Follow-up sequence — drafts only, until approved

## What "autonomous" means here — honestly
Autonomous: research, dial-list prep, mock qualification, scoring,
drafting outreach/booking messages, preparing a sales packet.
**NOT autonomous: sending an email/SMS, placing a real call, charging,
closing a deal, or deleting data.** Those are blocked by the approval
gate (`framework/gate.py`) until a human reviews the exact packet and
runs `approve --confirm <packet_id>`. That gate is the immutable core.

## Quickstart
```bash
python run.py lead add "Jane Seller" --phone 5551234567 --source "FSBO list" --source-date 2026-10-29
python run.py scrub
python run.py qualify --mock --lead lead-1 --motivation high --timeline "<30d"
python run.py book --lead lead-1 --when "2026-11-02 14:00 America/Toronto"
python run.py packet --lead lead-1
python run.py approve --confirm packet-1
```

## Free stack
Local-first, file-based state, no dependencies, mock dialer ($0).
Models: Ollama local + OpenRouter free tier only (`router.yaml`,
free-only filter — never silently upgrades to paid). Twilio/Vapi are
STUBS only: no keys, no real calls, bring your own keys later.

## Compliance
See COMPLIANCE.md: business hours only, DNC/scrub absolute, opt-out
on first request, identify yourself, no robocalls without consent.
This is not legal advice.

## Honest status — skeleton v0.1.0-skeleton (bottom, not headline)
- Mock dialer only. $0. No real calls, no real sales, no pricing,
  no payment system — none invented.
- No real model runners yet; qualification in the skeleton is mock.
- No Twilio/Vapi wiring, no DNC API, no CRM yet.

## What to add next for real calls
Twilio/Vapi keys (your own env, never committed), a DNC API check,
a CRM connection, a compliance review for your jurisdiction, and a
real Windows / live-call test with consenting test numbers first.
EOF_HCF
mkdir -p data
cat > data/scrub-list.csv << 'EOF_HCF'
phone,reason
5550001111,opt-out
5550002222,dnc
EOF_HCF
mkdir -p framework
cat > framework/__init__.py << 'EOF_HCF'
"""Hermes Caller Framework — skeleton, mock dialer, $0, no real calls."""
__version__ = "0.1.0-skeleton"
EOF_HCF
mkdir -p framework
cat > framework/__main__.py << 'EOF_HCF'
from .cli import main
import sys
if __name__ == "__main__":
    sys.exit(main())
EOF_HCF
mkdir -p framework
cat > framework/adapters.py << 'EOF_HCF'
"""Optional provider adapters — STUBS ONLY. No keys, no real calls.

Twilio / Vapi: bring your own keys, set them in your own environment,
never commit them. Compliance (DNC, hours, consent, identification) is
yours — see COMPLIANCE.md. These stubs exist so the shape is clear,
not so a real call can slip through the skeleton.
"""
TWILIO_STUB = {"provider": "twilio", "configured": False, "note": "Set TWILIO_* in your own env; never commit keys."}
VAPI_STUB = {"provider": "vapi", "configured": False, "note": "Set VAPI_* in your own env; never commit keys."}
EOF_HCF
mkdir -p framework
cat > framework/cli.py << 'EOF_HCF'
"""CLI: lead add/list, scrub, qualify --mock, book, packet, approve, dial-prep."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .state import StateStore
from . import leads as L, scrub as S, gate as G
from .dialer import MockDialer
from .scrub import normalize_phone

def store() -> StateStore:
    return StateStore(Path(__file__).resolve().parent.parent / ".framework")

def _load_scrub_file(st: StateStore, state: dict):
    root = Path(__file__).resolve().parent.parent
    nums = S.load_scrub_numbers(root / "data" / "scrub-list.csv")
    for n in nums:
        if n not in state["scrub_numbers"]:
            state["scrub_numbers"].append(n)
    return state

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="hermes-caller", description="Hermes Caller Framework — mock dialer, human closes.")
    sub = p.add_subparsers(dest="cmd")
    a = sub.add_parser("lead"); la = a.add_subparsers(dest="op")
    add = la.add_parser("add"); add.add_argument("name"); add.add_argument("--phone", required=True)
    add.add_argument("--source", required=True); add.add_argument("--source-date", required=True)
    add.add_argument("--verified", default="unverified"); add.add_argument("--notes", default="")
    la.add_parser("list")
    sub.add_parser("scrub")
    q = sub.add_parser("qualify"); q.add_argument("--lead", required=True); q.add_argument("--mock", action="store_true")
    q.add_argument("--motivation", default="medium"); q.add_argument("--timeline", default="<90d")
    q.add_argument("--price", default="flexible"); q.add_argument("--condition", default="average")
    b = sub.add_parser("book"); b.add_argument("--lead", required=True); b.add_argument("--when", required=True)
    pk = sub.add_parser("packet"); pk.add_argument("--lead", required=True)
    ap = sub.add_parser("approve"); ap.add_argument("--confirm", required=True)
    dp = sub.add_parser("dial-prep"); dp.add_argument("--lead", required=True)
    sub.add_parser("status")
    args = p.parse_args(argv)
    st = store(); state = _load_scrub_file(st, st.load())
    if args.cmd == "lead" and args.op == "add":
        try:
            lead = L.add_lead(state, args.name, args.phone, args.source, args.source_date, args.verified, args.notes)
        except ValueError as e:
            print(f"ERROR: {e}"); return 2
        st.save(state); print(json.dumps(lead, indent=2)); return 0
    if args.cmd == "lead" and args.op == "list":
        print(json.dumps(state["leads"], indent=2)); return 0
    if args.cmd == "scrub":
        r = S.apply_scrub(state); st.save(state); print(json.dumps(r, indent=2)); return 0
    if args.cmd == "qualify":
        if not args.mock:
            print("ERROR: skeleton only supports --mock qualification (no real calls)."); return 2
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        if lead.get("status") == "scrubbed" or S.is_scrubbed(lead["phone"], state["scrub_numbers"]):
            print(f"REFUSED: {lead['id']} is scrubbed — never call, ever"); return 3
        sc = L.score_qualification(args.motivation, args.timeline, args.price, args.condition)
        rec = {"lead_id": lead["id"], "mock": True, "motivation": args.motivation, "timeline": args.timeline,
               "price": args.price, "condition": args.condition, **sc}
        state["qualifications"].append(rec); lead["status"] = "qualified"; st.save(state)
        print(json.dumps(rec, indent=2)); return 0
    if args.cmd == "book":
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        if lead.get("status") == "scrubbed": print("REFUSED: scrubbed"); return 3
        bk = {"id": f"booking-{len(state['bookings'])+1}", "lead_id": lead["id"], "when": args.when, "status": "booked-pending-human-confirmation"}
        state["bookings"].append(bk); st.save(state); print(json.dumps(bk, indent=2)); return 0
    if args.cmd == "packet":
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        qual = [q for q in state["qualifications"] if q["lead_id"] == lead["id"]]
        bk = [b for b in state["bookings"] if b["lead_id"] == lead["id"]]
        payload = {"action": "send", "to": "human-closer", "lead_id": lead["id"],
                   "message": f"Handoff packet for {lead['name']} ({lead['phone']}): source {lead['source']} on {lead['source_date']}, verified={lead['verified']}. Qualifications: {qual}. Bookings: {bk}. HUMAN CLOSES — do not auto-send or auto-close."}
        packet = {"id": f"packet-{len(state['packets'])+1}", "lead_id": lead["id"], "lead": lead,
                  "qualifications": qual, "bookings": bk, "proposed_action_payload": payload,
                  "note": "REVIEW THIS EXACT PACKET FIRST. Nothing is sent until approve --confirm <packet_id>."}
        state["packets"].append(packet); st.save(state); print(json.dumps(packet, indent=2)); return 0
    if args.cmd == "approve":
        packet = next((x for x in state["packets"] if x["id"] == args.confirm), None)
        if not packet: print("ERROR: packet not found — nothing approved"); return 2
        print("APPROVING EXACT PACKET (reviewed above / in packet command output):")
        print(json.dumps(packet["proposed_action_payload"], indent=2))
        r = G.approve_packet(state, packet); st.save(state); print(json.dumps(r, indent=2))
        print("Approved ONLY for this exact payload. The human still closes the deal."); return 0
    if args.cmd == "dial-prep":
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        # Gate first: a real call is dangerous, and the skeleton has no approval path to dial.
        chk = G.check(state, "call", {"lead_id": lead["id"], "phone": lead["phone"]})
        blocked_payload = None
        if not chk["allowed"]:
            print(f"BLOCKED (gate): {chk['reason']} — mock dial-prep only, no real call placed.")
            blocked_payload = {"lead_id": lead["id"], "phone": lead["phone"]}
        try:
            rec = MockDialer().would_call(st, lead)
        except ValueError as e:
            print(f"ERROR: {e}"); return 3
        # MockDialer already saved; re-load and re-apply the gate block so it is not lost.
        if blocked_payload is not None:
            fresh = st.load()
            if not any(e.get("hash") == chk.get("hash") for e in fresh.get("blocked_events", [])):
                fresh.setdefault("blocked_events", []).append({"action": "call", "hash": chk.get("hash"), "payload": blocked_payload})
            st.save(fresh)
        print(json.dumps(rec, indent=2)); print("MOCK ONLY: no real number was dialed."); return 0
    if args.cmd == "status":
        print(json.dumps({k: len(v) for k, v in state.items() if isinstance(v, list)}, indent=2)); return 0
    p.print_help(); return 0

if __name__ == "__main__":
    sys.exit(main())
EOF_HCF
mkdir -p framework
cat > framework/dialer.py << 'EOF_HCF'
"""Mock dialer — logs 'would call' and NEVER dials a real number.

A real Twilio/Vapi adapter is a STUB only (see adapters.py): no keys,
no calls, no network. Real calling needs keys + compliance + approval.
"""
from __future__ import annotations
from .scrub import is_scrubbed, normalize_phone

class MockDialer:
    def would_call(self, store, lead: dict) -> dict:
        state = store.load()
        if lead.get("status") == "scrubbed" or is_scrubbed(lead.get("phone", ""), state.get("scrub_numbers", [])):
            raise ValueError(f"REFUSED: {lead.get('id')} is scrubbed — never call, ever")
        rec = {"lead_id": lead.get("id"), "phone": lead.get("phone"), "action": "would_call_mock", "dialed": False}
        state.setdefault("calls", []).append(rec)
        store.save(state)
        return rec

class RealDialerStub:
    """Bring your own keys. Not wired, never called by the skeleton."""
    def call(self, *a, **k):
        raise RuntimeError("Real dialer NOT configured: add Twilio/Vapi keys, DNC API, and compliance review first. See COMPLIANCE.md.")
EOF_HCF
mkdir -p framework
cat > framework/gate.py << 'EOF_HCF'
"""Approval gate — IMMUTABLE CORE. Never bypassed by any other module.

Dangerous actions (send, call, charge, close, delete) are BLOCKED unless
an exact approval exists for that exact payload. Approval is granted only
by `approve --confirm <packet_id>` after the packet/message is shown.
There is no auto-send, auto-dial, auto-charge, or auto-close path.
"""
from __future__ import annotations
import hashlib, json

DANGEROUS = {"send", "call", "charge", "close", "delete"}

def payload_hash(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]

def check(state: dict, action: str, payload) -> dict:
    if action not in DANGEROUS:
        return {"allowed": True, "reason": "not a dangerous action"}
    h = payload_hash(payload)
    if h in state.get("approvals", []):
        return {"allowed": True, "reason": "exact approval on file", "hash": h}
    state.setdefault("blocked_events", []).append({"action": action, "hash": h, "payload": payload})
    return {"allowed": False, "reason": "blocked: no exact approval — run packet, review it, then approve --confirm <packet_id>", "hash": h}

def approve_packet(state: dict, packet: dict) -> dict:
    """Record approval for this packet's exact proposed payload. Callers
    must have shown the packet to the human before calling this."""
    payload = packet.get("proposed_action_payload") or packet
    h = payload_hash(payload)
    if h not in state["approvals"]:
        state["approvals"].append(h)
    return {"approved": True, "packet_id": packet.get("id"), "hash": h}
EOF_HCF
mkdir -p framework
cat > framework/leads.py << 'EOF_HCF'
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
EOF_HCF
mkdir -p framework
cat > framework/scrub.py << 'EOF_HCF'
"""Scrub / DNC filter — absolute. A scrubbed number is NEVER called, ever.

No removal path exists in this module by design: once a number is on the
scrub list, qualify/call/dialer all refuse it, and that refusal is logged.
"""
from __future__ import annotations
import re

def normalize_phone(phone: str) -> str:
    return re.sub(r"\D", "", phone or "")

def load_scrub_numbers(path) -> set[str]:
    import csv
    out = set()
    try:
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                p = normalize_phone(row.get("phone", ""))
                if p:
                    out.add(p)
    except FileNotFoundError:
        pass
    return out

def is_scrubbed(phone: str, scrub_numbers) -> bool:
    return normalize_phone(phone) in {normalize_phone(p) for p in scrub_numbers}

def apply_scrub(state: dict) -> dict:
    scrub = {normalize_phone(p) for p in state.get("scrub_numbers", [])}
    marked = 0
    for lead in state.get("leads", []):
        if normalize_phone(lead.get("phone", "")) in scrub and lead.get("status") != "scrubbed":
            lead["status"] = "scrubbed"
            marked += 1
    return {"scrubbed_now": marked, "total_scrubbed": sum(1 for l in state["leads"] if l.get("status") == "scrubbed")}
EOF_HCF
mkdir -p framework
cat > framework/state.py << 'EOF_HCF'
"""Local, file-first state. No database, no external service."""
from __future__ import annotations
import json
from pathlib import Path

DEFAULT_STATE = {
    "leads": [], "scrub_numbers": [], "calls": [], "qualifications": [],
    "bookings": [], "packets": [], "approvals": [], "blocked_events": [],
}

class StateStore:
    def __init__(self, root: str | Path):
        self.dir = Path(root)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / "state.json"
    def load(self) -> dict:
        if not self.path.exists():
            return {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULT_STATE.items()}
        data = json.loads(self.path.read_text())
        for k, v in DEFAULT_STATE.items():
            data.setdefault(k, list(v) if isinstance(v, list) else v)
        return data
    def save(self, state: dict) -> None:
        self.path.write_text(json.dumps(state, indent=2, sort_keys=True))
    def next_id(self, state: dict, kind: str) -> str:
        n = len([x for x in state.get(kind, [])]) + 1
        return f"{kind}-{n}"
EOF_HCF
# root
cat > framework.yaml << 'EOF_HCF'
# Hermes Caller Framework — configuration
name: hermes-caller-framework
version: 0.1.0-skeleton
dialer: mock  # NEVER set to real without keys + compliance + approval gate review
business_hours_only: true
scrub_file: data/scrub-list.csv
state_dir: .framework
EOF_HCF
# root
cat > router.yaml << 'EOF_HCF'
# Model router — FREE ONLY. Never silently upgrade to paid.
free_only: true
default: ollama-local
models:
  - name: ollama-local
    provider: ollama
    cost: 0
  - name: openrouter-free
    provider: openrouter
    cost: 0
    note: free tier only; if no free model is available, pause and tell the human — never upgrade silently.
EOF_HCF
# root
cat > run.py << 'EOF_HCF'
#!/usr/bin/env python3
import sys
from framework.cli import main
if __name__ == "__main__":
    sys.exit(main())
EOF_HCF
mkdir -p skills
cat > skills/booking.md << 'EOF_HCF'
# Booking — playbook
Offer two concrete times, confirm date/time/timezone back to the person,
send the handoff packet to the human closer for confirmation. A booking
in this skeleton is "booked-pending-human-confirmation" — the human
confirms it, not the agent.
EOF_HCF
mkdir -p skills
cat > skills/follow-up.md << 'EOF_HCF'
# Follow-up — playbook
Follow up only with people who did not opt out, within business hours,
with the exact next step from the last conversation. Every follow-up
message is a draft until a human approves the exact packet. No follow-up
to a scrubbed number, ever.
EOF_HCF
mkdir -p skills
cat > skills/objection-handling.md << 'EOF_HCF'
# Objection handling — playbook
Listen first, repeat the concern back, answer honestly, never pressure.
"Not interested" = thank them and end the call. "Remove me" = scrub
immediately, no argument, no callback. Never claim data is "special",
"exclusive", or "never called" unless you can prove source + date +
verification for that exact list.
EOF_HCF
mkdir -p skills
cat > skills/qualify.md << 'EOF_HCF'
# Qualify — playbook
Ask, in order: (1) Why are you considering selling? (motivation)
(2) When do you need this done? (timeline) (3) What price would work?
(4) What condition is the property in? Record answers verbatim where
possible. Never invent motivation, price, or timeline. Score only from
answers given. If the person says stop / do not call, stop immediately
and add them to the scrub list.
EOF_HCF
mkdir -p tests
cat > tests/__init__.py << 'EOF_HCF'

EOF_HCF
mkdir -p tests
cat > tests/test_caller.py << 'EOF_HCF'
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
EOF_HCF
cp /dev/null COPY_PASTE.md 2>/dev/null || true  # NOTE: save the file you pasted from as COPY_PASTE.md here if you want it in this folder too
python3 -m unittest discover -s tests -t .
echo "BOOTSTRAP DONE — now run the first commands in COPY_PASTE.md section 4."
```

## 4. Exact first commands to run (after the script finishes)

```bash
cd hermes-caller-framework
python3 -m unittest discover -s tests -t .
python3 run.py lead add "Jane Seller" --phone 5551234567 --source "FSBO list" --source-date 2026-10-29
python3 run.py scrub
python3 run.py dial-prep --lead lead-1
python3 run.py qualify --mock --lead lead-1 --motivation high --timeline "<30d" --price flexible --condition poor
python3 run.py book --lead lead-1 --when "2026-11-02 14:00 America/Toronto"
python3 run.py packet --lead lead-1
# READ that exact packet first, then only:
python3 run.py approve --confirm packet-1
python3 run.py status
```

## Safety rules — do not change these, ever

- Scrub/DNC/opt-out numbers are NEVER called, ever. No removal path.
- Approval gate (`framework/gate.py`) blocks send/call/charge/close/
  delete without an exact approval for that exact payload, logged.
  Approval = `approve --confirm <packet_id>` after the packet is shown.
- Mock dialer only. No real calls, no keys in the repo, no pricing
  invented, no payment system. Real calls need keys + DNC API + CRM +
  a compliance review first. The human closes every deal.
