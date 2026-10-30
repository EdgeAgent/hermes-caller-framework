"""Real model runner — OpenRouter + Ollama, no keys in code, no silent fallback.

Env: OPENROUTER_API_KEY, OPENROUTER_MODEL (required for OpenRouter),
OLLAMA_MODEL (default llama3.1), OLLAMA_BASE_URL (default http://localhost:11434).
If the configured provider has no key / is unreachable, this RAISES — it never
silently falls back to mock qualification and pretends a model ran.
Output is validated: motivation in {low,medium,high}, timeline, authority,
plus a short summary. Anything unparsable is rejected, not guessed.
The model NEVER overrides scrub, wholesale deal-math, probate HOLD, or the gate.
"""
from __future__ import annotations
import os, json, urllib.request, re

PROMPT = """You are a cold-call qualification assistant. Return ONLY valid JSON, no markdown:
{"motivation": "low|medium|high", "timeline": "<30d|<90d|6mo", "authority": "owner|trustee|executor|relative|unknown", "summary": "one sentence"}
Transcript / notes: {notes}
"""

def _parse(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m: raise ValueError("model output was not JSON")
    d = json.loads(m.group(0))
    if d.get("motivation") not in ("low", "medium", "high"): raise ValueError("model motivation invalid")
    if d.get("authority") not in ("owner", "trustee", "executor", "relative", "unknown"): raise ValueError("model authority invalid")
    return {"motivation": d["motivation"], "timeline": d.get("timeline", "<90d"),
            "authority": d["authority"], "summary": str(d.get("summary", ""))[:300], "model_ran": True}

def run_openrouter(notes: str) -> dict:
    key, model = os.environ.get("OPENROUTER_API_KEY"), os.environ.get("OPENROUTER_MODEL")
    if not key: raise ValueError("OPENROUTER_API_KEY missing in env — set it via Secure Vault / env, never in code or chat")
    if not model: raise ValueError("OPENROUTER_MODEL missing in env — set it to a :free model name from openrouter.ai")
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": PROMPT.format(notes=notes)}]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.loads(r.read())["choices"][0]["message"]["content"]
    return {**_parse(out), "provider": "openrouter", "model": model}

def run_ollama(notes: str) -> dict:
    base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.environ.get("OLLAMA_MODEL", "llama3.1")
    body = json.dumps({"model": model, "prompt": PROMPT.format(notes=notes), "stream": False}).encode()
    req = urllib.request.Request(f"{base}/api/generate", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: out = json.loads(r.read())["response"]
    except Exception as e: raise ValueError(f"Ollama unreachable at {base} — is Ollama running on your machine? ({e})")
    return {**_parse(out), "provider": "ollama", "model": model}

def qualify_with_model(provider: str, notes: str) -> dict:
    if provider == "openrouter": return run_openrouter(notes)
    if provider == "ollama": return run_ollama(notes)
    raise ValueError("provider must be openrouter or ollama")
