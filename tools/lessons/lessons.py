"""Regenerate data/lessons.json (Uri Q "לקחים חשובים") from the question bank.

    python tools/lessons/lessons.py

Inputs:  data/questions.json, data/solutions/*.json  (the source content)
Rules:   tools/lessons/rules.py  (general cheat-sheet rules, written for Uri Q, marked as generated on the site)
Topics:  tools/lessons/topics.py (keyword classifier; first matching topic wins)
Every rule is linked to the questions it matches; a rule that matches nothing is dropped,
so the cheat sheet always reflects the questions that actually exist.
"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import topics as TP, rules as RL
REPO = TP.REPO
def first_sentence(t):
    t = t.strip(); m = re.search(r'(?<=[^\d\s])\.\s', t)
    return t[:m.start()+1] if m and m.start() > 25 else t
def build():
    Q, SOL, TOPIC = TP.Q, TP.SOL, TP.out
    order = [t[0] for t in TP.TOPICS]
    def key(i): return [int(p) for p in i.split('-')]
    ids_by = {k: [] for k in order}
    for i in sorted(TOPIC, key=key): ids_by[TOPIC[i]].append(i)
    def qtext(i): return ' '.join(Q[i]['stem'])+' '+' '.join(Q[i]['options'])+' '+SOL[i]['s']+' '+SOL[i]['p']
    LS = {'generated_from': 'data/questions.json + data/solutions/*.json', 'topics': {}, 'sets': {}}
    for k in order:
        ids = ids_by[k]
        if not ids: continue
        rules = []
        for txt, rx in RL.RULES.get(k, []):
            hit = [i for i in ids if re.search(rx, qtext(i))]
            if hit: rules.append({'t': txt, 'ids': hit})
        LS['topics'][k] = {'name': TP.NAMES[k], 'ids': ids, 'rules': rules,
                           'pitfalls': [{'id': i, 'p': SOL[i]['p']} for i in ids if SOL[i].get('p')]}
    sets = {}
    for i in sorted(TOPIC, key=key):
        n = i.split('-')[0]
        sets.setdefault(n, []).append({'id': i, 'topic': TOPIC[i], 'idea': first_sentence(SOL[i]['s']), 'pit': SOL[i]['p'], 'v': SOL[i]['v']})
    LS['sets'] = {str(n): sets.get(str(n), []) for n in range(1, 41)}
    return LS
if __name__ == '__main__':
    LS = build()
    json.dump(LS, open(os.path.join(REPO, 'data', 'lessons.json'), 'w'), ensure_ascii=False, indent=1)
    print('topics', len(LS['topics']), 'rules', sum(len(v['rules']) for v in LS['topics'].values()), 'questions', sum(len(v) for v in LS['sets'].values()))
