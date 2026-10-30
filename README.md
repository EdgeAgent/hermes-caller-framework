# Hermes Caller — Agent Phone / Cold-Caller Framework

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-2dd4bf?style=flat-square)
![Local-first](https://img.shields.io/badge/Local--first-yes-2dd4bf?style=flat-square)
![Tests: 7 passing](https://img.shields.io/badge/Tests-7%20passing-3fb950?style=flat-square)
![Status: Skeleton](https://img.shields.io/badge/Status-skeleton-ffd65a?style=flat-square)
![Dialer: Mock only](https://img.shields.io/badge/Dialer-mock%20only-ff7b72?style=flat-square)

<p align="center">
  <img src="docs/assets/hero.png" alt="Hermes Caller — Agent Phone for Lead Closing banner" width="100%" />
</p>

<p align="center">
  <img src="docs/assets/icon.png" alt="Hermes Caller icon" width="96" />
</p>

## What this is — is this an agent phone / cold caller?

Yes. Plainly: **this IS an agent-phone / cold-caller framework.**
An agent prepares the dial list, qualifies sellers, scores them,
books appointments, and hands a packet to a human closer — the human
closes the deal. That is the RunItRemote-style job, as a framework
you can hand to Hermes.

Honest limit, right up front: **in this skeleton it is NOT a real
phone dialer.** The dialer is mock only (`would_call_mock`,
`dialed: false`, $0). No real call is placed, no real sale is made.
Real calling needs Twilio/Vapi keys, a DNC API check, a CRM, and a
compliance review first — see "What to add next for real calls" below.

Parallel to Battle Court, built for Hermes: a lead list goes in, scrub
filter runs, qualification scores it, booking is drafted, and a handoff
packet goes to the human closer. The human closes. The agent prepares,
scores, and drafts — autonomously, up to a hard gate.

## Workflow — how a lead moves (diagram, not a screenshot)

![Workflow diagram](docs/assets/workflow.png)

1. Lead list in (CSV / `lead add`) — source + source date required
2. Scrub / DNC / opt-out filter — scrubbed numbers are NEVER called
3. Call script — motivation, timeline, price, condition (skills/)
4. Score — A / B / C from answers given, never invented
5. Book appointment — pending human confirmation
6. Handoff packet — for the human closer
7. Follow-up sequence — drafts only, until approved

## Architecture — what talks to what (diagram, not a screenshot)

![Architecture diagram](docs/assets/architecture.png)

CLI → Scrub → Gate → Dialer (mock) → Skills, all reading and writing
the same local state (`.framework/state.json`). Nothing leaves the
machine. The gate sits between the packet and any send/call/charge/
close — no approval, no action.

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

## Screenshots — the actual CLI (skeleton, mock, $0, no real calls)

These are real captures of the real CLI running in a clean demo
folder — text output first, rendered to PNG. Regenerate them with
`python3 scripts/capture_screenshots.py`. Branding art is generated
with `python3 scripts/make_assets.py` (PIL only, original art, no
copied logos).

### Leads + status

![Leads and status screenshot](docs/screenshots/status-leads.png)

Text capture: [`docs/screenshots/status-leads.txt`](docs/screenshots/status-leads.txt)

### Scrub + dial-prep (mock refusal for a scrubbed lead)

![Scrub and dial-prep screenshot](docs/screenshots/scrub-dialprep.png)

Text capture: [`docs/screenshots/scrub-dialprep.txt`](docs/screenshots/scrub-dialprep.txt)

### Qualify + book + packet

![Qualify, book and packet screenshot](docs/screenshots/qualify-book-packet.png)

Text capture: [`docs/screenshots/qualify-book-packet.txt`](docs/screenshots/qualify-book-packet.txt)

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
