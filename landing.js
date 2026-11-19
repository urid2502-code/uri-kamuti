(function(){
  'use strict';
  var U=window.URIQ||{}, D=U.D||window.KAMUTI||{exist:{}}, store=U.store||{sets:{}};
  var html=document.documentElement, body=document.body;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer=matchMedia('(pointer: fine)').matches;
  var nav=navigator, lite=reduce||(nav.connection&&nav.connection.saveData)||(nav.hardwareConcurrency&&nav.hardwareConcurrency<=4)||(nav.deviceMemory&&nav.deviceMemory<=4);
  if(lite) html.classList.add('lite');

  /* ---- load choreography: start once fonts are in (or after 700ms) ---- */
  var go=function(){ requestAnimationFrame(function(){ requestAnimationFrame(function(){ body.classList.add('loaded'); }); }); };
  var started=false; function start(){ if(started) return; started=true; go(); }
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(start);
  setTimeout(start,700);

  /* ---- top bar turns solid after the hero starts scrolling ---- */
  var top=document.querySelector('.top');

  /* ---- hero depth: pointer + scroll parallax, transform-only, rAF runs only while settling ---- */
  var stage=document.querySelector('.stage'), inner=document.getElementById('stage-in');
  var layers=[].slice.call(document.querySelectorAll('.geo [data-depth]')).map(function(el){ return {el:el,d:+el.dataset.depth}; });
  var tx=0,ty=0,cx=0,cy=0,sy=0,csy=0,raf=0,heroOn=true,H=innerHeight;
  function frame(){
    raf=0;
    cx+=(tx-cx)*0.085; cy+=(ty-cy)*0.085; csy+=(sy-csy)*0.2;
    var settle=Math.abs(tx-cx)<0.001&&Math.abs(ty-cy)<0.001&&Math.abs(sy-csy)<0.5;
    if(heroOn){
      for(var i=0;i<layers.length;i++){ var L=layers[i]; L.el.style.transform='translate3d('+(cx*L.d*22).toFixed(2)+'px,'+(cy*L.d*16-csy*L.d*0.22).toFixed(2)+'px,0)'; }
      if(inner){ var k=Math.min(1,csy/(H*0.85)); inner.style.transform='translate3d(0,'+(csy*0.32).toFixed(1)+'px,0)'; inner.style.opacity=(1-k*1.15).toFixed(3); }
    }
    if(!settle) raf=requestAnimationFrame(frame);
  }
  function kick(){ if(!raf) raf=requestAnimationFrame(frame); }
  if(!reduce){
    if(finePointer&&!lite) addEventListener('pointermove',function(e){ if(e.pointerType!=='mouse') return; tx=e.clientX/innerWidth-0.5; ty=e.clientY/innerHeight-0.5; kick(); },{passive:true});
    addEventListener('scroll',function(){ sy=Math.min(scrollY,H*1.2); kick(); },{passive:true});
    addEventListener('resize',function(){ H=innerHeight; },{passive:true});
  }
  function navState(){ if(top) top.classList.toggle('solid',scrollY>40); }
  addEventListener('scroll',navState,{passive:true}); navState();

  /* pause the looping hero animations whenever the hero is off-screen */
  if('IntersectionObserver' in window && stage){
    new IntersectionObserver(function(es){ heroOn=es[0].isIntersecting; stage.classList.toggle('paused',!heroOn); },{threshold:0}).observe(stage);
  }

  /* ---- scroll reveals ---- */
  var rv=[].slice.call(document.querySelectorAll('.rv'));
  if(reduce||!('IntersectionObserver' in window)) rv.forEach(function(e){ e.classList.add('in'); });
  else { var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); },{rootMargin:'0px 0px -12% 0px'}); rv.forEach(function(e){ io.observe(e); }); }

  /* ---- personal touches: resume link, live progress in the sets preview ---- */
  var pad=function(n){ return (n<10?'0':'')+n; };
  var resume=null, any=false;
  Object.keys(D.exist||{}).sort(function(a,b){ return a-b; }).forEach(function(s){
    var ex=D.exist[s]; if(!ex.length) return;
    var st=store.sets[s], done=0; if(st) ex.forEach(function(q){ if(st.a[s+'-'+q]) done++; });
    if(st&&(done||st.sub)) any=true;
    if(!resume&&!(st&&st.sub)) resume=s;
    var cell=document.querySelector('[data-pv="'+s+'"]'); if(!cell) return;
    if(st&&st.sub){ cell.classList.add('done'); cell.setAttribute('aria-label','מקבץ '+s+', הוגש'); }
    else if(done){ cell.classList.add('part'); cell.style.setProperty('--p',Math.round(100*done/ex.length)+'%'); cell.setAttribute('aria-label','מקבץ '+s+', נענו '+done+' מתוך '+ex.length); }
  });
  var heroGo=document.getElementById('hero-go');
  if(any&&resume&&heroGo){ heroGo.firstChild.nodeValue='להמשיך ממקבץ '+resume; heroGo.href='sets/'+pad(+resume)+'.html'; }
  var hl=document.getElementById('hero-login');
  if(hl&&U.UID){ hl.textContent='לאזור שלי'; hl.href='dashboard.html'; }

  /* ================= signature carousel ================= */
  var car=document.getElementById('car'); if(!car) return;
  var vp=car.querySelector('.car-vp'), tr=car.querySelector('.car-tr'), slides=[].slice.call(car.querySelectorAll('.slide'));
  var dots=[].slice.call(car.querySelectorAll('.car-dots button')), count=car.querySelector('.car-count');
  var prevB=car.querySelector('.car-prev'), nextB=car.querySelector('.car-next');
  var cur=0, base=0, rtl=getComputedStyle(car).direction==='rtl';
  function offsetFor(i){ var s=slides[i]; return vp.clientWidth/2-(s.offsetLeft+s.offsetWidth/2); }
  function place(x,anim){ tr.classList.toggle('nodrag',!anim); tr.style.transform='translate3d('+x.toFixed(1)+'px,0,0)'; }
  function goTo(i,anim){
    cur=Math.max(0,Math.min(slides.length-1,i)); base=offsetFor(cur); place(base,anim!==false);
    slides.forEach(function(s,j){ var on=j===cur; s.classList.toggle('on',on); s.setAttribute('aria-hidden',on?'false':'true');
      s.querySelectorAll('a,button').forEach(function(a){ if(on) a.removeAttribute('tabindex'); else a.setAttribute('tabindex','-1'); }); });
    dots.forEach(function(d,j){ d.setAttribute('aria-current',j===cur?'true':'false'); });
    if(count) count.textContent=(cur+1)+' / '+slides.length;
    prevB.disabled=cur===0; nextB.disabled=cur===slides.length-1;
  }
  prevB.addEventListener('click',function(){ goTo(cur-1); });
  nextB.addEventListener('click',function(){ goTo(cur+1); });
  dots.forEach(function(d,j){ d.addEventListener('click',function(){ goTo(j); }); });
  car.addEventListener('keydown',function(e){
    var fwd=rtl?'ArrowLeft':'ArrowRight', back=rtl?'ArrowRight':'ArrowLeft';
    if(e.key===fwd){ e.preventDefault(); goTo(cur+1); } else if(e.key===back){ e.preventDefault(); goTo(cur-1); }
    else if(e.key==='Home'){ e.preventDefault(); goTo(0); } else if(e.key==='End'){ e.preventDefault(); goTo(slides.length-1); }
  });
  /* drag / swipe: horizontal intent only, so vertical page scrolling stays native */
  var down=null, moved=false;
  vp.addEventListener('pointerdown',function(e){ if(e.button!==0) return; down={x:e.clientX,y:e.clientY,id:e.pointerId,t:performance.now(),lock:null}; moved=false; });
  vp.addEventListener('pointermove',function(e){
    if(!down||e.pointerId!==down.id) return;
    var dx=e.clientX-down.x, dy=e.clientY-down.y;
    if(down.lock===null&&(Math.abs(dx)>6||Math.abs(dy)>6)){ down.lock=Math.abs(dx)>Math.abs(dy); if(down.lock){ vp.setPointerCapture(e.pointerId); vp.classList.add('drag'); } }
    if(!down.lock) return;
    moved=true; var edge=(cur===0&&(rtl?dx<0:dx>0))||(cur===slides.length-1&&(rtl?dx>0:dx<0));
    place(base+(edge?dx*0.35:dx),false);
  });
  function up(e){
    if(!down||e.pointerId!==down.id) return;
    var dx=e.clientX-down.x, v=Math.abs(dx)/Math.max(1,performance.now()-down.t);
    vp.classList.remove('drag');
    if(down.lock){ var dir=(rtl?dx>0:dx<0)?1:-1; if(Math.abs(dx)>vp.clientWidth*0.12||v>0.5) goTo(cur+dir); else goTo(cur); }
    down=null;
  }
  vp.addEventListener('pointerup',up); vp.addEventListener('pointercancel',up);
  vp.addEventListener('click',function(e){
    if(moved){ e.preventDefault(); e.stopPropagation(); moved=false; return; }
    var s=e.target.closest('.slide'); var j=slides.indexOf(s);
    if(j>=0&&j!==cur){ e.preventDefault(); goTo(j); }
  },true);
  vp.addEventListener('dragstart',function(e){ e.preventDefault(); });
  var rt; addEventListener('resize',function(){ clearTimeout(rt); rt=setTimeout(function(){ goTo(cur,false); },120); },{passive:true});
  goTo(0,false);
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){ goTo(cur,false); });
})();
