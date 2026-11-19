(function(){
  var KEY='uri-kamuti:v1', st={};
  try{ st=JSON.parse(localStorage.getItem(KEY)||'{}')||{}; }catch(e){ st={}; }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(st)); }catch(e){} }
  var D=window.KAMUTI||{key:{},exist:{},review:[],fresh:[],idx:[]};
  var body=document.body, root=body.dataset.root||'';
  var REV={}, NEW={};
  D.review.forEach(function(i){REV[i]=1;}); D.fresh.forEach(function(i){NEW[i]=1;});
  function pad(n){ return (n<10?'0':'')+n; }
  function isRight(id){ var p=id.split('-'); return st[id]===D.key[p[0]][p[1]-1]; }
  function match(id,f){
    if(f==='open') return !st[id];
    if(f==='review') return !!REV[id];
    if(f==='new') return !!NEW[id];
    return true;
  }
  function allIds(){ var a=[]; Object.keys(D.exist).forEach(function(s){ D.exist[s].forEach(function(q){ a.push(s+'-'+q); }); }); return a; }

  /* ---- sidebar progress + mobile drawer ---- */
  function sideProgress(){
    Object.keys(D.exist).forEach(function(s){
      var ex=D.exist[s]; if(!ex.length) return;
      var done=0, ok=0; ex.forEach(function(q){ var id=s+'-'+q; if(st[id]){ done++; if(isRight(id)) ok++; } });
      var i=document.querySelector('[data-pb="'+s+'"]'); if(i) i.style.width=(100*done/ex.length)+'%';
      var sm=document.querySelector('[data-sp="'+s+'"]');
      if(sm){ sm.textContent= done ? done+'/'+ex.length : String(ex.length); sm.closest('.sl').classList.toggle('full',done===ex.length); sm.closest('.sl').setAttribute('aria-label','מקבץ '+s+', נענו '+done+' מתוך '+ex.length); }
    });
  }
  var side=document.getElementById('side'), nb=document.querySelector('.navbtn'), scrim=document.querySelector('.scrim');
  function drawer(open){
    if(!side) return; side.classList.toggle('open',open); if(scrim) scrim.hidden=!open;
    if(nb) nb.setAttribute('aria-expanded',open?'true':'false');
    if(open){ var c=side.querySelector('[aria-current]'); (c||side.querySelector('a')).focus(); }
  }
  if(nb) nb.addEventListener('click',function(){ drawer(!side.classList.contains('open')); });
  if(scrim) scrim.addEventListener('click',function(){ drawer(false); nb.focus(); });
  var sx=document.querySelector('.side-x'); if(sx) sx.addEventListener('click',function(){ drawer(false); nb.focus(); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape' && side && side.classList.contains('open')){ drawer(false); nb.focus(); } });
  if(side){ var cur=side.querySelector('[aria-current]'); if(cur) side.scrollTop=Math.max(0,cur.offsetTop-side.clientHeight/2); }

  /* ---- global search ---- */
  var inp=document.getElementById('q-search'), res=document.getElementById('q-results'), sel=-1;
  function norm(s){ return s.replace(/[֑-ׇ]/g,'').toLowerCase(); }
  var IDX=D.idx.map(function(r){ return [r[0],r[1],norm(r[1])]; });
  function esc(s){ return s.replace(/[&<>"]/g,function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function snippet(t,w){
    var i=norm(t).indexOf(w), a=Math.max(0,i-30), s=(a?'…':'')+t.slice(a,a+110)+(t.length>a+110?'…':'');
    if(i<0) return esc(s);
    var j=norm(s).indexOf(w); return esc(s.slice(0,j))+'<mark>'+esc(s.slice(j,j+w.length))+'</mark>'+esc(s.slice(j+w.length));
  }
  function close(){ if(!res) return; res.hidden=true; inp.setAttribute('aria-expanded','false'); sel=-1; }
  function run(){
    var v=norm(inp.value.trim()); if(!v){ close(); return; }
    var words=v.split(/\s+/), out=[];
    var m=v.match(/^(?:מקבץ\s*)?(\d{1,2})$/);
    if(m && +m[1]>=1 && +m[1]<=40) out.push('<li><a role="option" href="'+root+'sets/'+pad(+m[1])+'.html"><b>מעבר</b>מקבץ '+(+m[1])+'</a></li>');
    for(var k=0;k<IDX.length && out.length<12;k++){
      var r=IDX[k]; if(words.every(function(w){ return r[2].indexOf(w)>=0; })){
        var p=r[0].split('-');
        out.push('<li><a role="option" href="'+root+'sets/'+pad(+p[0])+'.html#q'+r[0]+'"><b>מקבץ '+p[0]+', שאלה '+p[1]+'</b>'+snippet(r[1],words[0])+'</a></li>');
      }
    }
    res.innerHTML=out.length?out.join(''):'<li class="nores">לא נמצאו שאלות. אפשר לחפש מילה מהשאלה או מספר מקבץ.</li>';
    res.hidden=false; inp.setAttribute('aria-expanded','true'); sel=-1;
  }
  if(inp){
    inp.addEventListener('input',run);
    inp.addEventListener('keydown',function(e){
      var links=res.querySelectorAll('a');
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){ if(!links.length) return; e.preventDefault(); sel=(sel+(e.key==='ArrowDown'?1:-1)+links.length)%links.length; links.forEach(function(a,i){ a.setAttribute('aria-selected',i===sel?'true':'false'); }); links[sel].scrollIntoView({block:'nearest'}); }
      else if(e.key==='Enter'){ var a=links[sel<0?0:sel]; if(a){ e.preventDefault(); close(); location.href=a.href; } }
      else if(e.key==='Escape'){ close(); }
    });
    res.addEventListener('click',function(){ close(); inp.value=''; });
    document.addEventListener('click',function(e){ if(!e.target.closest('.search')) close(); });
  }

  /* ---- filter chips ---- */
  function chips(apply,ids){
    var bs=[].slice.call(document.querySelectorAll('.chip'));
    function counts(){
      ['all','open','review','new'].forEach(function(f){
        var n=ids().filter(function(id){ return match(id,f); }).length, el=document.querySelector('[data-c="'+f+'"]');
        if(el) el.textContent=n;
        var b=document.querySelector('.chip[data-f="'+f+'"]'); if(b && f!=='all') b.disabled=!n && b.getAttribute('aria-pressed')!=='true';
      });
    }
    bs.forEach(function(b){ b.addEventListener('click',function(){
      bs.forEach(function(x){ x.setAttribute('aria-pressed',x===b?'true':'false'); });
      apply(b.dataset.f); counts();
    }); });
    counts(); return counts;
  }
  function curFilter(){ var b=document.querySelector('.chip[aria-pressed="true"]'); return b?b.dataset.f:'all'; }

  /* ---- set page ---- */
  if(body.classList.contains('setpage')){
    var key=body.dataset.key.split('').map(Number);
    var qs=[].slice.call(document.querySelectorAll('.q:not(.miss)')), miss=[].slice.call(document.querySelectorAll('.q.miss'));
    function render(q){
      var id=q.dataset.q, n=+id.split('-')[1], ans=key[n-1], picked=st[id];
      var opts=[].slice.call(q.querySelectorAll('.opt')), v=q.querySelector('.verdict');
      opts.forEach(function(o){ o.className='opt'; o.setAttribute('aria-pressed','false'); });
      q.classList.toggle('answered',!!picked);
      var mb=document.querySelector('.mb[data-q="'+id+'"]'); if(mb) mb.classList.remove('ok','no');
      if(!picked){ v.textContent=''; v.className='verdict'; return; }
      opts.forEach(function(o){
        var k=+o.dataset.n;
        if(k===ans) o.classList.add('correct');
        if(k===picked){ o.classList.add('picked', k===ans?'right':'wrong'); o.setAttribute('aria-pressed','true'); }
      });
      var ok=picked===ans;
      v.className='verdict '+(ok?'r':'w');
      v.textContent= ok ? 'נכון.' : 'לא נכון. התשובה הנכונה היא ('+ans+').';
      var b=document.createElement('button'); b.type='button'; b.className='again'; b.textContent='לענות שוב';
      b.onclick=function(){ delete st[id]; save(); render(q); update(); };
      v.appendChild(b);
      if(mb) mb.classList.add(ok?'ok':'no');
    }
    var recount=function(){};
    function apply(f){
      var shown=0;
      qs.forEach(function(q){ var m=match(q.dataset.q,f); q.hidden=!m; if(m) shown++; var mb=document.querySelector('.mb[data-q="'+q.dataset.q+'"]'); if(mb) mb.classList.toggle('dim',!m); });
      miss.forEach(function(q){ q.hidden=f!=='all'; });
      document.querySelectorAll('.mb.miss').forEach(function(m){ m.classList.toggle('dim',f!=='all'); });
      var e=document.querySelector('.empty'); if(e) e.hidden=shown>0 || f==='all';
    }
    function update(){
      var done=0, ok=0;
      qs.forEach(function(q){ var id=q.dataset.q; if(st[id]){ done++; if(isRight(id)) ok++; } });
      var sc=document.querySelector('.score');
      sc.textContent= !qs.length ? '' : done ? ok+' מתוך '+done+' נכונות' : qs.length+' שאלות לתרגול';
      var d=document.querySelector('.done');
      if(qs.length && done===qs.length){ d.hidden=false; d.querySelector('.done-t').textContent='סיימת את המקבץ: '+ok+' מתוך '+qs.length+' נכונות'; }
      else d.hidden=true;
      sideProgress(); recount();
      if(curFilter()==='open') apply('open');
    }
    qs.forEach(function(q){
      var id=q.dataset.q;
      q.querySelectorAll('.opt').forEach(function(o){
        o.addEventListener('click',function(){ if(st[id]) return; st[id]=+o.dataset.n; save(); render(q); update(); });
      });
      render(q);
    });
    if(document.querySelector('.chip')) recount=chips(apply,function(){ return qs.map(function(q){ return q.dataset.q; }); });
    update();
    document.querySelector('.redo').onclick=function(){
      qs.forEach(function(q){ delete st[q.dataset.q]; render(q); }); save(); update(); window.scrollTo(0,0);
    };
    document.addEventListener('keydown',function(e){
      if(e.altKey||e.ctrlKey||e.metaKey||!/^[1-4]$/.test(e.key)||/INPUT|TEXTAREA/.test(document.activeElement.tagName)) return;
      var cur=qs.find(function(q){ return !q.hidden && q.getBoundingClientRect().bottom>160 && !q.classList.contains('answered'); });
      if(!cur) return; var b=cur.querySelector('.opt[data-n="'+e.key+'"]'); if(b) b.click();
    });
  }

  /* ---- home ---- */
  if(body.classList.contains('home-page')){
    var done=0, ok=0, resume=null;
    Object.keys(D.exist).sort(function(a,b){return a-b;}).forEach(function(s){
      var sd=0, so=0;
      D.exist[s].forEach(function(q){
        var id=s+'-'+q, c=document.querySelector('.c[data-q="'+id+'"]');
        if(st[id]){ sd++; done++; var r=isRight(id); if(r){so++;ok++;} if(c) c.classList.add(r?'ok':'no'); }
        else if(!resume) resume=[s,q];
      });
      var rs=document.querySelector('.rs[data-set="'+s+'"]'); if(rs&&sd) rs.textContent=so+'/'+sd;
    });
    document.getElementById('t-done').textContent=done;
    document.getElementById('t-ok').textContent=ok;
    document.getElementById('t-pct').textContent=done?Math.round(100*ok/done)+'%':'–';
    var a=document.getElementById('resume');
    if(done&&resume){ a.href='sets/'+pad(+resume[0])+'.html#q'+resume[0]+'-'+resume[1]; a.textContent='להמשיך ממקבץ '+resume[0]+', שאלה '+resume[1]; }
    else if(done&&!resume){ a.textContent='עברת על כל השאלות'; a.href='solutions.html'; }
    chips(function(f){
      document.querySelectorAll('a.c').forEach(function(c){ var m=match(c.dataset.q,f); c.classList.toggle('dim',!m); c.classList.toggle('hit',m && f!=='all'); });
      document.querySelectorAll('.c.miss').forEach(function(c){ c.classList.toggle('dim',f!=='all'); });
    },allIds);
    document.getElementById('wipe').onclick=function(){
      if(this.dataset.armed){ st={}; save(); location.reload(); return; }
      this.dataset.armed=1; this.textContent='ללחוץ שוב כדי לאשר את האיפוס';
    };
  }

  /* ---- print: open every solution ---- */
  window.addEventListener('beforeprint',function(){ document.querySelectorAll('details.sol').forEach(function(d){ d.dataset.was=d.open?'1':''; d.open=true; }); });
  window.addEventListener('afterprint',function(){ document.querySelectorAll('details.sol').forEach(function(d){ d.open=!!d.dataset.was; }); });
  sideProgress();
})();
