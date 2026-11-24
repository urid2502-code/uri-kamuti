"""Keep Hebrew text and math from mixing in right-to-left pages.

Math is shown inside <bdi dir="ltr" class="m"> isolates. This tool:
  1. trims separators that belong to the Hebrew sentence off the edges of each
     isolate ("= 8", "x > y + z –", "60° ⇒") and splits isolates at sentence
     breaks ("ABCD = 18. FH = 2"), so they are placed in the right order;
  2. wraps math that was left as bare text in solutions and lessons
     ("9 · 10 = 90", "t² − 7t − 120 = 0 ⇒ t = 15"), which otherwise reads backwards;
  3. turns a stand-alone "⇒" in the Hebrew flow into "⇐", because arrows are not
     mirrored automatically and the sentence reads right to left.

It is idempotent. Run from the repository root, then `node scripts/build.mjs`:
    python3 tools/bidi/fix_bidi.py
"""
import glob
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OPEN = '<bdi dir="ltr" class="m">'
BDI = re.compile(r'<bdi dir="ltr" class="m">(.*?)</bdi>', re.S)

# Entities are mapped to private-use characters while working on text.
ENT = {'&lt;': '', '&gt;': '', '&amp;': ''}
UNENT = {v: k for k, v in ENT.items()}
LT, GT = ENT['&lt;'], ENT['&gt;']


def dec(s):
    for k, v in ENT.items():
        s = s.replace(k, v)
    return s


def enc(s):
    for k, v in UNENT.items():
        s = s.replace(k, v)
    return s


OPS = '=⇒⇔→–—+−·×÷±≤≥≠≈:' + LT + GT  # binary separators
EDGE_OP_LEAD = re.compile(r'^(\s*[' + OPS + r']\s+|\s*[\'"]|\s+)')
EDGE_OP_TRAIL = re.compile(r'(\s*[.?,;:]|\s+[' + OPS + r']\s*|\s+)$')
ALNUM = re.compile(r'[A-Za-z0-9²³¹⁰-⁹½⅓⅔¼¾⅕⅙⅛⅑π√∞$]')
HEB = re.compile(r'[֐-׿]')


def flip_arrows(text):
    """Arrows that sit in the Hebrew (right-to-left) flow point the reading way."""
    return text.replace('⇒', '⇐')


def split_top(inner):
    """Split an isolate's inner HTML at top-level sentence breaks (". ", "; ")."""
    parts, depth, paren, last, i = [], 0, 0, 0, 0
    while i < len(inner):
        c = inner[i]
        if c == '<':
            j = inner.index('>', i)
            tag = inner[i:j + 1]
            if not tag.startswith('</') and not tag.endswith('/>'):
                depth += 1
            elif tag.startswith('</'):
                depth -= 1
            i = j + 1
            continue
        if depth == 0:
            if c == '(':
                paren += 1
            elif c == ')':
                paren = max(0, paren - 1)
            elif c in '.,;:?' and paren == 0 and i + 1 < len(inner) and inner[i + 1] == ' ' \
                    and i > 0 and not inner[i - 1].isspace():
                parts.append((inner[last:i], c + ' '))
                last = i + 2
                i += 2
                continue
        i += 1
    parts.append((inner[last:], ''))
    return parts


def wrap(chunk):
    """Re-emit one math chunk: separators on its edges go outside the isolate."""
    if not chunk:
        return ''
    if '<' not in chunk and not ALNUM.search(chunk):
        return flip_arrows(chunk)  # "= ?" and the like: nothing to isolate
    lead = trail = ''
    while chunk:
        m = EDGE_OP_LEAD.match(chunk)
        if not m:
            break
        lead, chunk = lead + m.group(1), chunk[m.end():]
    while chunk:
        m = EDGE_OP_TRAIL.search(chunk)
        if not m:
            break
        trail, chunk = m.group(1) + trail, chunk[:m.start()]
    if chunk and '<' not in chunk and not ALNUM.search(chunk):
        return flip_arrows(lead + chunk + trail)
    return flip_arrows(lead) + (OPEN + chunk + '</bdi>' if chunk else '') + flip_arrows(trail)


def fix_isolates(html):
    def rep(m):
        inner = dec(m.group(1))
        out = ''
        for chunk, sep in split_top(inner):
            # trailing punctuation inside a chunk (". ", "?") belongs to the sentence
            out += wrap(chunk) + sep
        return enc(out)
    return BDI.sub(rep, html)


# ---------- wrapping bare math in explanation text ----------
MATHCH = r"\^÷±…′″A-Za-z0-9.,'()\[\]=+−\-×·/≤≥≠≈⇒⇔→:!?$%°√π∞½⅓⅔¼¾⅕⅙⅛⅑⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ˣʸᵃᵇⁿᵏᵐᶜ∢∠△✓|– "
RUN = re.compile('[' + MATHCH + ']+')
CONTAINERS = [('p', 'steps'), ('p', 'pit'), ('p', 'sol-note'), ('span', 'pt'), ('span', 'pit'), ('div', 'tk')]
VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr'}
SKIP = {'bdi', 'a', 'small', 'script', 'style', 'svg', 'sup', 'sub'}


def trim_run(r):
    """Strip what belongs to the Hebrew sentence from both ends of a math run."""
    lead = trail = ''
    while True:
        changed = False
        m = re.match(r'^(\s+|[.,;:?)\]\'"]|[' + OPS + r'](?=\s))', r)
        if m and m.group(0):
            lead += m.group(0); r = r[m.end():]; changed = True
        m = re.search(r'(\s+|[.,;:?(\[]|(?<=\s)[' + OPS + r'])$', r)
        if m and m.group(0) and r:
            trail = m.group(0) + trail; r = r[:m.start()]; changed = True
        # unbalanced brackets on the edges
        if r.startswith('(') and r.count('(') > r.count(')'):
            lead += '('; r = r[1:]; changed = True
        if r.endswith(')') and r.count(')') > r.count('('):
            trail = ')' + trail; r = r[:-1]; changed = True
        if not changed or not r:
            return lead, r, trail


def split_run(r):
    """Split at sentence punctuation outside brackets: "a = 1. b = 2" -> two pieces."""
    out, depth, last = [], 0, 0
    for i, c in enumerate(r):
        if c in '([':
            depth += 1
        elif c in ')]':
            depth = max(0, depth - 1)
        elif c in '.,;:?' and depth == 0 and i + 1 < len(r) and r[i + 1] == ' ':
            out.append(r[last:i]); out.append(c + ' '); last = i + 2
    out.append(r[last:])
    # out alternates piece, separator, piece ...
    return out


def split_parens(r):
    """Unmatched brackets belong to the Hebrew sentence: "9 (9" -> "9", " (", "9"."""
    stack, bad = [], set()
    for i, c in enumerate(r):
        if c in '([':
            stack.append(i)
        elif c in ')]':
            if stack:
                stack.pop()
            else:
                bad.add(i)
    bad |= set(stack)
    out, last = [], 0
    for i in sorted(bad):
        out += [r[last:i], r[i]]
        last = i + 1
    return out + [r[last:]]


def wrap_text(text):
    t = dec(text)
    res, pos = '', 0
    for m in RUN.finditer(t):
        res += flip_arrows(t[pos:m.start()])
        pieces = []
        for k, p in enumerate(split_run(m.group(0))):
            pieces += [p] if k % 2 else split_parens(p)
        for k, p in enumerate(pieces):
            if k % 2:  # separator
                res += p
                continue
            lead, core, trail = trim_run(p)
            # a lone dash or digit run between Hebrew words is fine as is, but
            # anything with an operator, a sign, a range or Latin letters is isolated
            if core and ALNUM.search(core) and not re.fullmatch(r'\d+', core):
                res += flip_arrows(lead) + OPEN + core + '</bdi>' + flip_arrows(trail)
            else:
                res += flip_arrows(lead + core + trail)
        pos = m.end()
    res += flip_arrows(t[pos:])
    return enc(res)


TOKEN = re.compile(r'<!--.*?-->|<[^>]+>|[^<]+', re.S)


def fix_bare(html):
    out, stack = [], []  # stack of (tag, is_container, is_skip)
    for tok in TOKEN.findall(html):
        if tok.startswith('<!--'):
            out.append(tok); continue
        if tok.startswith('</'):
            name = tok[2:-1].strip().lower()
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == name:
                    del stack[k:]
                    break
            out.append(tok); continue
        if tok.startswith('<'):
            m = re.match(r'<([a-zA-Z0-9]+)', tok)
            name = m.group(1).lower() if m else ''
            cls = re.search(r'class="([^"]*)"', tok)
            cls = cls.group(1).split() if cls else []
            cont = any(name == t and c in cls for t, c in CONTAINERS)
            if name not in VOID and not tok.endswith('/>'):
                stack.append((name, cont, name in SKIP))
            out.append(tok); continue
        inside = any(s[1] for s in stack) and not any(s[2] for s in stack)
        out.append(wrap_text(tok) if inside and not tok.isspace() else tok)
    return ''.join(out)


def fix_html(html, bare=True):
    html = fix_isolates(html)
    if bare:
        html = fix_bare(html)
        html = fix_isolates(html)
    # adjacent isolates produced by splitting: "</bdi><bdi ...>" never happens
    # without a separator, so nothing to merge.
    return html


def main():
    changed = 0
    pages = sorted(glob.glob(os.path.join(REPO, 'sets', '*.html'))) + [
        os.path.join(REPO, f) for f in ('solutions.html', 'lessons.html', 'index.html', 'review.html', 'sets.html')]
    for f in pages:
        if not os.path.exists(f):
            continue
        s = open(f, encoding='utf-8').read()
        t = fix_html(s)
        if t != s:
            open(f, 'w', encoding='utf-8').write(t)
            changed += 1
    bank_path = os.path.join(REPO, 'data', 'bank.json')
    bank = json.load(open(bank_path, encoding='utf-8'))
    for st in bank['sets']:
        for q in st['questions']:
            if q.get('stem'):
                q['stem'] = fix_html(q['stem'], bare=False)
            if q.get('options'):
                q['options'] = [fix_html(o, bare=False) for o in q['options']]
    json.dump(bank, open(bank_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('pages changed:', changed)


if __name__ == '__main__':
    main()
