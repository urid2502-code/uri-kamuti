# urIQ — Study Smarter.

אתר תרגול לכמותי בפסיכומטרי: 40 מקבצים × 10 שאלות מהספר. אין שלב בנייה, הכול רץ ישירות ב־GitHub Pages.
האתר החי: https://urid2502-code.github.io/uri-kamuti/

| עמוד | מה יש בו |
|---|---|
| `index.html` | דף הבית: הירו, שלושת השלבים, קרוסלת היעדים (מקבצים / תשובות / לקחים) ומפת נושאים. |
| `sets.html` | גיליון התשובות של כל 40 המקבצים, עם סינון והתקדמות. |
| `sets/NN.html` | מקבץ בתנאי מבחן: טיימר, פסילת מסיחים, הגשה, ציון ופתרון מלא. |
| `solutions.html` | כל התשובות והפתרונות לפי מקבץ ושאלה, מוכן להדפסה. |
| `lessons.html` | לקחים חשובים: דף נוסחאות לפי 14 נושאים ולקחים לכל מקבץ. |
| `dashboard.html` | האזור האישי: ציונים, דיוק, נושאים לחיזוק, היסטוריה והמלצות. |
| `review.html` | תרגול הטעויות מהמקבצים שהוגשו. |
| `login.html` | כניסה עם Google (Supabase Auth). הגדרה: `docs/AUTH-SETUP.md`. |

**נתונים**
- `data/questions.json`: 400 השאלות (`status: missing` = לא צולמה). `data/solutions/*.json`: הפתרונות, `v: false` = דורש בדיקה מול הספר.
- `data/lessons.json`: נוצר מחדש עם `python tools/lessons/lessons.py`. השאלות והמפתח הם מהספר. הכללים, ההסברים והמוקשים נכתבו ב־urIQ ומסומנים כך באתר.
- `AUDIT.md`: אילו שאלות עוד חסרות.
- כיווניות: נוסחאות עטופות ב־`<bdi dir="ltr" class="m">` כדי שלא יתערבבו בעברית. אחרי שינוי בדפים מריצים `python3 tools/bidi/fix_bidi.py` ואז `node scripts/build.mjs`.

**התקדמות**: נשמרת ב־localStorage (`uri-kamuti:v2`). אחרי כניסה היא מסונכרנת לטבלת `progress` ב־Supabase, וכל משתמש רואה רק את השורה שלו (RLS, ראו `supabase/migrations`).

**נכסים**: הלוגו והפביקון ב־`brand/`. הגופנים IBM Plex Sans Hebrew ו־IBM Plex Mono בקבצים מקומיים (`fonts/`, רישיון OFL). `vendor/supabase-2.119.2.js` (MIT) נטען רק בעמוד הכניסה או למשתמש מחובר.

Designed & built by Uri Deutsch.
