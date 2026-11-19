# mutyamkritin.com

Personal site. Plain HTML, CSS and vanilla JS: no framework, no build step to deploy.
Hosted on Vercel; every push to `main` redeploys.

## Files

| File | What it is |
|---|---|
| `index.html`, `about.html`, `projects.html`, `contact.html`, `404.html` | Pages (generated, see below) |
| `styles.css` | All styling: Arcade theme tokens at the top |
| `main.js` | Mouse trail, pixel page transitions, keyboard controls, achievements |
| `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` | Pixel comet tab icon |
| `vercel.json` | Clean URLs (`/about` instead of `/about.html`) |
| `tools/` | Generators, not deployed |

## Editing

The pages share one header, footer and `<head>`, so they're generated:

1. Edit text or projects in `tools/build.py` (project list is the `PROJECTS` array).
2. Run `python tools/build.py` from the repo root.
3. Commit and push.

Small one-off text fixes can go straight into the HTML, but the next build will overwrite them,
so copy the change into `tools/build.py` as well.

The tab icon is drawn by `tools/favicon.py` (`pip install pillow`, then `python tools/favicon.py`).

## Easter eggs

Footer pips track pages explored. Achievements unlock for visiting every page, looking at every
project, maxing out the mouse-trail boost, and entering the Konami code.
