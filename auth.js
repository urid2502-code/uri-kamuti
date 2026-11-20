/* Uri Q accounts: Google sign-in through Supabase Auth, progress synced to a row-level-secured table.
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

  /* ---------- login page UI ---------- */
  var gbtn=document.getElementById('gbtn'), msg=document.getElementById('auth-msg'), who=document.getElementById('auth-who');
  function say(kind,text){ if(msg) msg.innerHTML=text?'<p class="auth-msg '+kind+'">'+text+'</p>':''; }
  function busy(on,label){ if(!gbtn) return; gbtn.disabled=on; gbtn.querySelector('span').textContent=label||'Continue with Google'; var sp=gbtn.querySelector('.spin'); if(on&&!sp){ sp=document.createElement('i'); sp.className='spin'; sp.setAttribute('aria-hidden','true'); gbtn.insertBefore(sp,gbtn.firstChild); gbtn.querySelector('svg').style.display='none'; } if(!on&&sp){ sp.remove(); gbtn.querySelector('svg').style.display=''; } }
  function esc(s){ return String(s||'').replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function showUser(p){
    if(!who) return;
    document.getElementById('auth-h').textContent='מחובר/ת ל־Uri Q';
    document.getElementById('auth-p').textContent='ההתקדמות שלך נשמרת בחשבון ומסונכרנת בכל מכשיר שבו תתחברו.';
    if(gbtn) gbtn.hidden=true;
    var st=(window.URIQ&&URIQ.UID?URIQ.store:null)||{}, mine=st.avatar&&window.URIQ_AVATARS&&window.URIQ_AVATARS[st.avatar];
    var av=mine?mine.svg:(p.avatar?'<img src="'+esc(p.avatar)+'" alt="" referrerpolicy="no-referrer">':esc((p.name||p.email||'?').charAt(0)));
    who.hidden=false;
    who.innerHTML='<div class="who"><span class="av">'+av+'</span><div><b>'+esc(p.name||'')+'</b><span>'+esc(p.email||'')+'</span></div></div><div class="auth-acts"><a class="cta solid" href="dashboard.html">לאזור שלי</a><button type="button" class="cta line" id="logout">התנתקות</button></div>'+(mine?'':'<h2 class="av-h">בחרו דמות לפרופיל</h2><p class="av-p">היא תופיע בפינת המסך ובאזור האישי. אפשר להחליף בכל רגע.</p><div id="av-login"></div>');
    var box=document.getElementById('av-login'); if(box&&window.URIQ&&URIQ.avatarPicker) URIQ.avatarPicker(box,function(){ showUser(p); });
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
    out.bm=newer.bm||older.bm||{}; out.avatar=newer.avatar||older.avatar||''; out.accent=newer.accent||older.accent||'';
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
    window.addEventListener('uriq:save',function(){ clearTimeout(pushT); pushT=setTimeout(function(){ push().catch(function(){}); },1200); });
    window.addEventListener('pagehide',function(){ if(pushT){ clearTimeout(pushT); push().catch(function(){}); } });

    sb.auth.getSession().then(function(res){
      var sess=res.data&&res.data.session, user=sess&&sess.user;
      if(hasCode&&history.replaceState) history.replaceState(null,'',location.pathname);
      if(!user){
        if(stored){ set(UIDK,null); set(PROF,null); location.reload(); return; }
        if(isLogin){ busy(false); var err=new URLSearchParams(location.search).get('error_description'); if(err) say('err','ההתחברות נכשלה: '+esc(err)+'. אפשר לנסות שוב.'); }
        return;
      }
      uid=user.id; var prof=profileOf(user); set(PROF,JSON.stringify(prof));
      var mine=BASE+':'+uid;
      return pull().then(function(remote){
        var local=J(mine), merged;
        if(stored!==uid){ merged=merge(merge(local,J(BASE)),remote); }   // first sign-in on this device: bring anonymous progress along
        else merged=merge(local,remote);
        var changed=!same(merged,local||{});
        localStorage.setItem(mine,JSON.stringify(merged));
        var needPush=!same(merged,remote||{});
        var p=needPush?push():Promise.resolve();
        return p.then(function(){
          if(stored!==uid){ set(UIDK,uid); set(BASE,null); /* anonymous progress now lives in the account, so the next person on this device starts clean */ if(!isLogin){ location.reload(); return; } location.replace(location.pathname+'?welcome=1'); return; }
          else if(changed&&!isLogin){ location.reload(); return; }
          if(isLogin){ busy(false); showUser(prof); if(hasCode||/welcome=1/.test(location.search)) say('ok','התחברת בהצלחה. ההתקדמות שלך סונכרנה.'); }
        });
      }).catch(function(e){
        if(stored!==uid) set(UIDK,uid);
        if(isLogin){ busy(false); showUser(prof); say('err','התחברת, אבל הסנכרון נכשל ('+esc(e.message||e)+'). ההתקדמות נשמרת בינתיים בדפדפן וננסה שוב בפעם הבאה.'); }
      });
    }).catch(function(e){ if(isLogin){ busy(false); say('err','שגיאת התחברות: '+esc(e.message||e)); } });

    if(gbtn) gbtn.addEventListener('click',function(){
      busy(true,'מעביר ל־Google…'); say('','');
      var back=location.href.split(/[?#]/)[0];
      sb.auth.signInWithOAuth({provider:'google',options:{redirectTo:back}}).then(function(r){ if(r.error){ busy(false); say('err','לא הצלחתי להתחיל את ההתחברות: '+esc(r.error.message)); } });
    });
    document.addEventListener('click',function(e){
      if(!e.target.closest('#logout')) return;
      var b=e.target.closest('#logout'); b.disabled=true; b.textContent='מתנתק…';
      var flush=pushT?push():Promise.resolve(); clearTimeout(pushT); pushT=null;
      flush.catch(function(){}).then(function(){ return sb.auth.signOut(); }).then(function(){
        set(BASE+':'+uid,null); set(UIDK,null); set(PROF,null); location.replace('index.html'); // the account keeps the progress; this device keeps nothing of it
      });
    });
  }
})();
