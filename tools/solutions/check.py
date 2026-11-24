"""Sanity checks for data/explain: fractions never hold Hebrew text (it breaks the math isolation)."""
import glob, json, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fracs(s):
    i = 0
    while True:
        i = s.find('[', i)
        if i < 0:
            return
        d = 0
        for j in range(i, len(s)):
            d += (s[j] == '[') - (s[j] == ']')
            if d == 0:
                yield s[i:j + 1]
                break
        i += 1


bad = []
for f in sorted(glob.glob(os.path.join(REPO, 'data', 'explain', '*.json'))):
    for k, v in json.load(open(f, encoding='utf-8')).items():
        for line in v['steps'] + v.get('pit', []) + (v.get('note') or []):
            for fr in fracs(line):
                if '/' in fr and re.search('[א-ת]', fr):
                    bad.append((k, fr))
print('\n'.join('%s: %s' % b for b in bad) or 'ok')
sys.exit(1 if bad else 0)
