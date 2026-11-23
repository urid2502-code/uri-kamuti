"""Build a printable, roomy PDF for every set: pdf/NN.pdf.

The questions (text, figures and options) are taken from sets/NN.html and laid
out on A4 with room to work, an answer sheet and an answer key at the end.
Rendering uses Chromium through Playwright (tools/print/render.js).

    python3 tools/print/build_pdfs.py          # all sets
    python3 tools/print/build_pdfs.py 1 7      # only sets 1 and 7
"""
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BUILD = os.path.join(REPO, 'tools', 'print', '.build')
OUT = os.path.join(REPO, 'pdf')

CSS = r'''
@font-face{font-family:"Plex Hebrew";src:url(../../../fonts/IBMPlexSansHebrew-Regular.woff) format("woff");font-weight:400}
@font-face{font-family:"Plex Hebrew";src:url(../../../fonts/IBMPlexSansHebrew-Medium.woff) format("woff");font-weight:500}
@font-face{font-family:"Plex Hebrew";src:url(../../../fonts/IBMPlexSansHebrew-Bold.woff) format("woff");font-weight:700}
@font-face{font-family:"Plex Mono";src:url(../../../fonts/IBMPlexMono-Medium.woff) format("woff")}
@page{size:A4;margin:16mm 17mm 18mm}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font:400 12.3pt/1.75 "Plex Hebrew",Arial,sans-serif;color:#16181b;direction:rtl}
bdi{unicode-bidi:isolate}
.m{white-space:nowrap;font-variant-numeric:tabular-nums lining-nums}
.m sup{font-size:.68em;line-height:0;position:relative;top:-.05em;margin-left:1px}
.fr{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:.9em;line-height:1.25;margin:0 2px;text-align:center}
.fr>span{padding:0 3px;display:block}
.fr>span:first-child{border-bottom:1.2px solid currentColor;padding-bottom:1px}
.fr>span:last-child{padding-top:1px}
.fr .fr{font-size:.92em}
.m sup .fr{font-size:.85em;vertical-align:.55em}
.sq{white-space:nowrap}
.sq>span{border-top:1.2px solid currentColor;padding:0 1px;margin-left:1px}
u.em{text-decoration:underline;text-underline-offset:3px;font-weight:700}
.ln{display:block}
pre{direction:ltr;text-align:left;font:500 13pt/1.45 "Plex Mono",monospace;background:#f4f5f3;border-radius:6px;padding:8px 14px;display:inline-block;margin:6px 0}

/* cover header */
.head{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #16181b;padding-bottom:10px;margin-bottom:8px}
.head h1{margin:0;font-size:26pt;line-height:1;font-weight:700}
.head .sub{color:#5b6066;font-size:11pt;margin-top:4px}
.brand{direction:ltr;display:flex;align-items:center;gap:8px;color:#16181b}
.brand svg{height:22px;width:auto}
.fields{display:flex;gap:22px;margin:12px 0 16px;font-size:11pt;color:#3a3f44}
.fields span{flex:1;border-bottom:1px solid #9aa0a6;padding-bottom:2px}
.tip{font-size:10pt;color:#5b6066;margin:0 0 6px}

/* a question */
.q{break-inside:avoid;page-break-inside:avoid;padding:14px 0 0;margin-bottom:6px}
.q + .q{border-top:1px dashed #c6cbd0}
.qh{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.qn{display:inline-grid;place-items:center;min-width:30px;height:30px;padding:0 8px;border-radius:15px;background:#16181b;color:#fff;font-weight:700;font-size:11pt}
.stem p{margin:0 0 6px}
figure{margin:8px auto 10px;text-align:center}
figure img{max-width:100%;max-height:62mm;width:auto;height:auto}
.opts{list-style:none;margin:10px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:8px 22px}
.opts.wide{grid-template-columns:1fr}
.opts li{display:flex;align-items:center;gap:10px;min-height:28px}
.bub{flex:none;display:inline-grid;place-items:center;width:24px;height:24px;border:1.4px solid #16181b;border-radius:50%;font-size:10pt;font-weight:700}
.work{height:var(--work,34mm);margin-top:8px;border-radius:6px;
  background-image:radial-gradient(#cfd3d7 .8px,transparent .9px);background-size:6mm 6mm;background-position:center}

/* answer sheet and key */
.sheet{break-before:page;page-break-before:always}
.sheet h2{font-size:17pt;margin:0 0 4px}
.sheet p{margin:0 0 14px;color:#5b6066;font-size:10.5pt}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px 40px;max-width:150mm}
.row{display:flex;align-items:center;gap:14px;font-size:12pt}
.row b{width:74px;white-space:nowrap}
.row .bub{width:26px;height:26px}
.key{margin-top:26mm;border-top:2px solid #16181b;padding-top:10px}
.key .row b{width:74px}
.key .ans{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;background:#16181b;color:#fff;font-weight:700;font-size:10.5pt}
'''

WORDMARK = ('<svg viewBox="0 -8 244 116" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="17">'
            '<path d="M8.5 36V68A26 26 0 0 0 60.5 68M60.5 36V100"/><path d="M92 36V100M92 64A28 28 0 0 1 120 36"/><path d="M142 22V100"/>'
            '<circle cx="197.5" cy="61" r="30.5"/><path d="M197.5 16V24" stroke-width="7"/></g>'
            '<g fill="#12805C" stroke="#12805C"><rect x="188" y="8" width="19" height="9" rx="2.5" stroke="none"/>'
            '<path d="M197.5 61L227 91" stroke-width="15" stroke-linecap="round"/><circle cx="197.5" cy="61" r="7.5" stroke="none"/></g></svg>')


def plain_len(html):
    return len(re.sub(r'<[^>]+>', '', html))


def questions(n):
    """(number, stem html, [option html], key) for each question of set n."""
    page = open(os.path.join(REPO, 'sets', '%02d.html' % n), encoding='utf-8').read()
    out = []
    for m in re.finditer(r'<article class="q" id="q%d-(\d+)".*?</article>' % n, page, re.S):
        art = m.group(0)
        qb = re.search(r'<div class="qb">(.*?)(?:<ol class="opts">(.*?)</ol>|</div>)', art, re.S)
        stem, ol = qb.group(1), qb.group(2) or ''
        stem = re.sub(r'<span class="warn"[^>]*>.*?</span>', '', stem)
        stem = stem.replace('src="../fig/', 'src="../../../fig/')
        opts = re.findall(r'<span class="ot">(.*?)</span><span class="otag"', ol, re.S)
        opts = [re.sub(r'<span class="warn"[^>]*>.*?</span>', '', o).strip() for o in opts]
        key = re.search(r'<p class="final">.*?<span class="bub on"[^>]*>(\d)</span>', art, re.S)
        out.append((int(m.group(1)), stem, opts, key.group(1) if key else '?'))
    return out


def build(n):
    qs = questions(n)
    parts = ['<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>urIQ – מקבץ %d</title><style>%s</style></head><body>' % (n, CSS)]
    parts.append('<header class="head"><div><h1>מקבץ %d</h1><div class="sub">כמותי · %d שאלות · מומלץ לפתור בתנאי מבחן</div></div>'
                 '<div class="brand">%s</div></header>' % (n, len(qs), WORDMARK))
    parts.append('<div class="fields"><span>שם:</span><span>תאריך:</span><span>זמן:</span></div>')
    parts.append('<p class="tip">פתרו כל שאלה בשטח המנוקד שמתחתיה, וסמנו את התשובה בגיליון התשובות שבסוף. מפתח התשובות בעמוד האחרון.</p>')
    for num, stem, opts, key in qs:
        has_fig = '<figure' in stem
        wide = any(plain_len(o) > 26 for o in opts) or any('<span class="fr">' in o and plain_len(o) > 16 for o in opts)
        work = '24mm' if has_fig else '36mm'
        parts.append('<section class="q"><div class="qh"><span class="qn">%d</span></div>' % num)
        parts.append('<div class="stem">%s</div>' % stem)
        if opts:
            parts.append('<ol class="opts%s">%s</ol>' % (' wide' if wide else '', ''.join(
                '<li><span class="bub">%d</span><span>%s</span></li>' % (k + 1, o) for k, o in enumerate(opts))))
        parts.append('<div class="work" style="--work:%s"></div></section>' % work)
    # answer sheet and key
    parts.append('<section class="sheet"><h2>גיליון תשובות</h2><p>סמנו עיגול אחד בכל שורה.</p><div class="grid">')
    for num, *_ in qs:
        parts.append('<div class="row"><b>שאלה %d</b>%s</div>' % (num, ''.join('<span class="bub">%d</span>' % k for k in range(1, 5))))
    parts.append('</div><div class="key"><h2>מפתח תשובות</h2><p>לבדיקה אחרי הפתרון. הפתרונות המלאים באתר urIQ.</p><div class="grid">')
    for num, _s, _o, key in qs:
        parts.append('<div class="row"><b>שאלה %d</b><span class="ans">%s</span></div>' % (num, key))
    parts.append('</div></div></section></body></html>')
    os.makedirs(BUILD, exist_ok=True)
    path = os.path.join(BUILD, '%02d.html' % n)
    open(path, 'w', encoding='utf-8').write(''.join(parts))
    return path


def main():
    sets = [int(a) for a in sys.argv[1:]] or list(range(1, 41))
    jobs = [{'html': build(n), 'pdf': os.path.join(OUT, '%02d.pdf' % n), 'set': n} for n in sets]
    os.makedirs(OUT, exist_ok=True)
    jobs_file = os.path.join(BUILD, 'jobs.json')
    json.dump(jobs, open(jobs_file, 'w'))
    subprocess.run(['node', os.path.join(REPO, 'tools', 'print', 'render.js'), jobs_file], check=True)
    print('pdfs written:', len(jobs))


if __name__ == '__main__':
    main()
