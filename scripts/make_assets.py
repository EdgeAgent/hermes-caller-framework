"""Original branding assets for Hermes Caller — PIL only, no external images,
no copied logos. Run from repo root: python3 scripts/make_assets.py
Outputs: docs/assets/icon.png (512x512), hero.png (1200x400),
favicon.png (64x64), workflow.png, architecture.png.
Colours: deep navy background, teal/green accent, amber for the gate.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = (13, 27, 42)
NAVY2 = (21, 40, 61)
TEAL = (45, 212, 191)
GREEN = (63, 185, 80)
AMBER = (255, 214, 90)
WHITE = (230, 237, 243)
GREY = (139, 148, 158)
RED = (255, 123, 114)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def centre(d, y, text, f, fill, w):
    d.text((w / 2, y), text, font=f, fill=fill, anchor="ma")


def draw_phone(d, cx, cy, s, body=(32, 54, 79), accent=TEAL):
    """Original agent-phone glyph: a smartphone with a headset arc above it."""
    # headset band
    d.arc([cx - s * 0.95, cy - s * 1.35, cx + s * 0.95, cy + s * 0.35], start=180, end=360, fill=accent, width=max(6, int(s * 0.12)))
    # ear pads
    d.rounded_rectangle([cx - s * 1.05, cy - s * 0.45, cx - s * 0.65, cy + s * 0.15], radius=s * 0.12, fill=accent)
    d.rounded_rectangle([cx + s * 0.65, cy - s * 0.45, cx + s * 1.05, cy + s * 0.15], radius=s * 0.12, fill=accent)
    # smartphone body
    d.rounded_rectangle([cx - s * 0.55, cy - s * 0.35, cx + s * 0.55, cy + s * 0.95], radius=s * 0.15, fill=accent)
    d.rounded_rectangle([cx - s * 0.42, cy - s * 0.18, cx + s * 0.42, cy + s * 0.65], radius=s * 0.08, fill=NAVY)
    # mic dot / keypad dots on screen
    for dx, dy in ((-0.2, 0.15), (0.2, 0.15), (-0.2, 0.4), (0.2, 0.4)):
        d.ellipse([cx + dx * s - s * 0.06, cy + dy * s - s * 0.06, cx + dx * s + s * 0.06, cy + dy * s + s * 0.06], fill=TEAL)


# --- icon 512x512: navy disc, teal phone mark ---
img = Image.new("RGB", (512, 512), NAVY)
d = ImageDraw.Draw(img)
d.ellipse([56, 56, 456, 456], fill=NAVY2, outline=TEAL, width=6)
draw_phone(d, 256, 250, 110)
centre(d, 365, "HERMES CALLER", font(26, True), WHITE, 512)
img.save(OUT / "icon.png")

# --- favicon 64x64: same mark, simplified ---
img = Image.new("RGB", (64, 64), NAVY)
d = ImageDraw.Draw(img)
d.ellipse([4, 4, 60, 60], fill=NAVY2, outline=TEAL, width=3)
draw_phone(d, 32, 31, 13)
img.save(OUT / "favicon.png")

# --- hero banner 1200x400 ---
img = Image.new("RGB", (1200, 400), NAVY)
d = ImageDraw.Draw(img)
d.rectangle([0, 300, 1200, 400], fill=NAVY2)
draw_phone(d, 130, 150, 70)
d.text((250, 80), "HERMES CALLER", font=font(72, True), fill=WHITE)
d.text((250, 165), "Agent Phone for Lead Closing", font=font(32), fill=TEAL)
d.text((250, 215), "Scrub first. Qualify. Book. Human closes.", font=font(26), fill=GREY)
d.text((40, 325), "Mock dialer only  ·  Approval gate  ·  Local-first  ·  $0 in skeleton", font=font(22), fill=GREY)
img.save(OUT / "hero.png")


def box(d, x, y, w, h, title, sub, fill=NAVY2, border=TEAL):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fill, outline=border, width=3)
    centre(d, y + 14, title, font(20, True), WHITE, x * 2 + w)  # anchor trick below
    # redraw centred properly
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=fill, outline=border, width=3)
    tw = d.textlength(title, font=font(20, True))
    d.text((x + (w - tw) / 2, y + 12), title, font=font(20, True), fill=WHITE)
    tw = d.textlength(sub, font=font(15))
    d.text((x + (w - tw) / 2, y + 48), sub, font=font(15), fill=GREY)


def arrow(d, x1, y, x2, label=""):
    d.line([x1, y, x2, y], fill=TEAL, width=4)
    d.polygon([(x2, y), (x2 - 12, y - 7), (x2 - 12, y + 7)], fill=TEAL)
    if label:
        tw = d.textlength(label, font=font(14, True))
        d.text(((x1 + x2 - tw) / 2, y - 24), label, font=font(14, True), fill=AMBER)


# --- workflow diagram: lead -> scrub -> qualify -> score -> book -> packet -GATE-> human close ---
W, H = 1400, 460
img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
centre(d, 16, "HOW A LEAD MOVES — diagram, not a screenshot", font(22, True), WHITE, W)
steps = [("LEAD IN", "source + date"), ("SCRUB", "DNC / opt-out"), ("QUALIFY", "motivation · time"), ("SCORE", "A / B / C"), ("BOOK", "appointment"), ("PACKET", "for closer")]
bw, bh, gap, y = 165, 110, 28, 120
for i, (t, s) in enumerate(steps):
    x = 20 + i * (bw + gap)
    box(d, x, y, bw, bh, t, s, border=TEAL if t != "SCRUB" else RED)
    if i < len(steps) - 1:
        arrow(d, x + bw, y + bh // 2, x + bw + gap)
# gate row
d.rounded_rectangle([20, 300, 1380, 400], radius=14, fill=(60, 40, 10), outline=AMBER, width=3)
centre(d, 315, "APPROVAL GATE — packet shown first, human runs approve --confirm <packet>", font(22, True), AMBER, W)
centre(d, 355, "No approval = no send, no call, no charge, no close. Then: HUMAN CLOSES.", font(20), WHITE, W)
img.save(OUT / "workflow.png")

# --- architecture diagram: six boxes ---
W, H = 1400, 560
img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)
centre(d, 16, "ARCHITECTURE — diagram, not a screenshot", font(22, True), WHITE, W)
boxes = [
    ("CLI", "run.py commands", 20, 90),
    ("SCRUB", "DNC / opt-out", 280, 90),
    ("GATE", "approve gate", 540, 90),
    ("DIALER (MOCK)", "would_call only", 800, 90),
    ("SKILLS", "qualify · book", 1060, 90),
    ("STATE / BRAIN", ".framework/state", 540, 300),
]
for t, s, x, y in boxes:
    box(d, x, y, 220, 110, t, s, border=AMBER if t == "GATE" else TEAL)
for x1, x2 in ((240, 280), (500, 540), (760, 800), (1020, 1060)):
    arrow(d, x1, 145, x2)
# state links
d.line([650, 200, 650, 300], fill=TEAL, width=4)
d.polygon([(650, 300), (643, 288), (657, 288)], fill=TEAL)
centre(d, 440, "Every stage reads + writes the same local state. Nothing leaves the machine.", font(20), GREY, W)
img.save(OUT / "architecture.png")
print("wrote", sorted(p.name for p in OUT.iterdir()))
