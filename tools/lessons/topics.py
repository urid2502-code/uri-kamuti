import json,re,glob,sys
import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
Q={r['id']:r for r in json.load(open(REPO+'/data/questions.json'))}
SOL={}
for f in sorted(glob.glob(REPO+'/data/solutions/*.json')): SOL.update(json.load(open(f)))
# ordered: first match wins. Each topic: (slug, Hebrew name, regex over stem+options+solution)
TOPICS=[
 ('prob','הסתברות וקומבינטוריקה',r'הסתבר|סיכוי|בחירה אקראית|באקראי|קובי|מטבע|הטל|כמה דרכים|אפשרויות שונות|סידורים|לסדר|צירופ|תמור|!'),
 ('stats','ממוצעים וסטטיסטיקה',r'ממוצע|חציון|שכיח|סטיית|טווח הנתונים'),
 ('graph','קריאת טבלאות ותרשימים',r'בטבלה|הטבלה|בתרשים|התרשים|בגרף|הגרף שלפניכם|דיאגרמ'),
 ('coord','מערכת צירים וישרים',r'מערכת צירים|ציר ה|שיפוע|הישר y|נקודת חיתוך|נקודות \(|\(\s*-?\d+\s*,\s*-?\d+\s*\)'),
 ('motion','תנועה והספק',r'מהירות|קמ"ש|קמ״ש|נסע|נוסע|רכבת|הספק|עבודה|ברז|ממלא|מילוי|בשעה|דקות'),
 ('solid','גופים במרחב',r'קובייה|תיבה|גליל|פירמיד|נפח|חרוט|כדור|מנסר'),
 ('circle','מעגלים',r'מעגל|רדיוס|קוטר|היקף המעגל|π|קשת|משיק'),
 ('tri','משולשים וזוויות',r'משולש|זווית|פיתגורס|ניצב|יתר|תיכון|גובה ל|חוצה זווית|°'),
 ('poly','מרובעים ומצולעים',r'ריבוע|מלבן|מעוין|טרפז|מקבילית|מצולע|משושה|מחומש|שטח|היקף'),
 ('pct','אחוזים, יחסים ופרופורציה',r'אחוז|%|יחס|פרופורצ|הנחה|ייקר|הוזל|מחיר|רווח|ריבית|פי כמה|חלקי'),
 ('func','פעולות מוגדרות ופונקציות',r'מוגדר|מוגדרת|פעולה|הסימן|f\(|\$\(|נגדיר|לכל מספר'),
 ('numth','תורת המספרים',r'זוגי|אי-זוגי|ראשוני|מתחלק|שארית|מחלק|כפולה|ספרות|ספרת|שלם|שלמים|עוקבים|מספר דו'),
 ('pow','חזקות ושורשים',r'\^|√|שורש|חזקה|חזקות'),
 ('ineq','אי־שוויונים והשוואות',r'<|>|≤|≥|בהכרח|גדול מ|קטן מ'),
 ('alg','אלגברה ומשוואות',r'.'),
]
def text(i):
    r=Q[i]; s=SOL.get(i,{})
    return ' '.join(r['stem'])+' '+' '.join(r['options'])+' '+s.get('s','')
def stemtext(i):
    r=Q[i]; return ' '.join(r['stem'])+' '+' '.join(r['options'])
out={}
for i,r in Q.items():
    if r['status']!='extracted': continue
    st=stemtext(i); full=text(i)
    for slug,name,rx in TOPICS:
        if re.search(rx,st): out[i]=slug; break
NAMES={s:n for s,n,_ in TOPICS}
if __name__=='__main__':
    from collections import Counter
    c=Counter(out.values()); print(len(out)); [print(NAMES[k],v) for k,v in c.most_common()]
    if len(sys.argv)>1:
        for i,t in out.items():
            if t==sys.argv[1]: print(i, stemtext(i)[:150])
