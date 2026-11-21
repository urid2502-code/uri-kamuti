"""Print one set for writing explanations: question, options, key, status, current solution."""
import json, glob, sys, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {r['id']: r for r in json.load(open(os.path.join(REPO, 'data/questions.json')))}
B = {x['id']: x for s in json.load(open(os.path.join(REPO, 'data/bank.json')))['sets'] for x in s['questions']}
S = {}
for f in glob.glob(os.path.join(REPO, 'data/solutions/*.json')):
    S.update(json.load(open(f)))
for s in sys.argv[1:]:
    for n in range(1, 11):
        i = '%s-%d' % (s, n); r = Q[i]; b = B.get(i, {})
        print('=' * 8, i, 'KEY', r['answer'], '| status', b.get('status'), '| review' if r.get('needsReview') else '', '| unverified' if not S[i].get('v') else '', '| fig ' + r['figure'] if r['figure'] else '')
        print(' Q:', ' / '.join(r['stem']))
        print(' O:', ' ; '.join('(%d) %s' % (k + 1, o) for k, o in enumerate(r['options'])))
        if r.get('notes'): print(' N:', r['notes'])
        if b.get('flags'): print(' F:', b['flags'])
        print(' S:', S[i]['s']); print(' P:', S[i]['p'])
