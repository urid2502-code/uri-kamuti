"""Rewrite a question's stem or an option everywhere it appears.

Usage from Python:
    restem.stem('20-3', ['נתון: 3a = [6/x] + [y/x]', 'b = a + y + 6', ...])
    restem.option('8-5', 2, 'אם a ו־b חיוביים, אז $(a,b) = $(b,a)')
Text uses the explain.py markup ([a/b], √(…), x^(…)); math is isolated automatically.
Updates sets/NN.html, solutions.html, data/bank.json and data/questions.json.
Run scripts/build.mjs and tools/topics/build_topics.py afterwards.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import explain  # noqa: E402


def _plain(t):
    return re.sub(r'\[([^\[\]/]+)/([^\[\]]+)\]', r'\1/\2', re.sub(r'<[^>]+>', '', t))


def _render(t):
    # keep simple inline tags such as <u class="em">…</u>
    parts = re.split(r'(<u class="em">.*?</u>)', t)
    return ''.join(p if p.startswith('<u ') else explain.render_line(p) for p in parts)


def _bank(qid, fn):
    p = os.path.join(REPO, 'data', 'bank.json')
    B = json.load(open(p, encoding='utf-8'))
    for st in B['sets']:
        for x in st['questions']:
            if x['id'] == qid:
                fn(x)
    json.dump(B, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def _questions(qid, fn):
    p = os.path.join(REPO, 'data', 'questions.json')
    Q = json.load(open(p, encoding='utf-8'))
    for x in (Q if isinstance(Q, list) else Q['questions']):
        if x['id'] == qid:
            fn(x)
    json.dump(Q, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def stem(qid, lines):
    html = ''.join('<p>%s</p>' % _render(l) for l in lines)
    st = int(qid.split('-')[0])
    for p, anchor, rx in ((os.path.join(REPO, 'sets', '%02d.html' % st), 'id="q%s"' % qid, r'(<div class="qb">)(.*?)(<ol class="opts">)'),
                          (os.path.join(REPO, 'solutions.html'), 'id="sol%s"' % qid, r'(<div class="sq-stem">)(.*?)(</div><div class="sol-in">)')):
        s = open(p, encoding='utf-8').read()
        i = s.index(anchor)
        e = s.index('</article>', i)
        seg = s[i:e]
        m = re.search(rx, seg, re.S)
        keep = ''.join(re.findall(r'<figure.*?</figure>', m.group(2), re.S))
        seg = seg[:m.start(2)] + keep + html + seg[m.end(2):]
        open(p, 'w', encoding='utf-8').write(s[:i] + seg + s[e:])

    def bank(x):
        keep = ''.join(re.findall(r'<figure.*?</figure>', x.get('stem') or '', re.S))
        x['stem'] = keep + html
        x['text'] = ' '.join(_plain(l) for l in lines)
    _bank(qid, bank)
    _questions(qid, lambda x: x.update(stem=[_plain(l) for l in lines], needsReview=False))


def option(qid, n, text):
    html = _render(text)
    st = int(qid.split('-')[0])
    p = os.path.join(REPO, 'sets', '%02d.html' % st)
    s = open(p, encoding='utf-8').read()
    i = s.index('id="q%s"' % qid)
    e = s.index('</article>', i)
    seg = s[i:e]
    ots = list(re.finditer(r'(<span class="ot">)(.*?)(</span><span class="otag")', seg, re.S))
    old = ots[n - 1].group(2)
    seg = seg[:ots[n - 1].start(2)] + html + seg[ots[n - 1].end(2):]
    seg = seg.replace('<span class="fo">%s</span>' % old, '<span class="fo">%s</span>' % html)
    open(p, 'w', encoding='utf-8').write(s[:i] + seg + s[e:])
    sp = os.path.join(REPO, 'solutions.html')
    t = open(sp, encoding='utf-8').read()
    i = t.index('id="sol%s"' % qid)
    e = t.index('</article>', i)
    t = t[:i] + t[i:e].replace('<span class="fo">%s</span>' % old, '<span class="fo">%s</span>' % html) + t[e:]
    open(sp, 'w', encoding='utf-8').write(t)

    def bank(x):
        if x.get('options'):
            x['options'][n - 1] = html
    _bank(qid, bank)

    def qq(x):
        if x.get('options'):
            x['options'][n - 1] = _plain(text)
    _questions(qid, qq)
