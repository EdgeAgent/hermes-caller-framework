"""Local, file-first state. No database, no external service."""
from __future__ import annotations
import json
from pathlib import Path

DEFAULT_STATE = {
    "leads": [], "scrub_numbers": [], "calls": [], "qualifications": [],
    "bookings": [], "packets": [], "approvals": [], "blocked_events": [],
}

class StateStore:
    def __init__(self, root: str | Path):
        self.dir = Path(root)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / "state.json"
    def load(self) -> dict:
        if not self.path.exists():
            return {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULT_STATE.items()}
        data = json.loads(self.path.read_text())
        for k, v in DEFAULT_STATE.items():
            data.setdefault(k, list(v) if isinstance(v, list) else v)
        return data
    def save(self, state: dict) -> None:
        self.path.write_text(json.dumps(state, indent=2, sort_keys=True))
    def next_id(self, state: dict, kind: str) -> str:
        n = len([x for x in state.get(kind, [])]) + 1
        return f"{kind}-{n}"
