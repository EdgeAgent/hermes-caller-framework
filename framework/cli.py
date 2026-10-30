"""CLI: lead add/list, scrub, qualify --mock, book, packet, approve, dial-prep."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .state import StateStore
from . import leads as L, scrub as S, gate as G
from .dialer import MockDialer
from .wholesale import qualify_wholesale, SCRIPT
from .real_dialer import place_real_call
from .personas import list_personas, get_persona, score_persona
from .model import qualify_with_model
from .doctor import check as doctor_check
from .receipts import append as receipt_append
from .inbound import handle_inbound
from .warrior import objection_response, followup, advance_pipeline, warrior_score
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
    w = sub.add_parser("wholesale"); w.add_argument("--lead", required=True); w.add_argument("--mock", action="store_true")
    w.add_argument("--motivation", default="medium"); w.add_argument("--timeline", default="<90d")
    w.add_argument("--authority", default="owner"); w.add_argument("--probate", action="store_true")
    w.add_argument("--price", type=float, required=True); w.add_argument("--repairs", type=float, default=0)
    w.add_argument("--arv", type=float, required=True); w.add_argument("--fee", type=float, required=True)
    ws = sub.add_parser("wholesale-script"); ws.add_argument("--part", default="opening")
    c = sub.add_parser("call"); c.add_argument("--lead", required=True); c.add_argument("--provider", default="twilio")
    c.add_argument("--dry-run", action="store_true"); c.add_argument("--real", action="store_true"); c.add_argument("--packet", default=None)
    pe = sub.add_parser("persona"); pea = pe.add_subparsers(dest="op")
    pea.add_parser("list")
    sh = pea.add_parser("show"); sh.add_argument("--persona", required=True)
    pq = pea.add_parser("qualify"); pq.add_argument("--persona", required=True); pq.add_argument("--lead", required=True)
    pq.add_argument("--motivation", default="medium"); pq.add_argument("--timeline", default="<90d")
    pq.add_argument("--budget-fit", default="unknown"); pq.add_argument("--area-fit", default="unknown"); pq.add_argument("--capacity-fit", default="unknown")
    d = sub.add_parser("doctor")
    mq = sub.add_parser("model-qualify"); mq.add_argument("--lead", required=True); mq.add_argument("--provider", default="openrouter"); mq.add_argument("--notes", required=True)
    ib = sub.add_parser("inbound"); ib.add_argument("--persona", default="walkin_clinic"); ib.add_argument("--caller", required=True)
    ib.add_argument("--intent", default="greet"); ib.add_argument("--slot", default=None); ib.add_argument("--existing-number", default=None)
    wa = sub.add_parser("warrior"); wa.add_argument("--objection", default=None); wa.add_argument("--followup-day", type=int, default=None); wa.add_argument("--stage", default="new"); wa.add_argument("--to", default=None); wa.add_argument("--activities", type=int, default=0); wa.add_argument("--qualified", action="store_true"); wa.add_argument("--booked", action="store_true")
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
    if args.cmd == "wholesale":
        if not args.mock: print("ERROR: wholesale skeleton only supports --mock (no real calls)."); return 2
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        if lead.get("status") == "scrubbed" or S.is_scrubbed(lead["phone"], state["scrub_numbers"]):
            print(f"REFUSED: {lead['id']} is scrubbed — never call, ever"); return 3
        rec = {"lead_id": lead["id"], "mode": "wholesale", "mock": True, "motivation": args.motivation,
               "timeline": args.timeline, "authority": args.authority, "probate": args.probate,
               **qualify_wholesale(args.motivation, args.timeline, args.authority, args.probate, args.price, args.repairs, args.arv, args.fee)}
        state["qualifications"].append(rec); lead["status"] = "wholesale-" + rec["verdict"].lower(); st.save(state)
        print(json.dumps(rec, indent=2)); return 0
    if args.cmd == "wholesale-script":
        print(SCRIPT.get(args.part, "ERROR: part must be opening|motivation|open_math|probate|close_human")); return 0
    if args.cmd == "call":
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        if args.real and not any(x["id"] == args.packet for x in state["packets"]):
            print("BLOCKED: real call needs an existing approved packet id — run packet, review it, approve it first."); return 3
        r = place_real_call(state, lead, provider=args.provider, dry_run=not args.real, approved_packet_id=args.packet)
        if args.real and r.get("dialed"): receipt_append(st.dir, "real-call", r)
        print(json.dumps(r, indent=2))
        if not args.real: print("DRY RUN — no call placed. First real call needs: provider account + keys in env + approved packet + YOUR test number first."); return 0
        return 0 if r.get("dialed") else 3
    if args.cmd == "persona" and args.op == "list":
        print("\n".join(list_personas())); return 0
    if args.cmd == "persona" and args.op == "show":
        import json as _j; print(_j.dumps(get_persona(args.persona), indent=2)); return 0
    if args.cmd == "persona" and args.op == "qualify":
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        if lead.get("status") == "scrubbed" or S.is_scrubbed(lead["phone"], state["scrub_numbers"]):
            print(f"REFUSED: {lead['id']} is scrubbed — never call, ever"); return 3
        rec = {"lead_id": lead["id"], "mock": True, **score_persona(args.persona, args.motivation, args.timeline, args.budget_fit, args.area_fit, args.capacity_fit)}
        state["qualifications"].append(rec); st.save(state); print(json.dumps(rec, indent=2)); return 0
    if args.cmd == "doctor":
        print(json.dumps(doctor_check(), indent=2)); return 0
    if args.cmd == "model-qualify":
        lead = next((x for x in state["leads"] if x["id"] == args.lead), None)
        if not lead: print("ERROR: lead not found"); return 2
        if lead.get("status") == "scrubbed" or S.is_scrubbed(lead["phone"], state["scrub_numbers"]):
            print(f"REFUSED: {lead['id']} is scrubbed — never call, ever"); return 3
        try: m = qualify_with_model(args.provider, args.notes)
        except ValueError as e: print(f"ERROR: {e}"); return 2
        rec = {"lead_id": lead["id"], "model": True, **m}; state["qualifications"].append(rec); st.save(state)
        receipt_append(st.dir, "model-qualify", rec); print(json.dumps(rec, indent=2)); return 0
    if args.cmd == "inbound":
        r = handle_inbound(args.caller, args.persona, args.intent, slot=args.slot, existing_number=args.existing_number)
        receipt_append(st.dir, "inbound", r); print(json.dumps(r, indent=2)); return 0
    if args.cmd == "warrior":
        out = {}
        if args.objection: out["objection"] = objection_response(args.objection)
        if args.followup_day is not None: out["followup"] = followup(args.followup_day, args.stage)
        if args.to: out["pipeline"] = advance_pipeline(args.stage, args.to)
        out["score"] = warrior_score(args.activities, args.qualified, args.booked)
        print(json.dumps(out, indent=2)); return 0
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
