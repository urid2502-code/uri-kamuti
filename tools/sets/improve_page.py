"""Build sets/improve.html: an empty set page that app.js fills with an improvement set.

The questions come from the user's own mistakes (app.js: syncImp / loadImp), so the
page itself holds no questions. It is cut from the sets/01.html skeleton.

    python3 tools/sets/improve_page.py
"""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def build():
    s = open(os.path.join(REPO, 'sets', '01.html'), encoding='utf-8').read()
    s = s.replace('<title>מקבץ 1 – urIQ</title>', '<title>מקבץ שיפור – urIQ</title>', 1)
    s = re.sub(r'<body class="setpage" data-set="1" data-key="\d+"', '<body class="setpage" data-set="i" data-kind="imp"', s, count=1)
    s = s.replace(' aria-current="page" data-s="1"', ' data-s="1"', 1)
    s = re.sub(r'<!-- =+ מקבץ 1 =+ -->', '<!-- ================= מקבץ שיפור ================= -->', s)
    s = re.sub(r'<div class="sethead">.*?</div>\s*</div>',
               '<div class="sethead"><div><p class="eyebrow"><a href="../sets.html#improve">מקבצים לשיפור</a></p><h1>מקבץ שיפור</h1><p class="meta"></p></div></div>', s, count=1, flags=re.S)
    s = re.sub(r'<nav class="strip"[^>]*>.*?</nav>', '<nav class="strip" aria-label="מעבר לשאלה"></nav>', s, count=1, flags=re.S)
    s = re.sub(r'<div class="cards">.*?</div>\s*<p class="empty"', '<div class="cards"></div>\n<p class="empty"', s, count=1, flags=re.S)
    s = re.sub(r'<footer class="pager">.*?</footer>', '<footer class="pager"><a class="pn" href="../sets.html#improve"><small>חזרה</small>למקבצים לשיפור</a><span></span></footer>', s, count=1, flags=re.S)
    s = s.replace('<script src="../app.js', '<script src="../data/extra.js?v=1"></script><script src="../app.js', 1)
    assert 'article' not in s.split('<div class="cards">')[1].split('</div>')[0]
    open(os.path.join(REPO, 'sets', 'improve.html'), 'w', encoding='utf-8').write(s)
    print('sets/improve.html written')


if __name__ == '__main__':
    build()
