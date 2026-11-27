"""Helpers for the extra-set modules: answers are computed, then checked."""
import math
import os
import sys
from fractions import Fraction as F  # noqa: F401  (re-exported for the modules)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'figs'))
from draw import Fig, polar, lerp, unit  # noqa: E402,F401


def which(values, correct, tol=1e-9):
    """1-based index of the one value equal to `correct`; fails unless exactly one matches."""
    hits = [i for i, v in enumerate(values, 1) if abs(float(v) - float(correct)) < tol]
    assert len(hits) == 1, (values, correct, hits)
    return hits[0]


def only(flags):
    """1-based index of the one True in `flags` (e.g. which statement must hold)."""
    hits = [i for i, f in enumerate(flags, 1) if f]
    assert len(hits) == 1, flags
    return hits[0]


def grid(lo=-6, hi=6, step=0.5):
    n = int(round((hi - lo) / step))
    return [lo + k * step for k in range(n + 1)]


def axes(f, o, u, xr, yr, xl='x', yl='y'):
    """Coordinate axes through origin o with unit u; xr/yr = (min, max) in units."""
    x0, x1 = o[0] + xr[0] * u, o[0] + xr[1] * u
    y0, y1 = o[1] - yr[0] * u, o[1] - yr[1] * u
    f.line((x0, o[1]), (x1, o[1]), w=1.8)
    f.line((o[0], y0), (o[0], y1), w=1.8)
    f.poly([(x1 + 10, o[1]), (x1, o[1] - 5), (x1, o[1] + 5)], fill='#1f2328', w=1)
    f.poly([(o[0], y1 - 10), (o[0] - 5, y1), (o[0] + 5, y1)], fill='#1f2328', w=1)
    f.text((x1 + 16, o[1] + 16), xl, size=19, italic=True)
    f.text((o[0] - 14, y1 - 6), yl, size=19, italic=True)
    return lambda x, y: (o[0] + x * u, o[1] - y * u)


def ok(cond, msg=''):
    assert cond, msg


SQ2, SQ3 = math.sqrt(2), math.sqrt(3)
