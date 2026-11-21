"""Render the detailed step-by-step explanations into the pages.

Source: data/explain/NN.json, one file per set:
    {"1-4": {"steps": ["line", "> sub-line", ...], "pit": ["line", ...]}}

Each "steps" line is one numbered step. A line that starts with "> " continues the
step above it on its own line (a calculation or a reason), without a number.
"pit" (optional) replaces the common-traps text.
"note" (optional) sets the note under the solution ("" removes it).
"resolved": true marks a question whose data was fixed as matching the key.

Light math markup inside a line:
    [a/b]      fraction a over b (a and b may hold more markup)
    x^(2y+1)   superscript of a group;  x^2, 5^x   superscript of one term
    √(a+b)     square root over a group
Everything else is written as it should read. Math is isolated left-to-right
automatically, so Hebrew and numbers never mix.

Writes sets/NN.html (the question card) and solutions.html. Idempotent.
    python3 tools/solutions/explain.py
"""
import glob
import html
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, 'tools', 'bidi'))
import fix_bidi  # noqa: E402
import layout  # noqa: E402

BDI = re.compile(r'(<bdi dir="ltr" class="m">)(.*?)(</bdi>)', re.S)


def group(s, i, open_, close):
    """Return (content, end) of a bracket group starting at s[i] == open_."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == open_:
            depth += 1
        elif s[j] == close:
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    return s[i + 1:], len(s)


def unwrap(x):
    """(a + b) as a numerator or denominator needs no brackets: the bar groups it."""
    if x.startswith('(') and group(x, 0, '(', ')')[1] == len(x):
        return x[1:-1]
    return x


TERM = re.compile(r'[−-]?[A-Za-z0-9.]+')


def markup(s):
    """Turn the math markup of one isolate into HTML."""
    out, i = '', 0
    while i < len(s):
        c = s[i]
        if c == '[':
            inner, i = group(s, i, '[', ']')
            depth, cut = 0, -1
            for k, ch in enumerate(inner):
                depth += ch in '([' and 1 or ch in ')]' and -1 or 0
                if ch == '/' and depth == 0:
                    cut = k
                    break
            if cut < 0:
                out += '[' + markup(inner) + ']'
            else:
                a, b = (unwrap(x.strip()) for x in (inner[:cut], inner[cut + 1:]))
                out += '<span class="fr"><span>%s</span><span>%s</span></span>' % (markup(a), markup(b))
            continue
        if c == '^':
            if i + 1 < len(s) and s[i + 1] == '(':
                inner, i = group(s, i + 1, '(', ')')
            else:
                m = TERM.match(s, i + 1)
                inner, i = (m.group(0), m.end()) if m else ('', i + 1)
            out += '<sup>%s</sup>' % markup(inner)
            continue
        if c == '√' and i + 1 < len(s) and s[i + 1] == '(':
            inner, i = group(s, i + 1, '(', ')')
            out += '<span class="sq">√<span>%s</span></span>' % markup(inner)
            continue
        out += c
        i += 1
    return out


def render_line(line):
    text = html.escape(line, quote=False)
    text = fix_bidi.wrap_text(text)
    text = BDI.sub(lambda m: m.group(1) + layout.keep_math_together(markup(m.group(2))) + m.group(3), text)
    return layout.nowrap_parens(text)


def render_steps(lines):
    out = []
    for line in lines:
        if line.startswith('> ') and out:
            out[-1] += '<span class="th">%s</span>' % render_line(line[2:])
        else:
            out.append(render_line(line))
    return ''.join('<span class="ln">%s</span>' % s for s in out)


def replace_in(page, anchor, cls, body):
    """Replace <p class="cls">…</p> inside the <article> whose id is anchor."""
    start = page.find('id="%s"' % anchor)
    if start < 0:
        return page, False
    end = page.find('</article>', start)
    seg = page[start:end]
    pat = re.compile(r'<p class="%s">.*?</p>' % cls, re.S)
    if not pat.search(seg):
        return page, False
    seg = pat.sub(lambda m: '<p class="%s">%s</p>' % (cls, body), seg, count=1)
    return page[:start] + seg + page[end:], True


OK_FLAG = '<p class="flag ok"><span>נבדק</span>הפתרון תואם את מפתח התשובות של הספר.</p>'


def set_note(page, anchor, note, resolved):
    start = page.find('id="%s"' % anchor)
    if start < 0:
        return page
    end = page.find('</article>', start)
    seg = page[start:end]
    if resolved:
        seg = re.sub(r'<p class="flag rv">.*?</p>', OK_FLAG, seg, flags=re.S)
        seg = seg.replace(' data-review="1"', '', 1)
        if note is None:
            seg = re.sub(r'<p class="sol-note">.*?</p>', '', seg, flags=re.S)
    if note is not None:
        seg = re.sub(r'<p class="sol-note">.*?</p>', '', seg, flags=re.S)
        if note:
            html_note = '<p class="sol-note">%s</p>' % ''.join(render_line(x) + ' ' for x in note).strip()
            seg = re.sub(r'(<p class="flag [a-z]+">.*?</p>)', lambda m: m.group(1) + html_note, seg, count=1, flags=re.S)
    return page[:start] + seg + page[end:]


def main():
    data = {}
    for f in sorted(glob.glob(os.path.join(REPO, 'data', 'explain', '*.json'))):
        data.update(json.load(open(f, encoding='utf-8')))
    sol_path = os.path.join(REPO, 'solutions.html')
    sol = open(sol_path, encoding='utf-8').read()
    pages, done = {}, 0
    for qid, e in data.items():
        s, n = qid.split('-')
        path = os.path.join(REPO, 'sets', '%02d.html' % int(s))
        page = pages.get(path) or open(path, encoding='utf-8').read()
        steps = render_steps(e['steps'])
        page, ok1 = replace_in(page, 'q' + qid, 'steps', steps)
        sol, ok2 = replace_in(sol, 'sol' + qid, 'steps', steps)
        if e.get('pit'):
            pit = render_steps(e['pit'])
            page, _ = replace_in(page, 'q' + qid, 'pit', pit)
            sol, _ = replace_in(sol, 'sol' + qid, 'pit', pit)
        if 'note' in e or e.get('resolved'):
            note = e.get('note')
            page = set_note(page, 'q' + qid, note, e.get('resolved'))
            sol = set_note(sol, 'sol' + qid, note, e.get('resolved'))
        if not (ok1 and ok2):
            print('missing', qid, ok1, ok2)
        pages[path] = page
        done += 1
    for path, page in pages.items():
        open(path, 'w', encoding='utf-8').write(page)
    open(sol_path, 'w', encoding='utf-8').write(sol)
    print('explanations rendered:', done)


if __name__ == '__main__':
    main()
