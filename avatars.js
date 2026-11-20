/* Uri Q profile avatars: original flat illustrations, 80×80, one accent colour each. */
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
      '<path d="M22 47h9M22 51l9-2M58 47h-9M58 51l-9-2" stroke="#D9DAE0" stroke-width="1.1" stroke-linecap="round"/></svg>'}
  };
  window.URIQ_AVATARS=A;
  window.URIQ_AVATAR_ORDER=['explorer','professor','buddy','astro','fox','owl','robot','cat'];
})();
