(function(){
  'use strict';
  var UID=null; try{ UID=localStorage.getItem('uriq:uid'); }catch(e){}
  var KEY='uri-kamuti:v2'+(UID?':'+UID:''), OLD='uri-kamuti:v1', THEME='uri-kamuti:theme', HIDE='uri-kamuti:hideTimer';
  var D=window.KAMUTI||{key:{},exist:{},review:[],fresh:[],idx:[]};
  var body=document.body, root=body.dataset.root||'';
  function load(k,d){ try{ var v=JSON.parse(localStorage.getItem(k)); return v==null?d:v; }catch(e){ return d; } }
  function put(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} }
  var store=load(KEY,null);
  if(!store||!store.sets){
    store={sets:{}};
    var old=UID?{}:load(OLD,{}); // migrate earlier answers as unsubmitted selections
    Object.keys(old||{}).forEach(function(id){ var s=id.split('-')[0]; (store.sets[s]=store.sets[s]||fresh()).a[id]=old[id]; });
    put(KEY,store);
  }
  function fresh(){ return {a:{},x:{},sub:false,t:{el:0,run:false,st:0}}; }
  function S(n){ return store.sets[n]||(store.sets[n]=fresh()); }
  function save(){ store.u=Date.now(); put(KEY,store); try{ window.dispatchEvent(new CustomEvent('uriq:save')); }catch(e){} }
  store.hist=store.hist||[]; store.m=store.m||{}; store.bm=store.bm||{};
  function emit(t,d){ try{ window.dispatchEvent(new CustomEvent('uriq:'+t,{detail:d||{}})); }catch(e){} }
  function summarize(n,st){ var ok=0, wr=[], sk=[], ex=D.exist[n]||[]; ex.forEach(function(q){ var id=n+'-'+q, p=st.a[id], k=+keyOf(id); if(!p) sk.push(id); else if(p===k) ok++; else wr.push(id); }); return {ok:ok,tot:ex.length,wr:wr,sk:sk}; }
  function logAttempt(n,st){ var r=summarize(n,st); store.hist.push({n:+n,at:st.at||Date.now(),ok:r.ok,tot:r.tot,el:st.t.el||0,wr:r.wr,sk:r.sk}); }
  // older submissions (before the history log existed) become history entries from their saved answers
  Object.keys(store.sets).forEach(function(n){ var st=store.sets[n]; if(st&&st.sub&&!store.hist.some(function(h){ return h.n===+n&&h.at===st.at; })) logAttempt(n,st); });
  store.hist.sort(function(a,b){ return a.at-b.at; });
  var REV={}, NEW={};
  (D.review||[]).forEach(function(i){REV[i]=1;}); (D.fresh||[]).forEach(function(i){NEW[i]=1;});
  function pad(n){ return (n<10?'0':'')+n; }
  function keyOf(id){ var p=id.split('-'); return (D.key[p[0]]||[])[p[1]-1]; }
  function fmt(ms){ var s=Math.floor(ms/1000), h=Math.floor(s/3600), m=Math.floor(s%3600/60), r=s%60; return (h?h+':'+pad(m):pad(m))+':'+pad(r); }
  function fmtShort(ms){ var s=Math.round(ms/1000), m=Math.floor(s/60), r=s%60; return m+':'+pad(r); }

  /* ---- theme ---- */
  var tb=document.getElementById('theme');
  function syncTheme(){ var dk=document.documentElement.dataset.theme==='dark'; if(tb){ tb.setAttribute('aria-pressed',dk?'true':'false'); tb.setAttribute('aria-label',dk?'מצב בהיר':'מצב כהה'); } var m=document.querySelector('meta[name=theme-color]'); if(m&&!body.classList.contains('landing')&&!body.classList.contains('loginpage')) m.content=dk?'#0A0A0A':'#0B0B0B'; }
  if(tb) tb.addEventListener('click',function(){ var dk=document.documentElement.dataset.theme!=='dark'; if(dk) document.documentElement.dataset.theme='dark'; else delete document.documentElement.dataset.theme; try{ localStorage.setItem(THEME,dk?'dark':'light'); }catch(e){} syncTheme(); });
  syncTheme();

  /* ---- sidebar progress + drawer ---- */
  function sideProgress(){
    Object.keys(D.exist).forEach(function(s){
      var ex=D.exist[s]; if(!ex.length) return;
      var st=store.sets[s], done=0; if(st) ex.forEach(function(q){ if(st.a[s+'-'+q]) done++; });
      var i=document.querySelector('[data-pb="'+s+'"]'); if(i) i.style.width=(100*done/ex.length)+'%';
      var sm=document.querySelector('[data-sp="'+s+'"]');
      if(sm){ var sub=st&&st.sub; sm.textContent= done ? done+'/'+ex.length : String(ex.length); var a=sm.closest('.sl'); a.classList.toggle('full',!!sub); a.setAttribute('aria-label','מקבץ '+s+(sub?', הוגש':'')+', נענו '+done+' מתוך '+ex.length); }
    });
  }
  var side=document.getElementById('side'), nb=document.querySelector('.navbtn'), scrim=document.querySelector('.scrim');
  function drawer(open){ if(!side) return; side.classList.toggle('open',open); if(scrim) scrim.hidden=!open; if(nb) nb.setAttribute('aria-expanded',open?'true':'false'); if(open){ var c=side.querySelector('[aria-current]'); (c||side.querySelector('a')).focus(); } }
  if(nb) nb.addEventListener('click',function(){ drawer(!side.classList.contains('open')); });
  if(scrim) scrim.addEventListener('click',function(){ drawer(false); nb.focus(); });
  var sx=document.querySelector('.side-x'); if(sx) sx.addEventListener('click',function(){ drawer(false); nb.focus(); });
  if(side){ var cur=side.querySelector('[aria-current]'); if(cur) side.scrollTop=Math.max(0,cur.offsetTop-side.clientHeight/2); }
  var sel=document.getElementById('setsel'); if(sel) sel.addEventListener('change',function(){ location.href=sel.value+'.html'; });

  /* ---- global search ---- */
  var inp=document.getElementById('q-search'), res=document.getElementById('q-results'), si=-1;
  function norm(s){ return s.replace(/[֑-ׇ]/g,'').toLowerCase(); }
  var IDX=(D.idx||[]).map(function(r){ return [r[0],r[1],norm(r[1])]; });
  function esc(s){ return s.replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function snippet(t,w){ var i=norm(t).indexOf(w), a=Math.max(0,i-30), s=(a?'…':'')+t.slice(a,a+110)+(t.length>a+110?'…':''); if(i<0) return esc(s); var j=norm(s).indexOf(w); return esc(s.slice(0,j))+'<mark>'+esc(s.slice(j,j+w.length))+'</mark>'+esc(s.slice(j+w.length)); }
  function closeRes(){ if(!res) return; res.hidden=true; inp.setAttribute('aria-expanded','false'); si=-1; }
  function run(){
    var v=norm(inp.value.trim()); if(!v){ closeRes(); return; }
    var words=v.split(/\s+/), out=[], m=v.match(/^(?:מקבץ\s*)?(\d{1,2})$/);
    if(m && +m[1]>=1 && +m[1]<=40) out.push('<li><a role="option" href="'+root+'sets/'+pad(+m[1])+'.html"><b>מעבר</b>מקבץ '+(+m[1])+'</a></li>');
    for(var k=0;k<IDX.length && out.length<12;k++){ var r=IDX[k]; if(words.every(function(w){ return r[2].indexOf(w)>=0; })){ var p=r[0].split('-'); out.push('<li><a role="option" href="'+root+'sets/'+pad(+p[0])+'.html#q'+r[0]+'"><b>מקבץ '+p[0]+', שאלה '+p[1]+'</b>'+snippet(r[1],words[0])+'</a></li>'); } }
    res.innerHTML=out.length?out.join(''):'<li class="nores">לא נמצאו שאלות. אפשר לחפש מילה מהשאלה או מספר מקבץ.</li>';
    res.hidden=false; inp.setAttribute('aria-expanded','true'); si=-1;
  }
  if(inp){
    inp.addEventListener('input',run);
    inp.addEventListener('keydown',function(e){
      var links=res.querySelectorAll('a');
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){ if(!links.length) return; e.preventDefault(); si=(si+(e.key==='ArrowDown'?1:-1)+links.length)%links.length; links.forEach(function(a,i){ a.setAttribute('aria-selected',i===si?'true':'false'); }); links[si].scrollIntoView({block:'nearest'}); }
      else if(e.key==='Enter'){ var a=links[si<0?0:si]; if(a){ e.preventDefault(); closeRes(); location.href=a.href; } }
      else if(e.key==='Escape'){ closeRes(); }
    });
    res.addEventListener('click',function(){ closeRes(); inp.value=''; });
    document.addEventListener('click',function(e){ if(!e.target.closest('.search')) closeRes(); });
  }

  /* ---- filter chips ---- */
  function chips(match,apply,ids){
    var bs=[].slice.call(document.querySelectorAll('.chip'));
    function counts(){ ['all','open','review','new'].forEach(function(f){ var n=ids().filter(function(id){ return match(id,f); }).length, el=document.querySelector('[data-c="'+f+'"]'); if(el) el.textContent=n; var b=document.querySelector('.chip[data-f="'+f+'"]'); if(b&&f!=='all') b.disabled=!n&&b.getAttribute('aria-pressed')!=='true'; }); }
    bs.forEach(function(b){ b.addEventListener('click',function(){ bs.forEach(function(x){ x.setAttribute('aria-pressed',x===b?'true':'false'); }); apply(b.dataset.f); counts(); }); });
    counts(); return counts;
  }
  function curFilter(){ var b=document.querySelector('.chip[aria-pressed="true"]'); return b?b.dataset.f:'all'; }

  /* ---- modal ---- */
  var dlg=document.getElementById('confirm');
  function ask(title,text,okLabel,cb){
    if(!dlg||typeof dlg.showModal!=='function'){ if(window.confirm(title+'\n'+text)) cb(); return; }
    document.getElementById('cf-t').textContent=title; document.getElementById('cf-p').textContent=text; document.getElementById('cf-ok').textContent=okLabel;
    var back=document.activeElement;
    dlg.returnValue=''; dlg.showModal(); document.getElementById('cf-no').focus();
    dlg.addEventListener('close',function h(){ dlg.removeEventListener('close',h); if(dlg.returnValue==='ok') cb(); else if(back) back.focus(); });
  }

  /* ================= set page ================= */
  if(body.classList.contains('setpage')){
    var n=body.dataset.set, st=S(n);
    var save0=save; save=function(){ st.u=Date.now(); save0(); };
    var cards=[].slice.call(document.querySelectorAll('.q:not(.miss)')), misses=[].slice.call(document.querySelectorAll('.q.miss'));
    var total=cards.length;
    var digits=document.getElementById('t-digits'), startB=document.getElementById('t-start'), resetB=document.getElementById('t-reset'), hideB=document.getElementById('t-hide'), paceEl=document.getElementById('t-pace');
    var hidden=!!load(HIDE,false), timerIv=null, nudged=false;
    function elapsed(){ return st.t.el+(st.t.run?Date.now()-st.t.st:0); }
    function answered(){ return cards.filter(function(c){ return st.a[c.dataset.q]; }).length; }
    function drawTimer(){
      if(!digits) return;
      var ms=elapsed(), idle=!st.t.run&&!ms;
      digits.textContent= hidden&&st.t.run ? '••:••' : fmt(ms);
      digits.classList.toggle('idle',idle);
      var a=answered(); if(paceEl) paceEl.textContent= ms&&a ? 'קצב '+fmtShort(ms/a)+' לשאלה' : '';
    }
    function drawStartBtn(){
      if(!startB) return;
      var lbl=startB.querySelector('.t-lbl');
      startB.classList.toggle('running',st.t.run);
      startB.innerHTML=(st.t.run?'<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="currentColor"/></svg>':'<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5.5v13l10-6.5z" fill="currentColor"/></svg>')+'<span class="t-lbl">'+(st.t.run?'השהיה':(st.t.el?'המשך':'התחלת טיימר'))+'</span>';
      startB.setAttribute('aria-label',st.t.run?'השהיית הטיימר':(st.t.el?'המשך הטיימר':'התחלת הטיימר'));
    }
    function loop(on){ if(timerIv){ clearInterval(timerIv); timerIv=null; } if(on) timerIv=setInterval(drawTimer,250); }
    function startPause(){ if(st.sub) return; if(st.t.run){ st.t.el+=Date.now()-st.t.st; st.t.run=false; } else { st.t.st=Date.now(); st.t.run=true; } save(); drawStartBtn(); drawTimer(); loop(st.t.run); }
    if(startB) startB.addEventListener('click',startPause);
    if(resetB) resetB.addEventListener('click',function(){ if(st.sub) return; st.t={el:0,run:false,st:0}; save(); drawStartBtn(); drawTimer(); loop(false); });
    if(hideB){ hideB.setAttribute('aria-pressed',hidden?'true':'false'); hideB.addEventListener('click',function(){ hidden=!hidden; put(HIDE,hidden); hideB.setAttribute('aria-pressed',hidden?'true':'false'); hideB.setAttribute('aria-label',hidden?'הצגת הספרות':'הסתרת הספרות'); drawTimer(); }); }

    function drawCard(c){
      var id=c.dataset.q, pick=st.a[id], strikes=st.x[id]||[], ans=+keyOf(id);
      c.querySelectorAll('.orow').forEach(function(row){
        var b=row.querySelector('.opt'), s=row.querySelector('.strike'), k=+b.dataset.n, out=strikes.indexOf(k)>=0;
        b.setAttribute('aria-pressed',pick===k?'true':'false');
        row.classList.toggle('out',out&&pick!==k); if(s) s.setAttribute('aria-pressed',out?'true':'false');
        b.classList.remove('correct','wrong'); var tag=b.querySelector('.otag'); if(tag) tag.textContent='';
        if(st.sub){
          b.setAttribute('aria-disabled','true');
          if(k===ans){ b.classList.add('correct'); if(tag) tag.textContent= pick===k?'התשובה שלך · נכונה':'התשובה הנכונה'; }
          else if(k===pick){ b.classList.add('wrong'); if(tag) tag.textContent='התשובה שלך'; }
        } else b.removeAttribute('aria-disabled');
      });
      var qr=c.querySelector('.qres'), sol=c.querySelector('.sol');
      if(st.sub){
        qr.hidden=false;
        qr.className='qres '+(!pick?'s':pick===ans?'r':'w');
        qr.textContent= !pick ? 'לא נענתה · התשובה הנכונה ('+ans+')' : pick===ans ? 'נכון' : 'לא נכון · בחרת ('+pick+'), התשובה הנכונה ('+ans+')';
        if(sol) sol.hidden=false;
      } else { qr.hidden=true; if(sol){ sol.hidden=true; sol.open=false; } }
      var mb=document.querySelector('.mb[data-q="'+id+'"]');
      if(mb){ mb.classList.remove('sel','ok','no','skip'); if(st.sub) mb.classList.add(!pick?'skip':pick===ans?'ok':'no'); else if(pick) mb.classList.add('sel'); }
    }
    function drawCounts(){
      var a=answered();
      document.querySelectorAll('.ans-n').forEach(function(e){ e.textContent=a; });
      var bar=document.querySelector('.eb-bar i'); if(bar) bar.style.width=(total?100*a/total:0)+'%';
      sideProgress(); recount(); if(curFilter()==='open') apply('open');
    }
    function drawResults(){
      var box=document.getElementById('results'); if(!box) return;
      if(!st.sub){ box.hidden=true; box.innerHTML=''; return; }
      var ok=0, pills='';
      cards.forEach(function(c){ var id=c.dataset.q, q=id.split('-')[1], p=st.a[id], k=+keyOf(id), cls=!p?'skip':p===k?'ok':'no'; if(cls==='ok') ok++;
        pills+='<a class="pill '+cls+'" href="#q'+id+'">'+q+'<span class="vh"> – '+(cls==='ok'?'נכונה':cls==='no'?'שגויה':'לא נענתה')+'</span></a>'; });
      var ms=st.t.el, pct=total?Math.round(100*ok/total):0;
      var nx=+n<40?'<a class="btn" href="'+pad(+n+1)+'.html">למקבץ '+(+n+1)+'</a>':'<a class="btn" href="../sets.html">לכל המקבצים</a>';
      box.innerHTML='<div class="rd-top"><div><h2 class="rd-h" id="res-h">תוצאות מקבץ '+n+'</h2><p class="rd-sub">המקבץ הוגש והתשובות נעולות. הפתרון המלא מופיע מתחת לכל שאלה.</p></div></div>'+
        '<div class="rd-stats"><div class="stat"><b><bdi dir="ltr">'+ok+' / '+total+'</bdi></b><span>ציון<small>'+pct+'%</small></span></div>'+
        '<div class="stat"><b>'+(ms?fmt(ms):'—')+'</b><span>'+(ms?'זמן כולל':'הטיימר לא הופעל')+'</span></div>'+
        '<div class="stat"><b>'+(ms&&total?fmtShort(ms/total):'—')+'</b><span>ממוצע לשאלה</span></div></div>'+
        '<nav class="rd-map" aria-label="מפת שאלות">'+pills+'</nav>'+
        '<ul class="rd-legend"><li><i style="background:var(--ok)"></i>נכונה</li><li><i style="background:var(--no)"></i>שגויה</li><li><i style="border:1.5px dashed var(--line2)"></i>לא נענתה</li></ul>'+
        '<div class="rd-act"><button type="button" class="btn primary" id="retake">איפוס מקבץ ופתרון מחדש</button>'+nx+'</div>';
      box.hidden=false;
      document.getElementById('retake').addEventListener('click',function(){
        ask('לאפס את המקבץ?','כל התשובות, הסימונים והזמן של מקבץ '+n+' יימחקו, ותוכלו לפתור אותו מחדש.','איפוס',function(){ store.sets[n]=fresh(); store.sets[n].u=Date.now(); save(); location.replace(location.pathname); });
      });
    }
    function drawAll(){ body.classList.toggle('is-review',!!st.sub); cards.forEach(drawCard); drawCounts(); drawResults(); drawStartBtn(); drawTimer(); }

    function apply(f){
      var shown=0;
      cards.forEach(function(c){ var id=c.dataset.q, m= f==='open'?!st.a[id] : f==='review'?!!REV[id] : f==='new'?!!NEW[id] : true; c.hidden=!m; if(m) shown++; var mb=document.querySelector('.mb[data-q="'+id+'"]'); if(mb) mb.classList.toggle('dim',!m); });
      misses.forEach(function(c){ c.hidden=f!=='all'; });
      document.querySelectorAll('.mb.miss').forEach(function(m){ m.classList.toggle('dim',f!=='all'); });
      var e=document.querySelector('.empty'); if(e) e.hidden=shown>0||f==='all';
    }
    var recount=function(){};
    if(document.querySelector('.chip')) recount=chips(function(id,f){ return f==='open'?!st.a[id]:f==='review'?!!REV[id]:f==='new'?!!NEW[id]:true; },apply,function(){ return cards.map(function(c){ return c.dataset.q; }); });

    var curIdx=-1;
    function setCur(i){ if(i<0||i>=cards.length) return; if(curIdx>=0&&cards[curIdx]) cards[curIdx].classList.remove('cur'); var ch=curIdx!==i; curIdx=i; cards[i].classList.add('cur'); if(ch) emit('focus',{id:cards[i].dataset.q,set:n}); }
    cards.forEach(function(c,i){
      var id=c.dataset.q;
      c.setAttribute('tabindex','-1');
      var qh=c.querySelector('.qh');
      if(qh){ var bmB=document.createElement('button'); bmB.type='button'; bmB.className='bm-btn';
        var bmDraw=function(){ var on=!!store.bm[id]; bmB.setAttribute('aria-pressed',on?'true':'false'); bmB.setAttribute('aria-label',(on?'הסרת סימנייה משאלה ':'סימון שאלה ')+id.split('-')[1]+(on?'':' כקשה')); bmB.title=on?'מסומנת כקשה':'סימון כשאלה קשה'; };
        bmB.innerHTML='<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M6 3.5h12v17l-6-4.2-6 4.2z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>';
        bmB.addEventListener('click',function(ev){ ev.stopPropagation(); if(store.bm[id]) delete store.bm[id]; else store.bm[id]=Date.now(); save(); bmDraw(); emit('bookmark',{id:id,on:!!store.bm[id]}); });
        bmDraw(); qh.appendChild(bmB); }
      c.addEventListener('focusin',function(){ setCur(i); });
      c.addEventListener('click',function(){ setCur(i); });
      c.querySelectorAll('.opt').forEach(function(b){ b.addEventListener('click',function(){
        if(st.sub) return; var k=+b.dataset.n;
        if(st.a[id]===k) delete st.a[id]; else { st.a[id]=k; var xs=st.x[id]; if(xs){ var j=xs.indexOf(k); if(j>=0) xs.splice(j,1); } }
        save(); drawCard(c); drawCounts(); drawTimer(); emit('pick',{id:id,set:n,n:st.a[id]||0,answered:answered(),total:total});
        if(!st.t.run&&!st.t.el&&!nudged&&startB){ nudged=true; startB.classList.add('nudge'); }
      }); });
      c.querySelectorAll('.strike').forEach(function(s){ s.addEventListener('click',function(){
        if(st.sub) return; var k=+s.dataset.n, xs=st.x[id]||(st.x[id]=[]), j=xs.indexOf(k);
        if(j>=0) xs.splice(j,1); else { xs.push(k); if(st.a[id]===k) delete st.a[id]; }
        save(); drawCard(c); drawCounts();
      }); });
    });

    function doSubmit(){
      if(st.t.run){ st.t.el+=Date.now()-st.t.st; st.t.run=false; } loop(false);
      st.sub=true; st.at=Date.now(); logAttempt(n,st); save(); drawAll();
      var last=store.hist[store.hist.length-1]; emit('submit',{set:n,ok:last.ok,tot:last.tot});
      var box=document.getElementById('results'); if(box){ box.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'}); box.focus({preventScroll:true}); }
    }
    document.querySelectorAll('[data-submit]').forEach(function(b){ b.addEventListener('click',function(){
      if(st.sub) return; var left=total-answered();
      if(left>0) ask(left===total?'עוד לא ענית על אף שאלה':'נותרו '+left+' שאלות לא פתורות', left===total?'להגיש את המקבץ בלי תשובות? אחרי ההגשה התשובות ננעלות.':'להגיש בכל זאת? אחרי ההגשה התשובות ננעלות ותוכלו לראות את הפתרונות.','הגשה',doSubmit);
      else ask('להגיש את המקבץ?','ענית על כל '+total+' השאלות. אחרי ההגשה התשובות ננעלות.','הגשה',doSubmit);
    }); });

    document.addEventListener('keydown',function(e){
      if(e.altKey||e.ctrlKey||e.metaKey) return;
      var t=document.activeElement; if(t&&/INPUT|TEXTAREA|SELECT/.test(t.tagName)) return;
      if(dlg&&dlg.open) return;
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){
        var vis=cards.filter(function(c){ return !c.hidden; }); if(!vis.length) return;
        e.preventDefault();
        var pos=vis.indexOf(cards[curIdx]);
        if(pos<0){ var top=0; vis.some(function(c,i){ if(c.getBoundingClientRect().bottom>140){ top=i; return true; } }); pos=e.key==='ArrowDown'?top-1:top+1; }
        var nxt=vis[Math.max(0,Math.min(vis.length-1,pos+(e.key==='ArrowDown'?1:-1)))];
        setCur(cards.indexOf(nxt)); nxt.focus({preventScroll:true}); nxt.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
        return;
      }
      if(/^[1-4]$/.test(e.key)&&!st.sub){
        var c=cards[curIdx]; if(!c||c.hidden){ c=cards.filter(function(x){ return !x.hidden; }).find(function(x){ return x.getBoundingClientRect().bottom>160; }); if(c) setCur(cards.indexOf(c)); }
        if(!c) return; var b=c.querySelector('.opt[data-n="'+e.key+'"]'); if(b){ e.preventDefault(); b.click(); }
      }
    });

    drawAll(); loop(st.t.run);
    if(location.hash){ var h=document.getElementById(location.hash.slice(1)); if(h&&cards.indexOf(h)>=0) setCur(cards.indexOf(h)); }
  }

  /* ================= home ================= */
  if(body.classList.contains('home-page')){
    var done=0, ok=0, resume=null;
    Object.keys(D.exist).sort(function(a,b){return a-b;}).forEach(function(s){
      var st=store.sets[s], sd=0, so=0;
      D.exist[s].forEach(function(q){
        var id=s+'-'+q, c=document.querySelector('.c[data-q="'+id+'"]'), p=st&&st.a[id];
        if(st&&st.sub){ if(p){ sd++; done++; } var r=p&&p===+keyOf(id); if(r){so++;ok++;} if(c) c.classList.add(r?'ok':p?'no':'miss'); }
        else { if(p&&c) c.classList.add('sel'); if(!resume&&!p) resume=[s,q]; }
      });
      var rs=document.querySelector('.rs[data-set="'+s+'"]'); if(rs&&st&&st.sub) rs.textContent=so+'/'+D.exist[s].length;
    });
    var nextSet=null;
    document.querySelectorAll('.setc').forEach(function(card){
      var s=card.dataset.set, ex=D.exist[s]||[], st=store.sets[s], ans=0, ok2=0, tot=ex.length;
      ex.forEach(function(q){ var id=s+'-'+q, p=st&&st.a[id]; if(p){ ans++; if(p===+keyOf(id)) ok2++; } });
      var lab=card.querySelector('.setc-s'), n=card.querySelector('.setc-n').textContent.replace(/\D/g,'');
      card.classList.remove('done','next','started');
      if(st&&st.sub){ card.classList.add('done'); card.style.setProperty('--p',1); lab.textContent='הוגש · '+ok2+'/'+tot; card.setAttribute('aria-label','מקבץ '+n+', הוגש, '+ok2+' נכונות מתוך '+tot); }
      else if(ans){ card.classList.add('started'); card.style.setProperty('--p',ans/tot); lab.textContent='נענו '+ans+' מתוך '+tot; card.setAttribute('aria-label','מקבץ '+n+', נענו '+ans+' מתוך '+tot); if(!nextSet) nextSet=card; }
      else { card.style.setProperty('--p',0); lab.textContent=tot+' שאלות'; if(!nextSet) nextSet=card; }
    });
    if(nextSet&&(done||Object.keys(store.sets).length)){ nextSet.classList.add('next'); var nl=nextSet.querySelector('.setc-s'); if(!nextSet.classList.contains('started')) nl.textContent='הבא בתור'; }
    (function(){ var track=document.querySelector('.setpages'); if(!track) return;
      var groups=[].slice.call(track.querySelectorAll('.setgroup')), dots=[].slice.call(document.querySelectorAll('.sn-dot')),
        prev=document.querySelector('.sn-prev'), next=document.querySelector('.sn-next'), label=document.getElementById('sn-label'), cur=-1;
      function mark(g){ if(g===cur) return; cur=g; label.textContent='מקבצים '+(g*10+1)+'–'+(g*10+10);
        dots.forEach(function(d,i){ d.setAttribute('aria-current',i===g?'true':'false'); });
        prev.disabled=g===0; next.disabled=g===groups.length-1;
        groups.forEach(function(el,i){ el.setAttribute('aria-hidden',i===g?'false':'true'); el.querySelectorAll('a').forEach(function(a){ a.tabIndex=i===g?0:-1; }); }); }
      function go(g,instant){ g=Math.max(0,Math.min(groups.length-1,g)); var el=groups[g];
        track.scrollTo({left:track.scrollLeft+el.getBoundingClientRect().left-track.getBoundingClientRect().left,behavior:instant?'auto':'smooth'}); mark(g); }
      function nearest(){ var r=track.getBoundingClientRect(), best=0, bd=1e9; groups.forEach(function(el,i){ var d=Math.abs(el.getBoundingClientRect().left-r.left); if(d<bd){bd=d;best=i;} }); return best; }
      var t; track.addEventListener('scroll',function(){ clearTimeout(t); t=setTimeout(function(){ mark(nearest()); },80); },{passive:true});
      prev.addEventListener('click',function(){ go(cur-1); }); next.addEventListener('click',function(){ go(cur+1); });
      dots.forEach(function(d,i){ d.addEventListener('click',function(){ go(i); }); });
      track.addEventListener('keydown',function(e){ if(e.key==='ArrowLeft'){ e.preventDefault(); go(cur+1); } if(e.key==='ArrowRight'){ e.preventDefault(); go(cur-1); } });
      var start=nextSet?Math.floor((+nextSet.dataset.set-1)/10):0; go(start,true);
    })();
    document.getElementById('t-done').textContent=done;
    document.getElementById('t-ok').textContent=ok;
    document.getElementById('t-pct').textContent=done?Math.round(100*ok/done)+'%':'–';
    var a=document.getElementById('resume');
    if(resume&&(done||Object.keys(store.sets).length)){ a.href='sets/'+pad(+resume[0])+'.html#q'+resume[0]+'-'+resume[1]; a.textContent='להמשיך ממקבץ '+resume[0]; }
    chips(function(id,f){ var s=id.split('-')[0], st=store.sets[s]; return f==='open'?!(st&&st.a[id]):f==='review'?!!REV[id]:f==='new'?!!NEW[id]:true; },function(f){
      document.querySelectorAll('a.c').forEach(function(c){ var id=c.dataset.q, s=id.split('-')[0], st=store.sets[s], m=f==='open'?!(st&&st.a[id]):f==='review'?!!REV[id]:f==='new'?!!NEW[id]:true; c.classList.toggle('dim',!m); c.classList.toggle('hit',m&&f!=='all'); });
      document.querySelectorAll('.c.miss:not(a)').forEach(function(c){ c.classList.toggle('dim',f!=='all'); });
    },function(){ var a=[]; Object.keys(D.exist).forEach(function(s){ D.exist[s].forEach(function(q){ a.push(s+'-'+q); }); }); return a; });
    document.getElementById('wipe').onclick=function(){
      if(this.dataset.armed){ store={sets:{},hist:[],m:{},wiped:Date.now()}; save(); location.reload(); return; }
      this.dataset.armed=1; this.textContent='ללחוץ שוב כדי לאשר את האיפוס';
    };
  }

  window.addEventListener('beforeprint',function(){ document.querySelectorAll('details.sol').forEach(function(d){ d.dataset.was=d.open?'1':''; d.open=true; }); });
  window.addEventListener('afterprint',function(){ document.querySelectorAll('details.sol').forEach(function(d){ d.open=!!d.dataset.was; }); });
  /* ---- sticky offsets follow the real header height ---- */
  (function(){ var hdr=document.querySelector('.top'); if(!hdr||body.classList.contains('landing')) return;
    var mq=matchMedia('(max-width: 860px)'), last=0;
    var set=function(){ var r=document.documentElement; if(!mq.matches){ r.style.removeProperty('--top'); last=0; return; } var h=hdr.offsetHeight; if(h!==last){ last=h; r.style.setProperty('--top',h+'px'); } };
    set(); addEventListener('resize',set,{passive:true}); if(window.ResizeObserver) new ResizeObserver(set).observe(hdr); })();
  /* ---- avatars ---- */
  var AV=window.URIQ_AVATARS||{}, AVO=window.URIQ_AVATAR_ORDER||[];
  function avatarHTML(id){ return AV[id]?AV[id].svg:''; }
  function avatarPicker(box,onPick){
    var cur=store.avatar||'';
    box.innerHTML='<fieldset class="avpick"><legend class="vh">בחירת דמות לפרופיל</legend>'+AVO.map(function(k){
      return '<label class="avopt"><input type="radio" name="uriq-av" value="'+k+'"'+(k===cur?' checked':'')+'><span class="avimg">'+AV[k].svg+'</span><span class="avname">'+AV[k].name+'</span></label>'; }).join('')+'</fieldset>';
    box.querySelectorAll('input').forEach(function(r){ r.addEventListener('change',function(){ store.avatar=r.value; save(); paintChip(); emit('avatar',{id:r.value}); if(onPick) onPick(r.value); }); });
  }
  /* ---- personal accent colour ---- */
  var ACC=[['green','ירוק','#12805C'],['ink','שחור','#111111'],['blue','כחול','#2B3BFF'],['violet','סגול','#7339F0'],['pink','ורוד','#E2336B'],['orange','כתום','#E25F14'],['teal','טורקיז','#0E7C86'],['sky','תכלת','#0A6CB5'],['red','אדום','#D12C2C'],['amber','חרדל','#A85F00'],['olive','זית','#5B7A12'],['wine','בורדו','#9C1F4A']];
  function applyAccent(a){ var r=document.documentElement; if(a&&a!=='green') r.dataset.accent=a; else delete r.dataset.accent; try{ if(a) localStorage.setItem('uriq:accent',a); else localStorage.removeItem('uriq:accent'); }catch(e){} }
  (function(){ var want=store.accent&&store.accent!=='green'?store.accent:''; if(want!==(document.documentElement.dataset.accent||'')) applyAccent(want); })();
  function accentPicker(box){
    var cur=store.accent||'green';
    box.innerHTML='<fieldset class="acpick"><legend class="vh">צבע האתר</legend>'+ACC.map(function(c){ return '<label class="acopt"><input type="radio" name="uriq-ac" value="'+c[0]+'"'+(c[0]===cur?' checked':'')+'><span class="sw" style="--c:'+c[2]+'"></span><span>'+c[1]+'</span></label>'; }).join('')+'</fieldset>';
    box.querySelectorAll('input').forEach(function(r){ r.addEventListener('change',function(){ store.accent=r.value; save(); applyAccent(r.value); emit('accent',{id:r.value}); }); });
  }
  /* ---- display name: the user's own choice, else the first name from Google ---- */
  function displayName(){ var n=(store.name||'').trim(); if(n) return n; var pf=UID?load('uriq:profile',null):null; return pf&&pf.name?pf.name.split(' ')[0]:''; }
  if(UID) document.querySelectorAll('a.f-login').forEach(function(a){ a.remove(); });
  /* ---- account chip ---- */
  var acct=document.getElementById('acct');
  function paintChip(){ if(!acct) return; var av=acct.querySelector('.av'), an=acct.querySelector('.an'), dn=displayName(); if(an&&dn) an.textContent=dn; if(store.avatar&&AV[store.avatar]){ av.innerHTML=avatarHTML(store.avatar); av.classList.add('has-av'); } }
  if(acct){ var pf=UID?load('uriq:profile',null):null;
    if(pf){ var av=acct.querySelector('.av'), nm=(pf.name||pf.email||'').split(' ')[0];
      acct.href=root+'dashboard.html'; acct.setAttribute('aria-label','האזור שלי – '+(pf.name||pf.email||''));
      acct.querySelector('.an').textContent=displayName()||nm||'החשבון שלי';
      if(store.avatar&&AV[store.avatar]){ /* painted below */ } else if(pf.avatar){ var im=new Image(); im.alt=''; im.referrerPolicy='no-referrer'; im.src=pf.avatar; im.onerror=function(){ av.textContent=(nm||'?').charAt(0); }; av.innerHTML=''; av.appendChild(im); } else av.textContent=(nm||'?').charAt(0);
    } paintChip(); }
  window.URIQ={displayName:displayName, accentPicker:accentPicker, applyAccent:applyAccent, avatarHTML:avatarHTML, avatarPicker:avatarPicker, paintChip:paintChip, emit:emit, get store(){ return store; }, set store(v){ store=v; }, KEY:KEY, UID:UID, save:save, keyOf:keyOf, D:D, fmt:fmt, fmtShort:fmtShort, pad:pad, summarize:summarize, load:load, put:put, ask:ask, root:root};
  sideProgress();
})();
