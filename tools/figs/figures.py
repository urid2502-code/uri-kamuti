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
