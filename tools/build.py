"""Generates index/about/projects/contact/404.html with a shared head, header and footer.

Edit the content below, then run from the repo root:   python tools/build.py
"""
import sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mutyamkritin.com"
# Adds .js; if we arrived via a pixel transition, keeps the page covered until main.js dissolves it in
HEAD_JS = ("(function(){var d=document.documentElement;d.classList.add('js');"
           "try{if(sessionStorage.getItem('km-pt')){sessionStorage.removeItem('km-pt');"
           "if(!matchMedia('(prefers-reduced-motion: reduce)').matches){d.classList.add('pt-in');"
           "d.style.setProperty('--enter-offset','360ms');"
           "setTimeout(function(){d.classList.remove('pt-in')},1500)}}}catch(e){}})()")


def head(title, desc, path, noindex=False):
    full = "Kritin Mutyam" if title is None else f"{title} · Kritin Mutyam"
    url = SITE + path
    extra = '  <meta name="robots" content="noindex">\n' if noindex else f'  <link rel="canonical" href="{url}">\n'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full}</title>
  <meta name="description" content="{desc}">
{extra}  <meta name="theme-color" content="#0f1119">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Kritin Mutyam">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{full}">
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
    def li(slug, label):
        cur = ' aria-current="page"' if slug == current else ''
        return f'          <li><a class="pop" href="/{slug}"{cur}>{label}</a></li>'
    return f'''  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container">
      <a class="brand pop" href="/">Kritin Mutyam</a>
      <nav aria-label="Primary">
        <ul>
{li("about", "About")}
{li("projects", "Projects")}
{li("contact", "Contact")}
        </ul>
      </nav>
    </div>
  </header>
'''


FOOTER = '''  <footer class="site-footer">
    <div class="container">
      <p>Contact me: <a class="pop" href="mailto:mutyam@wisc.edu">mutyam@wisc.edu</a></p>
      <p class="explored"></p>
      <p class="controls"><span><kbd>↑↓</kbd>Select</span><span><kbd>Enter</kbd>Open</span><span><kbd>←→</kbd>Switch page</span></p>
      <ul aria-label="Profiles">
        <li><a class="pop" href="https://github.com/kritin29">GitHub</a></li>
        <li><a class="pop" href="https://www.linkedin.com/in/mutyam-kritin">LinkedIn</a></li>
        <li><a class="pop" href="https://kritin29.itch.io/">itch.io</a></li>
      </ul>
    </div>
  </footer>
</body>
</html>
'''

# Same order as the resume
PROJECTS = [
    dict(id="facultywise", name="FacultyWise", kind="AI · Web", short="AI grading platform for university faculty",
         desc="An AI grading platform for university faculty. It retrieves student submissions from Canvas, scores them against each professor’s rubric, and returns grades with written feedback. I built the full technical stack on a two-person team, and the platform was piloted with five professors.",
         stack="React · TypeScript · Supabase · OpenAI · Inngest · Chrome MV3", link=None),
    dict(id="wingblade-arena", name="Wingblade Arena", kind="Game", short="Aerial combat game on Roblox",
         desc="A fast-paced aerial combat game on Roblox, built around flight, swordplay, and mid-air spear throws.",
         stack="Roblox · Luau · Blender", link=None),
    dict(id="claudepearl", name="ClaudePearl", kind="Developer tool", short="Desktop and mobile app for AI-assisted development",
         desc="A desktop and mobile application that replaces the terminal for AI-assisted development, with persistent project memory, a contextual skills library, and direct MCP control of Roblox Studio and Blender.",
         stack="TypeScript · Node.js · Fastify · SQLite · React · Tauri · Claude Agent SDK · MCP", link=None),
    dict(id="build-066", name="BUILD 0.66", kind="Game · Game jam", short="Stealth narrative game in Unreal Engine 5",
         desc="A first-person stealth narrative game set in a world where dinosaurs never went extinct. Raptors adapt each day to the player’s habits as he searches for a way out. Built solo in 90 hours for the Epic AI MegaJam 2026.",
         stack="Unreal Engine 5.8 · C++ · Python · Blender", link=("View on itch.io", "https://kritin29.itch.io/")),
]


def page(fname, slug, title, desc, current, main, noindex=False):
    path = "/" if slug == "" else "/" + slug
    page_attr = f' data-page="{current}"' if current else ""
    html = head(title, desc, path, noindex) + f'<body{page_attr}>\n' + header(current) + main + FOOTER
    with open(os.path.join(OUT, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


# ── Home
rows = "\n".join(
    f'        <li><a class="row in" href="/projects#{p["id"]}" data-project="{p["id"]}" style="--i:{5 + n}">'
    f'<span class="row-num">{n + 1:02d}</span><span class="row-body"><span class="row-title">{p["name"]}</span>'
    f'<span class="row-desc">{p["short"]}</span></span></a></li>'
    for n, p in enumerate(PROJECTS))
home = f'''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Kritin Mutyam</h1>
    <p class="intro in" style="--i:1">Computer Science and Data Science student, with a certificate in Game Design, at the University of Wisconsin–Madison.</p>
    <p class="intro in" style="--i:2">I build full-stack web applications, applied AI tools, and games.</p>
    <ul class="links in" style="--i:3" aria-label="Profiles">
      <li><a class="pop" href="https://github.com/kritin29">GitHub</a></li>
      <li><a class="pop" href="https://www.linkedin.com/in/mutyam-kritin">LinkedIn</a></li>
      <li><a class="pop" href="https://kritin29.itch.io/">itch.io</a></li>
      <li><a class="pop" href="mailto:mutyam@wisc.edu">Email</a></li>
    </ul>

    <section class="section" aria-labelledby="projects-h">
      <h2 class="label in" id="projects-h" style="--i:4">Projects</h2>
      <ul class="index index--compact">
{rows}
      </ul>
    </section>
  </main>
'''
page("index.html", "", None, "Kritin Mutyam studies Computer Science and Data Science, with a certificate in Game Design, at the University of Wisconsin–Madison. Full-stack web, applied AI, and game development.", "home", home)

# ── About
about = '''  <main id="main" class="container">
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
page("about.html", "about", "About", "About Kritin Mutyam: Computer Science and Data Science student, with a certificate in Game Design, at the University of Wisconsin–Madison.", "about", about)


# ── Projects
def prow(n, p):
    link = ""
    if p["link"]:
        link = f'\n          <a class="text-link pop" href="{p["link"][1]}">{p["link"][0]} <span aria-hidden="true">↗</span></a>'
    return f'''      <article class="row in" id="{p["id"]}" data-project="{p["id"]}" style="--i:{2 + n}">
        <span class="row-num">{n + 1:02d}</span>
        <div class="row-body">
          <div class="row-top"><h2>{p["name"]}</h2><span class="row-kind">{p["kind"]}</span></div>
          <p>{p["desc"]}</p>
          <p class="row-stack">{p["stack"]}</p>{link}
        </div>
      </article>'''


projects = f'''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Projects</h1>
    <p class="intro in" style="--i:1">Selected work across applied AI, games, and developer tools.</p>

    <div class="index projects-index">
{chr(10).join(prow(n, p) for n, p in enumerate(PROJECTS))}
    </div>
  </main>
'''
page("projects.html", "projects", "Projects", "Projects by Kritin Mutyam: FacultyWise, Wingblade Arena, ClaudePearl, and BUILD 0.66.", "projects", projects)


# ── Contact
def crow(i, k, label, href):
    return f'''      <div class="in" style="--i:{i}">
        <dt>{k}</dt>
        <dd><a class="text-link pop" href="{href}">{label}</a></dd>
      </div>'''


contact = f'''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Contact me</h1>
    <p class="intro in" style="--i:1">For opportunities, collaborations, or questions about my work, email is the best way to reach me.</p>

    <dl class="facts">
{crow(2, "Email", "mutyam@wisc.edu", "mailto:mutyam@wisc.edu")}
{crow(3, "GitHub", "github.com/kritin29", "https://github.com/kritin29")}
{crow(4, "LinkedIn", "linkedin.com/in/mutyam-kritin", "https://www.linkedin.com/in/mutyam-kritin")}
{crow(5, "itch.io", "kritin29.itch.io", "https://kritin29.itch.io/")}
    </dl>
  </main>
'''
page("contact.html", "contact", "Contact", "Get in touch with Kritin Mutyam by email, GitHub, LinkedIn, or itch.io.", "contact", contact)

# ── 404
nf = '''  <main id="main" class="container">
    <h1 class="page-title in" style="--i:0">Page not found</h1>
    <p class="intro in" style="--i:1">The page you’re looking for doesn’t exist. <a class="text-link pop" href="/">Return home</a>.</p>
  </main>
'''
page("404.html", "404", "Page not found", "This page could not be found.", None, nf, noindex=True)
print("built")
