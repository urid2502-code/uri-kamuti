(function(){
  'use strict';
  var U=window.URIQ; if(!U) return;
  var D=U.D, store=U.store, body=document.body, pad=U.pad;
  var TN=D.tnames||{}, TOP=D.topic||{};
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function sets(){ return Object.keys(D.exist).filter(function(s){ return D.exist[s].length; }).sort(function(a,b){ return a-b; }); }
  function setHref(id){ var p=id.split('-'); return 'sets/'+pad(+p[0])+'.html#q'+id; }

  /* ---- core numbers, from the latest submission of every set ---- */
  function compute(){
    var r={sub:0,ans:0,ok:0,no:0,sk:0,mis:[],topic:{},el:0};
    sets().forEach(function(s){
      var st=store.sets[s]; if(!st||!st.sub) return; r.sub++; r.el+=st.t&&st.t.el||0;
      D.exist[s].forEach(function(q){
        var id=s+'-'+q, p=st.a[id], k=+U.keyOf(id), t=TOP[id]||'alg', T=r.topic[t]||(r.topic[t]={n:0,ok:0});
        T.n++;
        if(!p){ r.sk++; } else { r.ans++; if(p===k){ r.ok++; T.ok++; } else r.no++; }
        if(p!==k){ var m=store.m&&store.m[id]; if(!(m&&m>(st.at||0))) r.mis.push(id); }
      });
    });
    return r;
  }
  function weakTopics(r){
    return Object.keys(r.topic).filter(function(t){ return r.topic[t].n>=2; })
      .map(function(t){ var T=r.topic[t]; return {t:t,n:T.n,ok:T.ok,acc:T.ok/T.n}; })
      .sort(function(a,b){ return a.acc-b.acc||b.n-a.n; });
  }
  function recommend(r){
    var w={}; weakTopics(r).forEach(function(x){ w[x.t]=1-x.acc; });
    var cand=sets().filter(function(s){ var st=store.sets[s]; return !(st&&st.sub); });
    var hasData=Object.keys(w).length>0;
    var scored=cand.map(function(s){
      var sc=0, tc={}; D.exist[s].forEach(function(q){ var t=TOP[s+'-'+q]; tc[t]=(tc[t]||0)+1; sc+= w[t]!=null?w[t]:0.35; });
      var best=Object.keys(tc).sort(function(a,b){ return ((w[b]||0)*tc[b])-((w[a]||0)*tc[a]); })[0];
      var st=store.sets[s], started=st&&Object.keys(st.a||{}).length;
      return {s:s,sc:hasData?sc+(started?2:0):-(+s)+(started?100:0),why: started?'כבר התחלת אותו':(hasData&&w[best]!=null&&w[best]>0? tc[best]+' שאלות ב'+TN[best]+', נושא שכדאי לחזק':'הבא בתור לפי הסדר')};
    });
    scored.sort(function(a,b){ return b.sc-a.sc; });
    return scored.slice(0,3);
  }
  function fmtDate(t){ try{ return new Date(t).toLocaleDateString('he-IL',{day:'numeric',month:'short'}); }catch(e){ return ''; } }

  function chart(hist){
    var h=hist.slice(-24); if(!h.length) return '<p class="pv-empty" style="color:var(--faint)">הגרף יתמלא אחרי ההגשה הראשונה.</p>';
    var W=640,H=220,L=34,R=8,T=12,B=30, bw=(W-L-R)/h.length, g='';
    [0,50,100].forEach(function(v){ var y=T+(H-T-B)*(1-v/100); g+='<line class="ax" x1="'+L+'" x2="'+(W-R)+'" y1="'+y+'" y2="'+y+'"/><text x="'+(L-6)+'" y="'+(y+4)+'" text-anchor="end">'+v+'%</text>'; });
    h.forEach(function(e,i){ var p=e.tot?e.ok/e.tot:0, bh=Math.max(2,(H-T-B)*p), w=Math.min(bw*0.64,40), x=L+i*bw+(bw-w)/2, y=H-B-bh;
      g+='<rect class="bar" x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+w.toFixed(1)+'" height="'+bh.toFixed(1)+'" rx="3"><title>מקבץ '+e.n+' · '+fmtDate(e.at)+' · '+e.ok+'/'+e.tot+'</title></rect>';
      if(h.length<=16||i%2===0) g+='<text class="lbl" x="'+(x+w/2).toFixed(1)+'" y="'+(H-B+16)+'" text-anchor="middle">'+e.n+'</text>'; });
    var last=h[h.length-1];
    return '<svg class="chart" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="ציון בכל הגשה לפי סדר הזמן. ההגשה האחרונה: מקבץ '+last.n+', '+last.ok+' מתוך '+last.tot+'." style="direction:ltr">'+g+'</svg>';
  }

  /* ================= dashboard ================= */
  if(body.classList.contains('dashpage')){
    var box=document.getElementById('dash'), r=compute(), pf=U.UID?U.load('uriq:profile',null):null;
    var cfg=window.URIQ_CONFIG||{}, authOn=!!(cfg.supabaseUrl&&cfg.supabaseAnonKey);
    var dn=U.displayName?U.displayName():''; if(dn) document.getElementById('dash-h').textContent='שלום, '+dn;
    var banner=U.UID?'':'<div class="dash-banner"><p><b>ההתקדמות נשמרת כרגע רק בדפדפן הזה.</b> '+(authOn?'כניסה עם Google תשמור אותה בחשבון ותסנכרן בין מכשירים.':'סנכרון בין מכשירים יופעל כשהכניסה עם Google תחובר.')+'</p><a class="cta" href="login.html">'+(authOn?'כניסה עם Google':'פרטים')+'</a></div>';
    var hist=(store.hist||[]).slice().sort(function(a,b){ return a.at-b.at; });
    var AVS=window.URIQ_AVATARS||{}, myAv=AVS[store.avatar];
    var profile='<section class="panel profile" id="avatar" aria-labelledby="pf-h"><div class="pf-top"><span class="pf-av'+(myAv?'':' empty')+'" aria-hidden="true">'+(myAv?U.avatarHTML(store.avatar):'?')+'</span><div class="pf-t"><h2 id="pf-h">'+esc((store.name||'').trim()||pf&&pf.name||'הפרופיל שלי')+'</h2><p>'+(pf&&pf.email?esc(pf.email):(U.UID?'':'לא מחובר/ת · הדמות נשמרת בדפדפן הזה'))+'</p>'+(myAv?'<p class="pf-n">הדמות שלך: '+myAv.name+'</p>':'')+'</div></div>'+
      '<details class="pf-pick"'+(myAv?'':' open')+'><summary>'+(myAv?'החלפת דמות':'בחרו דמות לפרופיל')+'</summary><div id="pf-picker"></div></details>'+
      '<div class="pf-sec" id="look"><h3>🛍️ החנות של הדמות</h3><p>כובעים, משקפיים, רקעים, מסגרות, אביזרים ואפקטים. חלק פתוחים מההתחלה, והשאר נפתחים כשמתקדמים: מגישים מקבצים, עונים נכון ומסיימים מקבצים בלי טעויות.</p><div id="look-shop"></div></div>'+'<div class="pf-sec"><h3><label for="pf-name">שם תצוגה</label></h3><p>השם שיופיע באתר, למשל בתפריט העליון ובברכה כאן.</p><form class="pf-name" id="pf-name-f"><input id="pf-name" type="text" maxlength="24" autocomplete="nickname" placeholder="'+esc(pf&&pf.name?pf.name.split(' ')[0]:'השם שלך')+'" value="'+esc(store.name||'')+'"><button type="submit" class="cta solid">שמירה</button><span class="pf-ok" id="pf-ok" role="status"></span></form></div>'+
      '<div class="pf-sec"><h3>הצבע שלך</h3><p>משנה את צבע הכפתורים, הבחירות וההדגשות בכל האתר. נשמר בחשבון.</p><div id="ac-picker"></div></div>'+(U.UID?'<div class="pf-sec pf-out"><h3>החשבון</h3><p>מחובר/ת עם Google'+(pf&&pf.email?' · '+esc(pf.email):'')+'. ההתקדמות נשמרת בחשבון.</p><button type="button" class="cta line" data-signout>התנתקות</button></div>':'')+'</section>';
    var bms=Object.keys(store.bm||{}).sort(function(a,b){ var x=a.split('-'),y=b.split('-'); return x[0]-y[0]||x[1]-y[1]; });
    var bmPanel='<section class="panel"><div class="ph"><h2>שאלות שסימנת</h2><p>'+(bms.length===1?'שאלה אחת':bms.length?bms.length+' שאלות':'עוד אין')+'</p></div>'+(bms.length?'<div class="ids refs" style="margin-bottom:16px">'+bms.map(function(i){ return '<a href="'+setHref(i)+'">'+i+'</a>'; }).join('')+'</div><a class="cta line" href="review.html?bm=1">לתרגל את השאלות המסומנות</a>':'<p style="color:var(--mute);margin:0;line-height:1.6">בכל שאלה יש כפתור סימנייה. סמנו שאלות קשות כדי לחזור אליהן מכאן.</p>')+'</section>';
    if(!r.sub){
      var st1=sets()[0];
      box.innerHTML=profile+banner+bmPanel.replace('class="panel"','class="panel" style="margin-bottom:18px"')+'<div class="panel empty-st"><h2>עוד לא הגשת מקבץ</h2><p>הנתונים כאן נבנים רק מהגשות אמיתיות. אחרי שתגישו מקבץ ראשון יופיעו כאן הציון, הדיוק לפי נושא והשאלות לחזרה.</p><a class="cta solid" href="sets/'+pad(+st1)+'.html">להתחיל ממקבץ '+st1+'</a></div>';
    } else {
      var acc=r.ok+r.no+r.sk?Math.round(100*r.ok/(r.ok+r.no+r.sk)):0;
      var wt=weakTopics(r), recs=recommend(r);
      var weakHtml=wt.length?wt.slice(0,6).map(function(x){ var p=Math.round(100*x.acc); return '<li><a href="lessons.html#t-'+x.t+'"><span class="wn">'+esc(TN[x.t]||x.t)+'</span><span class="wv">'+p+'%</span><span class="wb"><i class="'+(p<60?'lo':'')+'" style="--w:'+p+'%"></i></span><small>'+x.ok+' נכונות מתוך '+x.n+' שאלות</small></a></li>'; }).join(''):'<li style="color:var(--faint)">צריך לפחות שתי שאלות בנושא כדי לחשב דיוק.</li>';
      var ids=r.mis.slice().sort(function(a,b){ var x=a.split('-'),y=b.split('-'); return x[0]-y[0]||x[1]-y[1]; });
      var misHtml='<div class="big"><b>'+ids.length+'</b><span>שאלות לחזרה</span></div><div class="ids refs">'+ids.map(function(i){ return '<a href="'+setHref(i)+'">'+i+'</a>'; }).join('')+'</div>'+
        (ids.length?'<a class="cta solid" href="review.html">תרגול הטעויות</a>':'<p style="color:var(--mute);margin:0">אין כרגע שאלות לחזרה. כל הכבוד.</p>');
      var recHtml=recs.length?recs.map(function(x){ return '<a class="rec" href="sets/'+pad(+x.s)+'.html"><b>מקבץ '+x.s+'</b><span>'+esc(x.why)+'</span></a>'; }).join(''):'<p style="color:var(--mute)">הגשת את כל המקבצים. אפשר לאפס מקבץ ולפתור שוב.</p>';
      var rows=hist.slice().reverse().slice(0,30).map(function(h){ return '<tr><td>'+fmtDate(h.at)+'</td><td><a href="sets/'+pad(h.n)+'.html">מקבץ '+h.n+'</a></td><td class="n">'+h.ok+' / '+h.tot+'</td><td class="n">'+(h.tot?Math.round(100*h.ok/h.tot):0)+'%</td><td class="n">'+(h.el?U.fmt(h.el):'—')+'</td></tr>'; }).join('');
      var rl=store.rl||[], rlok=rl.filter(function(x){ return x.ok; }).length;
      box.innerHTML=profile+banner+
        '<section class="kpis" aria-label="סיכום">'+
        '<div class="kpi"><b>'+r.sub+'<small> / '+sets().length+'</small></b><span>מקבצים שהוגשו</span></div>'+
        '<div class="kpi"><b>'+r.ans+'</b><span>שאלות שנענו</span></div>'+
        '<div class="kpi"><b style="color:var(--ok)">'+r.ok+'</b><span>תשובות נכונות</span></div>'+
        '<div class="kpi"><b style="color:var(--no)">'+r.no+'</b><span>תשובות שגויות'+(r.sk?' · '+r.sk+' דולגו':'')+'</span></div>'+
        '<div class="kpi"><b>'+acc+'%</b><span>דיוק</span></div></section>'+
        '<div class="dgrid">'+
        '<section class="panel"><div class="ph"><h2>התקדמות לאורך זמן</h2><p>ציון בכל הגשה</p></div>'+chart(hist)+'</section>'+
        '<section class="panel"><div class="ph"><h2>נושאים לחיזוק</h2><p>מהחלש לחזק</p></div><ul class="weak">'+weakHtml+'</ul></section>'+
        '<section class="panel mistakes"><div class="ph"><h2>תרגול טעויות</h2><p>'+(rl.length?rl.length+' ניסיונות חוזרים, '+rlok+' נכונים':'שגויות ושדולגו')+'</p></div>'+misHtml+'</section>'+
        '<section class="panel"><div class="ph"><h2>מה לפתור עכשיו</h2><p>לפי הנושאים שלך</p></div><div class="recs" style="grid-template-columns:1fr">'+recHtml+'</div></section>'+
        bmPanel+
        '<section class="panel wide"><div class="ph"><h2>היסטוריית הגשות</h2><p>'+hist.length+' הגשות</p></div><div style="overflow-x:auto"><table class="hist"><thead><tr><th scope="col">תאריך</th><th scope="col">מקבץ</th><th scope="col">ציון</th><th scope="col">אחוז</th><th scope="col">זמן</th></tr></thead><tbody>'+rows+'</tbody></table></div></section>'+
        '</div>';
    }
  }

  if(body.classList.contains('dashpage')){ var ls=document.getElementById('look-shop'); if(ls&&U.lookShop){ U.lookShop(ls,function(){ var pa=document.querySelector('.pf-av'); if(pa&&store.avatar) pa.innerHTML=U.avatarHTML(store.avatar); }); if(location.hash==='#look') setTimeout(function(){ document.getElementById('look').scrollIntoView({block:'start'}); },60); } var pk=document.getElementById('pf-picker'); if(pk&&U.avatarPicker) U.avatarPicker(pk,function(){ location.reload(); }); var acp=document.getElementById('ac-picker'); if(acp&&U.accentPicker) U.accentPicker(acp); var nf=document.getElementById('pf-name-f'); if(nf) nf.addEventListener('submit',function(e){ e.preventDefault(); var v=document.getElementById('pf-name').value.replace(/\s+/g,' ').trim().slice(0,24); store.name=v; U.save(); var d=U.displayName(); document.getElementById('dash-h').textContent=d?'שלום, '+d:'האזור שלי'; var h=document.getElementById('pf-h'); if(h) h.textContent=v||(pf&&pf.name)||'הפרופיל שלי'; if(U.paintChip) U.paintChip(); var an=document.querySelector('#acct .an'); if(an&&!d) an.textContent='האזור שלי'; if(U.emit) U.emit('name',{}); var ok=document.getElementById('pf-ok'); ok.textContent=v?'נשמר':'השם הוסר'; setTimeout(function(){ ok.textContent=''; },2200); }); if(location.hash==='#avatar'){ var d=document.querySelector('.pf-pick'); if(d) d.open=true; } }
  /* ================= lessons: personal accuracy per topic ================= */
  if(body.classList.contains('lessonspage')){
    var rr=compute();
    document.querySelectorAll('[data-acc]').forEach(function(p){ var T=rr.topic[p.dataset.acc]; if(T&&T.n) p.textContent='הדיוק שלך בנושא: '+Math.round(100*T.ok/T.n)+'% ('+T.ok+' מתוך '+T.n+')'; });
    var tabs=[].slice.call(document.querySelectorAll('.ls-tabs a')), topics=[].slice.call(document.querySelectorAll('.ls-grid .topic'));
    function showTab(a){ var st=a.closest('.ls-tabs'); if(!st) return; var r=a.getBoundingClientRect(), sr=st.getBoundingClientRect(); if(r.left<sr.left+8||r.right>sr.right-8) st.scrollLeft+= (r.left+r.width/2)-(sr.left+sr.width/2); }
    function mark(id){ tabs.forEach(function(a){ var on=!!id&&a.getAttribute('href')==='#'+id; a.classList.toggle('on',on); if(on){ a.setAttribute('aria-current','true'); showTab(a); } else a.removeAttribute('aria-current'); }); }
    /* ---- a topic opens as a pop-up ---- */
    var dlg=document.createElement('dialog'); dlg.className='tp-dlg'; dlg.setAttribute('aria-labelledby','tp-dlg-h');
    dlg.innerHTML='<div class="tp-bar"><button type="button" class="tp-nav" data-step="-1" aria-label="הנושא הקודם"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button><span class="tp-pos" aria-live="polite"></span><button type="button" class="tp-nav" data-step="1" aria-label="הנושא הבא"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button><button type="button" class="tp-x" aria-label="סגירה"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div><div class="tp-body"></div>';
    document.body.appendChild(dlg);
    var cur=-1, opener=null;
    function fill(i){
      cur=(i+topics.length)%topics.length; var t=topics[cur], c=t.cloneNode(true);
      c.removeAttribute('id'); c.classList.add('in-dlg'); var h=c.querySelector('h3'); if(h) h.id='tp-dlg-h';
      c.querySelectorAll('details').forEach(function(d){ d.open=false; });   // inner lists open only on a click
      var body=dlg.querySelector('.tp-body'); body.innerHTML=''; body.appendChild(c); body.scrollTop=0;
      dlg.querySelector('.tp-pos').textContent=(cur+1)+' / '+topics.length;
      mark(t.id); if(history.replaceState) history.replaceState(null,'','#'+t.id);
    }
    function open(i,from){ opener=from||document.activeElement; fill(i); if(!dlg.open){ if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open',''); document.documentElement.classList.add('dlg-open'); } dlg.querySelector('.tp-x').focus({preventScroll:true}); }
    function close(){ if(dlg.open){ dlg.classList.add('closing'); setTimeout(function(){ dlg.classList.remove('closing'); if(dlg.close) dlg.close(); else dlg.removeAttribute('open'); },180); } }
    dlg.addEventListener('close',function(){ document.documentElement.classList.remove('dlg-open'); mark(''); if(history.replaceState) history.replaceState(null,'',location.pathname+location.search); if(opener&&opener.focus) opener.focus({preventScroll:true}); });
    dlg.addEventListener('click',function(e){
      if(e.target===dlg){ close(); return; }  // backdrop
      if(e.target.closest('.tp-x')){ close(); return; }
      var n=e.target.closest('.tp-nav'); if(n){ fill(cur+(+n.dataset.step)); return; }
    });
    dlg.addEventListener('keydown',function(e){ if(e.key==='ArrowLeft'){ fill(cur+1); } else if(e.key==='ArrowRight'){ fill(cur-1); } });
    topics.forEach(function(t,i){
      t.tabIndex=0; t.setAttribute('role','button'); t.setAttribute('aria-label','פתיחת הנושא '+(t.querySelector('h3')?t.querySelector('h3').firstChild.textContent:''));
      t.addEventListener('click',function(e){ if(e.target.closest('a,summary,button,details[open] .pits')) return; open(i,t); });
      t.addEventListener('keydown',function(e){ if(e.target===t&&(e.key==='Enter'||e.key===' ')){ e.preventDefault(); open(i,t); } });
      t.addEventListener('mouseenter',function(){ mark(t.id); }); t.addEventListener('mouseleave',function(){ if(!dlg.open) mark(''); });
    });
    tabs.forEach(function(a){ a.addEventListener('click',function(e){ var id=a.getAttribute('href').slice(1), i=topics.findIndex(function(t){ return t.id===id; }); if(i<0) return; e.preventDefault(); open(i,a); }); });
    var hashT=location.hash&&document.getElementById(location.hash.slice(1)), hi=topics.indexOf(hashT);
    if(hi>=0){ hashT.scrollIntoView({block:'start',behavior:'instant'}); open(hi,hashT); }
    if(location.hash){ var t=document.querySelector(location.hash); if(t&&t.tagName==='DETAILS') t.open=true; }
  }

  /* ================= review my mistakes ================= */
  if(body.classList.contains('reviewpage')&&U.UID){
    var root=document.getElementById('rv'), list=compute().mis.sort(function(a,b){ var x=a.split('-'),y=b.split('-'); return x[0]-y[0]||x[1]-y[1]; });
    var qs=new URLSearchParams(location.search); if(qs.get('set')) list=list.filter(function(i){ return i.split('-')[0]===qs.get('set'); });
    var bmMode=qs.get('bm')==='1';
    if(bmMode){ list=Object.keys(store.bm||{}).sort(function(a,b){ var x=a.split('-'),y=b.split('-'); return x[0]-y[0]||x[1]-y[1]; }); var h1=document.querySelector('.phead h1'), hp=document.querySelector('.phead p'); if(h1) h1.textContent='שאלות שסימנת'; if(hp) hp.textContent='השאלות שסימנת כקשות. פותרים שוב, רואים מיד אם צדקת, ומסירים את הסימנייה כשהשאלה כבר יושבת.'; }
    var pos=0, cache={};
    if(!list.length){ root.innerHTML=bmMode?'<div class="panel empty-st"><h2>אין שאלות מסומנות</h2><p>בכל שאלה במקבץ יש כפתור סימנייה. שאלות שתסמנו יופיעו כאן.</p><a class="cta solid" href="sets.html">למקבצים</a></div>':'<div class="panel empty-st"><h2>אין כרגע שאלות לחזרה</h2><p>כאן יופיעו שאלות שטעית בהן או דילגת עליהן במקבצים שהגשת, עד שתסמנו אותן כנלמדו.</p><a class="cta solid" href="sets.html">למקבצים</a></div>'; return; }
    function getCard(id){
      var s=pad(+id.split('-')[0]);
      if(!cache[s]) cache[s]=fetch('sets/'+s+'.html').then(function(r){ if(!r.ok) throw new Error(r.status); return r.text(); }).then(function(t){ return new DOMParser().parseFromString(t,'text/html'); });
      return cache[s].then(function(doc){ var a=doc.getElementById('q'+id); return a?document.importNode(a,true):null; });
    }
    function show(){
      var id=list[pos], p=id.split('-');
      root.innerHTML='<div class="rv-bar"><b>'+(pos+1)+' / '+list.length+'</b><span class="eb-bar" aria-hidden="true"><i style="width:'+(100*(pos+1)/list.length)+'%"></i></span></div><div class="rv-stage"><p class="empty-st">טוען את השאלה…</p></div>';
      getCard(id).then(function(c){
        var stg=root.querySelector('.rv-stage');
        if(!c){ stg.innerHTML='<p>השאלה לא נמצאה.</p>'; return; }
        c.querySelectorAll('img').forEach(function(im){ im.src=im.getAttribute('src').replace(/^\.\.\//,''); im.loading='lazy'; });
        c.querySelector('.qn').innerHTML='<a href="'+setHref(id)+'">מקבץ '+p[0]+' · שאלה '+p[1]+'</a>';
        var k=+U.keyOf(id), qr=c.querySelector('.qres'), sol=c.querySelector('.sol');
        c.querySelectorAll('.opt').forEach(function(b){ b.addEventListener('click',function(){
          if(c.classList.contains('answered')) return; c.classList.add('answered');
          var n=+b.dataset.n, ok=n===k;
          c.querySelectorAll('.opt').forEach(function(x){ var m=+x.dataset.n, tag=x.querySelector('.otag'); x.setAttribute('aria-disabled','true'); if(m===k){ x.classList.add('correct'); if(tag) tag.textContent=ok?'התשובה שלך · נכונה':'התשובה הנכונה'; } else if(m===n){ x.classList.add('wrong'); if(tag) tag.textContent='התשובה שלך'; } });
          b.setAttribute('aria-pressed','true');
          qr.hidden=false; qr.className='qres '+(ok?'r':'w'); qr.textContent=ok?'נכון':'לא נכון · התשובה הנכונה ('+k+')';
          if(sol){ sol.hidden=false; sol.open=!ok; }
          (store.rl=store.rl||[]).push({id:id,at:Date.now(),ok:ok}); if(U.emit) U.emit('answer',{id:id,ok:ok}); if(store.rl.length>500) store.rl.splice(0,store.rl.length-500); U.save();
          var mk=act.querySelector('.mk'); if(mk) mk.disabled=false;
        }); });
        stg.innerHTML=''; stg.appendChild(c);
        var act=document.createElement('div'); act.className='rv-act';
        act.innerHTML='<button type="button" class="cta solid mk" disabled>'+(bmMode?'להסיר את הסימנייה':'למדתי, להוציא מהרשימה')+'</button><button type="button" class="cta line nx">'+(pos<list.length-1?'לשאלה הבאה':'לסיום')+'</button>'+(pos>0?'<button type="button" class="cta line pv">הקודמת</button>':'');
        stg.appendChild(act);
        act.querySelector('.mk').addEventListener('click',function(){ if(bmMode) delete store.bm[id]; else (store.m=store.m||{})[id]=Date.now(); U.save(); list.splice(pos,1); if(!list.length){ location.reload(); return; } if(pos>=list.length) pos=list.length-1; show(); });
        act.querySelector('.nx').addEventListener('click',function(){ if(pos<list.length-1){ pos++; show(); } else location.href='dashboard.html'; });
        var pv=act.querySelector('.pv'); if(pv) pv.addEventListener('click',function(){ pos--; show(); });
        var first=c.querySelector('.opt'); if(first) c.focus({preventScroll:true});
      }).catch(function(){ root.querySelector('.rv-stage').innerHTML='<p class="auth-msg err">לא הצלחתי לטעון את השאלה. בדקו את החיבור ונסו שוב.</p>'; });
    }
    show();
    document.addEventListener('keydown',function(e){ if(/^[1-4]$/.test(e.key)&&!e.altKey&&!e.ctrlKey&&!e.metaKey){ var b=root.querySelector('.q:not(.answered) .opt[data-n="'+e.key+'"]'); if(b){ e.preventDefault(); b.click(); } } });
  }
})();
