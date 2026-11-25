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



def main():
    data = json.load(open(os.path.join(REPO, 'data', 'lessons', 'formulas.json'), encoding='utf-8'))
    cards = ''
    for i, g in enumerate(data):
        rows = ''.join('<div class="fm-r"><span class="fm-k">%s</span><span class="fm-v">%s</span></div>'
                       % (explain.render_line(k), val(v)) for k, v in g['rows'])
        cards += '<details class="fm-card"%s><summary>%s<small>%d</small></summary><div class="fm-rows">%s</div></details>' % (
            ' open' if i < 2 else '', g['h'], len(g['rows']), rows)
    sec = ('<section class="ls-sec" id="ls-formulas" aria-labelledby="h-formulas"><h2 id="h-formulas">דף נוסחאות – גאומטריה</h2>'
           '<p>כל הנוסחאות והיחסים בקיצור, מסודרים לפי נושא. לחצו על כותרת כדי לפתוח או לסגור.</p>'
           '<div class="fm-grid">%s</div></section>' % cards)
    p = os.path.join(REPO, 'lessons.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<section class="ls-sec" id="ls-formulas".*?</section>', '', s, flags=re.S)
    anchor = '<div class="pbody">'
    i = s.index(anchor) + len(anchor)
    s = s[:i] + '\n' + sec + s[i:]
    open(p, 'w', encoding='utf-8').write(s)
    print('formula groups:', len(data), 'rows:', sum(len(g['rows']) for g in data))


if __name__ == '__main__':
    main()
