"""Build practice-by-topic pages: topics.html and topics/<topic>-<part>.html.

Every question has a topic in data/site.js (KAMUTI.topic, names in KAMUTI.tnames).
Large topics are split into parts of at most 12 questions, so each part can be
solved and submitted like a set. The question cards are copied from sets/NN.html,
so solutions, figures and fixes stay in one place: run this after changing a set.

    python3 tools/topics/build_topics.py
"""
import json
import math
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAX = 12
ORDER = ['numth', 'alg', 'pow', 'ineq', 'func', 'pct', 'motion', 'stats', 'prob',
         'tri', 'poly', 'circle', 'solid', 'coord', 'graph']


def read(p):
    return open(os.path.join(REPO, p), encoding='utf-8').read()


def write(p, s):
    full = os.path.join(REPO, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(s)


def data():
    s = read('data/site.js')
    return json.loads(s[s.index('{'):s.rindex('}') + 1])


def articles():
    """id -> article html (with the card header naming its set)."""
    out = {}
    for n in range(1, 41):
        page = read('sets/%02d.html' % n)
        for m in re.finditer(r'<article class="q" id="q(\d+-\d+)".*?</article>', page, re.S):
            qid, art = m.group(1), m.group(0)
            q = qid.split('-')[1]
            art = art.replace('<span class="qn">שאלה %s</span>' % q,
                              '<span class="qn">שאלה %s <a class="qsrc" href="../sets/%02d.html#q%s">מקבץ %d</a></span>' % (q, n, qid, n), 1)
            out[qid] = art
    return out


def parts(D):
    """[(topic, part number, parts in topic, [ids])] in display order."""
    by = {}
    for qid, t in D['topic'].items():
        by.setdefault(t, []).append(qid)
    order = [t for t in ORDER if t in by] + sorted(t for t in by if t not in ORDER)
    res = []
    for t in order:
        ids = sorted(by[t], key=lambda i: tuple(int(x) for x in i.split('-')))
        k = math.ceil(len(ids) / MAX)
        size = math.ceil(len(ids) / k)
        for p in range(k):
            res.append((t, p + 1, k, ids[p * size:(p + 1) * size]))
    return res


def label(D, t, p, k):
    return D['tnames'][t] + (' · חלק %d' % p if k > 1 else '')


def build_part(skel, D, arts, allparts, idx):
    t, p, k, ids = allparts[idx]
    slug = '%s-%d' % (t, p)
    name = D['tnames'][t]
    s = skel
    s = re.sub(r'<title>.*?</title>', '<title>%s – urIQ</title>' % label(D, t, p, k), s, count=1)
    s = re.sub(r'<body class="setpage" data-set="1" data-key="\d+"', '<body class="setpage topicpage" data-set="t-%s" data-kind="topic"' % slug, s, count=1)
    s = s.replace('<span>מקבצים</span></button>', '<span>נושאים</span></button>', 1)
    # sidebar: every topic part
    items = []
    for j, (t2, p2, k2, ids2) in enumerate(allparts):
        cur = ' aria-current="page"' if j == idx else ''
        items.append('<li><a class="sl tl" href="%s-%d.html"%s data-tp="%s-%d"><b>%s</b><small>%d</small></a></li>'
                     % (t2, p2, cur, t2, p2, label(D, t2, p2, k2), len(ids2)))
    s = re.sub(r'<aside id="side" class="side" aria-label="מקבצים">.*?</aside>',
               '<aside id="side" class="side" aria-label="נושאים"><div class="side-in"><div class="side-top"><p class="side-h">תרגול לפי נושאים</p>'
               '<button type="button" class="side-x" aria-label="סגירת רשימת הנושאים">סגירה</button></div><ol class="sl-list">%s</ol></div></aside>' % ''.join(items),
               s, count=1, flags=re.S)
    # heading and picker
    opts = ''.join('<option value="%s-%d"%s>%s</option>' % (t2, p2, ' selected' if j == idx else '', label(D, t2, p2, k2))
                   for j, (t2, p2, k2, _) in enumerate(allparts))
    head = ('<div class="sethead"><div><p class="eyebrow"><a href="../topics.html">תרגול לפי נושאים</a></p><h1>%s</h1><p class="meta">%s%d שאלות מכל המקבצים</p></div>'
            '<div class="setact"><label class="setsel"><span class="vh">מעבר לנושא</span><select id="setsel">%s</select></label></div></div>'
            % (name, ('חלק %d מתוך %d · ' % (p, k)) if k > 1 else '', len(ids), opts))
    s = re.sub(r'<!-- =+ מקבץ 1 =+ -->\n<div class="sethead">.*?</div></div>\n', head + '\n', s, count=1, flags=re.S)
    n = len(ids)
    s = s.replace('<span class="sep">/</span>10</bdi>', '<span class="sep">/</span>%d</bdi>' % n)
    s = s.replace('<b class="ans-n">0</b> / 10</bdi>', '<b class="ans-n">0</b> / %d</bdi>' % n)
    s = s.replace('סיום מקבץ והגשה', 'סיום תרגול והגשה')
    s = s.replace('אין במקבץ הזה שאלות שמתאימות לסינון.', 'אין כאן שאלות שמתאימות לסינון.')
    strip = ''.join('<a class="mb" href="#q%s" data-q="%s" aria-label="שאלה %d (מקבץ %s)">%d</a>' % (i, i, j + 1, i.split('-')[0], j + 1)
                    for j, i in enumerate(ids))
    s = re.sub(r'<nav class="strip" aria-label="מעבר לשאלה">.*?</nav>', '<nav class="strip" aria-label="מעבר לשאלה">%s</nav>' % strip, s, count=1, flags=re.S)
    cards = '\n'.join(arts[i] for i in ids)
    s = re.sub(r'<div class="cards">.*?</div>\n<p class="empty"', '<div class="cards">\n%s</div>\n<p class="empty"' % cards.replace('\\', '\\\\'), s, count=1, flags=re.S)
    prev = allparts[idx - 1] if idx > 0 else None
    nxt = allparts[idx + 1] if idx + 1 < len(allparts) else None
    pager = '<footer class="pager">%s%s</footer>' % (
        '<a class="pn pv" href="%s-%d.html" rel="prev"><small>הקודם</small>%s</a>' % (prev[0], prev[1], label(D, *prev[:3])) if prev else '<span></span>',
        '<a class="pn nx" href="%s-%d.html" rel="next"><small>הבא</small>%s</a>' % (nxt[0], nxt[1], label(D, *nxt[:3])) if nxt else '<a class="pn nx" href="../topics.html"><small>סיום</small>לכל הנושאים</a>')
    s = re.sub(r'<footer class="pager">.*?</footer>', pager, s, count=1, flags=re.S)
    s = s.replace('<script src="../data/site.js', '<script src="../data/topics.js?v=%s"></script><script src="../data/site.js' % VER, 1)
    s = s.replace('<a href="../topics.html">נושאים</a>', '<a href="../topics.html" aria-current="page">נושאים</a>', 1)
    s = s.replace('<a href="../sets.html" aria-current="page">מקבצים</a>', '<a href="../sets.html">מקבצים</a>', 1)
    write('topics/%s.html' % slug, s)


def build_index(D, allparts):
    page = read('lessons.html')
    i, j = page.index('<main'), page.index('</main>') + len('</main>')
    groups = []
    for t in [x for x in ORDER if any(a[0] == x for a in allparts)]:
        ps = [a for a in allparts if a[0] == t]
        total = sum(len(a[3]) for a in ps)
        links = ''.join('<a class="tp" href="topics/%s-%d.html" data-tp="%s-%d"><span>%s</span><small>%d שאלות</small><i aria-hidden="true"></i></a>'
                        % (t, p, t, p, ('חלק %d' % p) if k > 1 else 'תרגול', len(ids)) for t, p, k, ids in ps)
        groups.append('<section class="topic" data-topic="%s"><div class="topic-h"><h2>%s</h2><span class="topic-n">%d שאלות</span></div>'
                      '<div class="topic-parts">%s</div></section>' % (t, D['tnames'][t], total, links))
    main = ('<main id="main" class="wrap topics">\n<section class="hero"><h1>תרגול לפי נושאים</h1>'
            '<p class="lede">כל 400 השאלות מסודרות לפי נושא. בחרו נושא ופתרו את השאלות שלו מכל המקבצים – עם טיימר, הגשה, ציון ופתרון מלא לכל שאלה.</p></section>\n'
            '<div class="topicgrid">%s</div>\n</main>' % ''.join(groups))
    s = page[:i] + main + page[j:]
    s = re.sub(r'<title>.*?</title>', '<title>תרגול לפי נושאים – urIQ</title>', s, count=1)
    s = re.sub(r'<body class="[^"]*"', '<body class="topicspage"', s, count=1)
    s = s.replace('<a href="lessons.html" aria-current="page">', '<a href="lessons.html">', 1)
    s = s.replace('<a href="topics.html">נושאים</a>', '<a href="topics.html" aria-current="page">נושאים</a>', 1)
    s = s.replace('<script src="data/site.js', '<script src="data/topics.js?v=%s"></script><script src="data/site.js' % VER, 1)
    s = re.sub(r'<script src="(?!data/|config|avatars|app|auth)[^"]+\.js[^"]*"></script>', '', s)
    write('topics.html', s)


VER = '1'


def main():
    global VER
    D = data()
    arts = articles()
    allparts = parts(D)
    js = 'window.TOPICS=' + json.dumps({'parts': {'%s-%d' % (t, p): ids for t, p, k, ids in allparts},
                                        'names': {'%s-%d' % (t, p): label(D, t, p, k) for t, p, k, ids in allparts}},
                                       ensure_ascii=False, separators=(',', ':')) + ';\n'
    write('data/topics.js', js)
    import hashlib
    VER = hashlib.md5(js.encode()).hexdigest()[:8]
    skel = read('sets/01.html')
    for f in os.listdir(os.path.join(REPO, 'topics')) if os.path.isdir(os.path.join(REPO, 'topics')) else []:
        if f.endswith('.html'):
            os.remove(os.path.join(REPO, 'topics', f))
    for idx in range(len(allparts)):
        build_part(skel, D, arts, allparts, idx)
    build_index(D, allparts)
    print('topic pages:', len(allparts))


if __name__ == '__main__':
    main()
