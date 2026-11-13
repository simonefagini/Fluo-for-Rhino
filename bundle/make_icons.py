# -*- coding: utf-8 -*-

"""
make_icons.py
Draws the toolbar icons: one light and one dark SVG per command in toolbar/icons (name.svg and name-dark.svg), on a 48x48 viewBox.
Run it with a regular Python 3 from the repository root:  python bundle/make_icons.py
The style follows Rhino 8's own command icons: heavy dark outlines, white and grey objects, a blue gradient for what the command
changes, white square control nodes, and red, green and blue for the X, Y and Z axes.
The SVG files are the icon source: edit them by hand and they stay as they are until this script is run again,
which rewrites every icon it knows. Change the colours in LIGHT and DARK, the line weight in SW, or a single drawing below.
Vibe coded with Claude Sonnet 5.5 by Anthropic
November 2026 in Basel, GPL3.0
"""

import math, os, sys

LIGHT = dict(ink="#141414", node="#ffffff", paper="#ffffff",
             g0="#ffffff", g1="#aeaeae", d0="#c9c9c9", d1="#6f6f6f",
             b0="#d4ddff", b1="#5a7af4", red="#d92121", green="#2c9a3a", blue="#2f5bea",
             slabred0="#ff9b7a", slabred1="#d0301c", slabblue0="#bcd0ff", slabblue1="#3b63d9")
DARK = dict(ink="#ececec", node="#2a2a2a", paper="#4a4a4a",
            g0="#9a9a9a", g1="#4a4a4a", d0="#6c6c6c", d1="#2e2e2e",
            b0="#86a0ff", b1="#2c4ccc", red="#ff6a5c", green="#5fd36f", blue="#7c9bff",
            slabred0="#ff9b7a", slabred1="#c42a16", slabblue0="#9db9ff", slabblue1="#2f55c9")
SW = 2.6

def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")

class Ctx:
    def __init__(self, T, name):
        self.T, self.n = T, name
    # gradient fills
    def defs(self):
        T, n = self.T, self.n
        def lin(i, a, b):
            return ('<linearGradient id="%s%s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/>'
                    '<stop offset="1" stop-color="%s"/></linearGradient>') % (n, i, a, b)
        rad = ('<radialGradient id="%sS" cx="0.38" cy="0.35" r="0.75"><stop offset="0" stop-color="%s"/>'
               '<stop offset="1" stop-color="%s"/></radialGradient>') % (n, T["b0"], T["b1"])
        return "<defs>" + lin("G", T["g0"], T["g1"]) + lin("D", T["d0"], T["d1"]) + lin("B", T["b0"], T["b1"]) \
            + lin("R", T["slabred0"], T["slabred1"]) + lin("U", T["slabblue0"], T["slabblue1"]) + rad + "</defs>"
    def fill(self, k):
        return "url(#%s%s)" % (self.n, k)

def pts(p):
    return " ".join(f(x) + "," + f(y) for x, y in p)

def poly(c, p, fill, w=SW, close=True, dash=None):
    tag = "polygon" if close else "polyline"
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<%s points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"%s/>' % (
        tag, pts(p), fill, c.T["ink"], f(w), d)

def line(c, x1, y1, x2, y2, color=None, w=SW, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>' % (
        f(x1), f(y1), f(x2), f(y2), color or c.T["ink"], f(w), d)

def path(c, d, fill="none", color=None, w=SW, dash=None):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"%s/>' % (
        d, fill, color or c.T["ink"], f(w), ds)

def rect(c, x, y, w, h, fill, rx=0, sw=SW, dash=None, extra=""):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s%s/>' % (
        f(x), f(y), f(w), f(h), f(rx), fill, c.T["ink"], f(sw), ds, extra)

def circle(c, x, y, r, fill, w=SW, color=None):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        f(x), f(y), f(r), fill, color or c.T["ink"], f(w))

def node(c, x, y, s=6):
    return rect(c, x - s / 2.0, y - s / 2.0, s, s, c.T["node"], sw=2)

def arrow(c, x1, y1, x2, y2, color=None, w=3.0, head=8):
    col = color or c.T["ink"]
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    bx, by = x2 - ux * head, y2 - uy * head
    px, py = -uy, ux
    wing = head * 0.62
    tri = [(x2, y2), (bx + px * wing, by + py * wing), (bx - px * wing, by - py * wing)]
    return (line(c, x1, y1, bx + ux * 1.5, by + uy * 1.5, col, w) +
            '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2" stroke-linejoin="round"/>' % (pts(tri), col, col))

def cube(c, cx, cy, r, top="B", left="G", right="D"):
    # isometric cube centred on (cx, cy), r = half width
    h = r * 0.5
    t = [(cx, cy - r), (cx + r, cy - h), (cx, cy), (cx - r, cy - h)]
    l = [(cx - r, cy - h), (cx, cy), (cx, cy + r), (cx - r, cy + r - h)]
    rr = [(cx, cy), (cx + r, cy - h), (cx + r, cy + r - h), (cx, cy + r)]
    return poly(c, l, c.fill(left)) + poly(c, rr, c.fill(right)) + poly(c, t, c.fill(top))

def sq(c, x, y, s, k="B", rot=0, dash=None, fill=None):
    ex = ' transform="rotate(%s %s %s)"' % (f(rot), f(x + s / 2.0), f(y + s / 2.0)) if rot else ""
    return rect(c, x, y, s, s, fill or c.fill(k), sw=2.2, dash=dash, extra=ex)

def pill(c, x, y, w, h):
    return rect(c, x, y, w, h, c.fill("G"), rx=h / 2.0)

def page(c, x=10, y=4, w=28, h=40, fold=9):
    body = path(c, "M%s %s H%s L%s %s V%s H%s Z" % (f(x), f(y), f(x + w - fold), f(x + w), f(y + fold), f(y + h), f(x)), fill=c.T["paper"])
    corner = path(c, "M%s %s V%s H%s" % (f(x + w - fold), f(y), f(y + fold), f(x + w)), fill=c.fill("G"))
    return body + corner

def slab(c, cy, k, cx=24, hw=16, hh=5, th=3.5):
    top = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
    front_l = [(cx - hw, cy), (cx, cy + hh), (cx, cy + hh + th), (cx - hw, cy + th)]
    front_r = [(cx, cy + hh), (cx + hw, cy), (cx + hw, cy + th), (cx, cy + hh + th)]
    side = c.fill("D")
    return poly(c, front_l, side) + poly(c, front_r, side) + poly(c, top, c.fill(k))

def digit1(c, x, y, h=14, w=SW):
    return path(c, "M%s %s L%s %s V%s" % (f(x - 3.5), f(y + 3.5), f(x + 0.5), f(y), f(y + h)), w=w)

def letterA(c, x, y, h=14):
    return path(c, "M%s %s L%s %s L%s %s M%s %s H%s" % (f(x - 5), f(y + h), f(x), f(y), f(x + 5), f(y + h),
                                                       f(x - 3), f(y + h * 0.65), f(x + 3)), w=2.4)

def play(c, x, y, s):
    return poly(c, [(x, y), (x, y + s), (x + s * 0.95, y + s / 2.0)], c.fill("B"))

def stack(c, top_cy=16, step=7):
    return slab(c, top_cy + 2 * step, "U") + slab(c, top_cy + step, "G") + slab(c, top_cy, "R")

# ---------------------------------------------------------------- icons
ICONS = {}
def icon(fn):
    ICONS[fn.__name__] = fn
    return fn

@icon
def axo(c):
    return cube(c, 24, 21, 17)

@icon
def deaxo(c):
    return (poly(c, [(9, 16), (35, 16), (35, 42), (9, 42)], c.fill("B")) +
            path(c, "M33 11 A9 9 0 0 0 16 8", w=2.8) +
            '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2" stroke-linejoin="round"/>' % (
                pts([(11, 3), (19, 12), (20, 5)]), c.T["ink"], c.T["ink"]))

@icon
def namedViewPerspective(c):
    return (rect(c, 4, 7, 40, 34, c.T["paper"], rx=2) +
            line(c, 4, 7, 17, 17, w=2) + line(c, 44, 7, 31, 17, w=2) +
            line(c, 4, 41, 17, 31, w=2) + line(c, 44, 41, 31, 31, w=2) +
            rect(c, 17, 17, 14, 14, c.fill("B"), sw=2.2))

@icon
def restoreView(c):
    return (rect(c, 4, 18, 30, 24, c.T["paper"], rx=2) +
            rect(c, 11, 24, 16, 12, c.fill("B"), sw=2.2) +
            path(c, "M30 17 A10 10 0 1 0 33 5", w=2.8) +
            '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2" stroke-linejoin="round"/>' % (
                pts([(38, 3), (30, 3.5), (34, 10)]), c.T["ink"], c.T["ink"]))

@icon
def toggleClip(c):
    return (cube(c, 20, 22, 15, top="G", left="G", right="D") +
            poly(c, [(27, 7), (45, 12), (45, 42), (27, 37)], c.fill("B")) +
            line(c, 27, 7, 27, 37, w=2) )

@icon
def centerOsnap(c):
    return (circle(c, 24, 24, 16, "none", w=3) +
            line(c, 24, 4, 24, 12, w=2.4) + line(c, 24, 36, 24, 44, w=2.4) +
            line(c, 4, 24, 12, 24, w=2.4) + line(c, 36, 24, 44, 24, w=2.4) +
            node(c, 24, 24, 8))

@icon
def midOsnap(c):
    return (line(c, 6, 36, 42, 12, w=3.2) + node(c, 6, 36, 7) + node(c, 42, 12, 7) +
            poly(c, [(24, 14), (31, 28), (17, 28)], c.fill("B"), w=2.6) )

@icon
def moveVertical(c):
    return (sq(c, 17, 33, 13, "G") + sq(c, 17, 3, 13, "B") +
            arrow(c, 23.5, 31, 23.5, 19, w=3.2, head=9))

@icon
def copyVertical(c):
    return (sq(c, 6, 31, 12, "G") + sq(c, 6, 18, 12, "B") + sq(c, 6, 5, 12, "B") +
            arrow(c, 24, 36, 24, 10, w=3.0, head=8) + line(c, 24, 36, 36, 36, w=3.0) )

@icon
def rotateReference(c):
    return (line(c, 12, 38, 42, 38, w=2.4, dash="4 3.4") +
            line(c, 12, 38, 36, 8, w=3.2) +
            path(c, "M32 38 A20 20 0 0 0 25 24", w=2.8) +
            node(c, 12, 38, 7) + node(c, 42, 38, 6) + node(c, 36, 8, 6))

@icon
def pastePoint(c):
    return (rect(c, 5, 8, 26, 34, c.fill("G"), rx=3) +
            rect(c, 11, 4, 14, 8, c.fill("D"), rx=2) +
            line(c, 11, 22, 25, 22, w=2) + line(c, 11, 29, 21, 29, w=2) +
            circle(c, 35, 35, 8, c.fill("B"), w=2.6) + line(c, 35, 24, 35, 46, w=2) + line(c, 24, 35, 46, 35, w=2) +
            node(c, 35, 35, 5))

@icon
def shake(c):
    return (sq(c, 6, 6, 12, dash="2.6 2.4", fill="none") + sq(c, 28, 6, 12, dash="2.6 2.4", fill="none") +
            sq(c, 6, 28, 12, dash="2.6 2.4", fill="none") +
            sq(c, 11, 10, 12, "B", rot=10) + sq(c, 30, 12, 12, "G", rot=-14) + sq(c, 3, 33, 12, "B", rot=-8) +
            path(c, "M32 28 q3 -3 6 0 t6 0", w=2.2) + path(c, "M26 40 q3 -3 6 0 t6 0", w=2.2))

@icon
def unshake(c):
    return (sq(c, 5, 8, 14, "B") + sq(c, 24, 8, 14, "B") + sq(c, 5, 27, 14, "G") + sq(c, 24, 27, 14, "G") +
            path(c, "M44 21 A8 8 0 1 1 40 12", w=2.8) +
            '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2" stroke-linejoin="round"/>' % (
                pts([(36, 6), (44, 8), (39, 15)]), c.T["ink"], c.T["ink"]))

@icon
def rotateRandom(c):
    return (sq(c, 5, 6, 14, "B", rot=18) + sq(c, 26, 5, 13, "G", rot=-30) + sq(c, 13, 27, 14, "B", rot=52) +
            path(c, "M43 30 A9 9 0 1 1 38 22", w=2.8) +
            '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2" stroke-linejoin="round"/>' % (
                pts([(34, 17), (42, 20), (36, 26)]), c.T["ink"], c.T["ink"]))

@icon
def keep(c):
    out = ""
    filled = {(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)}
    for r in range(3):
        for q in range(3):
            x, y = 5 + q * 14.5, 5 + r * 14.5
            if (q, r) in filled:
                out += sq(c, x, y, 10, "B")
            else:
                out += sq(c, x, y, 10, dash="2.4 2.2", fill="none")
    return out

@icon
def tagDot(c):
    return (pill(c, 4, 10, 40, 22) + letterA(c, 24, 15, 12) + node(c, 24, 41, 6) + line(c, 24, 32, 24, 38, w=2.2))

@icon
def heightDot(c):
    return (line(c, 9, 6, 9, 42, w=2.6) + line(c, 4, 6, 14, 6, w=2.4) + line(c, 4, 42, 14, 42, w=2.4) +
            arrow(c, 9, 20, 9, 8, w=2.6, head=6) + arrow(c, 9, 28, 9, 40, w=2.6, head=6) +
            pill(c, 19, 17, 25, 14) + line(c, 31.5, 29, 31.5, 19.5, w=2.2) +
            poly(c, [(27, 23), (31.5, 19), (36, 23)], c.T["ink"], w=1.6, close=False))

@icon
def countingDot(c):
    return (pill(c, 4, 10, 40, 22) + digit1(c, 24, 14.5, 13) + node(c, 24, 41, 6) + line(c, 24, 32, 24, 38, w=2.2))

@icon
def clickCounter(c):
    cur = path(c, "M8 4 L8 31 L15 25 L20 37 L25 35 L20 23 L29 23 Z", fill=c.T["paper"], w=2.4)
    return (cur + pill(c, 25, 30, 19, 14) + digit1(c, 34.5, 32.5, 9, w=2.2))

@icon
def liveDim(c):
    return (line(c, 7, 39, 38, 39, c.T["red"], 3.2) + line(c, 38, 39, 38, 9, c.T["blue"], 3.2) +
            line(c, 7, 39, 38, 9, w=3.0) +
            path(c, "M20 39 A13 13 0 0 0 16.4 30.6", color=c.T["green"], w=2.6) +
            node(c, 7, 39, 7) + node(c, 38, 9, 7) + node(c, 38, 39, 5))

@icon
def objectsByLayer(c):
    return stack(c, 20, 7) + sq(c, 18.5, 3, 11, "B")

@icon
def blocksByLayer(c):
    return stack(c, 22, 7) + cube(c, 24, 8, 9)

@icon
def blocksToParentLayer(c):
    return (slab(c, 10, "R", hw=17, hh=6) + cube(c, 14, 37, 10) +
            arrow(c, 36, 40, 36, 22, w=3.2, head=9))

@icon
def whichMaterial(c):
    return (circle(c, 21, 21, 16, c.fill("S"), w=2.8) +
            circle(c, 33, 33, 8, "none", w=3.4) + line(c, 39, 39, 45, 45, w=4.6))

@icon
def count(c):
    return (sq(c, 4, 7, 11, "B") + circle(c, 24, 12.5, 6.5, c.fill("G"), w=2.2) +
            poly(c, [(40, 6), (46, 19), (34, 19)], c.fill("D"), w=2.2) +
            path(c, "M4 28 Q4 32 9 32 H19 Q24 32 24 37 Q24 32 29 32 H39 Q44 32 44 28", w=2.6) +
            digit1(c, 24, 38, 7, w=2.4))

@icon
def allPointsOn(c):
    out = cube(c, 24, 22, 17, top="G", left="G", right="D")
    for x, y in [(24, 5), (41, 13.5), (7, 13.5), (24, 22), (7, 30.5), (41, 30.5), (24, 39)]:
        out += node(c, x, y, 6)
    return out

@icon
def dupAllBorder(c):
    sheet = poly(c, [(4, 36), (22, 28), (44, 34), (28, 44)], c.fill("B"))
    border = poly(c, [(8, 18), (26, 10), (44, 16), (28, 26)], "none", w=3.0)
    return sheet + border + line(c, 8, 18, 4, 36, w=1.6, dash="2 2.2") + line(c, 44, 16, 44, 34, w=1.6, dash="2 2.2") + line(c, 28, 26, 28, 44, w=1.6, dash="2 2.2")

@icon
def parapet(c):
    out = rect(c, 3, 9, 42, 6, c.fill("G"), rx=3)
    out += rect(c, 3, 35, 42, 5, c.fill("G"), rx=2.5)
    for x in (9, 17, 25, 33):
        out += line(c, x, 15, x, 35, w=2.2)
    for x in (4.5, 41.5):
        out += rect(c, x - 2.5, 13, 5, 25, c.fill("B"), sw=2.2)
    return out

@icon
def dwg(c):
    return (page(c, 8, 3, 32, 42, 10) +
            line(c, 14, 38, 34, 38, w=2.4) + line(c, 14, 38, 30, 20, w=2.4) +
            path(c, "M24 38 A10 10 0 0 0 21.5 31.4", w=2.2) +
            node(c, 14, 38, 5) + node(c, 30, 20, 5) + node(c, 34, 38, 5))

@icon
def urlAliasUpdate(c):
    cloud = path(c, "M13 28 A7 7 0 0 1 14 14 A10 10 0 0 1 32 11 A8 8 0 0 1 35 28 Z", fill=c.fill("G"))
    return cloud + arrow(c, 24, 27, 24, 45, c.T["blue"], 4.0, 11)

@icon
def localAliasUpdate(c):
    folder = path(c, "M4 16 H17 L21 21 H44 V43 H4 Z", fill=c.fill("G"))
    return folder + arrow(c, 24, 2, 24, 28, c.T["blue"], 4.0, 11)

@icon
def tempScript(c):
    return (page(c, 6, 3, 28, 40, 9) + line(c, 11, 17, 25, 17, w=2) + line(c, 11, 23, 22, 23, w=2) +
            line(c, 11, 29, 19, 29, w=2) + play(c, 25, 24, 18))

def carrow(c, cx, cy, r, a0, a1, w=2.8, head=7.5):
    # circular arrow on a circle (screen angles in degrees, y down); a1 > a0 turns clockwise
    sign = 1 if a1 > a0 else -1
    def at(a):
        return cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
    x0, y0 = at(a0)
    x1, y1 = at(a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if sign > 0 else 0
    arc = path(c, "M%s %s A%s %s 0 %d %d %s %s" % (f(x0), f(y0), f(r), f(r), large, sweep, f(x1), f(y1)), w=w)
    tx, ty = -math.sin(math.radians(a1)) * sign, math.cos(math.radians(a1)) * sign
    px, py = -ty, tx
    tip = (x1 + tx * head * 0.7, y1 + ty * head * 0.7)
    wing = head * 0.6
    tri = [tip, (x1 + px * wing, y1 + py * wing), (x1 - px * wing, y1 - py * wing)]
    return arc + '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2" stroke-linejoin="round"/>' % (pts(tri), c.T["ink"], c.T["ink"])

@icon
def deaxo(c):
    return poly(c, [(7, 17), (31, 17), (31, 41), (7, 41)], c.fill("B")) + carrow(c, 35, 13, 7.5, 140, 410)

@icon
def restoreView(c):
    return (rect(c, 4, 20, 30, 22, c.T["paper"], rx=2) + rect(c, 11, 26, 16, 10, c.fill("B"), sw=2.2) +
            carrow(c, 35, 13, 7.5, 140, 410))

@icon
def unshake(c):
    return (sq(c, 4, 20, 11, "B") + sq(c, 18, 20, 11, "B") + sq(c, 4, 34, 11, "G") + sq(c, 18, 34, 11, "G") +
            carrow(c, 37, 13, 7, 40, -230))

@icon
def rotateRandom(c):
    return (sq(c, 4, 6, 12, "B", rot=20) + sq(c, 22, 4, 11, "G", rot=-30) + sq(c, 6, 27, 13, "B", rot=45) +
            carrow(c, 35, 35, 8, 20, 300))

@icon
def copyVertical(c):
    return (sq(c, 8, 31, 12, "G") + sq(c, 8, 18, 12, "B") + sq(c, 8, 5, 12, "B") +
            arrow(c, 33, 42, 33, 6, w=3.2, head=10))

@icon
def rotateReference(c):
    return (line(c, 12, 38, 42, 38, w=2.4, dash="4 3.4") + line(c, 12, 38, 36, 8, w=3.2) +
            carrow(c, 12, 38, 19, 0, -50, w=2.8, head=8) +
            node(c, 12, 38, 7) + node(c, 42, 38, 6) + node(c, 36, 8, 6))

@icon
def count(c):
    return (sq(c, 4, 7, 11, "B") + circle(c, 24, 12.5, 6.5, c.fill("G"), w=2.2) +
            poly(c, [(40, 6), (46, 19), (34, 19)], c.fill("D"), w=2.2) +
            path(c, "M5 28 Q5 33 10 33 H18 Q24 33 24 39 Q24 33 30 33 H38 Q43 33 43 28", w=2.8))

@icon
def parapet(c):
    out = rect(c, 3, 9, 42, 6, c.fill("G"), rx=3) + rect(c, 3, 35, 42, 5, c.fill("G"), rx=2.5)
    for x in (16, 24, 32):
        out += line(c, x, 15, x, 35, w=2.2)
    for x in (4.5, 43.5):
        out += rect(c, x - 2.5, 13, 5, 25, c.fill("B"), sw=2.2)
    return out

@icon
def parapet(c):
    out = rect(c, 3, 10, 42, 5, c.fill("G"), rx=2.5) + rect(c, 3, 35, 42, 4, c.fill("G"), rx=2)
    for x in (11, 24, 37):
        out += rect(c, x - 2, 15, 4, 20, c.fill("B"), sw=2)
    return out

def svg(name, T):
    c = Ctx(T, name)
    body = ICONS[name](c)
    return ('<svg width="48" height="48" version="1.1" xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0pt 0pt 48pt 48pt">\n  ' + c.defs() + "\n  " + body + "\n</svg>\n")

def write_all(out_dir):
    for name in ICONS:
        for T, suffix in ((LIGHT, ""), (DARK, "-dark")):
            with open(os.path.join(out_dir, name + suffix + ".svg"), "w", newline="\n") as fh:
                fh.write(svg(name, T))

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "toolbar", "icons")
    write_all(target)
    print("Wrote " + str(len(ICONS) * 2) + " icons (light and dark) to " + target)
