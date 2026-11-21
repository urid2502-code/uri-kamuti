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
