import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile
from pathlib import Path
from framework.calendar import book, list_bookings, cancel
from framework.crm import export_csv
from framework.dashboard import render
def test_calendar_books_and_conflicts():
    with tempfile.TemporaryDirectory() as d:
        r = book(Path(d), "5550101234", "dental", "2026-11-02 10:00"); assert r["ok"] and r["status"].startswith("booked")
        r2 = book(Path(d), "5550109999", "dental", "2026-11-02 10:00"); assert not r2["ok"] and r2["action"] == "slot_taken"
        assert len(list_bookings(Path(d))) == 1
def test_calendar_cancel():
    with tempfile.TemporaryDirectory() as d:
        book(Path(d), "5550101234", "dental", "2026-11-02 10:00"); assert cancel(Path(d), "2026-11-02 10:00", "5550101234")["ok"]
        assert list_bookings(Path(d)) == []
def test_crm_export_has_header_and_lead():
    csv = export_csv({"leads": [{"id": "lead-1", "name": "Jane", "phone": "555", "source": "FSBO", "source_date": "2026-10-30", "verified": "yes", "status": "new"}], "bookings": []})
    assert "lead_id,name,phone" in csv and "Jane" in csv
def test_dashboard_renders_without_calling_anything():
    with tempfile.TemporaryDirectory() as d:
        html = render(Path(d)); assert "Hermes Caller" in html and "Read-only" in html and "Leads" in html
def test_install_script_exists_and_is_executable():
    import stat; p = Path("install.sh"); assert p.exists() and bool(p.stat().st_mode & stat.S_IXUSR)
def test_no_skeleton_badge_claim():
    assert "Status: Skeleton" not in open("README.md").read()
if __name__ == "__main__":
    for n, fn in list(globals().items()):
        if n.startswith("test_"): fn(); print(f"PASS {n}")
    print("ALL PASS")
