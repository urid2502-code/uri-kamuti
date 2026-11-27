/* urIQ profile avatars: original flat illustrations, 80×80, one accent colour each. */
(function(){
  var S='<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">';
  var A={
    explorer:{name:'החוקרת',svg:S+'<circle cx="40" cy="40" r="40" fill="#F5B841"/>'+
      '<path d="M14 80c2-15 13-22 26-22s24 7 26 22z" fill="#2F5D50"/><path d="M33 58h14l-7 9z" fill="#F2C6A0"/>'+
      '<rect x="34" y="48" width="12" height="12" rx="5" fill="#E8B48C"/>'+
      '<path d="M22 40c0-14 8-22 18-22s18 8 18 22c0 6-1 12-3 16H25c-2-4-3-10-3-16z" fill="#5A3825"/>'+
      '<ellipse cx="40" cy="38" rx="13" ry="15" fill="#F2C6A0"/>'+
      '<path d="M18 27c3-9 12-14 22-14s19 5 22 14z" fill="#C98F2E"/><rect x="14" y="26" width="52" height="5" rx="2.5" fill="#8A5A1C"/>'+
      '<circle cx="35" cy="38" r="2" fill="#1A1A1A"/><circle cx="45" cy="38" r="2" fill="#1A1A1A"/>'+
      '<path d="M35 45q5 4 10 0" stroke="#1A1A1A" stroke-width="2" fill="none" stroke-linecap="round"/>'+
      '<circle cx="31" cy="43" r="2.4" fill="#F09B7A" opacity=".55"/><circle cx="49" cy="43" r="2.4" fill="#F09B7A" opacity=".55"/></svg>'},
    professor:{name:'הפרופסור',svg:S+'<circle cx="40" cy="40" r="40" fill="#A9C1E0"/>'+
      '<path d="M13 80c2-15 13-23 27-23s25 8 27 23z" fill="#3B4252"/><path d="M33 57l7 10 7-10z" fill="#FFFFFF"/>'+
      '<path d="M34 64l6-3 6 3-6 3z" fill="#D7263D"/><circle cx="40" cy="64" r="1.6" fill="#9E1B2C"/>'+
      '<rect x="34" y="47" width="12" height="12" rx="5" fill="#E3B38F"/>'+
      '<ellipse cx="40" cy="37" rx="14" ry="16" fill="#EDC4A2"/>'+
      '<path d="M25 33c-3-4-2-10 2-11 1-5 8-8 13-6 5-2 12 1 13 6 4 1 5 7 2 11-1-5-5-8-15-8s-14 3-15 8z" fill="#E6E6E6"/>'+
      '<circle cx="34" cy="38" r="5" fill="none" stroke="#1A1A1A" stroke-width="1.8"/><circle cx="46" cy="38" r="5" fill="none" stroke="#1A1A1A" stroke-width="1.8"/><path d="M39 38h2" stroke="#1A1A1A" stroke-width="1.8"/>'+
      '<circle cx="34" cy="38" r="1.6" fill="#1A1A1A"/><circle cx="46" cy="38" r="1.6" fill="#1A1A1A"/>'+
      '<path d="M34 47c3-2 9-2 12 0" stroke="#BDBDBD" stroke-width="3" fill="none" stroke-linecap="round"/>'+
      '<path d="M37 49.5q3 1.8 6 0" stroke="#1A1A1A" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'},
    buddy:{name:'החבר',svg:S+'<circle cx="40" cy="40" r="40" fill="#8FD3A8"/>'+
      '<path d="M12 80c2-16 13-25 28-25s26 9 28 25z" fill="#2E7D4F"/><path d="M24 58c4 6 9 9 16 9s12-3 16-9" stroke="#1F5C39" stroke-width="3" fill="none"/>'+
      '<path d="M37 64v8M43 64v8" stroke="#E8F5EC" stroke-width="1.8" stroke-linecap="round"/>'+
      '<ellipse cx="40" cy="39" rx="14" ry="15" fill="#B7825B"/>'+
      '<path d="M25 36c-2-10 5-18 15-18s17 8 15 18c-2-5-4-7-6-7 0-3-3-4-5-2-2-3-6-3-8 0-2-2-5-1-5 2-2 0-5 2-6 7z" fill="#2B1B12"/>'+
      '<circle cx="34.5" cy="39" r="2.1" fill="#1A1A1A"/><circle cx="45.5" cy="39" r="2.1" fill="#1A1A1A"/>'+
      '<path d="M33 45q7 7 14 0z" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="1.6" stroke-linejoin="round"/></svg>'},
    astro:{name:'האסטרונאוטית',svg:S+'<circle cx="40" cy="40" r="40" fill="#1F2235"/>'+
      '<circle cx="14" cy="18" r="1.2" fill="#fff"/><circle cx="64" cy="14" r="1" fill="#fff"/><circle cx="68" cy="34" r="1.3" fill="#fff"/><circle cx="10" cy="44" r="1" fill="#fff"/>'+
      '<path d="M14 80c2-14 12-21 26-21s24 7 26 21z" fill="#E9EDF3"/><rect x="33" y="64" width="14" height="8" rx="2" fill="#F45B69"/>'+
      '<circle cx="40" cy="38" r="21" fill="#F4F6F9"/><circle cx="40" cy="38" r="21" fill="none" stroke="#C9D1DC" stroke-width="2"/>'+
      '<rect x="25" y="28" width="30" height="21" rx="10.5" fill="#2A3F6B"/>'+
      '<ellipse cx="40" cy="39" rx="10" ry="9" fill="#D9A27E"/><circle cx="36.5" cy="38" r="1.7" fill="#1A1A1A"/><circle cx="43.5" cy="38" r="1.7" fill="#1A1A1A"/>'+
      '<path d="M37 43q3 2.4 6 0" stroke="#1A1A1A" stroke-width="1.5" fill="none" stroke-linecap="round"/>'+
      '<path d="M29 31c5-3 12-3 17-1" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".55"/></svg>'},
    fox:{name:'השועל',svg:S+'<circle cx="40" cy="40" r="40" fill="#FFE3C7"/>'+
      '<path d="M16 80c3-13 12-19 24-19s21 6 24 19z" fill="#E8762C"/><path d="M33 61l7 10 7-10z" fill="#FFFFFF"/>'+
      '<path d="M18 18l14 12-10 9zM62 18L48 30l10 9z" fill="#E8762C"/><path d="M21 22l8 7-5 5zM59 22l-8 7 5 5z" fill="#3A2416"/>'+
      '<path d="M18 36c0-10 10-16 22-16s22 6 22 16c0 9-9 19-22 25-13-6-22-16-22-25z" fill="#F08A3C"/>'+
      '<path d="M24 42c6 0 11 4 16 13 5-9 10-13 16-13-2 8-8 14-16 19-8-5-14-11-16-19z" fill="#FFFFFF"/>'+
      '<circle cx="32" cy="38" r="2.3" fill="#1A1A1A"/><circle cx="48" cy="38" r="2.3" fill="#1A1A1A"/>'+
      '<ellipse cx="40" cy="52" rx="3.2" ry="2.4" fill="#1A1A1A"/></svg>'},
    owl:{name:'הינשופה',svg:S+'<circle cx="40" cy="40" r="40" fill="#CDBEEA"/>'+
      '<path d="M18 80V44c0-14 10-24 22-24s22 10 22 24v36z" fill="#6B4E9B"/>'+
      '<path d="M22 24l8 8M58 24l-8 8" stroke="#6B4E9B" stroke-width="6" stroke-linecap="round"/>'+
      '<path d="M28 62c4 4 8 6 12 6s8-2 12-6v18H28z" fill="#E9DFF8"/><path d="M33 68q2 2 4 0M43 68q2 2 4 0M38 74q2 2 4 0" stroke="#B9A6DB" stroke-width="1.4" fill="none"/>'+
      '<circle cx="31" cy="42" r="9" fill="#FFFFFF"/><circle cx="49" cy="42" r="9" fill="#FFFFFF"/>'+
      '<circle cx="31" cy="42" r="4" fill="#1A1A1A"/><circle cx="49" cy="42" r="4" fill="#1A1A1A"/><circle cx="32.4" cy="40.6" r="1.3" fill="#fff"/><circle cx="50.4" cy="40.6" r="1.3" fill="#fff"/>'+
      '<path d="M37 50l3 5 3-5z" fill="#F5A623"/>'+
      '<path d="M22 33c4-4 13-4 16 0M42 33c3-4 12-4 16 0" stroke="#4A356E" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>'},
    robot:{name:'הרובוט',svg:S+'<circle cx="40" cy="40" r="40" fill="#E4E4E2"/>'+
      '<path d="M40 12v8" stroke="#2B2B2B" stroke-width="2.4"/><circle cx="40" cy="11" r="3.2" fill="#2BB5A0"/>'+
      '<path d="M16 80c2-12 11-18 24-18s22 6 24 18z" fill="#2B2B2B"/><rect x="33" y="68" width="14" height="5" rx="2.5" fill="#2BB5A0"/>'+
      '<rect x="36" y="54" width="8" height="9" fill="#5A5A5A"/>'+
      '<rect x="20" y="20" width="40" height="36" rx="10" fill="#2B2B2B"/><rect x="16" y="32" width="5" height="12" rx="2" fill="#5A5A5A"/><rect x="59" y="32" width="5" height="12" rx="2" fill="#5A5A5A"/>'+
      '<rect x="25" y="26" width="30" height="20" rx="6" fill="#123B36"/>'+
      '<rect x="30" y="31" width="6" height="8" rx="3" fill="#2BE0C3"/><rect x="44" y="31" width="6" height="8" rx="3" fill="#2BE0C3"/>'+
      '<path d="M34 51h12" stroke="#2BE0C3" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 2.6"/></svg>'},
    cat:{name:'החתולה',svg:S+'<circle cx="40" cy="40" r="40" fill="#F6B5C6"/>'+
      '<path d="M16 80c3-13 12-20 24-20s21 7 24 20z" fill="#5C5F6A"/>'+
      '<path d="M20 34l2-18 13 10zM60 34l-2-18-13 10z" fill="#5C5F6A"/><path d="M23 30l1-9 6 5zM57 30l-1-9-6 5z" fill="#F6B5C6"/>'+
      '<ellipse cx="40" cy="40" rx="20" ry="18" fill="#6E717D"/>'+
      '<path d="M34 24l1 6M40 22v7M46 24l-1 6" stroke="#4A4C55" stroke-width="2" stroke-linecap="round"/>'+
      '<ellipse cx="32" cy="40" rx="3.6" ry="4.4" fill="#F7D046"/><ellipse cx="48" cy="40" rx="3.6" ry="4.4" fill="#F7D046"/>'+
      '<ellipse cx="32" cy="40" rx="1.3" ry="3.4" fill="#1A1A1A"/><ellipse cx="48" cy="40" rx="1.3" ry="3.4" fill="#1A1A1A"/>'+
      '<path d="M38 47h4l-2 2.4z" fill="#F28FA8"/><path d="M40 49.5v2M40 51.5q-3 2.5-5 0M40 51.5q3 2.5 5 0" stroke="#2B2B2B" stroke-width="1.3" fill="none" stroke-linecap="round"/>'+
      '<path d="M22 47h9M22 51l9-2M58 47h-9M58 51l-9-2" stroke="#D9DAE0" stroke-width="1.1" stroke-linecap="round"/></svg>'},
    panda:{name:'הפנדה',svg:S+'<circle cx="40" cy="40" r="40" fill="#CFE8D4"/>'+
      '<path d="M15 80c3-14 12-20 25-20s22 6 25 20z" fill="#2B2B2B"/><path d="M30 62c3 6 6 9 10 9s7-3 10-9z" fill="#FFFFFF"/>'+
      '<circle cx="22" cy="22" r="8" fill="#2B2B2B"/><circle cx="58" cy="22" r="8" fill="#2B2B2B"/>'+
      '<ellipse cx="40" cy="40" rx="21" ry="19" fill="#FFFFFF"/>'+
      '<ellipse cx="31" cy="39" rx="6" ry="7.5" transform="rotate(-25 31 39)" fill="#2B2B2B"/><ellipse cx="49" cy="39" rx="6" ry="7.5" transform="rotate(25 49 39)" fill="#2B2B2B"/>'+
      '<circle cx="32" cy="39" r="2" fill="#FFFFFF"/><circle cx="48" cy="39" r="2" fill="#FFFFFF"/>'+
      '<ellipse cx="40" cy="48" rx="3.4" ry="2.4" fill="#2B2B2B"/><path d="M36 52q4 3 8 0" stroke="#2B2B2B" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'},
    lion:{name:'האריה',svg:S+'<circle cx="40" cy="40" r="40" fill="#FFF0C2"/>'+
      '<path d="M16 80c3-13 12-19 24-19s21 6 24 19z" fill="#D9932B"/>'+
      '<circle cx="40" cy="40" r="25" fill="#B5651D"/><path d="M40 13l5 6 7-3 1 7 7 1-3 7 6 5-6 4 3 7-7 1-1 7-7-3-5 6-5-6-7 3-1-7-7-1 3-7-6-4 6-5-3-7 7-1 1-7 7 3z" fill="#B5651D"/>'+
      '<circle cx="26" cy="27" r="4.5" fill="#F2B54A"/><circle cx="54" cy="27" r="4.5" fill="#F2B54A"/>'+
      '<ellipse cx="40" cy="42" rx="16" ry="15" fill="#F2B54A"/>'+
      '<circle cx="34" cy="39" r="2.2" fill="#1A1A1A"/><circle cx="46" cy="39" r="2.2" fill="#1A1A1A"/>'+
      '<ellipse cx="40" cy="49" rx="6" ry="4.5" fill="#FBE3B0"/><path d="M37.5 46h5l-2.5 3z" fill="#5A2E12"/>'+
      '<path d="M40 49v2.5M40 51.5q-2.5 2-4.5 0M40 51.5q2.5 2 4.5 0" stroke="#5A2E12" stroke-width="1.3" fill="none" stroke-linecap="round"/></svg>'},
    frog:{name:'הצפרדע',svg:S+'<circle cx="40" cy="40" r="40" fill="#D7EEF7"/>'+
      '<path d="M14 80c3-14 13-21 26-21s23 7 26 21z" fill="#4E9F3D"/><ellipse cx="40" cy="72" rx="13" ry="8" fill="#B8E08A"/>'+
      '<ellipse cx="40" cy="46" rx="24" ry="17" fill="#5DB247"/>'+
      '<circle cx="28" cy="31" r="9" fill="#5DB247"/><circle cx="52" cy="31" r="9" fill="#5DB247"/>'+
      '<circle cx="28" cy="31" r="5.5" fill="#FFFFFF"/><circle cx="52" cy="31" r="5.5" fill="#FFFFFF"/><circle cx="29" cy="32" r="2.6" fill="#1A1A1A"/><circle cx="51" cy="32" r="2.6" fill="#1A1A1A"/>'+
      '<path d="M27 49q13 10 26 0" stroke="#2F6B24" stroke-width="2.4" fill="none" stroke-linecap="round"/>'+
      '<circle cx="24" cy="47" r="3" fill="#F29C9C" opacity=".6"/><circle cx="56" cy="47" r="3" fill="#F29C9C" opacity=".6"/></svg>'},
    bunny:{name:'הארנבת',svg:S+'<circle cx="40" cy="40" r="40" fill="#F9DCE6"/>'+
      '<path d="M16 80c3-13 12-19 24-19s21 6 24 19z" fill="#E7E2EC"/>'+
      '<ellipse cx="31" cy="20" rx="6" ry="15" fill="#F4F1F6"/><ellipse cx="49" cy="20" rx="6" ry="15" fill="#F4F1F6"/>'+
      '<ellipse cx="31" cy="21" rx="2.8" ry="10" fill="#F5A9C0"/><ellipse cx="49" cy="21" rx="2.8" ry="10" fill="#F5A9C0"/>'+
      '<ellipse cx="40" cy="44" rx="18" ry="17" fill="#F4F1F6"/>'+
      '<circle cx="33" cy="42" r="2.3" fill="#1A1A1A"/><circle cx="47" cy="42" r="2.3" fill="#1A1A1A"/>'+
      '<path d="M38 48h4l-2 2.4z" fill="#E86F93"/><path d="M40 50.5v2M40 52.5q-3 2.5-5 0M40 52.5q3 2.5 5 0" stroke="#5A4A5E" stroke-width="1.3" fill="none" stroke-linecap="round"/>'+
      '<rect x="37.5" y="54" width="5" height="4" rx="1" fill="#FFFFFF" stroke="#D8D2DE" stroke-width=".8"/>'+
      '<circle cx="29" cy="48" r="2.6" fill="#F5A9C0" opacity=".6"/><circle cx="51" cy="48" r="2.6" fill="#F5A9C0" opacity=".6"/></svg>'},
    penguin:{name:'הפינגווין',svg:S+'<circle cx="40" cy="40" r="40" fill="#BFE3F2"/>'+
      '<path d="M18 80c0-20 8-33 22-33s22 13 22 33z" fill="#22303C"/><path d="M28 80c0-14 5-24 12-24s12 10 12 24z" fill="#FFFFFF"/>'+
      '<ellipse cx="40" cy="38" rx="19" ry="19" fill="#22303C"/>'+
      '<path d="M26 42c0-8 6-13 14-13s14 5 14 13c0 7-6 11-14 11s-14-4-14-11z" fill="#FFFFFF"/>'+
      '<circle cx="34" cy="39" r="2.3" fill="#1A1A1A"/><circle cx="46" cy="39" r="2.3" fill="#1A1A1A"/>'+
      '<path d="M35 44h10l-5 5z" fill="#F5A623"/>'+
      '<circle cx="30" cy="46" r="2.4" fill="#F7A8B8" opacity=".6"/><circle cx="50" cy="46" r="2.4" fill="#F7A8B8" opacity=".6"/></svg>'},
    koala:{name:'הקואלה',svg:S+'<circle cx="40" cy="40" r="40" fill="#E3EFD9"/>'+
      '<path d="M16 80c3-13 12-19 24-19s21 6 24 19z" fill="#8E96A3"/>'+
      '<circle cx="20" cy="30" r="11" fill="#9AA3AF"/><circle cx="60" cy="30" r="11" fill="#9AA3AF"/><circle cx="20" cy="30" r="6" fill="#E9D7DE"/><circle cx="60" cy="30" r="6" fill="#E9D7DE"/>'+
      '<ellipse cx="40" cy="42" rx="20" ry="18" fill="#AEB6C1"/>'+
      '<circle cx="32" cy="38" r="2.3" fill="#1A1A1A"/><circle cx="48" cy="38" r="2.3" fill="#1A1A1A"/>'+
      '<ellipse cx="40" cy="47" rx="6" ry="7.5" fill="#3B3F47"/><path d="M36 56q4 3 8 0" stroke="#3B3F47" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'},
    scientist:{name:'המדענית',svg:S+'<circle cx="40" cy="40" r="40" fill="#C9E7E1"/>'+
      '<path d="M14 80c2-15 13-22 26-22s24 7 26 22z" fill="#FFFFFF"/><path d="M40 58l-7 22h14z" fill="#3E7CB1"/><path d="M33 58l7 9 7-9" fill="none" stroke="#D3D8DE" stroke-width="1.5"/>'+
      '<rect x="34" y="48" width="12" height="12" rx="5" fill="#C98E62"/>'+
      '<circle cx="26" cy="30" r="9" fill="#2A1B12"/><circle cx="54" cy="30" r="9" fill="#2A1B12"/><circle cx="40" cy="22" r="12" fill="#2A1B12"/><circle cx="24" cy="42" r="7" fill="#2A1B12"/><circle cx="56" cy="42" r="7" fill="#2A1B12"/>'+
      '<ellipse cx="40" cy="39" rx="13" ry="15" fill="#D9A27A"/>'+
      '<circle cx="34" cy="38" r="5" fill="none" stroke="#2C2C2C" stroke-width="1.8"/><circle cx="46" cy="38" r="5" fill="none" stroke="#2C2C2C" stroke-width="1.8"/><path d="M39 38h2" stroke="#2C2C2C" stroke-width="1.8"/>'+
      '<circle cx="34" cy="38" r="1.8" fill="#1A1A1A"/><circle cx="46" cy="38" r="1.8" fill="#1A1A1A"/>'+
      '<path d="M35 46q5 4 10 0" stroke="#1A1A1A" stroke-width="2" fill="none" stroke-linecap="round"/></svg>'},
    artist:{name:'האמן',svg:S+'<circle cx="40" cy="40" r="40" fill="#FFD9C9"/>'+
      '<path d="M14 80c2-15 13-22 26-22s24 7 26 22z" fill="#2E3A59"/><path d="M28 64q12 8 24 0" stroke="#F2C14E" stroke-width="5" fill="none" stroke-linecap="round"/>'+
      '<rect x="34" y="48" width="12" height="12" rx="5" fill="#8C5A3C"/>'+
      '<ellipse cx="40" cy="39" rx="13" ry="15" fill="#A86B47"/>'+
      '<path d="M24 30c2-9 9-13 16-13s16 3 18 9c-4-2-9-3-14-3-8 0-15 3-20 7z" fill="#1F1F1F"/>'+
      '<path d="M22 27c3-8 12-12 22-11 9 1 15 5 15 9-5-2-12-2-19-1-7 1-13 2-18 3z" fill="#D7263D"/><circle cx="44" cy="15" r="2.5" fill="#D7263D"/>'+
      '<circle cx="35" cy="39" r="2" fill="#1A1A1A"/><circle cx="45" cy="39" r="2" fill="#1A1A1A"/>'+
      '<path d="M34 47c2 1 4 1 6 0 2 1 4 1 6 0" stroke="#3B2416" stroke-width="2.2" fill="none" stroke-linecap="round"/>'+
      '<path d="M36 51q4 3 8 0" stroke="#1A1A1A" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>'}

  };
  window.URIQ_AVATARS=A;
  window.URIQ_AVATAR_ORDER=['explorer','professor','buddy','astro','scientist','artist','fox','owl','robot','cat','panda','lion','frog','bunny','penguin','koala'];
})();

/* ---- avatar looks: hats, glasses, backgrounds, frames, items and effects layered on any avatar.
   Every piece is an original drawing; most unlock with progress (sets submitted, perfect sets…). ---- */
(function(){
  var A=window.URIQ_AVATARS||{}, uid=0;
  // per avatar: [y where a hat sits, head width, eye line y, half distance between the eyes]
  var ANC={explorer:[24,28,38,5],professor:[24,30,38,6],buddy:[24,28,39,5.5],astro:[17,34,38,4.5],scientist:[19,34,37,6],artist:[21,26,39,5],
    fox:[25,32,38,8],owl:[24,34,40,9],robot:[21,38,35,7],cat:[26,36,40,8],panda:[25,36,39,8],lion:[23,38,39,6],frog:[25,40,31,11],
    bunny:[29,26,41,7],penguin:[23,30,39,6],koala:[26,36,37,8]};
  function star(cx,cy,r,f){ var p='',k; for(k=0;k<10;k++){ var a=Math.PI/5*k-Math.PI/2, rr=k%2?r*.45:r; p+=(k?'L':'M')+(cx+rr*Math.cos(a)).toFixed(2)+' '+(cy+rr*Math.sin(a)).toFixed(2); } return '<path d="'+p+'Z" fill="'+f+'"/>'; }
  function heart(cx,cy,s,f){ return '<path transform="translate('+cx+' '+cy+') scale('+s+')" d="M0 3.2C-1.5 1.8-4 .2-4-1.8-4-3.4-2.8-4.4-1.6-4.4-.8-4.4-.2-3.9 0-3.4.2-3.9.8-4.4 1.6-4.4 2.8-4.4 4-3.4 4-1.8 4 .2 1.5 1.8 0 3.2z" fill="'+f+'"/>'; }
  function spark(cx,cy,s,f){ return '<path transform="translate('+cx+' '+cy+') scale('+s+')" d="M0-4C.5-1 1-.5 4 0 1 .5.5 1 0 4-.5 1-1 .5-4 0-1-.5-.5-1 0-4z" fill="'+f+'"/>'; }

  // hats are drawn around (0,0) = the middle of the head line, 30 units wide
  var HATS={
    cap:'<path d="M-15 1C-15-15 15-15 15 1z" fill="#2B59C3"/><path d="M4 0h17a3 3 0 0 1 0 5H4z" fill="#1C3D8C"/><circle cy="-13" r="2" fill="#1C3D8C"/>',
    beanie:'<path d="M-15 1C-15-17 15-17 15 1z" fill="#E4572E"/><path d="M-9-11v10M-3-13v12M3-13v12M9-11v10" stroke="#C2410C" stroke-width="1.4"/><rect x="-16.5" y="-3" width="33" height="7" rx="3.5" fill="#F7B267"/><circle cy="-17" r="4.5" fill="#FFF3E0"/>',
    party:'<path d="M-11 1L0-28 11 1z" fill="#7B61FF"/><path d="M-7-9L4-20M-9-1L7-16M-3 0L10-11" stroke="#FFD166" stroke-width="2.2"/><circle cy="-29" r="3.6" fill="#FF5C8A"/>',
    grad:'<rect x="-12" y="-7" width="24" height="8" rx="1.5" fill="#1F2937"/><path d="M-22-9L0-17 22-9 0-1z" fill="#111827"/><path d="M0-9L14-7v9" stroke="#FBBF24" stroke-width="1.4" fill="none"/><rect x="12" y="1" width="4" height="6" rx="1" fill="#FBBF24"/>',
    headphones:'<path d="M-18 6C-18-22 18-22 18 6" stroke="#111827" stroke-width="4" fill="none" stroke-linecap="round"/><rect x="-23" y="0" width="9" height="14" rx="4" fill="#EF4444"/><rect x="14" y="0" width="9" height="14" rx="4" fill="#EF4444"/>',
    wizard:'<path d="M-15 1L5-33 16 1z" fill="#4C1D95"/><ellipse cy="1" rx="21" ry="4.5" fill="#5B21B6"/>'+star(1,-13,4,'#FDE047')+star(-6,-4,2.4,'#FDE047'),
    crown:'<path d="M-15 1V-13L-7.5-5 0-17 7.5-5 15-13V1z" fill="#FBBF24" stroke="#B45309" stroke-width="1.2" stroke-linejoin="round"/><circle cx="0" cy="-5" r="2.4" fill="#EF4444"/><circle cx="-9" cy="-3" r="1.7" fill="#3B82F6"/><circle cx="9" cy="-3" r="1.7" fill="#10B981"/>',
    viking:'<path d="M-15 1C-15-15 15-15 15 1z" fill="#9CA3AF"/><rect x="-16" y="-3" width="32" height="5" rx="2" fill="#6B7280"/><path d="M-14-6C-22-8-24-18-21-24-19-17-15-14-11-12z" fill="#FFF7E6"/><path d="M14-6C22-8 24-18 21-24 19-17 15-14 11-12z" fill="#FFF7E6"/>'
  };
  function glasses(t,y,dx){
    var r=Math.max(3.4,Math.min(6.4,dx*.78)), L=40-dx, R=40+dx, k='#111827';
    if(t==='round') return '<g fill="none" stroke="'+k+'" stroke-width="1.6"><circle cx="'+L+'" cy="'+y+'" r="'+r+'"/><circle cx="'+R+'" cy="'+y+'" r="'+r+'"/><path d="M'+(L+r)+' '+y+'H'+(R-r)+'"/></g>';
    if(t==='sun') return '<g><rect x="'+(L-r-.6)+'" y="'+(y-r*.8)+'" width="'+(2*r+1.2)+'" height="'+(r*1.6)+'" rx="'+(r*.6)+'" fill="#111827"/><rect x="'+(R-r-.6)+'" y="'+(y-r*.8)+'" width="'+(2*r+1.2)+'" height="'+(r*1.6)+'" rx="'+(r*.6)+'" fill="#111827"/><path d="M'+(L+r)+' '+(y-1)+'H'+(R-r)+'" stroke="#111827" stroke-width="1.6"/><path d="M'+(L-r*.5)+' '+(y-r*.3)+'l'+r*.6+' -'+r*.3+'M'+(R-r*.5)+' '+(y-r*.3)+'l'+r*.6+' -'+r*.3+'" stroke="#fff" stroke-width="1" opacity=".7"/></g>';
    if(t==='star') return '<g>'+star(L,y,r*1.35,'#FACC15')+star(R,y,r*1.35,'#FACC15')+'<path d="M'+(L+r)+' '+y+'H'+(R-r)+'" stroke="#CA8A04" stroke-width="1.4"/></g>';
    if(t==='heart') return '<g>'+heart(L,y,r*.34,'#F43F5E')+heart(R,y,r*.34,'#F43F5E')+'<path d="M'+(L+r)+' '+y+'H'+(R-r)+'" stroke="#BE123C" stroke-width="1.4"/></g>';
    if(t==='3d') return '<g stroke="#111827" stroke-width="1.4"><rect x="'+(L-r)+'" y="'+(y-r*.75)+'" width="'+2*r+'" height="'+r*1.5+'" fill="#EF4444" fill-opacity=".75"/><rect x="'+(R-r)+'" y="'+(y-r*.75)+'" width="'+2*r+'" height="'+r*1.5+'" fill="#06B6D4" fill-opacity=".75"/><path d="M'+(L+r)+' '+y+'H'+(R-r)+'" fill="none"/></g>';
    if(t==='monocle') return '<g fill="none" stroke="#B45309" stroke-width="1.8"><circle cx="'+R+'" cy="'+y+'" r="'+(r+.6)+'"/><path d="M'+(R+r)+' '+(y+1)+'C'+(R+r+4)+' '+(y+8)+' '+(R+2)+' '+(y+14)+' '+(R+6)+' '+(y+20)+'" stroke-width="1"/></g>';
    return '';
  }
  // backgrounds: [fill, extra drawing inside the circle]
  function bg(t,u){
    var g=function(a,b){ return '<linearGradient id="g'+u+'" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="'+a+'"/><stop offset="1" stop-color="'+b+'"/></linearGradient>'; };
    switch(t){
      case 'sunset': return [g('#FDBA74','#F43F5E'),'url(#g'+u+')',''];
      case 'ocean': return [g('#67E8F9','#2563EB'),'url(#g'+u+')',''];
      case 'mint': return [g('#D9F99D','#34D399'),'url(#g'+u+')',''];
      case 'grape': return [g('#E9D5FF','#7C3AED'),'url(#g'+u+')',''];
      case 'paper': { var l=''; for(var i=8;i<80;i+=8) l+='<path d="M'+i+' 0V80M0 '+i+'H80" stroke="#93C5FD" stroke-width=".5"/>'; return ['','#F8FAFC',l+'<text x="10" y="22" font-size="7" fill="#60A5FA" font-family="serif">π</text><text x="62" y="70" font-size="6" fill="#60A5FA">√x</text>']; }
      case 'night': return [g('#1E1B4B','#0F172A'),'url(#g'+u+')',spark(12,20,1,'#FDE68A')+spark(66,14,.8,'#fff')+spark(70,40,1.1,'#FDE68A')+spark(9,52,.7,'#fff')+'<circle cx="62" cy="62" r=".9" fill="#fff"/><circle cx="20" cy="9" r=".7" fill="#fff"/>'];
      case 'confetti': { var c=['#F43F5E','#FACC15','#22C55E','#3B82F6','#A855F7'], pts=[[10,18],[24,8],[58,10],[70,24],[8,44],[72,50],[14,66],[66,70],[34,4],[48,6]], s=''; pts.forEach(function(p,i){ s+='<rect x="'+p[0]+'" y="'+p[1]+'" width="4" height="2" rx=".8" fill="'+c[i%5]+'" transform="rotate('+(i*37%90)+' '+p[0]+' '+p[1]+')"/>'; }); return ['','#FFF7ED',s]; }
      case 'rainbow': return ['<linearGradient id="g'+u+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F87171"/><stop offset=".25" stop-color="#FBBF24"/><stop offset=".5" stop-color="#4ADE80"/><stop offset=".75" stop-color="#60A5FA"/><stop offset="1" stop-color="#A78BFA"/></linearGradient>','url(#g'+u+')',''];
    }
    return null;
  }
  function frame(t,u){
    if(t==='gold') return '<linearGradient id="f'+u+'" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FDE68A"/><stop offset=".5" stop-color="#D97706"/><stop offset="1" stop-color="#FDE68A"/></linearGradient>|<circle cx="40" cy="40" r="38.3" fill="none" stroke="url(#f'+u+')" stroke-width="3.4"/>';
    if(t==='rainbow') return '<linearGradient id="f'+u+'" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F43F5E"/><stop offset=".3" stop-color="#FACC15"/><stop offset=".6" stop-color="#22C55E"/><stop offset="1" stop-color="#6366F1"/></linearGradient>|<circle cx="40" cy="40" r="38.3" fill="none" stroke="url(#f'+u+')" stroke-width="3.4"/>';
    if(t==='neon') return '|<circle cx="40" cy="40" r="38" fill="none" stroke="#22FF9A" stroke-width="2.6"/><circle cx="40" cy="40" r="35.6" fill="none" stroke="#22FF9A" stroke-width=".8" opacity=".6"/>';
    if(t==='dashed') return '|<circle cx="40" cy="40" r="38" fill="none" stroke="#fff" stroke-width="2.4" stroke-dasharray="4 3"/>';
    return '|';
  }
  // items sit in a badge at the bottom right
  var ITEMS={
    pencil:'<path d="M-6 6L4-4l3 3L-3 9H-6z" fill="#FBBF24"/><path d="M4-4l2-2 3 3-2 2z" fill="#F472B6"/><path d="M-6 6v3h3z" fill="#1F2937"/>',
    star:star(0,0,7,'#FACC15'),
    heart:heart(0,.5,1.6,'#F43F5E'),
    bolt:'<path d="M2-8L-5 1h4l-2 8 7-10H0z" fill="#F59E0B"/>',
    trophy:'<path d="M-5-7h10v5a5 5 0 0 1-10 0z" fill="#FBBF24"/><path d="M-5-5h-3a3 3 0 0 0 3 5M5-5h3a3 3 0 0 1-3 5" stroke="#FBBF24" stroke-width="1.6" fill="none"/><rect x="-1.4" y="2" width="2.8" height="3" fill="#D97706"/><rect x="-4.5" y="5" width="9" height="2.6" rx="1" fill="#92400E"/>',
    pi:'<text x="0" y="5" text-anchor="middle" font-size="15" font-family="Georgia,serif" font-weight="700" fill="#2563EB">π</text>',
    rocket:'<path d="M0-9C4-6 5-1 4 4h-8C-5-1-4-6 0-9z" fill="#E5E7EB" stroke="#6B7280" stroke-width=".8"/><circle cy="-3" r="1.8" fill="#3B82F6"/><path d="M-4 1l-3 4h3M4 1l3 4H4" fill="#EF4444"/><path d="M-2 4.5L0 9 2 4.5z" fill="#F97316"/>',
    calc:'<rect x="-6" y="-8" width="12" height="16" rx="2" fill="#374151"/><rect x="-4" y="-6" width="8" height="4" rx="1" fill="#A7F3D0"/><g fill="#F9FAFB"><circle cx="-2.5" cy="1" r="1.1"/><circle cx="2.5" cy="1" r="1.1"/><circle cx="-2.5" cy="5" r="1.1"/><circle cx="2.5" cy="5" r="1.1"/></g>'
  };
  function fx(t){
    if(t==='sparkles') return spark(13,15,1.3,'#FDE047')+spark(67,12,1,'#fff')+spark(71,34,.8,'#FDE047')+spark(9,36,.8,'#fff');
    if(t==='hearts') return heart(13,16,.9,'#FB7185')+heart(68,14,.7,'#F43F5E')+heart(71,32,.55,'#FB7185');
    if(t==='math') return '<g font-family="Georgia,serif" font-weight="700" fill="#fff" opacity=".9" stroke="#1F2937" stroke-width=".35"><text x="7" y="20" font-size="9">π</text><text x="64" y="17" font-size="8">√</text><text x="68" y="38" font-size="7">∞</text><text x="5" y="40" font-size="7">Σ</text></g>';
    if(t==='bubbles') return '<g fill="none" stroke="#fff" stroke-width=".9" opacity=".9"><circle cx="12" cy="18" r="3"/><circle cx="18" cy="10" r="1.8"/><circle cx="67" cy="15" r="2.6"/><circle cx="71" cy="30" r="1.6"/></g>';
    return '';
  }

  /* the catalogue: category → items. req = what unlocks it ({k: stat, n: amount}); none = free */
  var CATS=[
    {k:'hat',name:'כובעים',items:[['','בלי'],['cap','כובע מצחייה'],['beanie','כובע צמר'],['party','כובע מסיבה',{k:'subs',n:1}],['headphones','אוזניות',{k:'subs',n:3}],['grad','כובע סיום',{k:'subs',n:5}],['viking','קסדת ויקינג',{k:'correct',n:100}],['wizard','כובע קוסם',{k:'perfect',n:1}],['crown','כתר',{k:'subs',n:20}]]},
    {k:'eyes',name:'משקפיים',items:[['','בלי'],['round','עגולים'],['sun','משקפי שמש'],['star','כוכבים',{k:'subs',n:2}],['heart','לבבות',{k:'correct',n:50}],['3d','תלת־ממד',{k:'imp',n:1}],['monocle','מונוקל',{k:'correct',n:200}]]},
    {k:'bg',name:'רקעים',items:[['','מקורי'],['sunset','שקיעה'],['ocean','ים'],['mint','מנטה'],['paper','מחברת חשבון',{k:'subs',n:3}],['grape','ענבים',{k:'subs',n:5}],['night','לילה',{k:'subs',n:10}],['confetti','קונפטי',{k:'perfect',n:1}],['rainbow','קשת',{k:'subs',n:25}]]},
    {k:'frame',name:'מסגרות',items:[['','בלי'],['dashed','מקווקוות'],['gold','זהב',{k:'subs',n:5}],['neon','ניאון',{k:'extra',n:1}],['rainbow','קשת',{k:'perfect',n:2}]]},
    {k:'item',name:'אביזרים',items:[['','בלי'],['pencil','עיפרון'],['heart','לב'],['star','כוכב',{k:'subs',n:1}],['calc','מחשבון',{k:'correct',n:30}],['bolt','ברק',{k:'imp',n:1}],['pi','פאי',{k:'correct',n:150}],['rocket','חללית',{k:'extra',n:3}],['trophy','גביע',{k:'perfect',n:1}]]},
    {k:'fx',name:'אפקטים',items:[['','בלי'],['bubbles','בועות'],['sparkles','נצנצים',{k:'subs',n:3}],['hearts','לבבות',{k:'correct',n:75}],['math','סמלי מתמטיקה',{k:'subs',n:8}]]}
  ];
  var REQ={subs:function(n){ return n===1?'הגישו מקבץ ראשון':'הגישו '+n+' מקבצים'; }, correct:function(n){ return n+' תשובות נכונות'; },
    perfect:function(n){ return n===1?'מקבץ אחד בלי טעויות':n+' מקבצים בלי טעויות'; }, imp:function(n){ return n===1?'הגישו מקבץ לשיפור':'הגישו '+n+' מקבצים לשיפור'; },
    extra:function(n){ return n===1?'הגישו מקבץ נוסף':'הגישו '+n+' מקבצים נוספים'; }};

  function render(id,look){
    var av=A[id]; if(!av) return '';
    look=look||{}; var u=++uid, S0='<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">';
    var inner=av.svg.slice(av.svg.indexOf('>')+1,av.svg.lastIndexOf('</svg>')), defs='', out='';
    var b=look.bg&&bg(look.bg,u);
    if(b){ defs+=b[0]; inner=inner.replace(/^<circle cx="40" cy="40" r="40" fill="[^"]*"\/>/,''); out+='<clipPath id="c'+u+'"><circle cx="40" cy="40" r="40"/></clipPath><circle cx="40" cy="40" r="40" fill="'+b[1]+'"/><g clip-path="url(#c'+u+')">'+b[2]+'</g>'; }
    out+=inner;
    var a=ANC[id]||[22,30,38,6];
    if(look.eyes) out+=glasses(look.eyes,a[2],a[3]);
    if(look.hat&&HATS[look.hat]) out+='<g transform="translate(40 '+a[0]+') scale('+(a[1]/30).toFixed(3)+')">'+HATS[look.hat]+'</g>';
    if(look.fx) out+=fx(look.fx);
    var fr=frame(look.frame,u).split('|'); defs+=fr[0]; out+=fr[1];
    if(look.item&&ITEMS[look.item]) out+='<g transform="translate(64 64)"><circle r="11" fill="#fff" stroke="#E5E7EB" stroke-width="1"/>'+ITEMS[look.item]+'</g>';
    return S0+(defs?'<defs>'+defs+'</defs>':'')+out+'</svg>';
  }
  window.URIQ_LOOK={render:render,cats:CATS,req:REQ};
})();
