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

## Copy-paste start here

**[COPY_PASTE.md](COPY_PASTE.md) — copy that one file into Hermes (or a new repo/chat) and it recreates this whole framework, with the brief, file list, bootstrap script, and first commands. No manual edits needed.**

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
