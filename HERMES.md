# Hermes handoff — how to hand this to Hermes

Hermes (Kevin's lead-gen agent) can run this framework as-is, locally,
with no new service. Copy this whole folder into Hermes's workspace,
or point Hermes at this repo folder. It is Python, no dependencies.

## Folder layout
- `run.py` — entry point: `python run.py <command>`
- `framework/` — state, scrub, gate, leads, dialer, real_dialer, model, personas, wholesale, inbound, receipts, doctor, cli
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
python run.py doctor
python run.py persona list
python run.py inbound --persona dental --caller 5550101234 --intent book --slot "2026-11-02 10:00"
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
