"""Put the takeaway of every question ("הלקח") into the site.

Source: data/lessons/*.json  ->  {"1-1": "the trick of the question", ...}

Writes, idempotently:
  * a "הלקח" box under the explanation in sets/NN.html and solutions.html
  * a "הלקח מכל שאלה" list in every topic of lessons.html (נקודות ולקחים)
Run tools/topics/build_topics.py afterwards so the topic pages pick it up.

    python3 tools/lessons/takeaways.py
"""
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, 'tools', 'solutions'))
import explain  # noqa: E402  (render_line: bidi-safe math)

BOX = re.compile(r'<div class="lesson">(?:(?!<div).)*?</div>|<div class="lesson">(?:(?!<div class="lesson").)*?</p></div></div>', re.S)


def load():
    L = {}
    for f in sorted(glob.glob(os.path.join(REPO, 'data', 'lessons', '[0-9]*.json'))):
        L.update(json.load(open(f, encoding='utf-8')))
    return L


TR = json.load(open(os.path.join(REPO, 'data', 'lessons', 'tricks.json'), encoding='utf-8'))


GEO = {'insc', 'regpoly', 'circles', 'tri3060', 'sector', 'arcs', 'areasq', 'solid', 'coord', 'trineq'}


def tricks_html(qid):
    out = ''
    for t in TR['q'].get(qid, []):
        tr = TR['tricks'][t]
        others = [i for i in tr['ids'] if i != qid]
        geo = t in GEO
        link = ' <a class="fm-link" href="%slessons.html#ls-formulas">📐 לדף הנוסחאות</a>' % ('{ROOT}') if geo else ''
        out += ('<div class="trk" data-trick="%s"><p class="trk-h"><b>🔁 דפוס חוזר: %s</b> %s%s</p><p class="seen" data-ids="%s"></p></div>'
                % (t, tr['name'], explain.render_line(tr['rule']), link, ','.join(others)))
    return out


def box(text, qid=''):
    return '<div class="lesson"><b class="lsn-h">💡 הלקח</b><p>%s</p>%s</div>' % (explain.render_line(text), tricks_html(qid))


def put(page, anchor, html):
    start = page.find('id="%s"' % anchor)
    if start < 0:
        return page, False
    end = page.find('</article>', start)
    seg = page[start:end]
    if BOX.search(seg):
        seg = BOX.sub(lambda m: html, seg, count=1)
    else:
        m = re.search(r'<p class="steps">.*?</p>', seg, re.S)
        if not m:
            return page, False
        seg = seg[:m.end()] + html + seg[m.end():]
    return page[:start] + seg + page[end:], True


def lessons_page(L):
    p = os.path.join(REPO, 'lessons.html')
    s = open(p, encoding='utf-8').read()
    LS = json.load(open(os.path.join(REPO, 'data', 'lessons.json'), encoding='utf-8'))
    s = re.sub(r'<details class="lsn-d"[^>]*>.*?</details>', '', s, flags=re.S)
    for k, t in LS['topics'].items():
        ids = [i for i in t['ids'] if i in L]
        items = ''.join('<li><a href="sets/%02d.html#q%s" title="מקבץ %s, שאלה %s">%s</a><span class="pt">%s</span></li>'
                        % (int(i.split('-')[0]), i, i.split('-')[0], i.split('-')[1], i, explain.render_line(L[i])) for i in ids)
        block = '<details class="lsn-d"><summary>הלקח מכל שאלה (%d)</summary><ul class="pits lsn">%s</ul></details>' % (len(ids), items)
        m = re.search(r'(<article class="topic" id="t-%s".*?)(<details><summary>מוקשים)' % re.escape(k), s, re.S)
        if m:
            s = s[:m.start(2)] + block + s[m.start(2):]
    s = re.sub(r'<section class="ls-sec" id="ls-tricks".*?</section>', '', s, flags=re.S)
    cards = ''.join('<details class="trk-card"><summary><h3>%s<small>%d שאלות</small></h3></summary><p>%s</p><p class="ex"><b>דוגמה</b> %s</p><div class="trk-qs">%s</div></details>'
                    % (v['name'], len(v['ids']), explain.render_line(v['rule']), explain.render_line(v.get('ex', '')),
                       ''.join('<a class="tq" data-q="%s" href="sets/%02d.html#q%s">%s</a>' % (i, int(i.split('-')[0]), i, i) for i in v['ids']))
                    for t, v in sorted(TR['tricks'].items(), key=lambda kv: -len(kv[1]['ids'])))
    sec = ('<section class="ls-sec" id="ls-tricks" aria-labelledby="h-tricks"><h2 id="h-tricks">דפוסים חוזרים</h2>'
           '<p>הטריקים שחוזרים שוב ושוב בשאלות. לחצו על טריק כדי לראות אותו עם דוגמה ואת השאלות שבהן הוא מופיע – שאלות שכבר פתרת מסומנות בירוק (נכון) או באדום (טעית).</p><div class="trk-grid">%s</div></section>' % cards)
    i = s.index('</section>', s.index('id="ls-topics"')) + len('</section>')
    s = s[:i] + '\n' + sec + s[i:]
    open(p, 'w', encoding='utf-8').write(s)


def main():
    L = load()
    sol_p = os.path.join(REPO, 'solutions.html')
    sol = open(sol_p, encoding='utf-8').read()
    pages, n = {}, 0
    for qid, text in L.items():
        st = int(qid.split('-')[0])
        p = os.path.join(REPO, 'sets', '%02d.html' % st)
        page = pages.get(p) or open(p, encoding='utf-8').read()
        html = box(text, qid)
        page, a = put(page, 'q' + qid, html.replace('{ROOT}', '../'))
        sol, b = put(sol, 'sol' + qid, html.replace('{ROOT}', ''))
        pages[p] = page
        n += a and b
        if not (a and b):
            print('not placed', qid, a, b)
    for p, page in pages.items():
        open(p, 'w', encoding='utf-8').write(page)
    open(sol_p, 'w', encoding='utf-8').write(sol)
    lessons_page(L)
    print('takeaways placed:', n)


if __name__ == '__main__':
    main()
