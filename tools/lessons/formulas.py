"""Put the compact geometry formula sheet (data/lessons/formulas.json) on lessons.html.

    python3 tools/lessons/formulas.py      # idempotent
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, 'tools', 'solutions'))
import explain  # noqa: E402
import html as _h
sys.path.insert(0, os.path.join(REPO, 'tools', 'bidi'))
import chunks  # noqa: E402

HEB = re.compile('[\u0590-\u05FF]')


def val(v):
    """All-math values are one left-to-right block; mixed ones go through the bidi fixer."""
    if HEB.search(v):
        return explain.render_line(v)
    return '<bdi dir="ltr" class="m">%s</bdi>' % chunks.chunk(explain.markup(_h.escape(v, quote=False)).replace('  ', ' \u00a0'))



SHEETS = [
    ('formulas.json', 'ls-formulas', 'דף נוסחאות – גאומטריה'),
    ('formulas_alg.json', 'ls-formulas-alg', 'דף נוסחאות – אלגברה וציר המספרים'),
]


def section(fname, sid, title):
    data = json.load(open(os.path.join(REPO, 'data', 'lessons', fname), encoding='utf-8'))
    cards = ''
    for i, g in enumerate(data):
        rows = ''.join('<div class="fm-r"><span class="fm-k">%s</span><span class="fm-v">%s</span></div>'
                       % (explain.render_line(k), val(v)) for k, v in g['rows'])
        cards += '<details class="fm-card"><summary>%s<small>%d</small></summary><div class="fm-rows">%s</div></details>' % (
            g['h'], len(g['rows']), rows)
    return ('<section class="ls-sec" id="%s" aria-labelledby="h-%s"><h2 id="h-%s">%s</h2>'
            '<p>כל הנוסחאות בקיצור, מסודרות לפי נושא. לחצו על כותרת כדי לפתוח אותה.</p>'
            '<div class="fm-grid">%s</div></section>' % (sid, sid, sid, title, cards)), sum(len(g['rows']) for g in data)


def main():
    p = os.path.join(REPO, 'lessons.html')
    s = open(p, encoding='utf-8').read()
    secs, n = '', 0
    for f, sid, title in SHEETS:
        s = re.sub(r'<section class="ls-sec" id="%s".*?</section>' % sid, '', s, flags=re.S)
        html, k = section(f, sid, title)
        secs += html
        n += k
    s = re.sub(r'<nav class="fm-nav".*?</nav>', '', s, flags=re.S)
    i = s.index('<section class="ls-sec" id="ls-sets"')       # the sheets come right before the lessons by set
    s = s[:i] + secs + '\n' + s[i:]
    open(p, 'w', encoding='utf-8').write(s)
    print('formula rows:', n)


if __name__ == '__main__':
    main()
