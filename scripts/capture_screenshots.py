"""Regenerate honest screenshots: run the real CLI in a /tmp copy, capture
exact text output, render it to PNG with a monospace font.
Mock dialer only, $0, no real calls. Run from repo root:
  python3 scripts/capture_screenshots.py
Outputs: docs/screenshots/*.txt + *.png
"""
import shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DEMO = Path("/tmp/hermes-caller-demo")
OUT = ROOT / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

if DEMO.exists():
    shutil.rmtree(DEMO)
shutil.copytree(ROOT, DEMO, ignore=shutil.ignore_patterns("__pycache__", ".framework", "docs"))


def run(*args):
    r = subprocess.run([sys.executable, str(DEMO / "run.py"), *args],
                       capture_output=True, text=True, cwd=str(DEMO))
    return f"$ python run.py {' '.join(args)}\n{r.stdout}{r.stderr}"


# (a) status / lead list
s1 = run("lead", "add", "Jane Seller", "--phone", "5551234567",
         "--source", "FSBO list", "--source-date", "2026-10-29")
s1 += run("lead", "list")
s1 += run("status")
# (b) scrub + dial-prep refusal: scrubbed lead first, then a clean lead prep
s2 = run("lead", "add", "Scrubbed Seller", "--phone", "5550001111",
         "--source", "FSBO list", "--source-date", "2026-10-29")
s2 += run("scrub")
s2 += run("dial-prep", "--lead", "lead-2")
s2 += run("dial-prep", "--lead", "lead-1")
# (c) qualify + book + packet + approve
s3 = run("qualify", "--mock", "--lead", "lead-1", "--motivation", "high",
         "--timeline", "<30d", "--price", "flexible", "--condition", "poor")
s3 += run("book", "--lead", "lead-1", "--when", "2026-11-02 14:00 America/Toronto")
s3 += run("packet", "--lead", "lead-1")
s3 += run("approve", "--confirm", "packet-1")

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def render(text, path, title):
    (OUT / (Path(path).stem + ".txt")).write_text(text)
    font = ImageFont.truetype(FONT, 14)
    bfont = ImageFont.truetype(BOLD, 15)
    lines = text.splitlines()
    tmp = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(tmp)
    cw = max((d.textlength(l, font=font) for l in lines), default=100)
    w = min(1400, int(cw + 40))
    h = 44 + len(lines) * 19 + 30
    img = Image.new("RGB", (w, h), (13, 27, 42))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 36], fill=(21, 40, 61))
    d.text((16, 9), title, font=bfont, fill=(45, 212, 191))
    y = 44
    for line in lines:
        col = (230, 237, 243)
        if "REFUSED" in line or "scrubbed" in line:
            col = (255, 123, 114)
        if "would_call_mock" in line or '"grade": "A"' in line:
            col = (63, 185, 80)
        if line.startswith("$ "):
            col = (255, 214, 90)
        d.text((16, y), line, font=font, fill=col)
        y += 19
    d.text((16, h - 24), "Skeleton capture — mock dialer, $0, no real calls.", font=font, fill=(139, 148, 158))
    img.save(OUT / path)
    print("wrote", path, img.size)


render(s1, "status-leads.png", "HERMES CALLER — LEADS + STATUS")
render(s2, "scrub-dialprep.png", "HERMES CALLER — SCRUB + DIAL PREP (MOCK)")
render(s3, "qualify-book-packet.png", "HERMES CALLER — QUALIFY + BOOK + PACKET")
print("done")
