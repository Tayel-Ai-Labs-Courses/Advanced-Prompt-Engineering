#!/usr/bin/env python3
"""PROMPT ENGINEER #2 — THE BUILD. Lessons 05-10, comic-book deck.
Tayel AI Labs. Big glossy iconic emblems rather than technical diagrams."""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SUP = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Impact", SUP + "Impact.ttf"))
pdfmetrics.registerFont(TTFont("Comic", SUP + "Comic Sans MS.ttf"))
pdfmetrics.registerFont(TTFont("ComicB", SUP + "Comic Sans MS Bold.ttf"))

W, H = landscape(A4)
OUT = ("/Users/adamyasser/Desktop/Mac/TAYEL AI LABS/COURSES/"
       "Advanced-Prompt-Engineering/presentations/"
       "session-2-the-build-comic.pdf")

RED, YEL, BLU = HexColor("#E8231F"), HexColor("#FFD400"), HexColor("#1B6FE0")
CYAN, GRN, PUR = HexColor("#3EC8F0"), HexColor("#35B44A"), HexColor("#7B3FA0")
ORG, INK, PAPER = HexColor("#FF8A1F"), HexColor("#121212"), HexColor("#FFF6E3")
DOT, WHITE, STEEL = HexColor("#EADCBE"), HexColor("#FFFFFF"), HexColor("#9AA7B4")
DARKBG, GOLD = HexColor("#1A1030"), HexColor("#F2B705")

REPO = "https://github.com/Tayel-Ai-Labs-Courses/Advanced-Prompt-Engineering"
B = REPO + "/blob/main"
LK = {k: B + v for k, v in {
    "05": "/lessons/05-roles-and-personas.md",
    "06": "/lessons/06-structured-output.md",
    "07": "/lessons/07-constraints-and-guardrails.md",
    "08": "/lessons/08-prompt-chaining-pipelines.md",
    "09": "/lessons/09-retrieval-rag.md",
    "10": "/lessons/10-agents-and-tools.md",
    "ex": "/examples/weak-vs-good.md",
    "tpl": "/templates/prompt-template.md",
    "maps": "/system-maps/pipelines.md",
    "asg": "/assignments/session-2-the-build.md",
}.items()}

c = canvas.Canvas(OUT, pagesize=landscape(A4))
c.setTitle("PROMPT ENGINEER #2: THE BUILD | Tayel AI Labs")
c.setAuthor("Tayel AI Labs")
PAGE = [0]
TOP, BOT = H - 84, 112

# ───────────────────────── primitives ─────────────────────────
def halftone(x, y, w, h, color=DOT, step=11, r=1.7):
    c.saveState()
    p = c.beginPath(); p.rect(x, y, w, h); c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(color); j = 0; yy = y
    while yy < y + h:
        xx = x + (step/2 if j % 2 else 0)
        while xx < x + w:
            c.circle(xx, yy, r, fill=1, stroke=0); xx += step
        yy += step; j += 1
    c.restoreState()

def rays(cx, cy, r, color, n=22, spread=1.0):
    c.saveState(); c.setFillColor(color)
    for i in range(n):
        a = 2*math.pi*i/n
        p = c.beginPath(); p.moveTo(cx, cy)
        p.lineTo(cx + r*math.cos(a - spread/n), cy + r*math.sin(a - spread/n))
        p.lineTo(cx + r*math.cos(a + spread/n), cy + r*math.sin(a + spread/n))
        p.close(); c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def panel(x, y, w, h, fill=PAPER, lw=3.2, shadow=True, dots=False, dotc=DOT):
    if shadow:
        c.setFillColor(INK); c.rect(x+5, y-5, w, h, fill=1, stroke=0)
    c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(lw)
    c.rect(x, y, w, h, fill=1, stroke=1)
    if dots:
        halftone(x, y, w, h, dotc)
        c.setStrokeColor(INK); c.setLineWidth(lw); c.rect(x, y, w, h, fill=0, stroke=1)

def otext(x, y, s, size, fill=YEL, stroke=INK, lw=2.4, font="Impact", center=False):
    c.saveState()
    t = c.beginText()
    t.setTextOrigin(x - (pdfmetrics.stringWidth(s, font, size)/2 if center else 0), y)
    t.setFont(font, size)
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(lw)
    t.setTextRenderMode(2); t.textLine(s); c.drawText(t)
    c.restoreState()

def txt(x, y, s, size=11, color=INK, font="Comic", center=False, right=False):
    c.setFillColor(color); c.setFont(font, size)
    if center: c.drawCentredString(x, y, s)
    elif right: c.drawRightString(x, y, s)
    else: c.drawString(x, y, s)

def caption(x, y, w, s, size=11.5, fill=YEL, color=INK, pad=9, font="ComicB"):
    lines = simpleSplit(s, font, size, w - 2*pad)
    h = len(lines)*(size+4) + 2*pad - 4
    c.setFillColor(INK); c.rect(x+3, y-h-3, w, h, fill=1, stroke=0)
    c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(2.4)
    c.rect(x, y-h, w, h, fill=1, stroke=1)
    yy = y - pad - size + 3
    for ln in lines:
        txt(x+pad, yy, ln, size, color, font); yy -= size+4
    return y - h

def bubble(cx, cy, w, s, size=11, tail=(0, -1), fill=WHITE, color=INK,
           font="ComicB", pad=11):
    lines = simpleSplit(s, font, size, w - 2*pad)
    h = len(lines)*(size+4) + 2*pad - 4
    x, y = cx - w/2, cy - h/2
    tx, ty = tail
    if tx or ty:
        c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(2.6)
        bx, by = cx + tx*w*0.26, cy + ty*h*0.5
        p = c.beginPath(); p.moveTo(bx-11, by); p.lineTo(bx+11, by)
        p.lineTo(bx + tx*18 + 4, by + ty*28); p.close()
        c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(2.6)
    c.roundRect(x, y, w, h, 13, fill=1, stroke=1)
    if tx or ty:
        c.setFillColor(fill)
        c.rect(cx + tx*w*0.26 - 9, cy + ty*h*0.5 - 2, 18, 4, fill=1, stroke=0)
    yy = y + h - pad - size + 3
    for ln in lines:
        txt(x+pad, yy, ln, size, color, font); yy -= size+4
    return h

def burst(cx, cy, ro, ri, n=13, fill=YEL, stroke=INK, lw=2.6, rot=0.0):
    p = c.beginPath()
    for i in range(n*2):
        r = ro if i % 2 == 0 else ri
        a = rot + math.pi*i/n
        px, py = cx + r*math.cos(a), cy + r*math.sin(a)
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    p.close()
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.drawPath(p, fill=1, stroke=1)

def arrow(x1, y1, x2, y2, color=INK, lw=3.2, head=9):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(lw)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2-y1, x2-x1)
    p = c.beginPath(); p.moveTo(x2, y2)
    p.lineTo(x2-head*math.cos(a-0.45), y2-head*math.sin(a-0.45))
    p.lineTo(x2-head*math.cos(a+0.45), y2-head*math.sin(a+0.45))
    p.close(); c.drawPath(p, fill=1, stroke=0)

# ───────────────────────── gloss / shine ─────────────────────────
def shine(cx, cy, rw, rh, alpha=0.38, color=WHITE, squash=0.55):
    """Glossy highlight blob — the 'lame3a' look."""
    c.saveState(); c.setFillAlpha(alpha); c.setFillColor(color)
    c.ellipse(cx-rw, cy-rh*squash, cx+rw, cy+rh*squash, fill=1, stroke=0)
    c.restoreState()

def sparkle(cx, cy, r, color=WHITE, lw=0):
    """Four-point star sparkle."""
    p = c.beginPath()
    k = r*0.26
    p.moveTo(cx, cy+r); p.curveTo(cx+k, cy+k, cx+k, cy+k, cx+r, cy)
    p.curveTo(cx+k, cy-k, cx+k, cy-k, cx, cy-r)
    p.curveTo(cx-k, cy-k, cx-k, cy-k, cx-r, cy)
    p.curveTo(cx-k, cy+k, cx-k, cy+k, cx, cy+r)
    p.close()
    c.setFillColor(color); c.drawPath(p, fill=1, stroke=0)

def sparkles(pts):
    for (x, y, r) in pts:
        sparkle(x, y, r, WHITE)

def plate(cx, cy, r, base, rim=INK, lw=4.0):
    """Glossy medallion the icons sit on."""
    c.setFillColor(INK); c.circle(cx+5, cy-5, r, fill=1, stroke=0)
    c.setFillColor(base); c.setStrokeColor(rim); c.setLineWidth(lw)
    c.circle(cx, cy, r, fill=1, stroke=1)
    c.saveState(); c.setFillAlpha(0.22); c.setFillColor(WHITE)
    c.circle(cx, cy, r*0.82, fill=1, stroke=0); c.restoreState()
    shine(cx - r*0.22, cy + r*0.44, r*0.52, r*0.40, 0.46)

# ───────────────────────── ICONIC EMBLEMS ─────────────────────────
def icon_masks(cx, cy, s=1.0):
    """Lesson 05 — the role: two theatre masks on a medallion."""
    c.saveState(); c.translate(cx, cy); c.scale(s, s)
    plate(0, 0, 86, PUR)
    for sx, col, mood in ((-30, YEL, 1), (30, CYAN, -1)):
        c.setFillColor(INK); c.circle(sx+3, -3, 42, fill=1, stroke=0)
        c.setFillColor(col); c.setStrokeColor(INK); c.setLineWidth(3.4)
        p = c.beginPath()
        p.moveTo(sx-40, 20); p.curveTo(sx-40, 54, sx+40, 54, sx+40, 20)
        p.curveTo(sx+40, -34, sx+16, -46, sx, -46)
        p.curveTo(sx-16, -46, sx-40, -34, sx-40, 20); p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.setFillColor(INK)
        c.ellipse(sx-24, 8, sx-8, 24, fill=1, stroke=0)
        c.ellipse(sx+8, 8, sx+24, 24, fill=1, stroke=0)
        c.setStrokeColor(INK); c.setLineWidth(3.2)
        p2 = c.beginPath()
        if mood > 0:
            p2.moveTo(sx-16, -18); p2.curveTo(sx-6, -28, sx+6, -28, sx+16, -18)
        else:
            p2.moveTo(sx-16, -26); p2.curveTo(sx-6, -14, sx+6, -14, sx+16, -26)
        c.drawPath(p2, fill=0, stroke=1)
        shine(sx-14, 30, 16, 13, 0.42)
    sparkles([(-82, 62, 13), (78, -56, 10), (64, 70, 8)])
    c.restoreState()

def icon_gem(cx, cy, s=1.0):
    """Lesson 06 — structured output: a cut gem (messy -> perfect shape)."""
    c.saveState(); c.translate(cx, cy); c.scale(s, s)
    plate(0, 0, 86, CYAN)
    c.setFillColor(INK)
    p = c.beginPath()
    p.moveTo(3, 63); p.lineTo(-57, 17); p.lineTo(-33, -57)
    p.lineTo(39, -57); p.lineTo(63, 17); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(PUR); c.setStrokeColor(INK); c.setLineWidth(3.6)
    p = c.beginPath()
    p.moveTo(0, 60); p.lineTo(-60, 14); p.lineTo(-36, -60)
    p.lineTo(36, -60); p.lineTo(60, 14); p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setStrokeColor(INK); c.setLineWidth(2.6)
    for a, b in (((0, 60), (-26, 6)), ((0, 60), (26, 6)), ((-60, 14), (-26, 6)),
                 ((60, 14), (26, 6)), ((-26, 6), (26, 6)),
                 ((-26, 6), (-36, -60)), ((26, 6), (36, -60)), ((-26, 6), (0, -60)),
                 ((26, 6), (0, -60))):
        c.line(a[0], a[1], b[0], b[1])
    c.saveState(); c.setFillAlpha(0.5); c.setFillColor(WHITE)
    p = c.beginPath(); p.moveTo(0, 58); p.lineTo(-24, 8); p.lineTo(0, 8); p.close()
    c.drawPath(p, fill=1, stroke=0); c.restoreState()
    shine(-18, 34, 17, 12, 0.55)
    sparkles([(-80, 52, 12), (76, 58, 9), (70, -58, 11)])
    c.restoreState()

def icon_shield(cx, cy, s=1.0):
    """Lesson 07 — guardrails: a glossy shield with a check."""
    c.saveState(); c.translate(cx, cy); c.scale(s, s)
    plate(0, 0, 86, GRN)
    c.setFillColor(INK)
    p = c.beginPath()
    p.moveTo(3, 65); p.lineTo(-54, 39); p.lineTo(-54, -17)
    p.curveTo(-54, -47, -24, -61, 3, -67)
    p.curveTo(30, -61, 60, -47, 60, -17); p.lineTo(60, 39); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setStrokeColor(INK); c.setLineWidth(3.6)
    p = c.beginPath()
    p.moveTo(0, 62); p.lineTo(-57, 36); p.lineTo(-57, -20)
    p.curveTo(-57, -50, -27, -64, 0, -70)
    p.curveTo(27, -64, 57, -50, 57, -20); p.lineTo(57, 36); p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(GRN); c.setStrokeColor(INK); c.setLineWidth(2.6)
    p = c.beginPath()
    p.moveTo(0, 48); p.lineTo(-43, 28); p.lineTo(-43, -16)
    p.curveTo(-43, -38, -20, -50, 0, -55)
    p.curveTo(20, -50, 43, -38, 43, -16); p.lineTo(43, 28); p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setStrokeColor(WHITE); c.setLineWidth(10)
    c.line(-20, 0, -5, -17); c.line(-5, -17, 24, 24)
    c.saveState(); c.setFillAlpha(0.42); c.setFillColor(WHITE)
    p = c.beginPath(); p.moveTo(-40, 40); p.lineTo(-6, 54); p.lineTo(-6, -40)
    p.lineTo(-40, -22); p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()
    sparkles([(-80, 56, 12), (78, 50, 10), (66, -62, 9)])
    c.restoreState()

def icon_chain(cx, cy, s=1.0):
    """Lesson 08 — chaining: three interlocking glossy links."""
    c.saveState(); c.translate(cx, cy); c.scale(s, s)
    plate(0, 0, 86, ORG)
    cols = (YEL, WHITE, CYAN)
    for i, col in enumerate(cols):
        x = -46 + i*46
        c.setFillColor(INK); c.setStrokeColor(INK); c.setLineWidth(15)
        c.roundRect(x-25+3, -25-3, 50, 50, 16, fill=0, stroke=1)
        c.setStrokeColor(INK); c.setLineWidth(16)
        c.roundRect(x-25, -25, 50, 50, 16, fill=0, stroke=1)
        c.setStrokeColor(col); c.setLineWidth(10)
        c.roundRect(x-25, -25, 50, 50, 16, fill=0, stroke=1)
        c.saveState(); c.setStrokeAlpha(0.6); c.setStrokeColor(WHITE); c.setLineWidth(3.4)
        c.line(x-21, 8, x-21, 20); c.line(x-18, 23, x-6, 23); c.restoreState()
    sparkles([(-78, 58, 12), (74, 56, 10), (0, -70, 10)])
    c.restoreState()

def icon_vault(cx, cy, s=1.0):
    """Lesson 09 — RAG: a glossy vault door (your knowledge, opened per question)."""
    c.saveState(); c.translate(cx, cy); c.scale(s, s)
    plate(0, 0, 86, BLU)
    c.setFillColor(INK); c.circle(4, -4, 62, fill=1, stroke=0)
    c.setFillColor(STEEL); c.setStrokeColor(INK); c.setLineWidth(3.6)
    c.circle(0, 0, 60, fill=1, stroke=1)
    c.setFillColor(HexColor("#C9D3DC")); c.setStrokeColor(INK); c.setLineWidth(2.6)
    c.circle(0, 0, 44, fill=1, stroke=1)
    c.setStrokeColor(INK); c.setLineWidth(3.0)
    for i in range(8):
        a = math.pi*i/4
        c.line(44*math.cos(a), 44*math.sin(a), 58*math.cos(a), 58*math.sin(a))
    c.setFillColor(GOLD); c.setStrokeColor(INK); c.setLineWidth(2.8)
    c.circle(0, 0, 21, fill=1, stroke=1)
    c.setStrokeColor(INK); c.setLineWidth(5.4)
    for i in range(4):
        a = math.pi*i/2 + math.pi/4
        c.line(13*math.cos(a), 13*math.sin(a), 34*math.cos(a), 34*math.sin(a))
    c.setFillColor(INK); c.circle(0, 0, 7, fill=1, stroke=0)
    shine(-22, 32, 24, 16, 0.45)
    sparkles([(-80, 56, 12), (76, 54, 10), (62, -64, 9)])
    c.restoreState()

def icon_robot_tools(cx, cy, s=1.0):
    """Lesson 10 — agents: robot head inside a gear, with a key."""
    c.saveState(); c.translate(cx, cy); c.scale(s, s)
    plate(0, 0, 86, RED)
    c.setFillColor(INK)
    for off in (3,):
        p = c.beginPath()
        for i in range(12):
            a0 = 2*math.pi*i/12
            a1 = a0 + math.pi/12
            p.moveTo(off+62*math.cos(a0), -off+62*math.sin(a0))
            p.lineTo(off+74*math.cos(a0+0.06), -off+74*math.sin(a0+0.06))
            p.lineTo(off+74*math.cos(a1-0.06), -off+74*math.sin(a1-0.06))
            p.lineTo(off+62*math.cos(a1), -off+62*math.sin(a1))
            p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.circle(off, -off, 62, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setStrokeColor(INK); c.setLineWidth(3.0)
    p = c.beginPath()
    for i in range(12):
        a0 = 2*math.pi*i/12
        a1 = a0 + math.pi/12
        p.moveTo(60*math.cos(a0), 60*math.sin(a0))
        p.lineTo(72*math.cos(a0+0.06), 72*math.sin(a0+0.06))
        p.lineTo(72*math.cos(a1-0.06), 72*math.sin(a1-0.06))
        p.lineTo(60*math.cos(a1), 60*math.sin(a1))
        p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(GOLD); c.setStrokeColor(INK); c.setLineWidth(3.4)
    c.circle(0, 0, 60, fill=1, stroke=1)
    c.setFillColor(CYAN); c.setStrokeColor(INK); c.setLineWidth(3.2)
    c.roundRect(-40, -30, 80, 62, 13, fill=1, stroke=1)
    c.setFillColor(HexColor("#13243A")); c.roundRect(-32, -22, 64, 44, 9, fill=1, stroke=1)
    c.setFillColor(WHITE)
    c.circle(-14, 4, 10, fill=1, stroke=1); c.circle(14, 4, 10, fill=1, stroke=1)
    c.setFillColor(INK)
    c.circle(-14, 4, 4.2, fill=1, stroke=0); c.circle(14, 4, 4.2, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(3.2); c.line(0, 32, 0, 46)
    c.setFillColor(RED); c.circle(0, 51, 7, fill=1, stroke=1)
    shine(-24, 24, 20, 13, 0.45)
    sparkles([(-84, 52, 12), (80, 46, 10), (56, -70, 10)])
    c.restoreState()

# ───────────────────────── page chrome ─────────────────────────
def newpage(bg=PAPER, dots=True, dotc=DOT):
    c.setFillColor(bg); c.rect(0, 0, W, H, fill=1, stroke=0)
    if dots: halftone(0, 0, W, H, dotc)

def actbar(x, y, w, text, fill=RED):
    c.setFillColor(INK); c.rect(x+4, y-4, w, 30, fill=1, stroke=0)
    c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(2.6)
    c.rect(x, y, w, 30, fill=1, stroke=1)
    txt(x+12, y+9, text.upper(), 17, WHITE, "Impact")

def fieldnotes(x, y, w, title, lines, fill=WHITE, accent=BLU):
    size = 9.8
    body = []
    for ln in lines:
        body += simpleSplit("• " + ln, "Comic", size, w-26)
    h = 30 + len(body)*(size+4)
    c.setFillColor(INK); c.rect(x+4, y-h-4, w, h, fill=1, stroke=0)
    c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(2.6)
    c.rect(x, y-h, w, h, fill=1, stroke=1)
    c.setFillColor(accent); c.rect(x, y-24, w, 24, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(2.6); c.rect(x, y-h, w, h, fill=0, stroke=1)
    txt(x+10, y-17, title.upper(), 13, WHITE, "Impact")
    yy = y - 24 - size - 7
    for ln in body:
        txt(x+13, yy, ln, size, INK, "Comic"); yy -= size+4
    return y - h

def hook(s, fill=INK, color=YEL):
    c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(2.4)
    c.rect(30, 62, W-60, 32, fill=1, stroke=1)
    c.setFillColor(RED); c.rect(30, 62, 74, 32, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(2.4); c.rect(30, 62, W-60, 32, fill=0, stroke=1)
    txt(67, 72, "NEXT", 15, WHITE, "Impact", center=True)
    txt(118, 72, s.upper(), 14, color, "Impact")

def footer(label, link_key=None, tone=INK):
    PAGE[0] += 1
    c.setStrokeColor(tone); c.setLineWidth(1.4); c.line(30, 48, W-30, 48)
    txt(30, 35, "TAYEL AI LABS  //  PROMPT ENGINEER #2", 8.5, tone, "ComicB")
    txt(W-30, 35, f"{PAGE[0]}", 9, tone, "ComicB", right=True)
    txt(W/2, 35, label.upper(), 8.5, tone, "ComicB", center=True)
    if link_key:
        lbl = "READ THE FULL LESSON  >"
        wd = pdfmetrics.stringWidth(lbl, "ComicB", 8.5)
        txt(W-30, 16, lbl, 8.5, RED, "ComicB", right=True)
        c.linkURL(LK[link_key], (W-30-wd, 12, W-30, 26), relative=0, thickness=0)

def weakgood(x, y, w, weak, good, h=118):
    """Side-by-side weak/good strip."""
    cw = (w-14)/2
    c.setFillColor(INK); c.rect(x+4, y-h-4, cw, h, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFE9E6")); c.setStrokeColor(RED); c.setLineWidth(3)
    c.rect(x, y-h, cw, h, fill=1, stroke=1)
    txt(x+12, y-24, "WEAK", 15, RED, "Impact")
    yy = y - 44
    for ln in simpleSplit(weak, "Comic", 9.6, cw-24):
        txt(x+12, yy, ln, 9.6, INK, "Comic"); yy -= 14
    x2 = x + cw + 14
    c.setFillColor(INK); c.rect(x2+4, y-h-4, cw, h, fill=1, stroke=0)
    c.setFillColor(HexColor("#E2F7E6")); c.setStrokeColor(GRN); c.setLineWidth(3)
    c.rect(x2, y-h, cw, h, fill=1, stroke=1)
    txt(x2+12, y-24, "GOOD", 15, GRN, "Impact")
    yy = y - 44
    for ln in simpleSplit(good, "Comic", 9.6, cw-24):
        txt(x2+12, yy, ln, 9.6, INK, "Comic"); yy -= 14
    return y - h

def lesson_page(num, act, title, icon_fn, icon_col, kicker, bullets_, weak, good,
                notes_title, notes, hook_txt, link, big_line):
    newpage()
    actbar(30, H-66, 190 + 6*len(act), f"Lesson {num} — {act}", icon_col)
    otext(248 + 6*len(act), H-58, title, 29, fill=YEL, lw=2.4)
    # icon medallion, left
    icon_fn(166, 330, 1.02)
    txt(166, 196, big_line, 15, icon_col, "Impact", center=True)
    # right column
    txt(330, TOP-26, kicker, 12.5, INK, "ComicB")
    yy = TOP - 56
    for b in bullets_:
        c.setFillColor(icon_col); c.circle(338, yy+4, 4.6, fill=1, stroke=0)
        for ln in simpleSplit(b, "Comic", 10.6, 448):
            txt(352, yy, ln, 10.6, INK, "Comic"); yy -= 15
        yy -= 7
    weakgood(330, yy - 4, 482, weak, good, 112)
    fieldnotes(330, yy - 128, 482, notes_title, notes, accent=icon_col)
    hook(hook_txt)
    footer(f"Lesson {num} — {act}", link)
    c.showPage()

# ═════════════════════════ 1 — COVER ═════════════════════════
newpage(DARKBG, dotc=HexColor("#2A1C4A"))
rays(W*0.72, H*0.5, 560, HexColor("#2E1F55"), n=24, spread=1.4)
c.setFillColor(RED); c.rect(0, H-74, W, 74, fill=1, stroke=0)
c.setFillColor(INK); c.rect(0, H-81, W, 7, fill=1, stroke=0)
txt(34, H-48, "TAYEL AI LABS COMICS", 20, WHITE, "Impact")
txt(W-34, H-48, "ISSUE #2  //  LESSONS 05-10", 15, YEL, "Impact", right=True)
otext(46, H-182, "THE BUILD", 82, fill=YEL, lw=3.4)
txt(50, H-214, "Six tools that turn a clever prompt into a system", 15, WHITE, "ComicB")
txt(50, H-240, "Roles • Structure • Guardrails • Chains • Memory • Agents", 12, CYAN, "ComicB")
# icon row
icons = [(icon_masks, "ROLE"), (icon_gem, "STRUCTURE"), (icon_shield, "GUARDRAILS"),
         (icon_chain, "CHAINS"), (icon_vault, "MEMORY"), (icon_robot_tools, "AGENTS")]
for i, (fn, lbl) in enumerate(icons):
    x = 110 + i*126
    fn(x, 236, 0.52)
    txt(x, 160, lbl, 12, YEL, "Impact", center=True)
caption(46, 126, 420, "LAST ISSUE YOU LEARNED TO WRITE ONE GOOD PROMPT. "
                      "THIS ISSUE YOU BUILD A MACHINE OUT OF THEM.", 12)
c.setFillColor(YEL); c.setStrokeColor(INK); c.setLineWidth(2.6)
c.roundRect(492, 56, 206, 36, 9, fill=1, stroke=1)
txt(595, 68, "OPEN THE COURSE  >", 14, INK, "Impact", center=True)
c.linkURL(REPO, (492, 56, 698, 92), relative=0, thickness=0)
txt(W-34, 68, "SESSION 2", 13, STEEL, "ComicB", right=True)
c.showPage()

# ═════════════════════════ 2 — ROLES ═════════════════════════
lesson_page(
    "05", "Roles & Personas", "WHO IS IT BEING?", icon_masks, PUR,
    "A role sets vocabulary, judgement and defaults — in one line.",
    ["A good role answers three questions: who are you, who are you talking to, "
     "and what do you optimise for?",
     "It changes STYLE and JUDGEMENT. It does NOT add knowledge — \"you are a "
     "doctor\" doesn't tell it your patient's history.",
     "It grants no real authority and lifts no safety limits.",
     "The SYSTEM PROMPT is the role set once, governing every conversation — your "
     "product's personality and its safety policy."],
    "\"Reply to this angry customer.\"  ->  a generic corporate apology that "
    "promises things you don't even offer.",
    "\"You are the owner of a small coffee shop replying personally to an upset "
    "regular. Warm, no corporate script. You may offer one free drink — nothing "
    "more. Under four sentences.\"",
    "Make the role load-bearing",
    ["Name who it is, who it serves, and what it optimises for.",
     "Pair the role with its hard limits — they are strongest together.",
     "Treat the system prompt as a secret worth protecting, but never put real "
     "secrets inside it."],
    "a role shapes the words. now shape the SHAPE.", "05",
    "SET THE REGISTER")

# ═════════════════════════ 3 — STRUCTURED OUTPUT ═════════════════════════
lesson_page(
    "06", "Structured Output", "TALK TO SOFTWARE", icon_gem, CYAN,
    "The moment a MACHINE reads the answer, prose becomes a liability.",
    ["Give the exact schema — the keys and their types — plus one example.",
     "Say \"return ONLY the JSON, no prose, no markdown fences\".",
     "Always give a missing-value rule: use null, never invent a field.",
     "Messy text in, clean data out — this is the engine behind most real "
     "prompt products: invoices, reviews, CVs, tickets."],
    "\"Read this review and tell me the rating and what they liked.\"  ->  a "
    "paragraph you still have to read and retype somewhere.",
    "\"Return ONLY JSON: { stars: 1-5, liked: [string], disliked: [string] }.\"  "
    "->  { \"stars\": 3, \"liked\": [\"coffee\"], \"disliked\": [\"wifi down\"] } "
    "— straight into a dashboard.",
    "Make it reliable",
    ["Validate the schema in code and retry on malformed output.",
     "Many APIs have a strict JSON / schema mode — use it.",
     "This is the leap from chatbot to SYSTEM: { \"priority\": \"high\" } can "
     "route a ticket with no human in the middle."],
    "it answers well. now stop it answering WRONGLY.", "06",
    "CUT THE SHAPE")

# ═════════════════════════ 4 — GUARDRAILS ═════════════════════════
lesson_page(
    "07", "Constraints & Guardrails", "THE HONEST MACHINE", icon_shield, GRN,
    "The single most valuable line you can write gives it a way out.",
    ["\"If you are not sure, or it isn't in what I gave you, say so or ask. "
     "Do not guess.\" — this one clause separates a demo from a product.",
     "Prefer positive framing; naming a thing can summon it. If a negative is "
     "essential, say what to do INSTEAD.",
     "Scope limits keep it useful and make it harder to hijack.",
     "Five-point checklist: escape hatch, scope, the dangerous invention in YOUR "
     "domain, a fallback to a human, and grounding."],
    "\"You're a support bot for our shop. Answer customer questions.\"  ->  "
    "invents a loyalty programme, wrong holiday hours, writes poems on request.",
    "\"Answer only about our menu, hours, location and orders, from the info "
    "below. If it isn't covered, say 'Let me check.' Decline off-topic. Never "
    "invent prices, hours or promotions.\"",
    "What a client is really buying",
    ["A bot that admits uncertainty is trustworthy; one that fabricates is a "
     "liability.",
     "Guardrails are most of what makes a workflow sellable.",
     "Try to break your own assistant before a customer does."],
    "one prompt can't do it all. break it apart.", "07",
    "HOLD THE LINE")

# ═════════════════════════ 5 — CHAINS ═════════════════════════
lesson_page(
    "08", "Chaining & Pipelines", "ONE JOB PER LINK", icon_chain, ORG,
    "A mega-prompt does five things adequately and fails invisibly.",
    ["Three patterns: SEQUENTIAL (refine in stages), ROUTER (classify, then send "
     "to a specialist), MAP-REDUCE (same prompt over many pieces, then combine).",
     "Pass STRUCTURED data between steps, never prose — that's what makes a "
     "chain reliable.",
     "Mix prompts with plain code. Use the model only where judgement is needed; "
     "everything else is cheaper and exact in code.",
     "Log every step's input and output — that log becomes your eval set."],
    "One prompt: \"read this email, classify it, draft a reply in their "
    "language, and list the action items.\" Four jobs, one score, no way to tell "
    "which half broke.",
    "Four steps: classify -> draft -> translate -> extract actions. Each testable "
    "alone. Translations go wrong? You fix ONE prompt and leave the rest.",
    "Debug the link, not the rope",
    ["Feed a known input to step 1 — is the output correct and well-formed?",
     "Feed that to step 2. Continue. The first wrong step is your bug.",
     "This is the leap from prompting to building systems."],
    "it still only knows what you paste. open the vault.", "08",
    "SPLIT THE WORK")

# ═════════════════════════ 6 — RAG ═════════════════════════
lesson_page(
    "09", "Retrieval (RAG)", "GIVE IT YOUR WORLD", icon_vault, BLU,
    "You can't paste a 300-page manual into every question — so fetch the slice.",
    ["Two jobs bolted together: RETRIEVAL (find the relevant pieces) then "
     "GENERATION (answer from them, grounded).",
     "EMBEDDINGS, plainly: text turned into numbers that capture MEANING, so "
     "similar meanings sit close together — search by meaning, not keywords.",
     "Prepare once: chunk the docs, embed, store. Per question: embed the "
     "question, grab the nearest chunks, put them in the prompt.",
     "Update a document and the answers update — no retraining, ever."],
    "\"What's the warranty on our espresso machines?\" asked of a bare model -> "
    "a confident, invented warranty.",
    "The system pulls the real warranty section from YOUR docs and prompts: "
    "\"Answer using only the text below; if it doesn't cover it, say you'll "
    "check.\" -> the real answer, or an honest escalation.",
    "Almost every failure is a RETRIEVAL failure",
    ["Wrong chunks fetched = confident wrong answer. The prompt isn't the bug.",
     "Tune chunk size; retrieve more candidates, then filter.",
     "Don't reach for RAG when a simple paste will do — it is real overhead."],
    "it can answer anything now. what if it could ACT?", "09",
    "OPEN THE VAULT")

# ═════════════════════════ 7 — AGENTS ═════════════════════════
lesson_page(
    "10", "Agents & Tools", "FROM TALKING TO DOING", icon_robot_tools, RED,
    "A model alone can only produce text. Tools let it act.",
    ["THE LOOP: think -> act (call a tool) -> observe the result -> repeat until "
     "done.",
     "The model doesn't run the tool. It EMITS a structured request; your code "
     "runs it and feeds the result back. (Lesson 06, doing real work.)",
     "Tool descriptions ARE prompts — a vague one gets misused, a precise one "
     "gets used correctly.",
     "Retrieved text and tool results are DATA to consider, never commands to "
     "obey — that boundary matters most once it can act."],
    "Give it a send_email tool and say \"handle customer emails.\" It can email "
    "the wrong person, promise the wrong thing, or be tricked into forwarding "
    "your customer list.",
    "Read-only tools that DRAFT replies, a human approval step before anything "
    "sends, a hard step cap, and email contents treated as data. It drafts; a "
    "person clicks send.",
    "The safety model is the hard part",
    ["For each tool ask: read-only or does-something? Reversible or not?",
     "Least privilege — don't hand it tools it doesn't need.",
     "The less undoable the action (money, deletion, outbound), the more it "
     "needs an explicit human confirmation."],
    "you've built the machine. now prove it works.", "10",
    "LET IT ACT")

# ═════════════════════════ 8 — HOW THEY STACK ═════════════════════════
newpage(HexColor("#101A2B"), dotc=HexColor("#1B2740"))
actbar(30, H-66, 250, "The Whole Machine", GRN)
otext(302, H-58, "SIX TOOLS, ONE SYSTEM", 30, fill=YEL, lw=2.4)
stack = [(icon_masks, "ROLE", "who it is", PUR),
         (icon_gem, "STRUCTURE", "a shape code can read", CYAN),
         (icon_shield, "GUARDRAILS", "what it must never do", GRN),
         (icon_chain, "CHAINS", "one job per step", ORG),
         (icon_vault, "MEMORY", "your facts, fetched", BLU),
         (icon_robot_tools, "AGENTS", "it can finally act", RED)]
for i, (fn, t, s, col) in enumerate(stack):
    x = 110 + (i % 3)*300
    y = 360 - (i//3)*158
    fn(x - 46, y, 0.46)
    c.setFillColor(col); c.setStrokeColor(INK); c.setLineWidth(2.6)
    c.roundRect(x+10, y-20, 182, 44, 9, fill=1, stroke=1)
    txt(x+22, y+4, t, 15, WHITE if col in (PUR, RED, BLU) else INK, "Impact")
    txt(x+22, y-12, s, 9.4, WHITE if col in (PUR, RED, BLU) else INK, "ComicB")
caption(30, 196, 470, "A REAL SUPPORT SYSTEM IS A ROUTER IN FRONT, RAG FOR "
                      "QUESTIONS, AN AGENT FOR ORDERS — EACH WITH ITS OWN ROLE, "
                      "SCHEMA AND GUARDRAILS.", 11)
fieldnotes(520, 196, 292, "Start small", [
    "Build ONE grounded assistant first.",
    "Add a chain only when a step clearly needs it.",
    "Complexity you don't need is cost and risk, not sophistication.",
], accent=CYAN)
hook("your assignment is waiting", color=YEL)
footer("six buildable system maps are in the repo", "maps", tone=STEEL)
c.showPage()

# ═════════════════════════ 9 — ASSIGNMENT ═════════════════════════
newpage()
actbar(30, H-66, 220, "Your Turn", RED)
otext(272, H-58, "ASSIGNMENT — SESSION 2", 30, fill=YEL, lw=2.4)
icon_shield(150, 322, 0.86)
parts = [
    ("1", "Write a load-bearing ROLE", "who it is, who it serves, what it "
     "optimises for — plus its one hard limit.", PUR),
    ("2", "Force a SCHEMA", "pick a messy text you handle often; return only "
     "JSON, null for anything missing. Test on 5 real inputs.", CYAN),
    ("3", "Fit the five GUARDRAILS", "escape hatch, scope, the dangerous "
     "invention, a human fallback, grounding. Then try to break it.", GRN),
    ("4", "Split it into a CHAIN", "take one overloaded prompt, draw the steps, "
     "pass JSON between them.", ORG),
    ("5", "Design the RETRIEVAL", "sketch how you'd chunk your docs and what one "
     "question should fetch.", BLU),
    ("6", "Draw the AGENT's safety model", "list the tools; mark read-only vs "
     "acting, reversible vs not, and which need human approval.", RED),
]
yy = TOP - 18
for n, t, s, col in parts:
    c.setFillColor(col); c.setStrokeColor(INK); c.setLineWidth(2.4)
    c.circle(312, yy-10, 15, fill=1, stroke=1)
    txt(312, yy-16, n, 15, WHITE if col in (PUR, RED, BLU) else INK, "Impact", center=True)
    txt(338, yy-6, t, 13, INK, "Impact")
    yy -= 20
    for ln in simpleSplit(s, "Comic", 10, 460):
        txt(338, yy, ln, 10, STEEL, "Comic"); yy -= 14
    yy -= 14
c.setFillColor(YEL); c.setStrokeColor(INK); c.setLineWidth(2.6)
c.roundRect(60, 180, 212, 38, 9, fill=1, stroke=1)
txt(166, 192, "OPEN THE ASSIGNMENT  >", 13, INK, "Impact", center=True)
c.linkURL(LK["asg"], (60, 180, 272, 218), relative=0, thickness=0)
txt(166, 160, "No code required.", 10.5, STEEL, "ComicB", center=True)
hook("next issue: evaluation, security, cost — and the money")
footer("assignments/session-2-the-build.md", "asg")
c.showPage()

# ═════════════════════════ 10 — END / LINKS ═════════════════════════
newpage(DARKBG, dotc=HexColor("#2A1C4A"))
rays(W*0.5, H*0.6, 540, HexColor("#2E1F55"), n=24, spread=1.4)
otext(W/2, H-116, "TO BE CONTINUED", 44, fill=YEL, lw=3, center=True)
txt(W/2, H-146, "Issue #3: evaluation • prompt security • cost • the business",
    12.5, CYAN, "ComicB", center=True)
icon_robot_tools(128, 250, 0.62)
items = [("Lesson 05 — Roles & Personas", LK["05"]),
         ("Lesson 06 — Structured Output", LK["06"]),
         ("Lesson 07 — Constraints & Guardrails", LK["07"]),
         ("Lesson 08 — Chaining & Pipelines", LK["08"]),
         ("Lesson 09 — Retrieval (RAG)", LK["09"]),
         ("Lesson 10 — Agents & Tools", LK["10"]),
         ("Session 2 assignment", LK["asg"]),
         ("Weak vs Good — paired prompts", LK["ex"])]
for i, (lbl, url) in enumerate(items):
    x = 282 + (i % 2)*270
    y = H-196 - (i//2)*54
    c.setFillColor(INK); c.rect(x+4, y-42, 258, 40, fill=1, stroke=0)
    c.setFillColor(YEL if i >= 6 else WHITE); c.setStrokeColor(INK); c.setLineWidth(2.4)
    c.rect(x, y-38, 258, 40, fill=1, stroke=1)
    txt(x+12, y-23, lbl, 10.3, INK, "ComicB")
    txt(x+244, y-25, ">", 15, RED, "Impact", right=True)
    c.linkURL(url, (x, y-38, x+258, y+2), relative=0, thickness=0)
c.setFillColor(RED); c.rect(0, 52, W, 46, fill=1, stroke=0)
txt(W/2, 67, "TAYEL AI LABS  //  ADVANCED PROMPT ENGINEERING", 17, WHITE, "Impact",
    center=True)
PAGE[0] += 1
txt(W-30, 28, f"{PAGE[0]}", 9, STEEL, "ComicB", right=True)
c.showPage()

c.save()
print("wrote", OUT, "pages:", PAGE[0])
