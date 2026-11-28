"""Write sw.js: the service worker that lets the site (and the home-screen app) work offline.

Precached on install: the app shell (style, scripts, fonts, icons, main pages) and every
figure the pages use. Every other page is cached the first time it is opened.
Run after changing figures or assets (the version changes, and phones refresh their copy):

    python3 tools/pwa/build_sw.py
"""
import glob
import hashlib
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES = ['index.html', 'sets.html', 'topics.html', 'lessons.html', 'dashboard.html', 'review.html', 'sets/improve.html']


def main():
    urls = set(PAGES)
    for page in glob.glob(os.path.join(REPO, '*.html')) + glob.glob(os.path.join(REPO, 'sets', '*.html')) + glob.glob(os.path.join(REPO, 'topics', '*.html')):
        s = open(page, encoding='utf-8').read()
        base = os.path.relpath(os.path.dirname(page), REPO)
        for u in re.findall(r'(?:src|href)="([^"#:]+\.(?:js|css|svg|png|woff|webmanifest)(?:\?v=[\w]+)?)"', s):
            path = os.path.normpath(os.path.join(base, u.split('?')[0])).replace(os.sep, '/')
            if path.startswith('..') or not os.path.exists(os.path.join(REPO, path)):
                continue
            urls.add(path + ('?' + u.split('?')[1] if '?' in u else ''))
    urls = sorted(urls)
    h = hashlib.md5()
    for u in urls:
        h.update(u.encode())
        p = os.path.join(REPO, u.split('?')[0])
        if os.path.exists(p):
            h.update(open(p, 'rb').read())
    ver = h.hexdigest()[:10]
    sw = open(os.path.join(REPO, 'tools', 'pwa', 'sw.template.js'), encoding='utf-8').read()
    sw = sw.replace('__VERSION__', ver).replace('__PRECACHE__', json.dumps(urls, ensure_ascii=False, indent=0))
    open(os.path.join(REPO, 'sw.js'), 'w', encoding='utf-8').write(sw)
    print('sw.js:', ver, len(urls), 'files precached')


if __name__ == '__main__':
    main()
