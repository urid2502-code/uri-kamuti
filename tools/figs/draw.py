"""Redraw the book's figures as clean SVG (fig/N-M.svg).

Each figure in figures.py is a function that draws on a Fig. Coordinates are in
SVG units (y grows downward). Labels are placed by hand, next to their point.
    python3 tools/figs/figures.py            # writes every figure
"""
import math

INK = '#1f2328'
FONT = "'IBM Plex Sans','Arial',sans-serif"


class Fig:
    def __init__(self, w, h, pad=0):
        self.w, self.h, self.items = w, h, []

    # ---- primitives -------------------------------------------------------
    def line(self, p, q, w=2.4, dash=False):
        d = ' stroke-dasharray="7 6"' if dash else ''
        self.items.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>'
                          % (p[0], p[1], q[0], q[1], INK, w, d))

    def poly(self, pts, close=True, w=2.4, fill='none', dash=False):
        tag = 'polygon' if close else 'polyline'
        d = ' stroke-dasharray="7 6"' if dash else ''
        self.items.append('<%s points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>'
                          % (tag, ' '.join('%.1f,%.1f' % p for p in pts), fill, INK, w, d))

    def circle(self, c, r, w=2.4, fill='none', dash=False):
        d = ' stroke-dasharray="7 6"' if dash else ''
        self.items.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (c[0], c[1], r, fill, INK, w, d))

    def ellipse(self, c, u, v, w=2.4, dash=False):
        """Ellipse c + u·cos t + v·sin t: a circle seen in a slanted face (u, v = half-edges)."""
        d = ' stroke-dasharray="7 6"' if dash else ''
        self.items.append('<circle r="1" fill="none" stroke="%s" stroke-width="%s" vector-effect="non-scaling-stroke"%s '
                          'transform="matrix(%.3f %.3f %.3f %.3f %.1f %.1f)"/>' % (INK, w, d, u[0], u[1], v[0], v[1], c[0], c[1]))

    def arrow2(self, p, q, w=1.8, s=9):
        """Double-headed dimension arrow from p to q."""
        self.line(p, q, w=w)
        for a, b in ((p, q), (q, p)):
            ux, uy = unit(a, b)
            self.poly([a, (a[0] + ux * s - uy * s * .5, a[1] + uy * s + ux * s * .5),
                       (a[0] + ux * s + uy * s * .5, a[1] + uy * s - ux * s * .5)], fill=INK, w=1)

    def dot(self, p, r=3.6):
        self.items.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (p[0], p[1], r, INK))

    def path(self, d, w=2.4, fill='none'):
        self.items.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (d, fill, INK, w))

    def shade(self, pts, fill='#d9dcd8'):
        self.items.insert(0, '<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % p for p in pts), fill))

    def shade_path(self, d, fill='#d9dcd8'):
        self.items.insert(0, '<path d="%s" fill="%s"/>' % (d, fill))

    def text(self, p, s, size=20, anchor='middle', italic=False, weight=500):
        st = ' font-style="italic"' if italic else ''
        s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        self.items.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" dominant-baseline="central" font-weight="%s"%s fill="%s">%s</text>'
                          % (p[0], p[1], size, anchor, weight, st, INK, s))

    def label(self, p, s, dx=0, dy=0, size=21):
        """A point's name, offset from the point."""
        self.text((p[0] + dx, p[1] + dy), s, size=size, weight=600)

    # ---- marks -------------------------------------------------------------
    def angle(self, v, a, b, r=24, text=None, tr=None, w=1.8):
        """Arc for the angle at v between rays v→a and v→b (the smaller one)."""
        a1 = math.atan2(a[1] - v[1], a[0] - v[0])
        a2 = math.atan2(b[1] - v[1], b[0] - v[0])
        d = (a2 - a1) % (2 * math.pi)
        if d > math.pi:
            a1, a2, d = a2, a1, 2 * math.pi - d
        p1 = (v[0] + r * math.cos(a1), v[1] + r * math.sin(a1))
        p2 = (v[0] + r * math.cos(a1 + d), v[1] + r * math.sin(a1 + d))
        self.items.append('<path d="M%.1f %.1fA%s %s 0 0 1 %.1f %.1f" fill="none" stroke="%s" stroke-width="%s"/>'
                          % (p1[0], p1[1], r, r, p2[0], p2[1], INK, w))
        if text:
            m = a1 + d / 2
            rr = tr or r + 13
            self.text((v[0] + rr * math.cos(m), v[1] + rr * math.sin(m)), text, size=18, italic=text.isalpha() and len(text) == 1)

    def right(self, v, a, b, s=13, w=1.8):
        """Right-angle square at v between v→a and v→b."""
        ua, ub = unit(v, a), unit(v, b)
        p1 = (v[0] + ua[0] * s, v[1] + ua[1] * s)
        p3 = (v[0] + ub[0] * s, v[1] + ub[1] * s)
        p2 = (p1[0] + ub[0] * s, p1[1] + ub[1] * s)
        self.items.append('<polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="%s"/>'
                          % (p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], INK, w))

    def tick(self, p, q, n=1, s=7, w=1.8):
        """Equal-length ticks across the middle of segment pq."""
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        u = unit(p, q)
        nrm = (-u[1], u[0])
        for k in range(n):
            o = (k - (n - 1) / 2) * 5
            c = (m[0] + u[0] * o, m[1] + u[1] * o)
            self.line((c[0] - nrm[0] * s, c[1] - nrm[1] * s), (c[0] + nrm[0] * s, c[1] + nrm[1] * s), w=w)

    def seglabel(self, p, q, s, off=16, size=19, side=1):
        """A length written beside the middle of segment pq."""
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        u = unit(p, q)
        nrm = (-u[1] * side, u[0] * side)
        self.text((m[0] + nrm[0] * off, m[1] + nrm[1] * off), s, size=size, italic=s.isalpha() and len(s) == 1)

    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="%s">'
                '<rect width="%d" height="%d" fill="#fff"/>%s</svg>\n'
                % (self.w, self.h, FONT, self.w, self.h, ''.join(self.items)))


def unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n


def polar(c, r, deg):
    """Point on a circle; deg counter-clockwise from the positive x axis (as on paper)."""
    t = math.radians(deg)
    return (c[0] + r * math.cos(t), c[1] - r * math.sin(t))


def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
