"""Generates every page from tools/content.py with a shared head, header and footer.

Run from the repo root:   python tools/build.py
Outputs: index, about, software, games, contact, 404, and software/<slug>.html for each entry.
"""
import os, sys
from html import escape as esc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mutyamkritin.com"
EMAIL = "mutyam@wisc.edu"
GITHUB = "https://github.com/kritin29"
LINKEDIN = "https://www.linkedin.com/in/mutyam-kritin"
ITCH = "https://kritin29.itch.io/"

# Adds .js; if we arrived via a pixel transition, keeps the page covered until main.js dissolves it in
HEAD_JS = ("(function(){var d=document.documentElement;d.classList.add('js');"
           "try{if(sessionStorage.getItem('km-pt')){sessionStorage.removeItem('km-pt');"
           "if(!matchMedia('(prefers-reduced-motion: reduce)').matches){d.classList.add('pt-in');"
           "d.style.setProperty('--enter-offset','300ms');"
           "setTimeout(function(){d.classList.remove('pt-in')},1500)}}}catch(e){}})()")

NAV = [("about", "About"), ("software", "Software"), ("games", "Games"), ("contact", "Contact")]


# ───────────────────────── shared chrome ─────────────────────────
def head(title, desc, path, noindex=False):
    full = "Kritin Mutyam" if title is None else f"{title} · Kritin Mutyam"
    url = SITE + path
    extra = '  <meta name="robots" content="noindex">\n' if noindex else f'  <link rel="canonical" href="{url}">\n'
    desc = esc(desc)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(full)}</title>
  <meta name="description" content="{desc}">
{extra}  <meta name="theme-color" content="#0f1119">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Kritin Mutyam">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc(full)}">
  <meta property="og:description" content="{desc}">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <script>{HEAD_JS}</script>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.gstatic.com/s/silkscreen/v6/m8JXjfVPf62XiF7kO-i9YLNlaw.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="https://fonts.gstatic.com/s/ibmplexmono/v23/-F63fjptAgt5VM-kVkqdyU8n1i8q1w.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css">
  <script src="/main.js" defer></script>
</head>
'''


def header(current):
    items = "\n".join(
        f'          <li><a class="pop" href="/{slug}"{" aria-current=\"page\"" if slug == current else ""}>{label}</a></li>'
        for slug, label in NAV)
    return f'''  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container">
      <a class="brand pop" href="/">Kritin Mutyam</a>
      <nav aria-label="Primary">
        <ul>
{items}
        </ul>
      </nav>
    </div>
  </header>
'''


def footer(controls):
    hint = "".join(f'<span><kbd>{k}</kbd>{v}</span>' for k, v in controls)
    return f'''  <footer class="site-footer">
    <div class="container">
      <p>Contact me: <a class="pop" href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="explored"></p>
      <ul aria-label="Profiles">
        <li><a class="pop" href="{GITHUB}">GitHub</a></li>
        <li><a class="pop" href="{LINKEDIN}">LinkedIn</a></li>
        <li><a class="pop" href="{ITCH}">itch.io</a></li>
      </ul>
      <p class="controls">{hint}</p>
    </div>
  </footer>
</body>
</html>
'''


TOP_CONTROLS = [("↑↓", "Select"), ("Enter", "Open"), ("←→", "Switch page")]
DETAIL_CONTROLS = [("1–9", "Jump to section"), ("←→", "Prev / next"), ("Esc", "Back")]


def with_toc(main):
    """Number every section header on a detail page, give it an id, and add an
    'On this page' sidebar that links to each one."""
    import re
    items = []

    def repl(m):
        open_tag, rest, gap, raw = m.group(1), m.group(2), m.group(3), m.group(4)
        text = re.sub(r'<span class="feat-count">.*?</span>', '', raw)
        text = re.sub(r'<[^>]+>', '', text).replace('&amp;', '&').replace('&#x27;', "'").strip()
        sid = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or f'section-{len(items) + 1}'
        items.append((sid, text))
        n = len(items)
        return f'{open_tag} id="{sid}"{rest}{gap}<h2 class="label"><span class="sec-n">{n:02d}</span>{raw}</h2>'

    main = re.sub(r'(<section class="block[^"]*")([^>]*>)(\s*)<h2 class="label">(.*?)</h2>', repl, main)
    if not items:
        return main
    links = "".join(f'<li><a href="#{sid}"><span class="toc-n">{n:02d}</span>{esc(text)}</a></li>'
                    for n, (sid, text) in enumerate(items, 1))
    toc = (f'\n    <nav class="toc" aria-label="On this page"><p class="toc-k">On this page</p>'
           f'<ol>{links}</ol><span class="toc-bar" aria-hidden="true"><span></span></span></nav>')
    return re.sub(r'(<a class="crumb[^>]*>[^<]*</a>)', lambda m: m.group(1) + toc, main, count=1)


def page(fname, path, title, desc, current, main, body_attrs="", controls=TOP_CONTROLS, noindex=False):
    html = (head(title, desc, path, noindex) + f'<body{body_attrs}>\n' + header(current) + main + footer(controls))
    fpath = os.path.join(OUT, fname)
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def ext_link(label, url):
    arrow = "→" if url.startswith("mailto:") or url.startswith("/") else "↗"
    return f'<a class="pop" href="{esc(url)}">{esc(label)} <span aria-hidden="true">{arrow}</span></a>'


# ───────────────────────── home ─────────────────────────
def build_home():
    soft_meta = f"{len(C.EXPERIENCE)} roles · {len(C.PROJECTS)} projects"
    game_meta = f"{len(C.GAMES)} games"
    main = f'''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Kritin Mutyam</h1>
    <p class="intro in" style="--i:1">Computer Science and Data Science student, with a certificate in Game Design, at the University of Wisconsin–Madison.</p>
    <p class="intro in" style="--i:2">I build full-stack web applications, applied AI tools, and games.</p>
    <ul class="links in" style="--i:3" aria-label="Profiles">
      <li><a class="pop" href="{GITHUB}">GitHub</a></li>
      <li><a class="pop" href="{LINKEDIN}">LinkedIn</a></li>
      <li><a class="pop" href="{ITCH}">itch.io</a></li>
      <li><a class="pop" href="mailto:{EMAIL}">Email</a></li>
    </ul>

    <section class="section" aria-labelledby="track-h">
      <h2 class="label in" id="track-h" style="--i:4">Select track</h2>
      <div class="tiles">
        <a class="tile in" href="/software" style="--i:5">
          <span class="tile-k">Track 01</span>
          <span class="tile-title">Software</span>
          <span class="tile-desc">Full-stack web · Applied AI · Developer tools</span>
          <span class="tile-desc">{soft_meta}</span>
        </a>
        <a class="tile in" href="/games" style="--i:6">
          <span class="tile-k">Track 02</span>
          <span class="tile-title">Games</span>
          <span class="tile-desc">Unreal Engine 5 · Roblox · Game jams</span>
          <span class="tile-desc">{game_meta}</span>
        </a>
      </div>
    </section>
  </main>
'''
    page("index.html", "/", None,
         "Kritin Mutyam studies Computer Science and Data Science, with a certificate in Game Design, at the "
         "University of Wisconsin–Madison. Full-stack web, applied AI, and game development.", "home", main,
         ' data-page="home"')


# ───────────────────────── software track ─────────────────────────
def row(n, item, i):
    thumb = ""
    cls = "row in"
    if item.get("thumb"):
        src, w, h = item["thumb"]
        thumb = f'<img class="row-thumb" src="{src}" width="{w}" height="{h}" alt="" loading="lazy">'
        cls += " row--thumb"
    return f'''        <li><a class="{cls}" href="/software/{item["slug"]}" style="--i:{i}">
          <span class="row-num">{n:02d}</span>
          <span class="row-body">
            <span class="row-top"><h3 class="row-title">{esc(item["title"])}</h3><span class="row-kind">{esc(item["row_kind"])}</span></span>
            <span class="row-meta">{esc(item["row_meta"])}</span>
            <span class="row-desc">{esc(item["oneliner"])}</span>
          </span>{thumb}
        </a></li>'''


def build_software():
    i = 3
    exp_rows = []
    for n, item in enumerate(C.EXPERIENCE, 1):
        exp_rows.append(row(n, item, i)); i += 1
    i += 1
    proj_rows = []
    for n, item in enumerate(C.PROJECTS, 1):
        proj_rows.append(row(n, item, i)); i += 1
    skills = "\n".join(f'        <div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in C.SKILLS)
    main = f'''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Software</h1>
    <p class="intro in" style="--i:1">{esc(C.SOFTWARE_INTRO)}</p>
    <ul class="links in" style="--i:2" aria-label="Profiles">
      <li><a class="pop" href="{GITHUB}">GitHub</a></li>
      <li><a class="pop" href="{LINKEDIN}">LinkedIn</a></li>
      <li><a class="pop" href="mailto:{EMAIL}">Email</a></li>
    </ul>

    <section class="section" aria-labelledby="exp-h">
      <h2 class="label in" id="exp-h" style="--i:3">Experience</h2>
      <ul class="index">
{chr(10).join(exp_rows)}
      </ul>
    </section>

    <section class="section" aria-labelledby="proj-h">
      <h2 class="label in" id="proj-h" style="--i:{3 + len(C.EXPERIENCE)}">Projects</h2>
      <ul class="index">
{chr(10).join(proj_rows)}
      </ul>
    </section>

    <section class="section" aria-labelledby="skills-h">
      <h2 class="label" id="skills-h">Skills</h2>
      <dl class="facts skills">
{skills}
      </dl>
    </section>
  </main>
'''
    page("software.html", "/software", "Software",
         "Kritin Mutyam's software engineering work: internships, full-stack and applied AI projects, and skills.",
         "software", main, ' data-page="software"')


def detail(item, prev, nxt):
    i = 0
    def nx():
        nonlocal i
        i += 1
        return i
    hud = "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in item["hud"])
    links = ""
    if item["links"]:
        links = (f'\n    <ul class="links in" style="--i:{nx()}">' +
                 "".join(f'<li>{ext_link(l, u)}</li>' for l, u in item["links"]) + '</ul>')
    note = f'\n    <p class="note in" style="--i:{nx()}; margin-top:{16 if links else 24}px">{esc(item["note"])}</p>' if item["note"] else ""

    shots = item.get("shots") or []
    hero = extra_shots = ""
    if shots:
        src, w, h, alt, cap = shots[0]
        hero = f'''
    <figure class="shot in" style="--i:{nx()}">
      <img src="{src}" width="{w}" height="{h}" alt="{esc(alt)}">
      {f"<figcaption>{esc(cap)}</figcaption>" if cap else ""}
    </figure>'''
        if len(shots) > 1:
            figs = "".join(f'''
      <figure class="shot"><img src="{s}" width="{w2}" height="{h2}" alt="{esc(a)}" loading="lazy">{f"<figcaption>{esc(c)}</figcaption>" if c else ""}</figure>'''
                           for s, w2, h2, a, c in shots[1:])
            extra_shots = (f'\n\n    <section class="block">\n      <h2 class="label">Screens</h2>'
                           f'\n      <div class="shots">{figs}\n      </div>\n    </section>')

    flow = ""
    if item["flow"]:
        flow = '\n      <ol class="flow" aria-label="How it works, step by step">' + "".join(
            f'<li><span class="flow-k">{esc(k)}</span>{esc(v)}</li>' for k, v in item["flow"]) + '</ol>'
    how = "".join(f'<li>{esc(b)}</li>' for b in item["how"])
    why = ""
    if item.get("why"):
        why = f'''
    <section class="block in" style="--i:{nx()}">
      <h2 class="label">Why build it</h2>
      <p>{esc(item.get("why_lead", ""))}</p>
      <ul style="margin-top:12px">{"".join(f"<li>{esc(b)}</li>" for b in item["why"])}</ul>
    </section>
'''
    mine = ""
    if item.get("mine"):
        mine = f'''
    <section class="block in" style="--i:{nx()}">
      <h2 class="label">My part</h2>
      <p>{esc(item["mine"])}</p>
    </section>
'''
    features = ""
    if item.get("features"):
        cards = "".join(f'<li><span class="feat-n">{esc(n)}</span><span class="feat-d">{esc(d)}</span></li>'
                        for n, d in item["features"])
        features = f'''

    <section class="block in" style="--i:{nx()}">
      <h2 class="label">Features <span class="feat-count">{len(item["features"])}</span></h2>
      <ul class="feats">{cards}</ul>
    </section>'''
    stats = ""
    if item["stats"]:
        stats = f'''
    <section class="block in" style="--i:{nx()}">
      <h2 class="label">{esc(item.get("stats_label", "Results"))}</h2>
      <div class="stats">{"".join(f'<p class="stat"><span class="stat-v">{esc(v)}</span><span class="stat-l">{esc(l)}</span></p>' for v, l in item["stats"])}</div>
    </section>'''
    takeaway = ""
    if item.get("takeaway"):
        takeaway = f'''
    <aside class="takeaway in" style="--i:{nx()}">
      <p class="label">Takeaway</p>
      <p>{esc(item["takeaway"])}</p>
    </aside>'''

    pager = '\n    <nav class="pager" aria-label="More work">'
    if prev:
        pager += f'<a class="prev" href="/software/{prev["slug"]}"><span class="pager-k">← Previous</span><span class="pager-t">{esc(prev["title"])}</span></a>'
    if nxt:
        pager += f'<a class="next" href="/software/{nxt["slug"]}"><span class="pager-k">Next →</span><span class="pager-t">{esc(nxt["title"])}</span></a>'
    pager += '</nav>'

    main = f'''  <main id="main" class="container detail">
    <a class="crumb pop in" href="/software" style="--i:0">← Software</a>
    <h1 class="page-title in" style="--i:{nx()}">{esc(item["title"])}</h1>
    <p class="intro in" style="--i:{nx()}">{esc(item["oneliner"])}</p>
    <dl class="hud in" style="--i:{nx()}">{hud}</dl>{links}{note}{hero}

    <section class="block in" style="--i:{nx()}">
      <h2 class="label">Problem</h2>
      <p>{esc(item["problem"])}</p>
    </section>

    <section class="block in" style="--i:{nx()}">
      <h2 class="label">Solution</h2>
      <p>{esc(item["solution"])}</p>
    </section>

{why}{mine}
    <section class="block in" style="--i:{nx()}">
      <h2 class="label">How it works</h2>{flow}
      <ul{' style="margin-top:20px"' if flow else ''}>{how}</ul>
    </section>{features}{extra_shots}{stats}{takeaway}{pager}
  </main>
'''
    attrs = f' data-up="/software"'
    if prev: attrs += f' data-prev="/software/{prev["slug"]}"'
    if nxt: attrs += f' data-next="/software/{nxt["slug"]}"'
    attrs += f' data-detail="{item["slug"]}"'
    page(f"software/{item['slug']}.html", f"/software/{item['slug']}", item["title"], item["oneliner"],
         "software", with_toc(main), attrs, DETAIL_CONTROLS)


def build_details():
    items = C.EXPERIENCE + C.PROJECTS
    for k, item in enumerate(items):
        detail(item, items[k - 1] if k > 0 else None, items[k + 1] if k < len(items) - 1 else None)


# ───────────────────────── games track ─────────────────────────
def build_games():
    """/games: a level-select screen of game 'cartridges'."""
    carts = []
    # C.GAMES is in level order (level 1 first); show the highest level at the top, like climbing a tower
    levels = list(enumerate(C.GAMES, 1))[::-1]
    for shown, (lvl, g) in enumerate(levels, 1):
        src, w, h = g["cover"]
        chip = f'<span class="cart-stat">{esc(g["cart_stat"])}</span>' if g.get("cart_stat") else ""
        carts.append(f'''      <a class="cart in" href="/games/{g["slug"]}" style="--i:{2 + shown}">
        <span class="cart-media"><img src="{src}" width="{w}" height="{h}" alt="" loading="{"eager" if shown <= 2 else "lazy"}"><span class="cart-start" aria-hidden="true">&gt; Start</span></span>
        <span class="cart-body">
          <span class="cart-top"><span class="tag">{esc(g["engine"])}</span>{chip}</span>
          <h2 class="cart-title"><span class="cart-num">Lv {lvl:02d}</span>{esc(g["title"])}</h2>
          <span class="cart-desc">{esc(g["short"])}</span>
        </span>
      </a>''')
    main = f'''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Games</h1>
    <p class="intro in" style="--i:1">{esc(C.GAMES_INTRO)}</p>
    <ul class="links in" style="--i:2" aria-label="Profiles">
      <li><a class="pop" href="{ITCH}">itch.io</a></li>
      <li><a class="pop" href="mailto:{EMAIL}">Email</a></li>
    </ul>

    <section class="section" aria-labelledby="levels-h">
      <h2 class="label in" id="levels-h" style="--i:2">Select a game</h2>
      <div class="carts">
{chr(10).join(carts)}
      </div>
    </section>
  </main>
'''
    page("games.html", "/games", "Games",
         "Games by Kritin Mutyam: " + ", ".join(g["title"] for g in C.GAMES) + ".",
         "games", main, ' data-page="games"')


def game_detail(g, prev, nxt):
    i = 0
    def nx():
        nonlocal i
        i += 1
        return i
    hud = "".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in g["hud"])
    play = ""
    if g.get("play"):
        play = (f'\n    <div class="play-row in" style="--i:{nx()}">' +
                "".join(f'<a class="btn-play" href="{esc(u)}">&gt; {esc(l)}</a>' for l, u in g["play"]) + '</div>')
    note = f'\n    <p class="note in" style="--i:{nx()}; margin-top:16px">{esc(g["note"])}</p>' if g.get("note") else ""

    # hero: a looping clip if we have one, otherwise the first screenshot
    hero = ""
    clips = g.get("clips") or []
    shots = g.get("shots") or []
    if clips:
        mp4, poster, cap = clips[0]
        hero = f'''
    <figure class="clip clip--hero in" style="--i:{nx()}">
      <video src="{mp4}" poster="{poster}" width="1280" height="720" autoplay muted loop playsinline preload="metadata" aria-label="{esc(cap)}"></video>
      <figcaption>{esc(cap)}</figcaption>
    </figure>'''
    elif shots:
        src, w, h, alt, cap = shots[0]
        hero = f'''
    <figure class="shot in" style="--i:{nx()}"><img src="{src}" width="{w}" height="{h}" alt="{esc(alt)}"><figcaption>{esc(cap)}</figcaption></figure>'''
        shots = shots[1:]

    def section(label, body, extra=""):
        return f'''

    <section class="block in" style="--i:{nx()}">
      <h2 class="label">{label}{extra}</h2>{body}
    </section>'''

    pitch = section("The game", f'\n      <p>{esc(g["pitch"])}</p>')
    loop = ""
    if g.get("loop"):
        loop = section("Core loop", '\n      <ol class="flow" aria-label="Core gameplay loop">' + "".join(
            f'<li><span class="flow-k">{esc(k)}</span>{esc(v)}</li>' for k, v in g["loop"]) + '</ol>')
    credits = ""
    if g.get("credits"):
        credits = section("Credits", '\n      <dl class="credits">' + "".join(
            f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in g["credits"]) + '</dl>')
    systems = ""
    if g.get("systems"):
        systems = section("Systems", '\n      <ul>' + "".join(f'<li>{esc(b)}</li>' for b in g["systems"]) + '</ul>')
    mechanics = ""
    if g.get("features"):
        cards = "".join(f'<li><span class="feat-n">{esc(n)}</span><span class="feat-d">{esc(d)}</span></li>' for n, d in g["features"])
        mechanics = section("Mechanics", f'\n      <ul class="feats">{cards}</ul>',
                            f' <span class="feat-count">{len(g["features"])}</span>')
    trailer = ""
    if g.get("trailer"):
        mp4, poster, title = g["trailer"]
        trailer = section("Watch", f'''
      <figure class="trailer"><video src="{mp4}" poster="{poster}" width="1280" height="720" controls preload="none" playsinline aria-label="{esc(title)}"></video></figure>''')
    elif g.get("youtube"):
        vid, title = g["youtube"]
        trailer = section("Watch", f'''
      <button class="yt" type="button" data-yt="{esc(vid)}" aria-label="Play video: {esc(title)}" style="background-image:url(https://i.ytimg.com/vi/{esc(vid)}/hqdefault.jpg)"><span class="yt-play" aria-hidden="true"></span><span class="yt-title">{esc(title)}</span></button>''')
    more_clips = ""
    if len(clips) > 1:
        figs = "".join(f'''
        <figure class="clip"><video src="{m}" poster="{p}" width="1280" height="720" autoplay muted loop playsinline preload="none" aria-label="{esc(c)}"></video><figcaption>{esc(c)}</figcaption></figure>'''
                       for m, p, c in clips[1:])
        more_clips = section("Clips", f'\n      <div class="shots">{figs}\n      </div>')
    screens = ""
    if shots:
        figs = "".join(f'''
        <figure class="shot"><img src="{s}" width="{w2}" height="{h2}" alt="{esc(a)}" loading="lazy"><figcaption>{esc(c)}</figcaption></figure>'''
                       for s, w2, h2, a, c in shots)
        screens = section("Screens", f'\n      <div class="shots">{figs}\n      </div>')
    assets = ""
    if g.get("asset_groups"):
        rows = ""
        for label, items in g["asset_groups"]:
            tiles = "".join(f'<figure class="asset"><img src="{g["asset_dir"]}/{slug}.webp" width="256" height="256" alt="{esc(name)} ({esc(label.lower().rstrip("s"))})" loading="lazy"><figcaption>{esc(name)}</figcaption></figure>'
                            for slug, name in items)
            rows += f'\n        <div class="asset-row"><p class="asset-row-k">{esc(label)}</p><div class="assets assets--icons">{tiles}</div></div>'
        note_html = f'\n      <p class="asset-note">{esc(g["assets_note"])}</p>' if g.get("assets_note") else ""
        assets = section(esc(g.get("assets_label", "Assets")), f'{note_html}\n      <div class="asset-rows">{rows}\n      </div>',
                         f' <span class="feat-count">{esc(g.get("assets_count", ""))}</span>')
    elif g.get("assets"):
        kind = g.get("assets_kind", "models")
        figs = "".join(f'''
        <figure class="asset"><img src="{s}" width="{w2}" height="{h2}" alt="{esc(a)}" loading="lazy"><figcaption>{esc(c)}</figcaption></figure>'''
                       for s, w2, h2, a, c in g["assets"])
        note_html = f'\n      <p class="asset-note">{esc(g["assets_note"])}</p>' if g.get("assets_note") else ""
        assets = section(esc(g.get("assets_label", "Made by me")),
                         f'{note_html}\n      <div class="assets assets--{kind}">{figs}\n      </div>',
                         f' <span class="feat-count">{len(g["assets"])}</span>')
    stats = ""
    if g.get("stats"):
        stats = section("High scores", '\n      <div class="stats">' + "".join(
            f'<p class="stat"><span class="stat-v">{esc(v)}</span><span class="stat-l">{esc(l)}</span></p>' for v, l in g["stats"]) + '</div>')
    takeaway = ""
    if g.get("takeaway"):
        takeaway = f'''

    <aside class="takeaway in" style="--i:{nx()}">
      <p class="label">Dev note</p>
      <p>{esc(g["takeaway"])}</p>
    </aside>'''

    # Left = next level, right = previous level (the ← / → keys match the sides)
    pager = '\n\n    <nav class="pager" aria-label="More games">'
    if nxt:
        pager += f'<a class="prev" href="/games/{nxt["slug"]}"><span class="pager-k">← Next level</span><span class="pager-t">{esc(nxt["title"])}</span></a>'
    if prev:
        pager += f'<a class="next" href="/games/{prev["slug"]}"><span class="pager-k">Prev level →</span><span class="pager-t">{esc(prev["title"])}</span></a>'
    pager += '</nav>'

    main = f'''  <main id="main" class="container game detail">
    <a class="crumb pop in" href="/games" style="--i:0">← Games</a>
    <h1 class="page-title in" style="--i:{nx()}">{esc(g["title"])}</h1>
    <p class="intro in" style="--i:{nx()}">{esc(g["oneliner"])}</p>
    <dl class="hud in" style="--i:{nx()}">{hud}</dl>{play}{note}{hero}{pitch}{loop}{credits}{systems}{mechanics}{trailer}{more_clips}{screens}{assets}{stats}{takeaway}{pager}
  </main>
'''
    attrs = ' data-up="/games"'
    if nxt: attrs += f' data-prev="/games/{nxt["slug"]}"'    # ← key = left link (next level)
    if prev: attrs += f' data-next="/games/{prev["slug"]}"'  # → key = right link (prev level)
    attrs += f' data-detail="{g["slug"]}"'
    page(f"games/{g['slug']}.html", f"/games/{g['slug']}", g["title"], g["oneliner"], "games", with_toc(main), attrs, DETAIL_CONTROLS)


def build_game_details():
    # Level order: next = one level up (P.I.G. → Ascend → Wingblade → BUILD), prev = one level down
    order = C.GAMES
    for k, g in enumerate(order):
        game_detail(g, order[k - 1] if k > 0 else None, order[k + 1] if k < len(order) - 1 else None)


# ───────────────────────── about / contact / 404 ─────────────────────────
def build_about():
    main = '''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">About</h1>
    <p class="intro in" style="--i:1">I study Computer Science and Data Science, with a certificate in Game Design, at the University of Wisconsin–Madison. My work spans full-stack web development, applied AI, and game development.</p>

    <dl class="facts">
      <div class="in" style="--i:2">
        <dt>Education</dt>
        <dd>University of Wisconsin–Madison<span class="sub">B.S. Computer Sciences and Data Science, Certificate in Game Design</span><span class="sub">Expected May 2028</span></dd>
      </div>
      <div class="in" style="--i:3">
        <dt>Focus</dt>
        <dd>Full-stack web, applied AI, game development</dd>
      </div>
      <div class="in" style="--i:4">
        <dt>Activities</dt>
        <dd>Game Development Club, Claude Club</dd>
      </div>
      <div class="in" style="--i:5">
        <dt>Outside class</dt>
        <dd>Basketball, gaming</dd>
      </div>
    </dl>
  </main>
'''
    page("about.html", "/about", "About",
         "About Kritin Mutyam: Computer Science and Data Science student, with a certificate in Game Design, "
         "at the University of Wisconsin–Madison.", "about", main, ' data-page="about"')


def build_contact():
    rows = [("Email", EMAIL, f"mailto:{EMAIL}"), ("LinkedIn", "linkedin.com/in/mutyam-kritin", LINKEDIN)]
    dl = "\n".join(f'''      <div class="in" style="--i:{2 + n}">
        <dt>{k}</dt>
        <dd><a class="text-link pop" href="{u}">{label}</a></dd>
      </div>''' for n, (k, label, u) in enumerate(rows))
    main = f'''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Contact me</h1>
    <p class="intro in" style="--i:1">For opportunities, collaborations, or questions about my work, email is the best way to reach me.</p>

    <dl class="facts">
{dl}
    </dl>
  </main>
'''
    page("contact.html", "/contact", "Contact", "Get in touch with Kritin Mutyam by email or LinkedIn.",
         "contact", main, ' data-page="contact"')


def build_404():
    main = '''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Page not found</h1>
    <p class="intro in" style="--i:1">The page you’re looking for doesn’t exist. <a class="text-link pop" href="/">Return home</a>.</p>
  </main>
'''
    page("404.html", "/404", "Page not found", "This page could not be found.", None, main, noindex=True)


def build_sitemap():
    paths = (["/", "/about", "/software", "/games", "/contact"]
             + [f"/software/{x['slug']}" for x in C.EXPERIENCE + C.PROJECTS]
             + [f"/games/{g['slug']}" for g in C.GAMES])
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc></url>" for p in paths)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


if __name__ == "__main__":
    build_home(); build_about(); build_software(); build_details(); build_games(); build_game_details()
    build_contact(); build_404(); build_sitemap()
    print("built", 6 + len(C.EXPERIENCE) + len(C.PROJECTS) + len(C.GAMES), "pages")
