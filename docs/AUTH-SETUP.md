# חיבור "Continue with Google"

האתר עובד גם בלי חשבונות: כש־`config.js` ריק, ההתקדמות נשמרת בדפדפן והכפתור מציג "עוד לא חובר".
כדי להפעיל כניסה עם Google צריך פרויקט Supabase ומפתח OAuth של Google. המפתח הסודי של Google נכנס רק ל־Supabase, אף פעם לא לקוד.

1. **Supabase**: ✅ כבר בוצע. הפרויקט `uri-q` (eu-central-1, ‏`kxwuwnygyhadbmebmkza`) נוצר בארגון Uri Deutsch, וההגדרות ב־`supabase/migrations/001_progress.sql` כבר הוחלו עליו.
2. **Google Cloud Console** → APIs & Services → Credentials → Create OAuth client ID → Web application.
   - Authorized JavaScript origins: `https://urid2502-code.github.io`
   - Authorized redirect URIs: `https://kxwuwnygyhadbmebmkza.supabase.co/auth/v1/callback`
3. **Supabase** → Authentication → Sign In / Providers → Google: מדביקים Client ID ו־Client Secret ושומרים.
4. **Supabase** → Authentication → URL Configuration:
   - Site URL: `https://urid2502-code.github.io/uri-kamuti/`
   - Redirect URLs: `https://urid2502-code.github.io/uri-kamuti/**`
5. ✅ כבר בוצע: ב־`config.js` מופיעים כתובת הפרויקט והמפתח הציבורי (publishable). שניהם ציבוריים בכוונה, וההגנה על הנתונים היא ה־RLS.

מה קורה בכניסה הראשונה: ההתקדמות שנשמרה בדפדפן עוברת לחשבון. ביציאה, העותק המקומי של החשבון נמחק מהמכשיר, כך שהאדם הבא באותו מחשב מתחיל נקי.
