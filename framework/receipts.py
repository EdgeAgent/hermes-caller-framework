"""Hash-chained receipts — PROOF-style, local file, tamper-evident.
Every qualification / call / approval appends one JSONL line with prev_hash.
If a line is edited, the chain breaks on verify. No real money, no PII beyond
what the lead record already holds. File: .framework/receipts.jsonl
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

def _hash(rec: dict) -> str:
    return hashlib.sha256(json.dumps(rec, sort_keys=True, default=str).encode()).hexdigest()

def append(root: Path, kind: str, data: dict) -> dict:
    path = Path(root) / "receipts.jsonl"; prev = "GENESIS"
    if path.exists() and path.read_text().strip():
        prev = json.loads(path.read_text().strip().splitlines()[-1])["hash"]
    rec = {"kind": kind, "prev_hash": prev, "data": data}; rec["hash"] = _hash(rec)
    with open(path, "a") as f: f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec

def verify(root: Path) -> dict:
    path = Path(root) / "receipts.jsonl"
    if not path.exists(): return {"ok": True, "count": 0}
    prev, count = "GENESIS", 0
    for line in path.read_text().strip().splitlines():
        rec = json.loads(line)
        if rec["prev_hash"] != prev: return {"ok": False, "count": count, "failed_at": count}
        h = rec.pop("hash"); ok = _hash(rec) == h; rec["hash"] = h
        if not ok: return {"ok": False, "count": count, "failed_at": count}
        prev, count = h, count + 1
    return {"ok": True, "count": count}
