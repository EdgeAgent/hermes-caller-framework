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
