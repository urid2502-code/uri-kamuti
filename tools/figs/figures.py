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


# ---------------------------------------------------------------- set 15
@fig('15-7')
def _():
    import math
    f = Fig(400, 470)
    r = 88
    B = (200, 150)
    D = (200, 150 + 2 * r)
    half = 2 * r / math.sqrt(3)
    A, C = (B[0] - half, B[1]), (B[0] + half, B[1])
    f.shade([A, C, D])
    f.circle(B, r, fill='#fff')
    f.circle(D, r, fill='#fff')
    f.poly([A, C, D])
    f.line(B, D)
    E, F = (B[0] - r, B[1]), (B[0] + r, B[1])
    for p in (E, F, B, D):
        f.dot(p)
    f.label(A, 'A', dx=-16)
    f.label(C, 'C', dx=16)
    f.label(E, 'E', dx=-8, dy=-18)
    f.label(F, 'F', dx=8, dy=-18)
    f.label(B, 'B', dy=-18)
    f.label(D, 'D', dy=22)
    return f


# ---------------------------------------------------------------- set 17
@fig('17-4')
def _():
    f = Fig(380, 380)
    c, R = (190, 190), 160
    A, B, C, D = (polar(c, R, a) for a in (225, 135, 45, 315))
    E, F, G, H = (polar(c, R / 3, a) for a in (225, 135, 45, 315))
    # grey: the circle outside ABCD, and the small square
    d = 'M%.1f %.1f' % A
    for p in (B, C, D, A):
        d += ' A%d %d 0 0 1 %.1f %.1f' % (R, R, *p)
    d += ' Z M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z' % (A + D + C + B)
    f.items.insert(0, '<path d="%s" fill="#c9ccc8" fill-rule="evenodd"/>' % d)
    f.shade([E, F, G, H], fill='#c9ccc8')
    f.circle(c, R)
    f.poly([A, B, C, D])
    f.poly([E, F, G, H])
    f.line(A, C)
    f.line(B, D)
    for p, n, dx, dy in ((A, 'A', -14, 14), (B, 'B', -14, -14), (C, 'C', 14, -14), (D, 'D', 14, 14),
                         (E, 'E', -4, 20), (F, 'F', -4, -18), (G, 'G', 4, -18), (H, 'H', 4, 20)):
        f.label(p, n, dx, dy)
    return f


# ---------------------------------------------------------------- set 18
@fig('18-2')
def _():
    f = Fig(380, 380)
    c, R = (190, 190), 170
    V = [polar(c, R, 112.5 - 45 * k) for k in range(8)]   # V0 top-left, clockwise
    x0, x1 = V[0][0], V[1][0]          # the two vertical diagonals
    y0, y1 = V[7][1], V[6][1]          # the two horizontal diagonals
    # grey: the middle band; black: the four corner triangles
    f.shade([(V[7][0], y0), (V[2][0], y0), (V[3][0], y1), (V[6][0], y1)], fill='#c9ccc8')
    for tri in ([V[7], V[0], (x0, y0)], [V[1], V[2], (x1, y0)], [V[3], V[4], (x1, y1)], [V[5], V[6], (x0, y1)]):
        f.shade(tri, fill='#1f2328')
    f.poly(V)
    f.line(V[0], (x0, y0))
    f.line((x0, y1), V[5])
    f.line(V[1], (x1, y0))
    f.line((x1, y1), V[4])
    f.line(V[7], V[2])
    f.line(V[6], V[3])
    return f


@fig('18-4')
def _():
    f = Fig(420, 400)
    s, dx, dy = 230, 110, -100
    A, D = (50, 360), (50 + s, 360)
    b = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
    tA, tD = (A[0], A[1] - s), (D[0], D[1] - s)
    C, B = b(tA), b(tD)
    f.poly([A, D, tD, tA])
    f.poly([tA, C, B, tD], close=False)
    f.poly([D, b(D), B], close=False)
    f.line(A, b(A), dash=True, w=1.6)
    f.line(b(A), b(D), dash=True, w=1.6)
    f.line(b(A), C, dash=True, w=1.6)
    f.arrow(A, B, at=.97, w=2.6)
    f.arrow(B, C, at=.95, w=2.6)
    f.arrow(C, D, at=.97, w=2.6)
    f.arrow(D, A, at=.95, w=2.6)
    f.label(A, 'A', dx=-16, dy=12)
    f.label(D, 'D', dx=10, dy=20)
    f.label(B, 'B', dx=18, dy=-8)
    f.label(C, 'C', dx=-12, dy=-16)
    return f


@fig('18-6')
def _():
    import math
    f = Fig(440, 260)
    O, r = (215, 135), 82
    # BC tangent at the bottom (F), AD tangent at E, slanted
    F = (O[0], O[1] + r)
    t = math.radians(-108)
    E = (O[0] + r * math.cos(t), O[1] + r * math.sin(t))
    ux, uy = -math.sin(t), math.cos(t)          # tangent direction at E
    A = (E[0] - ux * 150, E[1] - uy * 150)
    D = (E[0] + ux * 175, E[1] + uy * 175)
    B, C = (A[0] + 30, F[1]), (D[0] + 70, F[1])
    f.poly([A, D, C, B])
    f.circle(O, r)
    f.dot(E)
    f.dot(F)
    f.label(A, 'A', dx=-16)
    f.label(D, 'D', dx=14, dy=-12)
    f.label(B, 'B', dx=-12, dy=18)
    f.label(C, 'C', dx=14, dy=16)
    f.label(E, 'E', dx=-4, dy=-20)
    f.label(F, 'F', dy=22)
    return f


# ---------------------------------------------------------------- set 19
@fig('19-4')
def _():
    f = Fig(380, 380)
    o, u = (40, 40), 34          # A at the top-left; AE = 6u, AF = 8u, AB = 9u
    sq = lambda n: [o, (o[0] + n * u, o[1]), (o[0] + n * u, o[1] + n * u), (o[0], o[1] + n * u)]  # noqa: E731
    # dotted (grey): the L between AEKI and AFGH
    for n, fill in ((8, '#c9ccc8'), (6, '#fff')):
        f.items.append('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in sq(n)), fill))
    for n in (9, 8, 6):
        f.poly(sq(n))
    A = o
    E, F, B = (o[0] + 6 * u, o[1]), (o[0] + 8 * u, o[1]), (o[0] + 9 * u, o[1])
    I, H, D = (o[0], o[1] + 6 * u), (o[0], o[1] + 8 * u), (o[0], o[1] + 9 * u)
    K, G, C = (o[0] + 6 * u, o[1] + 6 * u), (o[0] + 8 * u, o[1] + 8 * u), (o[0] + 9 * u, o[1] + 9 * u)
    f.label(A, 'A', dx=-16, dy=-14)
    for p_, n in ((E, 'E'), (F, 'F'), (B, 'B')):
        f.label(p_, n, dy=-16)
    for p_, n in ((I, 'I'), (H, 'H'), (D, 'D')):
        f.label(p_, n, dx=-16)
    f.label(K, 'K', dx=-14, dy=-14)
    f.label(G, 'G', dx=-14, dy=-14)
    f.label(C, 'C', dx=14, dy=14)
    return f


@fig('19-8')
def _():
    import math
    f = Fig(460, 360)
    O, r = (150, 180), 110
    s = 280
    B = (O[0] + s * math.cos(math.radians(30)), O[1] - s * math.sin(math.radians(30)))
    C = (B[0], O[1] + s * math.sin(math.radians(30)))
    A = (O[0] + r * math.cos(math.radians(30)), O[1] - r * math.sin(math.radians(30)))
    D = (A[0], O[1] + r * math.sin(math.radians(30)))
    # dark: the part of the circle outside the triangle (a 300 degree sector)
    f.shade_path('M%.1f %.1f L%.1f %.1f A%d %d 0 1 0 %.1f %.1f Z' % (O[0], O[1], A[0], A[1], r, r, D[0], D[1]), fill='#9ea29d')
    f.path('M%.1f %.1f A%d %d 0 1 0 %.1f %.1f' % (A[0], A[1], r, r, D[0], D[1]))
    f.path('M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (A[0], A[1], r, r, D[0], D[1]), w=1.6)
    f.poly([O, B, C])
    f.dot(O)
    f.label(O, 'O', dx=-16)
    f.label(A, 'A', dx=-4, dy=-18)
    f.label(D, 'D', dx=-4, dy=20)
    f.label(B, 'B', dx=14, dy=-10)
    f.label(C, 'C', dx=14, dy=12)
    return f


@fig('19-10')
def _():
    import math
    f = Fig(560, 300)
    R = 95

    def base(c, title):
        A, B = (c[0], c[1] - R), (c[0], c[1] + R)
        D, C = (c[0] - R, c[1]), (c[0] + R, c[1])
        f.circle(c, R, w=1.6)
        f.line(A, B, w=1.4)
        f.line(D, C, w=1.4)
        f.text((c[0], 22), title, size=19, rtl=True, weight=600)
        f.label(A, 'A', dy=-16, size=18)
        f.label(B, 'B', dy=18, size=18)
        f.label(D, 'D', dx=-16, size=18)
        f.label(C, 'C', dx=16, size=18)
        f.label(c, 'O', dx=13, dy=-13, size=16)
        return A, B, C, D

    def arc(c, p, q, sweep):
        f.path('M%.1f %.1f A%d %d 0 0 %d %.1f %.1f' % (p[0], p[1], R, R, sweep, q[0], q[1]), w=3.2)
        # arrowhead at q, along the tangent
        ang = math.atan2(q[1] - c[1], q[0] - c[0])
        tx, ty = (-math.sin(ang), math.cos(ang)) if sweep else (math.sin(ang), -math.cos(ang))
        s = 12
        f.poly([q, (q[0] - tx * s - ty * s * .42, q[1] - ty * s + tx * s * .42),
                (q[0] - tx * s + ty * s * .42, q[1] - ty * s - tx * s * .42)], fill='#1f2328', w=1)

    c1 = (140, 160)
    A, B, C, D = base(c1, 'מסלול הארנב')
    arc(c1, A, D, 0)
    f.arrow(D, C, w=3.2, at=.97)
    arc(c1, C, B, 1)
    c2 = (420, 160)
    A, B, C, D = base(c2, 'מסלול הצב')
    arc(c2, A, D, 0)
    f.arrow(D, c2, w=3.2, at=.93)
    f.arrow(c2, B, w=3.2, at=.97)
    return f


# ---------------------------------------------------------------- set 20
@fig('20-10')
def _():
    f = Fig(380, 380)
    c, R = (190, 190), 165
    V = [polar(c, R, 90 + 60 * k) for k in range(6)]
    f.poly(V)
    f.poly([V[0], V[2], V[4]])
    f.circle(c, R)
    return f


# ---------------------------------------------------------------- set 21
@fig('21-2')
def _():
    f = Fig(360, 360)
    O, R = (180, 180), 140
    a = 72
    P1, P2 = polar(O, R, a / 2), polar(O, R, -a / 2)            # right bold arc
    Q1, Q2 = polar(O, R, 180 - a / 2), polar(O, R, 180 + a / 2)  # left bold arc
    f.circle(O, R, w=1.8)
    f.line(P1, Q2, w=1.8)
    f.line(P2, Q1, w=1.8)
    f.path('M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (P1[0], P1[1], R, R, P2[0], P2[1]), w=6)
    f.path('M%.1f %.1f A%d %d 0 0 0 %.1f %.1f' % (Q1[0], Q1[1], R, R, Q2[0], Q2[1]), w=6)
    f.dot(O, 4.5)
    f.angle(O, P1, P2, r=30, text='α', tr=46)
    f.label(O, 'O', dx=-4, dy=-22)
    return f


# ---------------------------------------------------------------- set 22
@fig('22-2')
def _():
    f = Fig(360, 340)
    c = (180, 170)
    r = 120
    R = r * 2 / 3 ** 0.5
    V = [polar(c, R, 30 + 60 * k) for k in range(6)]
    f.poly(V)
    f.circle(c, r)
    f.dot(c, 4.5)
    f.line(c, (c[0] + r, c[1]), w=1.8)
    f.text((c[0] + r / 2, c[1] - 14), 'r', size=19, italic=True)
    f.label(c, 'O', dx=-4, dy=-20)
    return f


@fig('22-10')
def _():
    f = Fig(520, 330)
    B, R = (160, 170), 140
    A, r = (420, 170), 70
    beta, alpha = 50, 150
    b1, b2 = polar(B, R, 90 + beta / 2), polar(B, R, 90 - beta / 2)
    a1, a2 = polar(A, r, 90 + alpha / 2), polar(A, r, 90 - alpha / 2)
    f.shade_path('M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' % (B[0], B[1], b1[0], b1[1], R, R, b2[0], b2[1]))
    f.shade_path('M%.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z' % (A[0], A[1], a1[0], a1[1], r, r, a2[0], a2[1]))
    f.circle(B, R)
    f.circle(A, r)
    f.line(B, b1)
    f.line(B, b2)
    f.line(A, a1)
    f.line(A, a2)
    f.angle(B, b1, b2, r=26, text='β', tr=42)
    f.angle(A, a1, a2, r=20, text='α', tr=34)
    f.seglabel(B, b2, 'R', off=16)
    f.seglabel(A, a2, 'r', off=14)
    f.dot(B, 4.5)
    f.dot(A, 4.5)
    f.label(B, 'B', dy=22)
    f.label(A, 'A', dy=22)
    return f


# ---------------------------------------------------------------- set 23
@fig('23-5')
def _():
    f = Fig(500, 260)
    R = 115
    c1, c2 = (130, 130), (130 + 2 * R, 130)
    f.circle(c1, R)
    f.circle(c2, R)
    for k in range(3):
        f.circle((c1[0] - R + R / 2 * (2 * k + 1), 130), R / 2, fill='#1f2328')
    return f


@fig('23-8')
def _():
    f = Fig(460, 220)
    A, B, C, D = (40, 185), (420, 185), (420, 35), (40, 35)
    f.poly([A, B, C, D])
    f.arrow(A, C, dash=True, at=.97, w=2.2)
    f.arrow(C, D, dash=True, at=.96, w=2.2)
    f.arrow(D, B, dash=True, at=.97, w=2.2)
    f.label(A, 'A', dx=-16, dy=10)
    f.label(B, 'B', dx=16, dy=10)
    f.label(C, 'C', dx=16, dy=-10)
    f.label(D, 'D', dx=-16, dy=-10)
    return f


@fig('23-10')
def _():
    f = Fig(400, 380)
    s, dx, dy = 210, 100, -85
    F0 = (40, 340)
    u = s / 3
    v = (dx / 3, dy / 3)
    # front face grid with the centre square grey
    fx, fy = F0[0], F0[1] - s
    f.shade([(fx + u, fy + u), (fx + 2 * u, fy + u), (fx + 2 * u, fy + 2 * u), (fx + u, fy + 2 * u)], fill='#9ea29d')
    # top face centre
    tp = lambda i, j: (fx + i * u + j * v[0], fy + j * v[1])  # noqa: E731
    f.shade([tp(1, 1), tp(2, 1), tp(2, 2), tp(1, 2)], fill='#9ea29d')
    # right face centre
    rp = lambda j, k: (fx + s + j * v[0], fy + k * u + j * v[1])  # noqa: E731
    f.shade([rp(1, 1), rp(2, 1), rp(2, 2), rp(1, 2)], fill='#9ea29d')
    for k in range(4):
        f.line((fx, fy + k * u), (fx + s, fy + k * u), w=1.6 if 0 < k < 3 else 2.4)
        f.line((fx + k * u, fy), (fx + k * u, fy + s), w=1.6 if 0 < k < 3 else 2.4)
        f.line(tp(k, 0), tp(k, 3), w=1.6 if 0 < k < 3 else 2.4)
        f.line(tp(0, k), tp(3, k), w=1.6 if 0 < k < 3 else 2.4)
        f.line(rp(k, 0), rp(k, 3), w=1.6 if 0 < k < 3 else 2.4)
        f.line(rp(0, k), rp(3, k), w=1.6 if 0 < k < 3 else 2.4)
    return f


# ---------------------------------------------------------------- set 24
@fig('24-2')
def _():
    import math
    f = Fig(340, 500)
    r = 125
    d = r * math.sqrt(2)
    O1, O2 = (170, 250 - d / 2), (170, 250 + d / 2)
    P, Q = (170 + d / 2, 250), (170 - d / 2, 250)
    def pt(c, deg):
        return polar(c, r, deg)
    # grey: the square, and the outer quadrant of each circle (top of the upper, bottom of the lower)
    f.shade([O1, P, O2, Q], fill='#c9ccc8')
    a1, a2 = pt(O1, 45), pt(O1, 135)
    f.shade_path('M%.1f %.1f L%.1f %.1f A%d %d 0 0 0 %.1f %.1f Z' % (O1[0], O1[1], a1[0], a1[1], r, r, a2[0], a2[1]), fill='#c9ccc8')
    b1, b2 = pt(O2, 225), pt(O2, 315)
    f.shade_path('M%.1f %.1f L%.1f %.1f A%d %d 0 0 0 %.1f %.1f Z' % (O2[0], O2[1], b1[0], b1[1], r, r, b2[0], b2[1]), fill='#c9ccc8')
    f.circle(O1, r)
    f.circle(O2, r)
    f.line(pt(O1, 135), pt(O1, 315))
    f.line(pt(O1, 45), pt(O1, 225))
    f.line(pt(O2, 135), pt(O2, 315))
    f.line(pt(O2, 45), pt(O2, 225))
    for v, a, b in ((O1, P, Q), (O2, P, Q), (P, O1, O2), (Q, O1, O2)):
        f.right(v, a, b, s=11)
    return f


@fig('24-6')
def _():
    import math
    f = Fig(480, 250)
    B, C = (40, 215), (440, 215)
    BC = C[0] - B[0]
    AB = BC * math.cos(math.radians(30))
    A = (B[0] + AB * math.cos(math.radians(30)), B[1] - AB * math.sin(math.radians(30)))
    D = (A[0], B[1])
    BD = D[0] - B[0]
    BE = BD * math.cos(math.radians(30))
    E = (B[0] + BE * math.cos(math.radians(30)), B[1] - BE * math.sin(math.radians(30)))
    f.poly([A, B, C])
    f.line(A, D)
    f.line(D, E)
    f.right(A, B, C, s=12)
    f.right(D, B, A, s=12)
    f.right(E, B, D, s=12)
    f.angle(B, C, A, r=34, text='30°', tr=56)
    f.label(A, 'A', dy=-18)
    f.label(B, 'B', dx=-16)
    f.label(C, 'C', dx=16)
    f.label(D, 'D', dy=20)
    f.label(E, 'E', dx=-6, dy=-18)
    return f


# ---------------------------------------------------------------- set 25
@fig('25-1')
def _():
    f = Fig(460, 290)
    P = (40, 240)
    Y, O = (420, 40), (190, 240)
    f.arrow(P, Y, w=2.6, at=1)
    f.arrow(P, O, w=2.6, at=1)
    f.line(O, Y, dash=True, w=2)
    f.text((190, 112), 'יהלי', size=20, rtl=True, weight=600)
    f.text((110, 272), 'עומר', size=20, rtl=True, weight=600)
    f.text((362, 150), '40 ק"מ', size=19, rtl=True)
    return f


@fig('25-7')
def _():
    f = Fig(560, 300)
    # the box 2x by 2x by x
    w, h, dx, dy = 190, 95, 70, -60
    F0 = (40, 250)
    a, b = F0, (F0[0] + w, F0[1])
    c, d = (F0[0] + w, F0[1] - h), (F0[0], F0[1] - h)
    bk = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
    f.poly([a, b, c, d])
    f.poly([d, bk(d), bk(c), c], close=False)
    f.poly([b, bk(b), bk(c)], close=False)
    f.line(a, bk(a), dash=True, w=1.6)
    f.line(bk(a), bk(b), dash=True, w=1.6)
    f.line(bk(a), bk(d), dash=True, w=1.6)
    f.text(((a[0] + b[0]) / 2, a[1] + 26), '2x', size=20, italic=True)
    f.text((b[0] + 50, b[1] - 18), '2x', size=20, italic=True)
    f.text((a[0] - 18, (a[1] + d[1]) / 2), 'x', size=20, italic=True)
    # two pyramids on a common square base of side x, each of height x
    cx, cy = 450, 165
    s, ddx, ddy = 95, 55, -40
    q1, q2 = (cx - s / 2 - ddx / 2, cy - ddy / 2), (cx + s / 2 - ddx / 2, cy - ddy / 2)
    q3, q4 = (q2[0] + ddx, q2[1] + ddy), (q1[0] + ddx, q1[1] + ddy)
    top, bot = (cx, cy - 115), (cx, cy + 115)
    f.line(q1, q2)
    f.line(q2, q3)
    f.line(q3, q4, dash=True, w=1.6)
    f.line(q4, q1, dash=True, w=1.6)
    for q in (q1, q2, q3):
        f.line(top, q)
        f.line(bot, q)
    f.line(top, q4, dash=True, w=1.6)
    f.line(bot, q4, dash=True, w=1.6)
    f.line(top, bot, dash=True, w=1.4)
    f.text(((q1[0] + q2[0]) / 2, q1[1] + 20), 'x', size=20, italic=True)
    return f


# ---------------------------------------------------------------- set 26
@fig('26-6')
def _():
    import math
    f = Fig(480, 260)
    h = 170
    DE = h / math.sqrt(3)
    EC = 220
    D = (40, 220)
    E, C = (D[0] + DE, D[1]), (D[0] + DE + EC, D[1])
    A, F = (E[0], E[1] - h), (C[0], C[1] - h)
    B = (F[0] + DE, F[1])
    f.shade([F, B, C], fill='#c9ccc8')
    f.poly([A, B, C, D])
    f.line(A, E)
    f.line(F, C)
    f.right(E, A, C, s=12)
    f.right(F, A, C, s=12)
    f.angle(A, D, E, r=40, text='30°', tr=60)
    f.label(A, 'A', dx=-14, dy=-12)
    f.label(B, 'B', dx=14, dy=-12)
    f.label(C, 'C', dx=10, dy=18)
    f.label(D, 'D', dx=-14, dy=14)
    f.label(E, 'E', dy=20)
    f.label(F, 'F', dy=-18)
    return f


# ---------------------------------------------------------------- set 27
@fig('27-3')
def _():
    import math
    f = Fig(340, 420)
    O, R = (150, 210), 170
    r = R / math.sqrt(2)
    A, B = (O[0], O[1] - R), (O[0], O[1] + R)
    C, D = (O[0], O[1] - r), (O[0], O[1] + r)
    # hatched big half circle to the right of AB
    f.items.append('<defs><pattern id="h273" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">'
                   '<line x1="0" y1="0" x2="0" y2="9" stroke="#1f2328" stroke-width="1.6"/></pattern></defs>')
    f.items.append('<path d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z" fill="url(#h273)" stroke="#1f2328" stroke-width="2.4"/>' % (A[0], A[1], R, R, B[0], B[1]))
    f.path('M%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f' % (C[0], C[1], r, r, D[0], D[1]))
    f.line(A, B, w=2)
    f.line(A, C, w=6)
    f.line(D, B, w=6)
    f.dot(O)
    f.text((O[0] + 16, O[1] - R / 2), '1', size=19)
    f.label(A, 'A', dy=-16)
    f.label(B, 'B', dy=18)
    f.label(C, 'C', dx=-16, dy=-6)
    f.label(D, 'D', dx=-16, dy=6)
    f.label(O, 'O', dx=-14, dy=0)
    return f


@fig('27-6')
def _():
    f = Fig(420, 330)
    o = (40, 285)
    f.line((15, o[1]), (400, o[1]), w=1.8)
    f.line((o[0], 315), (o[0], 20), w=1.8)
    f.poly([(400, o[1]), (390, o[1] - 5), (390, o[1] + 5)], fill='#1f2328', w=1)
    f.poly([(o[0], 20), (o[0] - 5, 30), (o[0] + 5, 30)], fill='#1f2328', w=1)
    f.text((406, o[1] + 18), 'x', size=19, italic=True)
    f.text((o[0] - 16, 26), 'y', size=19, italic=True)
    A, B, C = (190, 80), (110, 240), (285, 240)
    D = (A[0], B[1])
    f.poly([A, B, C])
    f.line(A, D)
    f.right(D, A, C, s=11)
    f.dot(A)
    f.text((A[0] + 6, A[1] - 20), 'A(3,7)', size=18)
    f.text((D[0] + 4, D[1] + 22), 'D(x,y)', size=18)
    f.label(B, 'B', dx=-12, dy=16)
    f.label(C, 'C', dx=14, dy=16)
    return f


# ---------------------------------------------------------------- set 28
@fig('28-5')
def _():
    f = Fig(380, 380)
    c, R = (190, 190), 170
    V = [polar(c, R, 112.5 - 45 * k) for k in range(8)]   # V0 top-left, clockwise
    f.shade([V[7], V[2], V[3], V[6]], fill='#5f645e')
    f.poly(V)
    f.line(V[7], V[2])
    f.line(V[6], V[3])
    return f


@fig('28-8')
def _():
    f = Fig(460, 340)
    c, R = (230, 185), 120
    names = 'CDEAB'
    P = [polar(c, R, 90 - 72 * k) for k in range(5)]   # C top, then D, E, A, B clockwise
    r = 48
    # dark: each circle minus the part inside the pentagon (clip by an even-odd path)
    poly = 'M' + ' L'.join('%.1f %.1f' % p for p in P) + ' Z'
    f.items.append('<defs><clipPath id="out288"><path clip-rule="evenodd" d="M0 0 H460 V340 H0 Z %s"/></clipPath></defs>' % poly)
    for p in P:
        f.items.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="#5f645e" clip-path="url(#out288)"/>' % (p[0], p[1], r))
    for p in P:
        f.circle(p, r, w=1.8)
    f.poly(P, fill='#fff')
    for p, n in zip(P, names):
        q = (p[0] + (c[0] - p[0]) * .22, p[1] + (c[1] - p[1]) * .22)
        f.label(q, n)
    return f


# ---------------------------------------------------------------- set 29
@fig('29-4')
def _():
    f = Fig(400, 420)
    R = 180
    O = (200, 200)
    A = (O[0], O[1] + R)
    B = (O[0], O[1] - R / 2)
    c = (O[0], (A[1] + B[1]) / 2)
    r = (A[1] - B[1]) / 2
    f.items.append('<path d="M%.1f %.1f a%d %d 0 1 0 0.1 0 Z M%.1f %.1f a%.1f %.1f 0 1 0 0.1 0 Z" fill="#c9ccc8" fill-rule="evenodd"/>'
                   % (O[0], O[1] - R, R, R, c[0], c[1] - r, r, r))
    f.circle(O, R)
    f.circle(c, r, fill='#fff')
    f.line(A, B, w=2)
    f.dot(O, 4.5)
    f.dot(A)
    f.dot(B)
    f.label(O, 'O', dx=20)
    f.label(A, 'A', dy=22)
    f.label(B, 'B', dx=-18, dy=-4)
    return f


@fig('29-9')
def _():
    f = Fig(400, 340)
    c, R = (200, 170), 150
    V = [polar(c, R, a) for a in (180, 120, 60, 0, 300, 240)]   # A left, B top-left, …
    A, B, _, D, C, _ = V
    f.poly(V, w=1.6)
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        f.line(p, q, w=4.2)
    f.label(A, 'A', dx=-18)
    f.label(B, 'B', dx=-10, dy=-18)
    f.label(D, 'D', dx=18)
    f.label(C, 'C', dx=8, dy=20)
    return f


# ---------------------------------------------------------------- set 31
@fig('31-1')
def _():
    f = Fig(400, 380)
    o, u = (60, 330), 72
    P = lambda x, y: (o[0] + x * u, o[1] - y * u)  # noqa: E731
    f.line((20, o[1]), (390, o[1]), w=1.8)
    f.line((o[0], 365), (o[0], 15), w=1.8)
    f.poly([(390, o[1]), (380, o[1] - 5), (380, o[1] + 5)], fill='#1f2328', w=1)
    f.poly([(o[0], 15), (o[0] - 5, 25), (o[0] + 5, 25)], fill='#1f2328', w=1)
    f.text((392, o[1] + 20), 'x', size=19, italic=True)
    f.text((o[0] - 16, 22), 'y', size=19, italic=True)
    A, B, C, D = P(0, 2), P(1, 0), P(3, 1), P(2, 3)
    f.poly([A, B, C, D])
    f.dot(A)
    f.dot(B)
    f.text((A[0] - 34, A[1]), '(0,a)', size=18)
    f.text((B[0] + 10, B[1] + 22), 'B(b,0)', size=18)
    f.label(C, 'C', dx=16, dy=6)
    f.label(D, 'D', dx=4, dy=-18)
    return f


@fig('31-5')
def _():
    f = Fig(340, 340)
    c = (170, 170)
    R = 150
    r = R / 5 ** 0.5
    f.items.append('<path d="M%.1f %.1f a%d %d 0 1 0 0.1 0 Z M%.1f %.1f a%.1f %.1f 0 1 0 0.1 0 Z" fill="#c9ccc8" fill-rule="evenodd"/>'
                   % (c[0], c[1] - R, R, R, c[0], c[1] - r, r, r))
    f.circle(c, R)
    f.circle(c, r)
    f.dot(c, 4)
    return f


@fig('31-8')
def _():
    f = Fig(380, 380)
    o, u = (40, 340), 60
    P = lambda x, y: (o[0] + x * u, o[1] - y * u)  # noqa: E731
    C, B, A, D = P(0, 0), P(5, 0), P(5, 5), P(0, 5)
    G, F, H, E = P(2, 0), P(5, 3), P(0, 2), P(3, 5)
    f.shade([E, F, G, H], fill='#c9ccc8')
    f.poly([A, B, C, D])
    f.poly([E, F, G, H])
    f.angle(G, B, F, r=30, text='45°', tr=50)
    for p_, n, dx, dy in ((A, 'A', 14, -10), (B, 'B', 14, 10), (C, 'C', -14, 10), (D, 'D', -14, -10),
                          (E, 'E', 0, -18), (F, 'F', 16, 0), (G, 'G', 0, 20), (H, 'H', -16, 0)):
        f.label(p_, n, dx, dy)
    return f


# ---------------------------------------------------------------- set 32
@fig('32-3')
def _():
    f = Fig(360, 360)
    c, r = (180, 180), 105
    R = r * 2 ** 0.5
    sq = [(c[0] - r, c[1] - r), (c[0] + r, c[1] - r), (c[0] + r, c[1] + r), (c[0] - r, c[1] + r)]
    f.items.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z M%.1f %.1f a%d %d 0 1 0 0.1 0 Z" fill="#c9ccc8" fill-rule="evenodd"/>'
                   % (sq[0] + sq[1] + sq[2] + sq[3] + (c[0], c[1] - r, r, r)))
    f.circle(c, R)
    f.poly(sq)
    f.circle(c, r)
    f.dot(c, 4)
    f.line(c, (c[0] + r, c[1]), w=1.8)
    f.text((c[0] + r / 2, c[1] - 13), 'r', size=19, italic=True)
    return f


@fig('32-8')
def _():
    f = Fig(400, 380)
    s, dx, dy = 210, 100, -85
    ftl, ftr, fbr, fbl = (40, 130), (40 + s, 130), (40 + s, 130 + s), (40, 130 + s)
    b = lambda p: (p[0] + dx, p[1] + dy)  # noqa: E731
    f.items.append('<defs><pattern id="h328" width="8" height="8" patternUnits="userSpaceOnUse">'
                   '<line x1="0" y1="0" x2="0" y2="8" stroke="#1f2328" stroke-width="1.4"/></pattern></defs>')
    for tri in ([ftl, ftr, b(ftr)], [ftl, ftr, fbr], [ftr, b(ftr), fbr]):
        f.items.append('<polygon points="%s" fill="url(#h328)"/>' % ' '.join('%.1f,%.1f' % q for q in tri))
    f.poly([ftl, ftr, fbr, fbl])
    f.poly([ftl, b(ftl), b(ftr), ftr], close=False)
    f.poly([ftr, b(ftr), b(fbr), fbr], close=False)
    f.line(ftl, b(ftr), w=2.8)
    f.line(ftl, fbr, w=2.8)
    f.line(b(ftr), fbr, w=2.8)
    return f


@fig('32-10')
def _():
    f = Fig(340, 340)
    O, R = (160, 170), 140
    P1, P2 = polar(O, R, 30), polar(O, R, -42)
    f.circle(O, R, w=1.8)
    f.path('M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (P1[0], P1[1], R, R, P2[0], P2[1]), w=6)
    f.line(O, P1, w=1.8)
    f.line(O, P2, w=1.8)
    f.dot(O, 4.5)
    f.angle(O, P1, P2, r=34, text='72°', tr=56)
    f.label(O, 'O', dx=-18)
    return f


# ---------------------------------------------------------------- set 33
@fig('33-1')
def _():
    import math
    f = Fig(590, 440)
    u = 52
    B = (360, 410)
    A = (B[0], B[1] - 5 * u)          # AB = 5
    E = (B[0], B[1] - u)              # EB = 1, AE = 4
    C = (B[0] - 2.5 * u, B[1])        # CB chosen so that the figure is like the book's
    t = (E[1] - A[1]) / (C[1] - A[1])
    D = (A[0] + (C[0] - A[0]) * t, E[1])   # D on AC, on the line through E (parallel to CB)
    F, G = (A[0] + 4 * u, A[1]), (A[0] + 4 * u, E[1])
    # square ADHK on AD, away from the triangle
    vx, vy = D[0] - A[0], D[1] - A[1]
    K, H = (A[0] - vy, A[1] + vx), (D[0] - vy, D[1] + vx)
    f.poly([A, F, G, E])
    f.poly([A, D, H, K])
    f.poly([A, C, B], close=True)
    f.line(D, E)
    f.right(B, A, C, s=11)
    for p_, n, dx, dy in ((A, 'A', 6, -18), (F, 'F', 14, -10), (G, 'G', 14, 12), (E, 'E', 14, 12), (B, 'B', 12, 16),
                          (C, 'C', -14, 12), (D, 'D', -16, -8), (H, 'H', -16, 4), (K, 'K', -6, -16)):
        f.label(p_, n, dx, dy)
    return f


@fig('33-5')
def _():
    f = Fig(380, 360)
    c, R = (190, 180), 165
    V = [polar(c, R, 112.5 - 45 * k) for k in range(8)]   # V0 top-left, clockwise
    A, C = V[6], V[3]                  # lower ends of the two vertical sides
    B = (V[1][0], A[1])
    f.poly(V)
    f.line(A, C)
    f.line(V[1], V[4])
    f.right(A, V[7], C, s=13)
    f.right(B, V[4], A, s=13)
    f.label(A, 'A', dx=-18)
    f.label(C, 'C', dx=18)
    f.label(B, 'B', dx=-14, dy=-16)
    return f


# ---------------------------------------------------------------- set 34
@fig('34-1')
def _():
    f = Fig(440, 230)
    P, Q = (40, 170), (400, 170)
    T = (165, 80)
    f.poly([P, Q, T])
    f.angle(T, P, Q, r=24, text='α', tr=40)
    f.text(((P[0] + Q[0]) / 2, 196), '7 ס"מ', size=19, rtl=True)
    f.text((70, 112), 'x ס"מ', size=19, rtl=True)
    f.text((315, 102), 'y ס"מ', size=19, rtl=True)
    return f


@fig('34-6')
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


# ---------------------------------------------------------------- set 36
@fig('36-1')
def _():
    f = Fig(360, 380)
    c, R = (180, 190), 170
    V = [polar(c, R, 90 + 60 * k) for k in range(6)]
    inner = [polar(c, R / 3 ** 0.5, 60 * k) for k in range(6)]   # vertices of the small hexagon
    f.shade(inner, fill='#c9ccc8')
    f.poly(V)
    f.poly([V[0], V[2], V[4]])
    f.poly([V[1], V[3], V[5]])
    return f


# ---------------------------------------------------------------- set 37
@fig('37-6')
def _():
    f = Fig(360, 360)
    O, R = (180, 180), 150
    for a, b in ((0, 90), (120, 180), (234, 306)):
        p, q = polar(O, R, a), polar(O, R, b)
        f.shade_path('M%.1f %.1f L%.1f %.1f A%d %d 0 0 0 %.1f %.1f Z' % (O[0], O[1], p[0], p[1], R, R, q[0], q[1]))
    f.circle(O, R)
    for a in (0, 90, 120, 180, 234, 306):
        f.line(O, polar(O, R, a))
    f.right(O, polar(O, R, 0), polar(O, R, 90), s=14)
    f.text(polar(O, 48, 150), '60°', size=17)
    f.text(polar(O, 52, 270), '72°', size=17)
    f.dot(O, 4.5)
    f.label(O, 'O', dx=14, dy=16)
    return f


@fig('37-8')
def _():
    f = Fig(480, 320)
    D, C = (40, 280), (400, 280)
    A = (275, 50)
    B = (440, 75)
    f.poly([A, B, C, D])
    f.line(A, C)
    f.angle(A, D, C, r=26, text='α', tr=40)
    f.angle(A, C, B, r=46, text='β+10°', tr=74)
    f.angle(C, D, A, r=26, text='α', tr=40)
    f.angle(C, A, B, r=46, text='β', tr=60)
    f.seglabel(A, D, '8', off=18)
    f.seglabel(B, C, '5', off=-18)
    f.label(A, 'A', dy=-18)
    f.label(B, 'B', dx=16, dy=-6)
    f.label(C, 'C', dx=12, dy=16)
    f.label(D, 'D', dx=-14, dy=12)
    return f


# ---------------------------------------------------------------- set 38
@fig('38-3')
def _():
    f = Fig(380, 380)
    O, R, r = (190, 190), 165, 95
    def sector(rad, a, b):
        p, q = polar(O, rad, a), polar(O, rad, b)
        return 'M%.1f %.1f L%.1f %.1f A%d %d 0 0 0 %.1f %.1f Z' % (O[0], O[1], p[0], p[1], rad, rad, q[0], q[1])
    # ring sector of 60 degrees (between 15 and 75), and two small-circle sectors filling the rest of the half-plane
    p1, p2, q1, q2 = polar(O, R, 15), polar(O, R, 75), polar(O, r, 15), polar(O, r, 75)
    f.shade_path('M%.1f %.1f A%d %d 0 0 0 %.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z'
                 % (p1[0], p1[1], R, R, p2[0], p2[1], q2[0], q2[1], r, r, q1[0], q1[1]))
    f.shade_path(sector(r, 75, 135))
    f.shade_path(sector(r, -45, 15))
    f.circle(O, R)
    f.circle(O, r)
    f.line(polar(O, R, 135), polar(O, R, 315))
    f.line(O, polar(O, R, 75))
    f.line(O, polar(O, R, 15))
    f.text(polar(O, 62, 45), '60°', size=17)
    f.dot(O, 4.5)
    f.label(O, 'O', dx=-16, dy=14)
    return f


@fig('38-4')
def _():
    import math
    f = Fig(420, 420)
    O, R = (215, 210), 185
    A, B, C, E = polar(O, R, 205), polar(O, R, 148), polar(O, R, 92), polar(O, R, -18)
    D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])         # rhombus-like ABCD (as in the book)
    F = (B[0] + E[0] - C[0], B[1] + E[1] - C[1])         # parallelogram BCEF
    f.circle(O, R)
    f.poly([A, B, C, D])
    f.poly([B, C, E, F])
    f.angle(A, B, D, r=24, text='α', tr=38)
    f.angle(B, A, F, r=26, text='β', tr=42)
    f.angle(C, D, E, r=26, text='?', tr=42)
    for p_, n, dx, dy in ((A, 'A', -16, 10), (B, 'B', -16, -8), (C, 'C', 0, -18), (D, 'D', 16, 6), (E, 'E', 16, 8), (F, 'F', 4, 20)):
        f.label(p_, n, dx, dy)
    return f


@fig('38-6')
def _():
    f = Fig(380, 360)
    c = (190, 180)
    s = 95
    h = s * 3 ** 0.5 / 2
    V = [(c[0] - s, c[1]), (c[0] - s / 2, c[1] - h), (c[0] + s / 2, c[1] - h), (c[0] + s, c[1]), (c[0] + s / 2, c[1] + h), (c[0] - s / 2, c[1] + h)]
    TL, TR, BR, BL = (c[0] - s, c[1] - h), (c[0] + s, c[1] - h), (c[0] + s, c[1] + h), (c[0] - s, c[1] + h)
    for tri in ((V[0], TL, V[1]), (V[2], TR, V[3]), (V[3], BR, V[4]), (V[5], BL, V[0])):
        f.shade(list(tri), fill='#5f645e')
    f.poly([TL, TR, BR, BL])
    f.poly(V)
    return f


@fig('38-10')
def _():
    f = Fig(320, 440)
    c, rx, ry = (160, 360), 120, 34
    hgt = 130
    top = (c[0], c[1] - hgt)
    apex = (c[0], c[1] - 2 * hgt - 30)
    f.ellipse(top, (rx, 0), (0, ry), w=2.2)
    f.path('M%.1f %.1f A%d %d 0 0 0 %.1f %.1f' % (c[0] - rx, c[1], rx, ry, c[0] + rx, c[1]), w=2.4)
    f.path('M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (c[0] - rx, c[1], rx, ry, c[0] + rx, c[1]), w=1.6)
    f.line((c[0] - rx, c[1]), (c[0] - rx, top[1]))
    f.line((c[0] + rx, c[1]), (c[0] + rx, top[1]))
    f.line(apex, (c[0] - rx, c[1]))
    f.line(apex, (c[0] + rx, c[1]))
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
