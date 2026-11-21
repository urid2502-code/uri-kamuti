"""Lay out solutions and givens so they read cleanly, on a phone too.

  * explanations (p.steps) and common traps (p.pit): one sentence per line,
    <span class="ln">…</span>; the steps get numbers from CSS when there are several;
  * "נתון:" paragraphs in the question text: one given per line;
  * math (<bdi class="m">) may wrap only after "=", "⇒" or "≈", never inside a term:
    other spaces in it become no-break spaces.

Idempotent. Run after fix_bidi.py:  python3 tools/bidi/layout.py
"""
import glob
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NBSP = ' '
TOKEN = re.compile(r'<[^>]+>|[^<]+')


def split_sentences(inner):
    """Split inner HTML into sentences at top-level ". ", "? ", "; " (outside tags and brackets)."""
    out, cur, depth, paren = [], '', 0, 0
    for tok in TOKEN.findall(inner):
        if tok.startswith('<'):
            if tok.startswith('</'):
                depth -= 1
            elif not tok.endswith('/>') and not re.match(r'<(br|img|wbr)\b', tok):
                depth += 1
            cur += tok
            continue
        if depth > 0:
            cur += tok
            continue
        i = 0
        while i < len(tok):
            c = tok[i]
            cur += c
            if c == '(':
                paren += 1
            elif c == ')':
                paren = max(0, paren - 1)
            elif c in '.?;' and paren == 0 and i + 1 < len(tok) and tok[i + 1] == ' ':
                out.append(cur)
                cur = ''
                i += 1  # drop the space between sentences
                while i + 1 < len(tok) and tok[i + 1] == ' ':
                    i += 1
            i += 1
    if cur.strip():
        out.append(cur)
    return [s.strip() for s in out if s.strip()]


def conclusions(sentence):
    """A "⇐" in the Hebrew flow (outside math) starts a conclusion: put it on its own line."""
    out, depth = '', 0
    for tok in TOKEN.findall(sentence):
        if tok.startswith('<'):
            depth += -1 if tok.startswith('</') else (0 if tok.endswith('/>') else 1)
            out += tok
        elif depth == 0 and ' ⇐ ' in tok:
            out += tok.replace(' ⇐ ', '\x00')
        else:
            out += tok
    head, *rest = out.split('\x00')
    return head + ''.join('<span class="th">⇐ %s</span>' % r for r in rest)


CHAIN_MIN = 28  # characters of math text; shorter chains stay on one line


def split_chain(m):
    """A long math chain "a ⇒ b ⇒ c" in a solution step: each ⇒ starts a new line."""
    inner = m.group(2)
    if 'class="mc"' in inner or len(re.sub(r'<[^>]+>', '', inner)) < CHAIN_MIN:
        return m.group(0)
    out, depth = [], 0
    for tok in TOKEN.findall(inner):
        if tok.startswith('<'):
            depth += -1 if tok.startswith('</') else (0 if tok.endswith('/>') else 1)
        elif depth == 0:
            tok = re.sub(r'[ \u00a0]⇒[ \u00a0]', '\x00⇒\u00a0', tok)
        out.append(tok)
    parts = ''.join(out).split('\x00')
    if len(parts) == 1:
        return m.group(0)
    return ''.join(m.group(1) + '<span class="mc">' + p + '</span>' + m.group(3) for p in parts)


def nowrap_parens(html, limit=24):
    """Keep a short "( … )" on one line: its spaces become no-break spaces."""
    toks = TOKEN.findall(html)
    flat = []  # (token index, char index) of every top-level text character
    depth = 0
    for ti, tok in enumerate(toks):
        if tok.startswith('<'):
            depth += -1 if tok.startswith('</') else (0 if tok.endswith('/>') else 1)
            continue
        if depth == 0:
            flat += [(ti, ci) for ci in range(len(tok))]
    chars = ''.join(toks[ti][ci] for ti, ci in flat)
    edits = set()
    for i, c in enumerate(chars):
        if c != '(':
            continue
        j = chars.find(')', i)
        if j < 0:
            continue
        a, b = flat[i], flat[j]
        visible = re.sub(r'<[^>]+>', '', ''.join(toks[a[0]:b[0] + 1]))
        if len(visible) <= limit + 40 and j - i <= limit:
            edits |= {flat[k] for k in range(i, j) if chars[k] == ' '}
    if not edits:
        return html
    toks = [list(t) if not t.startswith('<') else t for t in toks]
    for ti, ci in edits:
        toks[ti][ci] = NBSP
    return ''.join(t if isinstance(t, str) else ''.join(t) for t in toks)


def lines(inner, chain=False):
    if 'class="ln"' in inner:
        return inner
    parts = split_sentences(inner)
    if chain:
        parts = [BDI.sub(split_chain, conclusions(p)) for p in parts]
        parts = [re.sub(r'(</span></bdi>)\.$', r'\1', p) for p in parts]
    parts = [nowrap_parens(p) for p in parts]
    return ''.join('<span class="ln">%s</span>' % p for p in parts)


def para(cls):
    return re.compile(r'(<p class="%s">)(.*?)(</p>)' % cls, re.S)


GIVEN = re.compile(r'(<p>)(נתון[^<:]{0,30}:.*?)(</p>)', re.S)
BDI = re.compile(r'(<bdi dir="ltr" class="m">)(.*?)(</bdi>)', re.S)


MATH_BREAK_MIN = 30  # shorter expressions never wrap


def keep_math_together(inner):
    if len(re.sub(r'<[^>]+>', '', inner)) < MATH_BREAK_MIN:
        return re.sub(r'(?<=[^<]) (?=[^>]*(<|$))', NBSP, inner) if '<' in inner else inner.replace(' ', NBSP)
    out = []
    for tok in TOKEN.findall(inner):
        if tok.startswith('<'):
            out.append(tok)
            continue
        # a normal space stays only right after =, ⇒, ≈ (the allowed break points)
        tok = re.sub(r'(?<![=⇒≈]) ', NBSP, tok)
        out.append(tok)
    return ''.join(out)


def fix(html):
    for cls in ('steps', 'pit'):
        html = para(cls).sub(lambda m: m.group(1) + lines(m.group(2), chain=cls == 'steps') + m.group(3), html)
    html = GIVEN.sub(lambda m: m.group(1) + (lines(m.group(2)) if len(split_sentences(m.group(2))) > 1 else m.group(2)) + m.group(3), html)
    html = BDI.sub(lambda m: m.group(1) + keep_math_together(m.group(2)) + m.group(3), html)
    return html


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(REPO, 'sets', '*.html'))) + [os.path.join(REPO, 'solutions.html')]:
        s = open(f, encoding='utf-8').read()
        t = fix(s)
        if t != s:
            open(f, 'w', encoding='utf-8').write(t)
            n += 1
    print('pages changed:', n)


if __name__ == '__main__':
    main()
