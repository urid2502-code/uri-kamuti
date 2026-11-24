"""Keep math from breaking at random places on phones.

On narrow screens .m allows line breaks (long expressions must wrap), but the
browser may then break anywhere it sees an opportunity, e.g. between ")(" in
y(x − 7)(z + 8). This wraps the parts of every math isolate in
<span class="nw"> (no wrap). The only breaks left are the ordinary spaces that
layout.py kept on purpose (after =, ⇒ in long expressions).

    python3 tools/bidi/chunks.py        # all pages; idempotent
"""
import glob
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BDI = re.compile(r'(<bdi dir="ltr" class="m">)(.*?)(</bdi>)', re.S)
TOKEN = re.compile(r'(<[^>]+>)')


def chunk(inner):
    if inner.startswith('<span class="nw">'):
        return inner
    parts, cur, depth = [], '', 0
    for tok in TOKEN.split(inner):
        if not tok:
            continue
        if tok.startswith('<'):
            if tok.startswith('</'):
                depth -= 1
            elif not tok.endswith('/>') and not re.match(r'<(br|wbr|img)\b', tok):
                depth += 1
            cur += tok
            continue
        for i, piece in enumerate(tok.split(' ')):
            if i and depth == 0:
                parts.append(cur)
                cur = ''
            elif i:
                cur += ' '
            cur += piece
    parts.append(cur)
    return ' '.join('<span class="nw">%s</span>' % p for p in parts if p != '')


def main():
    files = glob.glob(os.path.join(REPO, '*.html')) + glob.glob(os.path.join(REPO, 'sets', '*.html'))
    n = 0
    for f in files:
        s = open(f, encoding='utf-8').read()
        t = BDI.sub(lambda m: m.group(1) + chunk(m.group(2)) + m.group(3), s)
        if t != s:
            open(f, 'w', encoding='utf-8').write(t)
            n += 1
    print('pages updated:', n)


if __name__ == '__main__':
    main()
