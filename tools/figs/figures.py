"""The redrawn figures. Each one follows the book's figure (fig/N-M.png): the same
points, labels and marks, drawn cleanly. Only figures whose content is fully
clear are redrawn; the rest keep the photo.

    python3 tools/figs/figures.py     # writes fig/N-M.svg and points the pages at them
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import Fig, polar, lerp  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIGS = {}


def fig(qid):
    def reg(fn):
        FIGS[qid] = fn
        return fn
    return reg


# ---------------------------------------------------------------- set 1
@fig('1-4')
def _():
    f = Fig(400, 380)
    O = (190, 200)
    r = 150
    A, B = polar(O, r, 60), polar(O, r, 0)
    f.circle(O, r)
    f.line(A, B)
    f.dot(O)
    f.label(O, 'O', dy=26)
    f.label(A, 'A', dx=8, dy=-20)
    f.label(B, 'B', dx=20)
    f.seglabel(A, B, '2', off=18, side=1)
    return f


@fig('1-7')
def _():
    f = Fig(470, 410)
    B, D, E = (60, 215), (262, 215), (422, 215)
    C = (161, 40)
    G = (242, 310)
    A = (B[0] + G[0] - D[0], B[1] + G[1] - D[1])
    F = (E[0] - 20 * 1.7, E[1] + 95 * 1.7)
    f.poly([B, C, D])
    f.poly([A, B, D, G])
    f.poly([D, E, F, G])
    f.angle(A, B, G, r=24, text='y')
    f.angle(F, G, E, r=24, text='x')
    f.angle(D, C, E, r=20, text='?', tr=34)
    f.label(B, 'B', dx=-20)
    f.label(C, 'C', dy=-18)
    f.label(D, 'D', dx=10, dy=22)
    f.label(E, 'E', dx=20)
    f.label(A, 'A', dx=-16, dy=14)
    f.label(G, 'G', dx=-4, dy=24)
    f.label(F, 'F', dx=8, dy=20)
    return f


# ---------------------------------------------------------------- set 2
@fig('2-4')
def _():
    f = Fig(470, 380)
    A, B, C, D = (50, 340), (50, 180), (365, 180), (365, 340)
    # CF = CD/2 with a right angle at F, so angle FCD = 60 deg; E, C, F on one line
    F = (C[0] + 80 * 0.866, C[1] + 80 * 0.5)
    # angle BCE = 30 deg, right angle at E
    E = (C[0] - 315 * 0.866 * 0.866, C[1] - 315 * 0.866 * 0.5)
    f.poly([A, B, C, D])
    f.poly([B, E, C], close=False)
    f.line(E, F)
    f.line(F, D)
    f.right(E, B, C)
    f.right(F, C, D)
    f.right(C, B, D, s=11)
    f.label(A, 'A', dx=-18, dy=4)
    f.label(B, 'B', dx=-20)
    f.label(C, 'C', dx=2, dy=-20)
    f.label(D, 'D', dx=6, dy=20)
    f.label(E, 'E', dy=-20)
    f.label(F, 'F', dx=20)
    return f


@fig('2-6')
def _():
    f = Fig(460, 380)
    o = (130, 212)   # origin
    u = 28           # one unit
    P = lambda x, y: (o[0] + x * u, o[1] - y * u)  # noqa: E731
    f.line((20, o[1]), (440, o[1]), w=1.8)
    f.line((o[0], 365), (o[0], 20), w=1.8)
    f.poly([(440, o[1]), (430, o[1] - 5), (430, o[1] + 5)], fill='#1f2328', w=1)
    f.poly([(o[0], 20), (o[0] - 5, 30), (o[0] + 5, 30)], fill='#1f2328', w=1)
    f.text((448, o[1] + 16), 'x', size=19, italic=True)
    f.text((o[0] - 14, 24), 'y', size=19, italic=True)
    A, C, B = P(-2, -4), P(1, 0), P(5.5, 6)  # B drawn on line AC (not to scale)
    f.line(A, B)
    for p in (A, C, B):
        f.dot(p)
    f.text((A[0] - 6, A[1] + 22), 'A(−2,−4)', size=19)
    f.text((C[0] + 30, C[1] + 20), 'C(1,0)', size=19)
    f.text((B[0] + 10, B[1] - 18), 'B(x,y)', size=19)
    return f


# ---------------------------------------------------------------- set 3
@fig('3-4')
def _():
    import math
    f = Fig(450, 400)
    s, dx, dy = 250, 110, -105          # cube edge (front face) and depth offset
    F0 = (30, 380)                       # front bottom-left
    fbl, fbr = F0, (F0[0] + s, F0[1])
    ftl, ftr = (F0[0], F0[1] - s), (F0[0] + s, F0[1] - s)
    b = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
    # visible edges
    f.poly([fbl, fbr, ftr, ftl])
    f.poly([ftl, b(ftl), b(ftr), ftr], close=False)
    f.poly([fbr, b(fbr), b(ftr)], close=False)
    # hidden edges
    f.line(fbl, b(fbl), dash=True, w=1.6)
    f.line(b(fbl), b(fbr), dash=True, w=1.6)
    f.line(b(fbl), b(ftl), dash=True, w=1.6)
    # the cylinder: its bases fill the top and bottom faces
    u, v = (s / 2, 0), (dx / 2, dy / 2)
    ct = (ftl[0] + s / 2 + dx / 2, ftl[1] + dy / 2)
    cb = (fbl[0] + s / 2 + dx / 2, fbl[1] + dy / 2)
    f.ellipse(ct, u, v, w=2.2)
    f.ellipse(cb, u, v, w=2.2, dash=True)
    t = math.atan2(v[0], u[0])
    for k in (0, math.pi):
        ex = (u[0] * math.cos(t + k) + v[0] * math.sin(t + k), u[1] * math.cos(t + k) + v[1] * math.sin(t + k))
        f.line((ct[0] + ex[0], ct[1] + ex[1]), (cb[0] + ex[0], cb[1] + ex[1]), w=2.2)
    # edge length a
    x = b(fbr)[0] + 22
    f.arrow2((x, b(ftr)[1]), (x, b(fbr)[1]))
    f.text((x + 14, (b(ftr)[1] + b(fbr)[1]) / 2), 'a', size=21, italic=True)
    return f


@fig('3-8')
def _():
    f = Fig(400, 420)
    R = 180
    O = (200, 205)
    A = (O[0], O[1] + R)
    B = (O[0], O[1] - R * 2 / 3)
    c = (O[0], (A[1] + B[1]) / 2)
    f.circle(O, R)
    f.circle(c, (A[1] - B[1]) / 2)
    f.line(A, B, w=2)
    f.dot(O, 4.5)
    f.dot(A)
    f.dot(B)
    f.label(O, 'O', dx=20)
    f.label(A, 'A', dy=22)
    f.label(B, 'B', dy=-18)
    return f


# ---------------------------------------------------------------- set 4
@fig('4-4')
def _():
    f = Fig(400, 400)
    c, R = (200, 200), 165
    names = 'ABCDEFGH'
    V = [polar(c, R, 112.5 - 45 * k) for k in range(8)]   # A top-left, clockwise
    A, B, C, D, E = V[:5]
    f.shade([A, B, C, D], fill='#c9ccc8')
    f.shade([A, D, E], fill='#1f2328')
    f.poly(V)
    f.line(A, D)
    f.line(A, E)
    off = {'A': (-8, -18), 'B': (8, -18), 'C': (20, -6), 'D': (20, 8), 'E': (10, 20), 'F': (-10, 20), 'G': (-20, 8), 'H': (-20, -6)}
    for n, p in zip(names, V):
        f.label(p, n, *off[n])
    return f


@fig('4-8')
def _():
    f = Fig(440, 400)
    c, R = (220, 195), 170
    E, F, A, B, C, D = (polar(c, R, a) for a in (0, 60, 120, 180, 240, 300))
    G = lerp(C, D, 0.5)
    H = lerp(D, E, 0.68)
    f.poly([A, F, E, D, C, B])
    f.line(G, H)
    f.dot(G)
    f.dot(H)
    f.angle(G, D, H, r=30, text='α', tr=44)
    f.angle(H, G, D, r=30, text='β', tr=44)
    for p, n, dx, dy in ((A, 'A', -10, -18), (F, 'F', 10, -18), (E, 'E', 22, 0), (D, 'D', 10, 20), (C, 'C', -10, 20), (B, 'B', -22, 0), (G, 'G', 0, 22), (H, 'H', 20, 4)):
        f.label(p, n, dx, dy)
    return f


# ---------------------------------------------------------------- set 5
@fig('5-1')
def _():
    f = Fig(400, 400)
    O, R = (200, 200), 170
    A, B, D, C = (polar(O, R, a) for a in (110, 18, 186, 266))
    f.circle(O, R)
    f.line(A, C)
    f.line(B, D)
    f.line(A, B)
    f.line(D, C)
    # E = intersection of AC and BD
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = A, C, B, D
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    E = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    f.label(A, 'A', dx=-12, dy=-16)
    f.label(B, 'B', dx=18, dy=-6)
    f.label(D, 'D', dx=-18)
    f.label(C, 'C', dy=20)
    f.label(E, 'E', dx=14, dy=18)
    return f


@fig('5-4')
def _():
    f = Fig(520, 150)
    A, B, C = (30, 100), (180, 100), (490, 100)
    f.line(A, C)
    for p in (A, B, C):
        f.line((p[0], p[1] - 7), (p[0], p[1] + 7), w=2.2)
    f.brace((A[0], 78), (B[0] - 3, 78))
    f.brace((B[0] + 3, 78), (C[0], 78))
    f.text(((A[0] + B[0]) / 2, 38), 'x ק"מ', size=20, rtl=True)
    f.text(((B[0] + C[0]) / 2, 38), '2x ק"מ', size=20, rtl=True)
    f.label(A, 'A', dy=26)
    f.label(B, 'B', dy=26)
    f.label(C, 'C', dy=26)
    return f


@fig('5-7')
def _():
    f = Fig(480, 270)
    D, A = (40, 50), (340, 50)
    C, B = (40, 223), (340, 223)
    E, F = (240, 223), (440, 223)
    f.poly([D, A, B, C])
    f.line(B, F)
    f.line(A, E)
    f.line(A, F)
    f.right(B, A, F, s=12)
    f.label(D, 'D', dx=-16, dy=-10)
    f.label(A, 'A', dx=14, dy=-12)
    f.label(C, 'C', dx=-14, dy=18)
    f.label(E, 'E', dy=22)
    f.label(B, 'B', dy=22)
    f.label(F, 'F', dx=8, dy=20)
    return f


# ---------------------------------------------------------------- set 6
@fig('6-4')
def _():
    f = Fig(480, 360)
    r = 125
    O1, O2 = (178, 180), (178 + r, 180)
    h = r * 3 ** 0.5 / 2
    A = ((O1[0] + O2[0]) / 2, 180 + h)
    D = (A[0], 180 - h)
    B = (2 * O1[0] - A[0], 2 * O1[1] - A[1])
    C = (2 * O2[0] - A[0], 2 * O2[1] - A[1])
    f.circle(O1, r)
    f.circle(O2, r)
    f.line(A, B)
    f.line(A, C)
    f.dot(O1, 4.5)
    f.dot(O2, 4.5)
    f.angle(A, B, C, r=30, text='60°', tr=62)
    f.text((O1[0] - 22, O1[1] + 8), 'O₁', size=19)
    f.text((O2[0] + 24, O2[1] + 8), 'O₂', size=19)
    f.label(A, 'A', dy=22)
    f.label(D, 'D', dy=-18)
    f.label(B, 'B', dx=-14, dy=-14)
    f.label(C, 'C', dx=14, dy=-14)
    return f


# ---------------------------------------------------------------- set 7
@fig('7-4')
def _():
    f = Fig(380, 380)
    c, r = (190, 190), 150
    sq = [polar(c, r, a) for a in (45, 135, 225, 315)]
    # grey: the four circle segments between the circle and the inner square
    d = 'M%.1f %.1f' % sq[0]
    for k in range(4):
        d += ' A%d %d 0 0 0 %.1f %.1f' % (r, r, *sq[(k + 1) % 4])
    d += ' Z M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (sq[0] + sq[3] + sq[2] + sq[1])
    f.items.insert(0, '<path d="%s" fill="#c9ccc8" fill-rule="evenodd"/>' % d)
    f.poly([(c[0] - r, c[1] - r), (c[0] + r, c[1] - r), (c[0] + r, c[1] + r), (c[0] - r, c[1] + r)])
    f.circle(c, r)
    f.poly(sq)
    return f


@fig('7-5')
def _():
    f = Fig(420, 330)
    o, u = (70, 260), 42      # origin, one unit
    P = lambda x, y: (o[0] + x * u, o[1] - y * u)  # noqa: E731
    f.line((20, o[1]), (400, o[1]), w=1.8)
    f.line((o[0], 310), (o[0], 20), w=1.8)
    f.poly([(400, o[1]), (390, o[1] - 5), (390, o[1] + 5)], fill='#1f2328', w=1)
    f.poly([(o[0], 20), (o[0] - 5, 30), (o[0] + 5, 30)], fill='#1f2328', w=1)
    f.text((406, o[1] + 18), 'x', size=19, italic=True)
    f.text((o[0] - 16, 26), 'y', size=19, italic=True)
    O, A, C, B = P(0, 0), P(4, 0), P(4, 4), P(0, 4)
    D = P(8 - 2 * 3.14159, 4)
    f.poly([O, A, C, B])
    f.path('M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (B[0], B[1], 4 * u, 4 * u, A[0], A[1]))
    f.dot(D)
    f.label(O, 'O', dx=-16, dy=18)
    f.label(A, 'A', dx=4, dy=22)
    f.label(C, 'C', dx=18, dy=-6)
    f.label(B, 'B', dx=-18, dy=-10)
    f.label(D, 'D', dy=-18)
    f.text((o[0] - 18, (O[1] + B[1]) / 2), '4', size=19)
    return f


@fig('7-8')
def _():
    f = Fig(400, 400)
    O, R = (230, 200), 165
    C = (O[0] - R, O[1])
    M = ((O[0] + C[0]) / 2, O[1])
    d = R / 2
    T, A = (M[0], M[1] - d), (M[0], M[1] + d)
    # B: ray O->A continued to the circle
    ux, uy = A[0] - O[0], A[1] - O[1]
    n = (ux * ux + uy * uy) ** 0.5
    B = (O[0] + ux / n * R, O[1] + uy / n * R)
    f.circle(O, R)
    f.poly([C, T, O, A])
    f.line(A, B)
    f.line(C, B)
    f.dot(O, 4.5)
    f.label(O, 'O', dx=20)
    f.label(C, 'C', dx=-18)
    f.label(A, 'A', dx=14, dy=14)
    f.label(B, 'B', dx=-10, dy=20)
    return f


# ---------------------------------------------------------------- set 8
@fig('8-2')
def _():
    f = Fig(400, 360)
    O, R = (200, 180), 165
    A, B = (O[0] - R, O[1]), (O[0] + R, O[1])
    h = R / 2
    f.circle(O, R)
    f.poly([A, (O[0] - h, O[1] - h), O, (O[0] - h, O[1] + h)])
    f.poly([O, (O[0] + h, O[1] - h), B, (O[0] + h, O[1] + h)])
    f.dot(O, 4.5)
    f.label(O, 'O', dy=-22)
    f.label(A, 'A', dx=-18)
    f.label(B, 'B', dx=18)
    return f


@fig('8-4')
def _():
    f = Fig(420, 230)
    A, B, C, D = (40, 35), (380, 35), (380, 195), (40, 195)
    f.poly([A, B, C, D])
    f.line(A, C)
    f.line(B, D)
    f.label(A, 'A', dx=-16, dy=-8)
    f.label(B, 'B', dx=16, dy=-8)
    f.label(C, 'C', dx=16, dy=10)
    f.label(D, 'D', dx=-16, dy=10)
    return f


# ---------------------------------------------------------------- set 9
@fig('9-3')
def _():
    f = Fig(400, 330)
    c, R = (200, 165), 150
    V = [polar(c, R, a) for a in (180, 120, 60, 0, 300, 240)]   # A=V[0] left, B=V[3] right
    f.poly(V)
    for k in range(3):
        f.line(V[k], V[k + 3])
    f.dot(c, 4.5)
    f.label(V[0], 'A', dx=-20)
    f.label(V[3], 'B', dx=20)
    return f


@fig('9-10')
def _():
    f = Fig(520, 240)
    R = 105
    c1, c2 = (125, 120), (395, 120)
    f.circle(c1, R)
    f.circle(c2, R)
    for k in range(3):
        f.circle((c1[0] - R + R / 3 * (2 * k + 1), c1[1]), R / 3, w=2)
    for k in range(2):
        f.circle((c2[0] - R + R / 2 * (2 * k + 1), c2[1]), R / 2, w=2)
    return f


# ---------------------------------------------------------------- set 10
@fig('10-2')
def _():
    f = Fig(440, 250)
    B, C = (40, 205), (320, 205)
    A, D = (110, 45), (390, 45)
    E = lerp(B, C, 0.4)
    f.poly([A, B, C, D])
    f.line(A, E)
    f.label(A, 'A', dx=-12, dy=-16)
    f.label(D, 'D', dx=14, dy=-12)
    f.label(B, 'B', dx=-12, dy=18)
    f.label(E, 'E', dy=22)
    f.label(C, 'C', dx=8, dy=20)
    return f


@fig('10-8')
def _():
    f = Fig(420, 420)
    c = (210, 210)
    names = {90: 'צפון', 270: 'דרום', 0: 'מזרח', 180: 'מערב',
             45: 'צפון־מזרח', 135: 'צפון־מערב', 225: 'דרום־מערב', 315: 'דרום־מזרח'}
    for a, n in names.items():
        L = 120 if a % 90 == 0 else 105
        tip = polar(c, L, a)
        f.line(c, tip, w=2.2)
        import math
        ux, uy = math.cos(math.radians(a)), -math.sin(math.radians(a))
        s = 12
        f.poly([tip, (tip[0] - ux * s - uy * s * .45, tip[1] - uy * s + ux * s * .45),
                (tip[0] - ux * s + uy * s * .45, tip[1] - uy * s - ux * s * .45)], fill='#1f2328', w=1)
        lp = polar(c, L + (30 if a % 90 == 0 else 48), a)
        f.text(lp, n, size=17, rtl=True)
    f.dot(c, 5)
    return f


# ---------------------------------------------------------------- set 11
@fig('11-3')
def _():
    f = Fig(400, 410)
    k = 0.5
    P = lambda x, y: (x * k + 10, y * k - 25)  # noqa: E731  (the book figure's proportions)
    A, D, B, C = P(270, 95), P(70, 340), P(455, 340), P(260, 580)
    E, F = P(700, 520), P(510, 770)
    f.shade([D, B, C], fill='#9ea29d')
    f.shade([B, C, F], fill='#9ea29d')
    f.poly([A, B, C, D])
    f.poly([B, E, F, C])
    f.line(D, B)
    f.line(B, F)
    f.label(A, 'A', dy=-18)
    f.label(B, 'B', dx=16, dy=-12)
    f.label(C, 'C', dx=-16, dy=14)
    f.label(D, 'D', dx=-18)
    f.label(E, 'E', dx=18)
    f.label(F, 'F', dy=20)
    return f


@fig('11-5')
def _():
    f = Fig(460, 210)
    d = 190
    A = (30, 105)
    B, C = (A[0] + d, 105), (A[0] + 2 * d, 105)
    f.poly([(A[0], 105 - d / 2), (C[0], 105 - d / 2), (C[0], 105 + d / 2), (A[0], 105 + d / 2)])
    f.path('M%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f' % (A[0], A[1], d / 2, d / 2, B[0], B[1]))
    f.path('M%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f' % (B[0], B[1], d / 2, d / 2, C[0], C[1]))
    for p in (A, B, C):
        f.dot(p, 4.5)
    f.label(A, 'A', dx=-18)
    f.label(B, 'B', dx=-18)
    f.label(C, 'C', dx=18)
    return f


@fig('11-8')
def _():
    f = Fig(380, 380)
    o, d = (30, 30), 320 / 3
    f.poly([o, (o[0] + 320, o[1]), (o[0] + 320, o[1] + 320), (o[0], o[1] + 320)])
    centres = [(o[0] + d * (i + .5), o[1] + d * (j + .5)) for j in range(3) for i in range(3)]
    for c in centres:
        f.circle(c, d / 2, w=2)
    f.line(centres[0], centres[8], w=3.6)
    f.dot(centres[0], 6)
    f.dot(centres[8], 6)
    return f


@fig('11-10')
def _():
    f = Fig(400, 380)
    s, dx, dy = 210, 110, -90
    P = lambda x, y: (x, y)  # noqa: E731
    ftl, ftr, fbr, fbl = (40, 130), (40 + s, 130), (40 + s, 130 + s), (40, 130 + s)
    b = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
    # the three shaded half-faces meet at the corner ftr
    f.shade([ftl, ftr, b(ftr)], fill='#b9bdb8')
    f.shade([ftl, ftr, fbr], fill='#d9dcd8')
    f.shade([ftr, b(ftr), fbr], fill='#c9ccc8')
    f.poly([ftl, ftr, fbr, fbl])
    f.poly([ftl, b(ftl), b(ftr), ftr], close=False)
    f.poly([ftr, b(ftr), b(fbr), fbr], close=False)
    f.line(ftl, b(ftr))
    f.line(ftl, fbr)
    f.line(b(ftr), fbr)
    return f


# ---------------------------------------------------------------- set 12
@fig('12-4')
def _():
    import math
    f = Fig(340, 490)
    a = 220
    y0 = 335
    B, C = (60, y0), (60 + a, y0)
    A = (60 + a / 2, y0 - a * math.sqrt(3) / 2)
    r = a / 2
    f.shade([A, B, C], fill='#c9ccc8')
    mAB, mAC = lerp(A, B, .5), lerp(A, C, .5)
    # circle around A: the part outside the triangle (300 degrees)
    f.path('M%.1f %.1f A%.1f %.1f 0 1 0 %.1f %.1f' % (mAC[0], mAC[1], r, r, mAB[0], mAB[1]))
    # half circle on BC, below it
    f.path('M%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f' % (B[0], B[1], r, r, C[0], C[1]))
    f.poly([A, B, C])
    f.label(A, 'A', dy=-20)
    f.label(B, 'B', dx=-18)
    f.label(C, 'C', dx=18)
    return f


@fig('12-5')
def _():
    f = Fig(440, 420)
    s, dx, dy = 230, 120, -95
    A, D = (50, 365), (50 + s, 365)
    b = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
    E, B = b(A), b(D)
    tA, tD = (A[0], A[1] - s), (D[0], D[1] - s)
    C, tB = b(tA), b(tD)
    # cube edges
    f.poly([A, D, tD, tA])
    f.poly([tA, C, tB, tD], close=False)
    f.poly([D, B, tB], close=False)
    f.line(A, E, dash=True, w=1.6)
    f.line(E, B, dash=True, w=1.6)
    f.line(E, C, dash=True, w=1.6)
    # the two paths
    f.arrow(A, B, at=.97)
    f.arrow(B, C, at=.97)
    f.arrow(C, A, at=.97)
    f.arrow(B, D, at=.95)
    f.arrow(D, E, at=.95)
    f.arrow(E, A, at=.92)
    f.label(A, 'A', dx=-16, dy=12)
    f.label(D, 'D', dx=10, dy=20)
    f.label(B, 'B', dx=18, dy=6)
    f.label(E, 'E', dx=-16, dy=-10)
    f.label(C, 'C', dx=-8, dy=-18)
    return f


@fig('12-8')
def _():
    f = Fig(420, 380)
    c, R = (200, 190), 150
    V = [polar(c, R, 36 * k) for k in range(10)]   # vertices on the x axis
    f.line((20, c[1]), (400, c[1]), w=1.8)
    f.line((c[0], 360), (c[0], 18), w=1.8)
    f.poly([(400, c[1]), (390, c[1] - 5), (390, c[1] + 5)], fill='#1f2328', w=1)
    f.poly([(c[0], 18), (c[0] - 5, 28), (c[0] + 5, 28)], fill='#1f2328', w=1)
    f.text((408, c[1] + 18), 'x', size=19, italic=True)
    f.text((c[0] - 16, 24), 'y', size=19, italic=True)
    f.poly(V)
    return f


# ---------------------------------------------------------------- set 13
@fig('13-8')
def _():
    f = Fig(400, 460)
    o = (200, 190)
    f.line((20, o[1]), (380, o[1]), w=1.8)
    f.line((o[0], 445), (o[0], 20), w=1.8)
    f.poly([(380, o[1]), (370, o[1] - 5), (370, o[1] + 5)], fill='#1f2328', w=1)
    f.poly([(o[0], 20), (o[0] - 5, 30), (o[0] + 5, 30)], fill='#1f2328', w=1)
    f.text((386, o[1] + 18), 'x', size=19, italic=True)
    f.text((o[0] - 16, 24), 'y', size=19, italic=True)
    A, C = (o[0] + 105, o[1]), (o[0] - 105, o[1])
    D, B = (o[0], o[1] - 85), (o[0], o[1] + 150)
    f.poly([A, D, C, B])
    for p in (A, B, C, D):
        f.dot(p)
    f.text((A[0] + 8, A[1] + 22), 'A(a,0)', size=18)
    f.text((C[0] - 8, C[1] + 22), 'C(c,0)', size=18)
    f.text((D[0] + 44, D[1] - 14), 'D(0,d)', size=18)
    f.text((B[0] + 44, B[1] + 18), 'B(0,b)', size=18)
    return f


# ---------------------------------------------------------------- set 14
@fig('14-2')
def _():
    f = Fig(480, 250)
    A, B, C = (40, 30), (150, 215), (440, 215)
    D = lerp(A, C, 0.62)
    E = lerp(B, D, 0.5)
    f.shade([A, B, E])
    f.shade([E, D, C])
    f.poly([A, B, C])
    f.line(B, D)
    f.line(A, E)
    f.line(E, C)
    f.label(A, 'A', dx=-14, dy=-10)
    f.label(B, 'B', dx=-10, dy=20)
    f.label(C, 'C', dx=16, dy=8)
    f.label(D, 'D', dx=8, dy=-18)
    f.label(E, 'E', dx=2, dy=-20)
    return f


@fig('14-6')
def _():
    f = Fig(360, 460)
    r = 62
    A, D = (40, 40), (40, 40 + 6 * r)
    w = r + 5 * r / 3 ** 0.5
    B, C = (A[0] + w, 40), (A[0] + w, 40 + 6 * r)
    f.poly([A, B, C, D])
    for k in range(3):
        f.circle((A[0] + r, A[1] + r * (2 * k + 1)), r, w=2)
    P = (A[0] + r, A[1] + 5 * r)
    f.line(B, P)
    f.dot(P, 4.5)
    f.angle(B, A, P, r=34, text='60°', tr=52)
    f.label(A, 'A', dx=-16, dy=-10)
    f.label(B, 'B', dx=16, dy=-10)
    f.label(C, 'C', dx=16, dy=10)
    f.label(D, 'D', dx=-16, dy=10)
    return f


@fig('14-8')
def _():
    f = Fig(360, 360)
    O, R = (180, 180), 145
    A, B, D, C = (O[0], O[1] - R), (O[0], O[1] + R), (O[0] - R, O[1]), (O[0] + R, O[1])
    f.circle(O, R)
    f.line(A, B)
    f.line(D, C)
    f.label(O, 'O', dx=16, dy=-16)
    f.label(A, 'A', dy=-18)
    f.label(B, 'B', dy=20)
    f.label(D, 'D', dx=-18)
    f.label(C, 'C', dx=18)
    return f


@fig('14-10')
def _():
    f = Fig(360, 380)
    c, R = (180, 190), 165
    V = [polar(c, R, 90 + 60 * k) for k in range(6)]
    f.poly(V)
    f.poly([V[0], V[2], V[4]])
    return f


# ---------------------------------------------------------------- writer
def main():
    only = set(sys.argv[1:])
    done = []
    for qid, fn in FIGS.items():
        if only and qid not in only:
            continue
        open(os.path.join(REPO, 'fig', qid + '.svg'), 'w').write(fn().svg())
        done.append(qid)
    # point the pages and the data at the SVG versions
    names = {'fig/%s.png' % q: 'fig/%s.svg' % q for q in FIGS}
    files = glob.glob(os.path.join(REPO, 'sets', '*.html')) + [os.path.join(REPO, p) for p in (
        'solutions.html', 'review.html', 'data/bank.json', 'data/bank.js', 'data/questions.json')]
    for path in files:
        if not os.path.exists(path):
            continue
        s = open(path, encoding='utf-8').read()
        t = re.sub(r'fig/\d+-\d+\.png', lambda m: names.get(m.group(0), m.group(0)), s)
        if t != s:
            open(path, 'w', encoding='utf-8').write(t)
    print('figures written:', len(done))


if __name__ == '__main__':
    main()
