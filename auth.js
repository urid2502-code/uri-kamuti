/* urIQ accounts: Google sign-in through Supabase Auth, progress synced to a row-level-secured table.
   The Supabase client (vendored, ~57 KB gzipped) is only downloaded on the login page or for signed-in users. */
(function(){
  'use strict';
  var C=window.URIQ_CONFIG||{}, U=window.URIQ||{}, body=document.body;
  var ON=!!(C.supabaseUrl&&C.supabaseAnonKey);
  var isLogin=body.classList.contains('loginpage');
  var root=body.dataset.root||'';
  var UIDK='uriq:uid', PROF='uriq:profile', BASE='uri-kamuti:v2';
  function get(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
  function set(k,v){ try{ if(v==null) localStorage.removeItem(k); else localStorage.setItem(k,v); }catch(e){} }
  function J(k){ try{ return JSON.parse(localStorage.getItem(k)); }catch(e){ return null; } }
  var stored=get(UIDK);
  var hasCode=/[?&#](code|access_token|error)=/.test(location.search+location.hash);
  var urlErr=(function(){ try{ var q=new URLSearchParams(location.search), h=new URLSearchParams(location.hash.slice(1)); return q.get('error_description')||h.get('error_description')||''; }catch(e){ return ''; } })();

  /* ---------- login page UI ---------- */
  var gbtn=document.getElementById('gbtn'), msg=document.getElementById('auth-msg'), who=document.getElementById('auth-who');
  function say(kind,text){ if(msg) msg.innerHTML=text?'<p class="auth-msg '+kind+'">'+text+'</p>':''; }
  function busy(on,label){ if(!gbtn) return; gbtn.disabled=on; gbtn.querySelector('span').textContent=label||(gbtn.classList.contains('alt')?'חשבון Google אחר':'Continue with Google'); var sp=gbtn.querySelector('.spin'); if(on&&!sp){ sp=document.createElement('i'); sp.className='spin'; sp.setAttribute('aria-hidden','true'); gbtn.insertBefore(sp,gbtn.firstChild); gbtn.querySelector('svg').style.display='none'; } if(!on&&sp){ sp.remove(); gbtn.querySelector('svg').style.display=''; } }
  function esc(s){ return String(s||'').replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  /* ---------- login art: drifting maths, orbiting rings, pointer parallax ---------- */
  if(isLogin) (function(){
    var art=document.querySelector('.auth-art'); if(!art) return;
    var still=matchMedia('(prefers-reduced-motion: reduce)').matches;
    var G=['π','√','x²','∑','≠','∞','÷','%','½','∠','≤','3!','a·b','(x+y)','n²','≈'], frag=document.createDocumentFragment(), els=[];
    for(var i=0;i<16;i++){ var e=document.createElement('span'); e.className='glyph'; e.textContent=G[i]; var d=.3+((i*37)%70)/100;
      var col=i%4, row=Math.floor(i/4), jx=((i*37)%17)-8, jy=((i*53)%15)-7; e.style.cssText='--x:'+(col*24+6+jx/2+(row%2)*10)+'%;--y:'+(row*23+5+jy/2)+'%;--d:'+d.toFixed(2)+';--s:'+(14+Math.round(d*30))+'px;--t:'+(9+(i*7)%11)+'s;--dl:-'+((i*13)%9)+'s';
      frag.appendChild(e); els.push(e); }
    var layer=document.createElement('div'); layer.className='glyphs'; layer.setAttribute('aria-hidden','true'); layer.appendChild(frag); art.insertBefore(layer,art.firstChild);
    art.classList.add('live');
    if(still) return;
    var tx=0,ty=0,cx=0,cy=0,raf=0;
    function loop(){ cx+=(tx-cx)*.08; cy+=(ty-cy)*.08; art.style.setProperty('--px',cx.toFixed(3)); art.style.setProperty('--py',cy.toFixed(3)); raf=Math.abs(tx-cx)+Math.abs(ty-cy)>.001?requestAnimationFrame(loop):0; }
    window.addEventListener('pointermove',function(ev){ if(ev.pointerType==='touch') return; tx=ev.clientX/innerWidth-.5; ty=ev.clientY/innerHeight-.5; if(!raf) raf=requestAnimationFrame(loop); },{passive:true});
  })();
  /* where to go after signing in: the page that asked for it (same site only), else the home page */
  function nextUrl(){ var n=''; try{ n=sessionStorage.getItem('uriq:next')||''; sessionStorage.removeItem('uriq:next'); }catch(e){} var base=location.pathname.replace(/[^\/]*$/,''); return (n&&n.indexOf(base)===0&&!/login\.html/.test(n))?n:'index.html'; }
  /* accounts remembered on this device for one-tap sign-in (name, email, picture only) */
  var ACCK='uriq:accounts';
  function accounts(){ try{ var l=JSON.parse(localStorage.getItem(ACCK)); return Array.isArray(l)?l:[]; }catch(e){ return []; } }
  function remember(p){ if(!p||!p.email) return; var st=(window.URIQ&&URIQ.store)||{}; var l=accounts().filter(function(a){ return a.email!==p.email; }); l.unshift({name:(st.name||'').trim()||p.name||'',email:p.email,pic:p.avatar||'',av:st.avatar||''}); set(ACCK,JSON.stringify(l.slice(0,3))); }
  function forget(email){ set(ACCK,JSON.stringify(accounts().filter(function(a){ return a.email!==email; }))); }
  function avOf(a){ var A=window.URIQ_AVATARS||{}; if(a.av&&A[a.av]) return A[a.av].svg; if(a.pic) return '<img src="'+esc(a.pic)+'" alt="" referrerpolicy="no-referrer">'; return esc((a.name||a.email||'?').charAt(0)); }
  function card(a,attrs,label){ return '<'+(attrs.indexOf('href=')===0?'a ':'button type="button" ')+attrs+' class="acc-card"><span class="av">'+avOf(a)+'</span><span class="acc-t"><b>'+esc(a.name||a.email)+'</b><span>'+esc(a.email)+'</span></span><span class="acc-go">'+label+'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span></'+(attrs.indexOf('href=')===0?'a':'button')+'>'; }
  function head(h,p){ document.getElementById('auth-h').textContent=h; document.getElementById('auth-p').textContent=p; }
  function showUser(p){
    if(!who) return;
    var st=(window.URIQ&&URIQ.UID?URIQ.store:null)||{}, nm=(st.name||'').trim()||(p.name||'').split(' ')[0];
    head(nm?'שלום, '+nm:'את/ה מחובר/ת','בחרו את החשבון כדי להמשיך לאתר.');
    if(gbtn) gbtn.hidden=true;
    who.hidden=false;
    who.innerHTML='<div class="acc-list">'+card({name:(st.name||'').trim()||p.name,email:p.email,pic:p.avatar,av:st.avatar},'href="index.html" aria-label="המשך בתור '+esc(p.name||p.email)+'"','המשך')+'</div>'+
      '<button type="button" class="acc-other" id="other-acct"><span class="plus" aria-hidden="true">+</span>כניסה עם חשבון Google אחר</button>';
  }
  function showChooser(){
    var l=accounts(); if(!who||!l.length) return;
    head('בחירת חשבון','לחצו על החשבון שלכם כדי להיכנס מחדש עם Google.');
    who.hidden=false;
    who.innerHTML='<div class="acc-list">'+l.map(function(a){ return '<div class="acc-row">'+card(a,'data-hint="'+esc(a.email)+'" aria-label="כניסה בתור '+esc(a.name||a.email)+'"','כניסה')+'<button type="button" class="acc-x" data-forget="'+esc(a.email)+'" aria-label="הסרת '+esc(a.email)+' מהמכשיר הזה" title="הסרה מהמכשיר">×</button></div>'; }).join('')+'</div>';
    if(gbtn){ gbtn.classList.add('alt'); gbtn.querySelector('span').textContent='חשבון Google אחר'; }
  }
  if(isLogin&&!ON){
    if(gbtn){ gbtn.disabled=true; }
    say('info','הכניסה עם Google עוד לא חוברה לשרת ההתחברות. בינתיים אפשר לתרגל כרגיל, וההתקדמות נשמרת בדפדפן הזה.');
  }
  if(!ON){ if(stored){ set(UIDK,null); set(PROF,null); location.reload(); } return; }
  if(!isLogin&&!stored&&!hasCode) return; // anonymous visitor: never download the auth client

  /* ---------- merge two progress stores (newest set wins, logs are unioned) ---------- */
  function merge(a,b){
    a=a||{sets:{}}; b=b||{sets:{}};
    var out={sets:{},hist:[],m:{},rl:[],u:Math.max(a.u||0,b.u||0),wiped:Math.max(a.wiped||0,b.wiped||0)};
    var ks={}; Object.keys(a.sets||{}).concat(Object.keys(b.sets||{})).forEach(function(k){ ks[k]=1; });
    Object.keys(ks).forEach(function(k){ var x=(a.sets||{})[k], y=(b.sets||{})[k], tx=x?(x.u||x.at||0):-1, ty=y?(y.u||y.at||0):-1, w=tx>=ty?x:y; if(w&&(w.u||w.at||0)>=out.wiped) out.sets[k]=w; });
    var seen={}; (a.hist||[]).concat(b.hist||[]).forEach(function(h){ var key=h.n+'@'+h.at; if(!seen[key]&&h.at>=out.wiped){ seen[key]=1; out.hist.push(h); } });
    out.hist.sort(function(x,y){ return x.at-y.at; });
    [a.m||{},b.m||{}].forEach(function(m){ Object.keys(m).forEach(function(id){ out.m[id]=Math.max(out.m[id]||0,m[id]); }); });
    var rs={}; (a.rl||[]).concat(b.rl||[]).forEach(function(r){ var key=r.id+'@'+r.at; if(!rs[key]){ rs[key]=1; out.rl.push(r); } });
    out.rl.sort(function(x,y){ return x.at-y.at; }); if(out.rl.length>500) out.rl=out.rl.slice(-500);
    var newer=(a.u||0)>=(b.u||0)?a:b, older=newer===a?b:a;
    out.bm=newer.bm||older.bm||{}; out.avatar=newer.avatar||older.avatar||''; out.accent=newer.accent||older.accent||''; out.name=newer.name||older.name||'';
    out.imp=a.imp&&b.imp?((a.imp.u||0)>=(b.imp.u||0)?a.imp:b.imp):(a.imp||b.imp||undefined);
    return out;
  }
  function same(a,b){ return JSON.stringify(a)===JSON.stringify(b); }

  var s=document.createElement('script'); s.src=root+'vendor/supabase-2.119.2.js'; s.async=true;
  s.onerror=function(){ if(isLogin){ busy(false); say('err','לא הצלחתי לטעון את רכיב ההתחברות. בדקו את החיבור לאינטרנט ונסו שוב.'); } };
  s.onload=init; document.head.appendChild(s);
  if(isLogin) busy(true,'בודק חיבור…');

  function init(){
    var sb=window.supabase.createClient(C.supabaseUrl,C.supabaseAnonKey,{auth:{flowType:'pkce',persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});
    var pushT=null, uid=null;
    function profileOf(u){ var m=u.user_metadata||{}; return {name:m.full_name||m.name||'',email:u.email||'',avatar:m.avatar_url||m.picture||''}; }
    function pull(){ return sb.from('progress').select('data').eq('user_id',uid).maybeSingle().then(function(r){ if(r.error) throw r.error; return r.data?r.data.data:null; }); }
    function push(){ if(!uid) return Promise.resolve(); var data=J(BASE+':'+uid)||{sets:{}}; return sb.from('progress').upsert({user_id:uid,data:data,updated_at:new Date().toISOString()}).then(function(r){ if(r.error) throw r.error; }); }
    /* new accounts wait for the site owner's approval (public.members, see supabase/migrations/002_members.sql) */
    function approved(){ return sb.from('members').select('approved').eq('user_id',uid).maybeSingle().then(function(r){ if(r.error) throw r.error; return !!(r.data&&r.data.approved); }); }
    function pending(p){
      if(stored){ set(UIDK,null); set(PROF,null); location.reload(); return; }
      if(!isLogin) return;
      busy(false); if(gbtn) gbtn.hidden=true;
      head('ההרשמה ממתינה לאישור','נרשמת בהצלחה. החשבון יאושר בקרוב, ואז תוכל/י לפתור את המקבצים ולשמור את ההתקדמות.');
      if(who){ who.hidden=false; who.innerHTML='<div class="acc-list"><div class="acc-card pend"><span class="av">'+avOf({name:p.name,email:p.email,pic:p.avatar})+'</span><span class="acc-t"><b>'+esc(p.name||p.email)+'</b><span>'+esc(p.email)+'</span></span><span class="acc-go">ממתין</span></div></div>'+
        '<button type="button" class="acc-other" id="other-acct"><span class="plus" aria-hidden="true">+</span>כניסה עם חשבון Google אחר</button>'; }
      say('info','אחרי האישור פשוט חוזרים לדף הזה (או מרעננים אותו), והכניסה תושלם.');
      sb.functions.invoke('signup-notify',{body:{}}).catch(function(){});
    }
    window.addEventListener('uriq:save',function(){ clearTimeout(pushT); pushT=setTimeout(function(){ push().catch(function(){}); },1200); });
    window.addEventListener('pagehide',function(){ if(pushT){ clearTimeout(pushT); push().catch(function(){}); } });

    sb.auth.getSession().then(function(res){
      var sess=res.data&&res.data.session, user=sess&&sess.user;
      if(hasCode&&history.replaceState) history.replaceState(null,'',location.pathname);
      if(!user){
        if(stored){ set(UIDK,null); set(PROF,null); location.reload(); return; }
        if(isLogin){ busy(false); showChooser(); if(urlErr) say('err','ההתחברות עם Google נכשלה. נסו שוב בעוד רגע, ואם זה חוזר, כתבו ל־urid2502@gmail.com.'); }
        return;
      }
      uid=user.id; var prof=profileOf(user);
      var mine=BASE+':'+uid;
      return approved().then(function(ok){
        if(!ok){ uid=null; pending(prof); return; }
        set(PROF,JSON.stringify(prof)); remember(prof);
        return sync();
      });
      function sync(){ return pull().then(function(remote){
        var local=J(mine), merged;
        if(stored!==uid){ merged=merge(merge(local,J(BASE)),remote); }   // first sign-in on this device: bring anonymous progress along
        else merged=merge(local,remote);
        var changed=!same(merged,local||{});
        localStorage.setItem(mine,JSON.stringify(merged));
        var needPush=!same(merged,remote||{});
        var p=needPush?push():Promise.resolve();
        return p.then(function(){
          if(stored!==uid){ set(UIDK,uid); set(BASE,null); /* anonymous progress now lives in the account, so the next person on this device starts clean */ if(!isLogin){ location.reload(); return; } location.replace(nextUrl()); return; }
          else if(changed&&!isLogin){ location.reload(); return; }
          if(isLogin&&hasCode){ location.replace(nextUrl()); return; }   // back from Google: go to the landing page
          if(isLogin){ busy(false); showUser(prof); if(hasCode||/welcome=1/.test(location.search)) say('ok','התחברת בהצלחה. ההתקדמות שלך סונכרנה.'); }
        });
      }).catch(function(e){
        if(stored!==uid) set(UIDK,uid);
        if(isLogin){ busy(false); showUser(prof); say('err','התחברת, אבל הסנכרון נכשל ('+esc(e.message||e)+'). ההתקדמות נשמרת בינתיים בדפדפן וננסה שוב בפעם הבאה.'); }
      }); }
    }).catch(function(e){ if(isLogin){ busy(false); say('err','שגיאת התחברות: '+esc(e.message||e)); } });

    function google(hint,el){
      say(''); var back=location.href.split(/[?#]/)[0], q=hint?{login_hint:hint}:{prompt:'select_account'};
      if(el){ el.classList.add('going'); el.setAttribute('aria-busy','true'); } else busy(true,'מעביר ל־Google…');
      sb.auth.signInWithOAuth({provider:'google',options:{redirectTo:back,queryParams:q}}).then(function(r){ if(r.error){ busy(false); if(el) el.classList.remove('going'); say('err','לא הצלחתי להתחיל את ההתחברות: '+esc(r.error.message)); } });
    }
    if(gbtn) gbtn.addEventListener('click',function(){ google(''); });
    if(who) who.addEventListener('click',function(e){
      var x=e.target.closest('[data-forget]'); if(x){ forget(x.dataset.forget); var row=x.closest('.acc-row'); row.classList.add('gone'); setTimeout(function(){ row.remove(); if(!accounts().length){ who.hidden=true; who.innerHTML=''; head('כניסה ל־urIQ','עם חשבון, ההתקדמות, הציונים והטעויות שלך נשמרים ומסונכרנים בין המחשב לטלפון. רק את/ה רואה אותם.'); if(gbtn){ gbtn.classList.remove('alt'); busy(false); } } },260); return; }
      var c=e.target.closest('[data-hint]'); if(c){ google(c.dataset.hint,c); return; }
      if(e.target.closest('#other-acct')){ var b=e.target.closest('#other-acct'); b.disabled=true; var flush=pushT?push():Promise.resolve(); clearTimeout(pushT); pushT=null;
        flush.catch(function(){}).then(function(){ return sb.auth.signOut(); }).then(function(){ set(BASE+':'+uid,null); set(UIDK,null); set(PROF,null); google(''); }); }
    });
    document.addEventListener('click',function(e){
      if(!e.target.closest('#logout,[data-signout]')) return;
      var b=e.target.closest('#logout,[data-signout]'); b.disabled=true; b.textContent='מתנתק…';
      var flush=pushT?push():Promise.resolve(); clearTimeout(pushT); pushT=null;
      flush.catch(function(){}).then(function(){ return sb.auth.signOut(); }).then(function(){
        set(BASE+':'+uid,null); set(UIDK,null); set(PROF,null); location.replace(root+'index.html'); // the account keeps the progress; this device keeps nothing of it
      });
    });
  }
})();
