"""Local dashboard — stdlib only, no login, no animation, no external calls.
Serves one page at http://127.0.0.1:8768 : leads, qualifications, bookings,
calendar, packets, receipts verification, doctor status. Read-only view of
local state — it NEVER sends, calls, or approves. Approvals stay CLI-only.
"""
from __future__ import annotations
import json, html
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from .state import StateStore
from .receipts import verify
from .calendar import list_bookings

def render(root: Path) -> str:
    st = StateStore(root); state = st.load()
    def table(rows, cols):
        if not rows: return "<p>None yet.</p>"
        th = "".join(f"<th>{c}</th>" for c in cols)
        tr = "".join("<tr>" + "".join(f"<td>{html.escape(str(r.get(c,'')))}</td>" for c in cols) + "</tr>" for r in rows)
        return f"<table border=1 cellpadding=6><tr>{th}</tr>{tr}</table>"
    return f"""<!doctype html><html><head><meta charset=utf-8><title>Hermes Caller — Dashboard</title>
<style>body{{font-family:system-ui,sans-serif;max-width:1000px;margin:30px auto;padding:0 20px}}h2{{margin-top:40px}}</style></head><body>
<h1>Hermes Caller — Dashboard</h1><p>Local only. Read-only. Approvals, sends and calls stay CLI-only, gated.</p>
<p>Receipts: {verify(root)}</p>
<h2>Leads</h2>{table(state['leads'], ['id','name','phone','source','status'])}
<h2>Qualifications</h2>{table(state['qualifications'], ['lead_id','score','verdict','persona'])}
<h2>Bookings (state)</h2>{table(state['bookings'], ['id','lead_id','when','status'])}
<h2>Calendar (real file)</h2>{table(list_bookings(root), ['caller','persona','slot','status'])}
<h2>Packets</h2>{table(state['packets'], ['id','lead_id'])}
<p>Run: python3 run.py doctor &nbsp;|&nbsp; python3 run.py packet --lead lead-1 &nbsp;|&nbsp; python3 run.py approve --confirm packet-1</p>
</body></html>"""

def serve(root: Path, port: int = 8768):
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            body = render(root).encode(); self.send_response(200); self.send_header("Content-Type", "text/html"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        def log_message(self, *a): pass
    print(f"Dashboard at http://127.0.0.1:{port} — read-only, Ctrl+C to stop.")
    HTTPServer(("127.0.0.1", port), H).serve_forever()
