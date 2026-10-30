"""CRM export — real CSV a real CRM can import. No invented CRM connection."""
from __future__ import annotations
import csv, io
def export_csv(state: dict) -> str:
    out = io.StringIO(); w = csv.writer(out)
    w.writerow(["lead_id", "name", "phone", "source", "source_date", "verified", "status"])
    for l in state.get("leads", []):
        w.writerow([l["id"], l["name"], l["phone"], l["source"], l["source_date"], l["verified"], l["status"]])
    w.writerow([]); w.writerow(["booking_lead_id", "when", "status"])
    for b in state.get("bookings", []):
        w.writerow([b["lead_id"], b["when"], b["status"]])
    return out.getvalue()
