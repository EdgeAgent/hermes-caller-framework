# Hermes Caller v1.0 — Production Readiness

## What is production-ready
- CLI: lead, scrub, qualify (mock), model-qualify (real OpenRouter/Ollama, validated JSON), wholesale, persona list/show/qualify, packet, approve, dial-prep, call (dry-run + real gated), status, doctor
- Gates: scrub never-call, packet approval for exact payload, probate HOLD, wholesale buyer-profit gate, clinic strict gate
- Receipts: .framework/receipts.jsonl, hash-chained, verify breaks on tamper
- Config: .env.example only, keys in env, never in code/chat/repo
- Tests: 43 passing (7 core + 5 branding + 8 wholesale + 5 real-dialer + 10 personas + 8 production)

## What is NOT done (your steps, in order)
1. Twilio or Vapi account, your own, with a verified number
2. Keys in env / Secure Vault, never chat
3. Compliance review + DNC check for your list
4. First call to YOUR test number, with an approved packet
5. Only then, live list, one approved packet per call, human closes every deal

## Runbook
python3 run.py doctor
python3 run.py lead add "Name" --phone ... --source ... --source-date ...
python3 run.py scrub
python3 run.py persona qualify --persona wholesale --lead lead-1 ...
python3 run.py packet --lead lead-1   # review exact packet
python3 run.py approve --confirm packet-1
python3 run.py call --lead lead-1 --provider twilio --real --packet packet-1
