(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
  };
  const MINT = '126 224 181';

  /* ───────── Progress & achievements ───────── */
  const ACH = {
    explorer: ['Explorer', 'Visited every page'],
    curious: ['Curious', 'Looked at every project'],
    cheat: ['Old habits', 'Entered the Konami code'],
    boost: ['Afterburner', 'Maxed out the trail boost'],
  };
  const PAGES = ['home', 'about', 'projects', 'contact'];
  const st = Object.assign({ pages: [], projects: [], got: [] }, store.get('km-progress', {}));
  const save = () => store.set('km-progress', st);

  const toastWrap = document.createElement('div');
  toastWrap.className = 'toast-wrap';
  toastWrap.setAttribute('role', 'status');
  document.body.appendChild(toastWrap);
  const queue = [];
  let showing = false;
  const nextToast = () => {
    if (showing || !queue.length) return;
    showing = true;
    const [name, desc] = queue.shift();
    const t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = '<span class="toast-k">Achievement unlocked</span><strong></strong><span></span>';
    t.children[1].textContent = name;
    t.children[2].textContent = desc;
    toastWrap.appendChild(t);
    setTimeout(() => t.classList.add('out'), 3200);
    setTimeout(() => { t.remove(); showing = false; nextToast(); }, 3550);
  };
  const unlock = id => {
    if (st.got.includes(id)) return;
    st.got.push(id); save();
    queue.push(ACH[id]); nextToast();
  };
  const track = (list, val, total, id) => {
    if (!st[list].includes(val)) { st[list].push(val); save(); }
    if (st[list].length >= total) unlock(id);
  };

  // Pages explored → footer pips
  const page = document.body.dataset.page;
  if (page) track('pages', page, PAGES.length, 'explorer');
  const pips = document.querySelector('.explored');
  if (pips) {
    const seen = PAGES.filter(p => st.pages.includes(p)).length;
    pips.innerHTML = '<span>Explored</span>' + PAGES.map(p =>
      `<span class="pip${st.pages.includes(p) ? ' on' : ''}" aria-hidden="true"></span>`).join('') +
      `<span class="pip-count">${seen}/${PAGES.length}</span>`;
    pips.setAttribute('aria-label', `Explored ${seen} of ${PAGES.length} pages`);
  }

  // Projects looked at
  document.querySelectorAll('[data-project]').forEach(el => {
    const mark = () => track('projects', el.dataset.project, 4, 'curious');
    el.addEventListener('pointerenter', mark);
    el.addEventListener('focusin', mark);
  });

  /* ───────── Mouse trail + click bursts ─────────
     A follower point eases toward the tail of the cursor arrow, so the trail
     draws smooth curves instead of copying every jitter of the hand. Moving
     fast builds "boost": the trail grows longer and brighter and sheds sparks. */
  const fx = document.createElement('canvas');
  fx.className = 'fx';
  fx.setAttribute('aria-hidden', 'true');
  fx.hidden = true; // only shown while something is animating
  document.body.appendChild(fx);
  const g = fx.getContext('2d');
  let W = 0, H = 0, raf = 0, pts = [], parts = [];
  const TAIL_X = 7, TAIL_Y = 17;      // offset from the pointer hotspot to the arrow's tail
  const EASE = .32;                   // follower easing per 60fps frame (lower = smoother, more lag)
  let tx = 0, ty = 0, fxp = 0, fyp = 0, active = false, lastMove = 0, prev = 0, boost = 0;

  const resize = () => {
    const r = Math.min(devicePixelRatio || 1, 2);
    W = innerWidth; H = innerHeight;
    fx.width = W * r; fx.height = H * r;
    g.setTransform(r, 0, 0, r, 0, 0);
  };
  // Chaikin corner-cutting: turns the raw pointer path into a smooth curve
  const smooth = a => {
    if (a.length < 3) return a;
    const o = [a[0]];
    for (let i = 0; i < a.length - 1; i++) {
      const p = a[i], q = a[i + 1];
      o.push({ x: p.x * .75 + q.x * .25, y: p.y * .75 + q.y * .25 },
             { x: p.x * .25 + q.x * .75, y: p.y * .25 + q.y * .75 });
    }
    o.push(a[a.length - 1]);
    return o;
  };
  const ribbon = now => {
    pts = pts.filter(p => now - p.t < 240 + boost * 360);   // longer trail at speed
    if (pts.length < 3) return;
    const WIDTH = 2.6 + boost * 2;
    // the head is pinned to the real cursor tail; the eased history forms the body
    const raw = active ? pts.concat({ x: tx, y: ty }) : pts;
    const c = smooth(smooth(smooth(raw))), n = c.length, L = [], R = [];
    for (let i = 0; i < n; i++) {
      const a = c[Math.max(i - 1, 0)], b = c[Math.min(i + 1, n - 1)];
      let tx = b.x - a.x, ty = b.y - a.y;
      const d = Math.hypot(tx, ty) || 1;
      tx /= d; ty /= d;
      const w = WIDTH * (i / (n - 1)) / 2; // tapers to nothing at the tail
      L.push([c[i].x - ty * w, c[i].y + tx * w]);
      R.push([c[i].x + ty * w, c[i].y - tx * w]);
    }
    const head = c[n - 1];
    g.beginPath();
    g.moveTo(L[0][0], L[0][1]);
    for (let i = 1; i < n; i++) g.lineTo(L[i][0], L[i][1]);
    g.arc(head.x, head.y, WIDTH / 2, 0, Math.PI * 2);
    for (let i = n - 1; i >= 0; i--) g.lineTo(R[i][0], R[i][1]);
    g.closePath();
    // mint → near-white as boost builds
    const col = [126 + 104 * boost, 224 + 28 * boost, 181 + 61 * boost].map(Math.round).join(' ');
    g.shadowColor = `rgb(${MINT} / ${.5 + boost * .4})`;
    g.shadowBlur = 8 + boost * 10;
    g.fillStyle = `rgb(${col} / ${.65 + boost * .25})`;
    g.fill();
    g.shadowBlur = 0;
  };
  const step = now => {
    const dt = Math.min(now - (prev || now), 50) || 16.7;
    prev = now;
    if (!active) { boost *= .9; return; }
    const k = 1 - Math.pow(1 - EASE, dt / 16.7);            // frame-rate independent easing
    const ox = fxp, oy = fyp;
    fxp += (tx - fxp) * k; fyp += (ty - fyp) * k;
    const moved = Math.hypot(fxp - ox, fyp - oy);
    boost += (Math.min(moved / dt / 2.2, 1) - boost) * .08;   // ~2.2 px/ms = full boost
    if (moved > .25) pts.push({ x: fxp, y: fyp, t: now });
    if (pts.length > 120) pts.splice(0, pts.length - 120);
    if (boost > .55 && Math.random() < boost * .45 && pts.length > 4) {  // sparks off the tail
      const p = pts[Math.floor(pts.length * .3)];
      parts.push({ x: p.x, y: p.y, vx: (Math.random() - .5) * 1.2, vy: .4 + Math.random(), g: .03, t: now, life: 420 });
    }
    if (boost > .9) unlock('boost');
    if (now - lastMove > 600 && moved < .1) active = false;
  };
  const frame = () => {
    const now = performance.now();
    g.clearRect(0, 0, W, H);
    step(now);
    ribbon(now);
    parts = parts.filter(p => now - p.t < p.life);
    for (const p of parts) {
      const k = (now - p.t) / p.life, a = Math.ceil((1 - k) * 4) / 4; // stepped pixel fade
      p.x += p.vx; p.y += p.vy; p.vx *= .94; p.vy = p.vy * .94 + p.g;
      g.fillStyle = `rgb(${MINT} / ${a * .8})`;
      g.fillRect(Math.round(p.x / 3) * 3 - 2, Math.round(p.y / 3) * 3 - 2, 4, 4);
    }
    if (active || pts.length > 2 || parts.length) raf = requestAnimationFrame(frame);
    else { raf = 0; prev = 0; pts = []; g.clearRect(0, 0, W, H); fx.hidden = true; }
  };
  const kick = () => { if (!raf) { fx.hidden = false; raf = requestAnimationFrame(frame); } };
  const burst = (x, y, n, speed, life, grav) => {
    const t = performance.now();
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2 + Math.random() * .6, v = speed * (.6 + Math.random() * .6);
      parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v - grav * 20, g: grav, t, life });
    }
    kick();
  };

  if (!reduced) {
    resize();
    addEventListener('resize', resize);
    addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse') return;
      tx = e.clientX + TAIL_X; ty = e.clientY + TAIL_Y;
      if (!active && pts.length < 3) { fxp = tx; fyp = ty; } // start fresh at the cursor
      active = true; lastMove = performance.now();
      kick();
    }, { passive: true });
    document.documentElement.addEventListener('pointerleave', () => { active = false; });
    addEventListener('pointerdown', e => burst(e.clientX, e.clientY, 7, 2.4, 520, 0), { passive: true });
  }

  /* ───────── Pixel page transitions ─────────
     Leaving: blocks fill the screen left → right (with a mint leading edge).
     Arriving: the head script hides the page, then the blocks dissolve away. */
  const root = document.documentElement;
  const TILE = 28;
  const BG = getComputedStyle(root).getPropertyValue('--bg').trim() || '#0f1119';
  let leaving = false;

  const cover = () => {
    const c = document.createElement('canvas');
    c.className = 'pt';
    c.setAttribute('aria-hidden', 'true');
    const r = Math.min(devicePixelRatio || 1, 2);
    c.width = innerWidth * r; c.height = innerHeight * r;
    const x = c.getContext('2d');
    x.setTransform(r, 0, 0, r, 0, 0);
    document.body.appendChild(c);
    const cols = Math.ceil(innerWidth / TILE), rows = Math.ceil(innerHeight / TILE), tiles = [];
    for (let ty = 0; ty < rows; ty++)
      for (let tx2 = 0; tx2 < cols; tx2++) tiles.push({ x: tx2 * TILE, y: ty * TILE, o: (tx2 / cols) * .65 + Math.random() * .35 });
    return { c, x, tiles };
  };
  const animate = (dur, draw, done) => {
    const t0 = performance.now();
    const f = now => {
      const k = Math.min((now - t0) / dur, 1);
      draw(k);
      if (k < 1) requestAnimationFrame(f); else if (done) done();
    };
    requestAnimationFrame(f);
  };
  const paint = (s, k, showing) => {   // showing: tile is drawn when true
    s.x.clearRect(0, 0, innerWidth, innerHeight);
    for (const t of s.tiles) {
      const on = showing(t, k);
      if (!on) continue;
      s.x.fillStyle = BG;
      s.x.fillRect(t.x, t.y, TILE + 1, TILE + 1);   // +1 hides hairline seams
      if (Math.abs(k - t.o) < .05) {                 // glowing leading edge
        s.x.fillStyle = `rgb(${MINT} / .35)`;
        s.x.fillRect(t.x, t.y, TILE + 1, TILE + 1);
      }
    }
  };

  const go = url => {
    if (leaving) return;
    leaving = true;
    if (reduced) { location.href = url; return; }
    try { sessionStorage.setItem('km-pt', '1'); } catch (e) {}
    const s = cover();
    animate(300, k => paint(s, k, t => t.o <= k), () => { location.href = url; });
    setTimeout(() => { location.href = url; }, 900); // in case animation frames are throttled
  };

  document.addEventListener('click', e => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest && e.target.closest('a[href]');
    if (!a || a.target || a.hasAttribute('download')) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return;                 // external, mailto, etc.
    if (url.pathname === location.pathname) {
      if (!url.hash) e.preventDefault();                        // already here
      return;                                                   // same-page anchors behave normally
    }
    e.preventDefault();
    go(url.href);
  });

  if (root.classList.contains('pt-in')) {
    const s = cover();
    const draw = k => paint(s, k, t => t.o > k);
    draw(0);
    root.classList.remove('pt-in');
    animate(340, draw, () => s.c.remove());
  }
  addEventListener('pageshow', e => {           // coming back via the back button
    if (!e.persisted) return;
    leaving = false;
    root.classList.remove('pt-in');
    document.querySelectorAll('.pt').forEach(c => c.remove());
  });

  /* ───────── Keyboard controls + Konami code ─────────
     ↑ ↓ select a project / link row · Enter opens it · ← → switch pages */
  const PAGE_URL = { home: '/', about: '/about', projects: '/projects', contact: '/contact' };
  const items = [...document.querySelectorAll('main .row, main .facts > div')]
    .filter(el => el.matches('.row') || el.querySelector('a'));
  items.forEach(el => { if (!el.matches('a, [tabindex]')) el.tabIndex = -1; });
  let sel = -1;
  const clearSel = () => { items.forEach(el => el.classList.remove('is-sel')); sel = -1; };
  const select = i => {
    clearSel();
    sel = i;
    const el = items[i];
    el.classList.add('is-sel');
    el.focus({ preventScroll: true });
    el.scrollIntoView({ block: 'nearest', behavior: reduced ? 'auto' : 'smooth' });
  };
  addEventListener('pointermove', e => { if (sel >= 0 && e.pointerType === 'mouse') clearSel(); }, { passive: true });

  const KONAMI = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
  const keys = [];
  // length of the longest Konami prefix that the most recent keys spell out
  const konamiProgress = () => {
    for (let L = Math.min(keys.length, KONAMI.length); L > 0; L--) {
      if (keys.slice(-L).every((k, i) => k === KONAMI[i])) return L;
    }
    return 0;
  };
  addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey || e.defaultPrevented) return;
    if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable]')) return;

    const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    keys.push(k);
    if (keys.length > KONAMI.length) keys.shift();
    const kpos = konamiProgress();
    if (kpos === KONAMI.length) {
      keys.length = 0;
      if (!reduced) burst(innerWidth / 2, innerHeight / 3, 48, 7, 1600, .12);
      unlock('cheat');
      return;
    }

    if ((k === 'ArrowDown' || k === 'ArrowUp') && items.length) {
      e.preventDefault();
      const d = k === 'ArrowDown' ? 1 : -1;
      select(sel < 0 ? (d > 0 ? 0 : items.length - 1) : (sel + d + items.length) % items.length);
    } else if (k === 'Enter' && sel >= 0 && document.activeElement === items[sel] && !items[sel].matches('a')) {
      const link = items[sel].querySelector('a');
      if (link) { e.preventDefault(); link.click(); }
    } else if ((k === 'ArrowLeft' || k === 'ArrowRight') && page && PAGE_URL[page] && !(kpos >= 5 && kpos <= 8)) {
      e.preventDefault();
      const i = PAGES.indexOf(page), n = PAGES.length;
      go(new URL(PAGE_URL[PAGES[(i + (k === 'ArrowRight' ? 1 : -1) + n) % n]], location.href).href);
    }
  });
})();

// A small hello for anyone who opens the console.
console.log(
  '%cKRITIN MUTYAM%c\nThanks for looking under the hood. This site is hand-written HTML, CSS, and JS.\nTry the Konami code. More of my work: %chttps://github.com/kritin29',
  'font: 20px Silkscreen, monospace; color: #7ee0b5; padding: 4px 0;',
  'font: 13px/1.6 "IBM Plex Mono", monospace; color: #7f87a8;',
  'font: 13px/1.6 "IBM Plex Mono", monospace; color: #7ee0b5;'
);
