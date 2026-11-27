"""Build the extra sets ("מקבצים נוספים"): sets/x01.html ... and data/extra.js.

Each set is a module tools/extra/qs/xNN.py with a list Q of ten questions:

    dict(src='1-5',                 # the book question that inspired it
         topic='alg',               # a key of KAMUTI.tnames
         stem=['line', ...],        # explain.py markup: [a/b], x^(..), √(..); **bold** is underlined
         opts=['..', '..', '..', '..'],
         ans=2,                     # computed in the module, never typed by hand
         steps=['..', '> ..'],      # the explanation, like data/explain
         pit=['..'], lesson='..', tricks=['dsq'],
         fig=callable_returning_Fig or None, figw=40)

The module itself checks every answer (see tools/extra/qs/_util.py).

    python3 tools/extra/build.py
"""
import glob
import html
import importlib.util
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, 'tools', 'solutions'))
sys.path.insert(0, os.path.join(REPO, 'tools', 'figs'))
sys.path.insert(0, os.path.join(REPO, 'tools', 'extra', 'qs'))
import explain  # noqa: E402

_site = open(os.path.join(REPO, 'data', 'site.js'), encoding='utf-8').read()
TOPIC = json.loads(_site[_site.index('{'):_site.rindex('}') + 1])['topic']
TR = json.load(open(os.path.join(REPO, 'data', 'lessons', 'tricks.json'), encoding='utf-8'))
GEO = {'insc', 'regpoly', 'circles', 'tri3060', 'sector', 'arcs', 'areasq', 'solid', 'coord', 'trineq'}
STRIKE = ('<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>'
          '<path d="M7 7l10 10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" opacity=".45"/></svg>')


def line(t):
    out = explain.render_line(t)
    return re.sub(r'\*\*(.+?)\*\*', r'<u class="em">\1</u>', out)


def tricks_html(ts):
    out = ''
    for t in ts:
        tr = TR['tricks'][t]
        link = ' <a class="fm-link" href="../lessons.html#ls-formulas">📐 לדף הנוסחאות</a>' if t in GEO else ''
        out += ('<div class="trk" data-trick="%s"><p class="trk-h"><b>🔁 דפוס חוזר: %s</b> %s%s</p><p class="seen" data-ids="%s"></p></div>'
                % (t, tr['name'], explain.render_line(tr['rule']), link, ','.join(tr['ids'])))
    return out


def card(sid, n, q):
    qid = '%s-%d' % (sid, n)
    fig = ''
    if q.get('fig'):
        fig = '<figure class="fig" style="--w:%d%%"><img src="../fig/%s.svg" alt="סרטוט לשאלה %d" loading="lazy"></figure>' % (q.get('figw', 40), qid, n)
    stem = ''.join('<p>%s</p>' % line(t) for t in q['stem'])
    opts = ''.join(
        '<li class="orow"><button type="button" class="opt" data-n="%d" aria-pressed="false"><span class="bub" aria-hidden="true">%d</span>'
        '<span class="ot">%s</span><span class="otag" aria-hidden="true"></span></button>'
        '<button type="button" class="strike" data-n="%d" aria-pressed="false" aria-label="סימון תשובה %d כפסולה">%s</button></li>'
        % (i, i, line(o), i, i, STRIKE) for i, o in enumerate(q['opts'], 1))
    a = q['ans']
    ts = q['tricks'] if 'tricks' in q else TR['q'].get(q['src'], [])
    lesson = '<div class="lesson"><b class="lsn-h">💡 הלקח</b><p>%s</p>%s</div>' % (line(q['lesson']), tricks_html(ts)) if q.get('lesson') else ''
    pit = '<h4>מוקשים נפוצים</h4><p class="pit">%s</p>' % ''.join('<span class="ln">%s</span>' % line(p) for p in q['pit']) if q.get('pit') else ''
    src = q['src'].split('-')
    sol = ('<details class="sol" hidden><summary>הצגת הפתרון</summary><div class="sol-in"><p class="final"><span class="lbl">התשובה הסופית</span>'
           '<span class="fa"><span class="bub on" aria-hidden="true">%d</span><span>תשובה (%d)</span><span class="fo">%s</span></span></p>\n'
           '<h4>דרך הפתרון והסבר</h4><p class="steps">%s</p>%s%s'
           '<p class="flag src"><span>השראה</span><a href="%02d.html#q%s">מקבץ %s, שאלה %s</a></p></div></details>'
           % (a, a, line(q['opts'][a - 1]), explain.render_steps(q['steps']), lesson, pit, int(src[0]), q['src'], src[0], src[1]))
    return ('<!-- ===== מקבץ נוסף %s · שאלה %d ===== -->\n<article class="q" id="q%s" data-q="%s"><header class="qh"><span class="qn">שאלה %d</span></header>\n'
            '<div class="qb">%s%s<ol class="opts">%s</ol></div><p class="qres" hidden></p>%s</article>\n') % (sid[1:], n, qid, qid, n, fig, stem, opts, sol)


def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def page(skel, num, Q, total):
    sid = 'x%d' % num
    s = skel
    s = s.replace('<title>מקבץ 1 – urIQ</title>', '<title>מקבץ נוסף %d – urIQ</title>' % num, 1)
    s = re.sub(r'<body class="setpage" data-set="1" data-key="\d+"',
               '<body class="setpage" data-set="%s" data-key="%s"' % (sid, ''.join(str(q['ans']) for q in Q)), s, count=1)
    s = s.replace(' aria-current="page" data-s="1"', ' data-s="1"', 1)
    s = re.sub(r'<!-- =+ מקבץ 1 =+ -->', '<!-- ================= מקבץ נוסף %d ================= -->' % num, s)
    srcs = sorted({int(q['src'].split('-')[0]) for q in Q})
    sel = ''.join('<option value="x%02d"%s>מקבץ נוסף %d</option>' % (k, ' selected' if k == num else '', k) for k in range(1, total + 1))
    s = re.sub(r'<div class="sethead">.*?</div>\s*</div>',
               '<div class="sethead"><div><p class="eyebrow"><a href="../sets.html#extra">מקבצים נוספים</a></p><h1>מקבץ נוסף %d</h1>'
               '<p class="meta">10 שאלות · בהשראת מקבצים %s</p></div>'
               '<div class="setact"><label class="setsel"><span class="vh">מעבר למקבץ</span><select id="setsel">%s</select></label></div></div>'
               % (num, '–'.join(map(str, (srcs[0], srcs[-1]))), sel), s, count=1, flags=re.S)
    strip = ''.join('<a class="mb" href="#q%s-%d" data-q="%s-%d" aria-label="שאלה %d">%d</a>' % (sid, n, sid, n, n, n) for n in range(1, len(Q) + 1))
    s = re.sub(r'<nav class="strip"[^>]*>.*?</nav>', '<nav class="strip" aria-label="מעבר לשאלה">%s</nav>' % strip, s, count=1, flags=re.S)
    cards = ''.join(card(sid, n, q) for n, q in enumerate(Q, 1))
    s = re.sub(r'<div class="cards">.*?</article>\s*</div>\s*<p class="empty"', lambda m: '<div class="cards">\n%s</div>\n<p class="empty"' % cards, s, count=1, flags=re.S)
    prev = '<a class="pn pv" href="x%02d.html" rel="prev"><small>הקודם</small>מקבץ נוסף %d</a>' % (num - 1, num - 1) if num > 1 else '<span></span>'
    nxt = ('<a class="pn nx" href="x%02d.html" rel="next"><small>הבא</small>מקבץ נוסף %d</a>' % (num + 1, num + 1) if num < total
           else '<a class="pn nx" href="../sets.html#extra"><small>סיום</small>לכל המקבצים הנוספים</a>')
    s = re.sub(r'<footer class="pager">.*?</footer>', '<footer class="pager">%s%s</footer>' % (prev, nxt), s, count=1, flags=re.S)
    s = s.replace('<script src="../app.js', '<script src="../data/extra.js?v=%s"></script><script src="../app.js' % VER, 1)
    s = re.sub(r'<script src="\.\./data/extra\.js\?v=[^"]*"></script>(<script src="\.\./data/extra\.js)', r'\1', s)
    assert s.count('<article') == len(Q), s.count('<article')
    open(os.path.join(REPO, 'sets', 'x%02d.html' % num), 'w', encoding='utf-8').write(s)


def main():
    global VER
    import hashlib
    mods = sorted(glob.glob(os.path.join(REPO, 'tools', 'extra', 'qs', 'x[0-9][0-9].py')))
    sets = [(int(os.path.basename(p)[1:3]), load(p).Q) for p in mods]
    data = {'key': {}, 'exist': {}, 'topic': {}, 'names': {}}
    for num, Q in sets:
        assert len(Q) == 10, (num, len(Q))
        sid = 'x%d' % num
        data['key'][sid] = [q['ans'] for q in Q]
        data['exist'][sid] = list(range(1, 11))
        data['names'][sid] = 'מקבץ נוסף %d' % num
        for n, q in enumerate(Q, 1):
            data['topic']['%s-%d' % (sid, n)] = q.get('topic') or TOPIC.get(q['src'], 'alg')
            if q.get('fig'):
                open(os.path.join(REPO, 'fig', '%s-%d.svg' % (sid, n)), 'w').write(q['fig']().svg())
    js = 'window.KAMUTI_X=%s;\n' % json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    open(os.path.join(REPO, 'data', 'extra.js'), 'w', encoding='utf-8').write(js)
    VER = hashlib.md5(js.encode()).hexdigest()[:8]
    skel = open(os.path.join(REPO, 'sets', '01.html'), encoding='utf-8').read()
    for num, Q in sets:
        page(skel, num, Q, len(sets))
    # every page that loads data/extra.js gets the new version
    for p in glob.glob(os.path.join(REPO, '*.html')) + glob.glob(os.path.join(REPO, 'sets', '*.html')):
        t = open(p, encoding='utf-8').read()
        u = re.sub(r'data/extra\.js\?v=[^"]*', 'data/extra.js?v=' + VER, t)
        if u != t:
            open(p, 'w', encoding='utf-8').write(u)
    print('extra sets:', [n for n, _ in sets])


VER = '1'
if __name__ == '__main__':
    main()
