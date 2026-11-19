(function(){
  var KEY='uri-kamuti:v1', st={};
  try{ st=JSON.parse(localStorage.getItem(KEY)||'{}')||{}; }catch(e){ st={}; }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(st)); }catch(e){} }
  var body=document.body;

  if(body.classList.contains('setpage')){
    var set=+body.dataset.set, key=body.dataset.key.split('').map(Number);
    var qs=[].slice.call(document.querySelectorAll('.q'));
    function render(q){
      var id=q.id.slice(1), n=+id.split('-')[1], ans=key[n-1], picked=st[id];
      var opts=[].slice.call(q.querySelectorAll('.opt'));
      var v=q.querySelector('.verdict');
      if(!v){ v=document.createElement('p'); v.className='verdict'; v.setAttribute('aria-live','polite'); q.querySelector('.opts').after(v); }
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
      v.textContent= ok ? 'נכון.' : 'לא נכון – התשובה הנכונה היא ('+ans+').';
      var b=document.createElement('button'); b.type='button'; b.className='again'; b.textContent='לענות שוב';
      b.onclick=function(){ delete st[id]; save(); render(q); summary(); };
      v.appendChild(b);
      if(mb) mb.classList.add(ok?'ok':'no');
    }
    function summary(){
      var done=0, ok=0;
      qs.forEach(function(q){ var id=q.id.slice(1), n=+id.split('-')[1]; if(st[id]){ done++; if(st[id]===key[n-1]) ok++; } });
      document.querySelector('.score').textContent = done? ok+'/'+done+' נכונות' : qs.length+' שאלות';
      var d=document.querySelector('.done');
      if(done===qs.length){ d.hidden=false; d.querySelector('.done-t').textContent='סיימת את המקבץ: '+ok+' מתוך '+qs.length+' נכונות'; }
      else d.hidden=true;
    }
    qs.forEach(function(q){
      var id=q.id.slice(1);
      q.querySelectorAll('.opt').forEach(function(o){
        o.addEventListener('click',function(){
          if(st[id]) return;
          st[id]=+o.dataset.n; save(); render(q); summary();
        });
      });
      render(q);
    });
    summary();
    document.querySelector('.redo').onclick=function(){
      qs.forEach(function(q){ delete st[q.id.slice(1)]; render(q); }); save(); summary(); window.scrollTo(0,0);
    };
    // keyboard: 1-4 answers the question nearest the top of the viewport
    document.addEventListener('keydown',function(e){
      if(e.altKey||e.ctrlKey||e.metaKey||!/^[1-4]$/.test(e.key)) return;
      var cur=qs.find(function(q){ return q.getBoundingClientRect().bottom>140 && !q.classList.contains('answered'); });
      if(!cur) return; var b=cur.querySelector('.opt[data-n="'+e.key+'"]'); if(b){ b.click(); }
    });
  }

  if(body.classList.contains('home-page')){
    var D=window.KAMUTI, done=0, ok=0, resume=null;
    Object.keys(D.exist).sort(function(a,b){return a-b;}).forEach(function(s){
      var sd=0, so=0;
      D.exist[s].forEach(function(q){
        var id=s+'-'+q, p=st[id], c=document.querySelector('.c[data-q="'+id+'"]');
        if(p){ sd++; done++; var r=p===D.key[s][q-1]; if(r){so++;ok++;} if(c) c.classList.add(r?'ok':'no'); }
        else if(!resume) resume=[s,q];
      });
      var rs=document.querySelector('.rs[data-set="'+s+'"]'); if(rs&&sd) rs.textContent=so+'/'+sd;
    });
    document.getElementById('t-done').textContent=done;
    document.getElementById('t-ok').textContent=ok;
    document.getElementById('t-pct').textContent=done?Math.round(100*ok/done)+'%':'–';
    var a=document.getElementById('resume');
    if(done&&resume){ a.href='sets/'+String(resume[0]).padStart(2,'0')+'.html#q'+resume[0]+'-'+resume[1]; a.textContent='להמשיך ממקבץ '+resume[0]+', שאלה '+resume[1]; }
    else if(done&&!resume){ a.textContent='ענית על הכול'; a.href='#'; }
    document.getElementById('wipe').onclick=function(){
      if(this.dataset.armed){ st={}; save(); location.reload(); return; }
      this.dataset.armed=1; this.textContent='ללחוץ שוב כדי לאשר איפוס';
    };
  }
})();
