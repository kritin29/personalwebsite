"""Pixel-art comet favicon (Arcade palette): a glowing head with a curved, tapering tail
and a few sparks, echoing the site's mouse trail. Writes favicon.svg, favicon.ico and
apple-touch-icon.png to the repo root.

Needs Pillow (pip install pillow). Run from the repo root:   python tools/favicon.py
"""
import sys, os, math
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = sys.argv[2] if len(sys.argv) > 2 else None
N = 16
BG = (15, 17, 25)
WHITE = (236, 255, 246)
MINT = (126, 224, 181)
TEAL = (64, 150, 132)
DEEP = (38, 82, 92)
STAR = (58, 66, 104)

def lerp(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def tail_color(t):  # t: 0 at tail end → 1 at head
    if t < .45: return lerp(DEEP, TEAL, t / .45)
    return lerp(TEAL, MINT, (t - .45) / .55)

g = [[BG] * N for _ in range(N)]

# faint background stars
for x, y in [(2, 2), (6, 1), (14, 13), (1, 8)]:
    g[y][x] = STAR

# tail: quadratic bezier from bottom-left up to the head, thickness grows toward the head
P0, P1, P2 = (1.4, 14.6), (3.2, 7.6), (9.8, 5.9)
samples = []
for i in range(400):
    t = i / 399
    x = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0]
    y = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]
    samples.append((x, y, t))
for py in range(N):
    for px in range(N):
        cx, cy = px + .5, py + .5
        best = min(samples, key=lambda s: (s[0] - cx) ** 2 + (s[1] - cy) ** 2)
        d = math.hypot(best[0] - cx, best[1] - cy)
        r = .32 + .78 * best[2] ** 1.3          # radius tapers toward the tail
        if d <= r:
            g[py][px] = tail_color(best[2])

# head: a rounded 4x4 blob with a bright core
head = {(11, 3): MINT, (12, 3): MINT,
        (10, 4): MINT, (11, 4): WHITE, (12, 4): WHITE, (13, 4): MINT,
        (10, 5): MINT, (11, 5): WHITE, (12, 5): WHITE, (13, 5): MINT,
        (11, 6): MINT, (12, 6): MINT}
for (x, y), c in head.items():
    g[y][x] = c
# soft glow around the head
for x, y in [(10, 3), (13, 3), (14, 4), (14, 5), (13, 6), (10, 6), (11, 2), (12, 2), (11, 7), (12, 7), (9, 4)]:
    if g[y][x] == BG:
        g[y][x] = lerp(BG, MINT, .28)
# sparks
for x, y, c in [(14, 1, lerp(BG, MINT, .7)), (8, 9, lerp(BG, MINT, .45)), (15, 8, lerp(BG, MINT, .4))]:
    g[y][x] = c

def img(scale, pad=0):
    im = Image.new('RGB', (N, N))
    for y in range(N):
        for x in range(N):
            im.putpixel((x, y), g[y][x])
    im = im.resize((N * scale, N * scale), Image.NEAREST)
    if pad:
        canvas = Image.new('RGB', (N * scale + pad * 2, N * scale + pad * 2), BG)
        canvas.paste(im, (pad, pad))
        im = canvas
    return im

hexc = lambda c: '#%02x%02x%02x' % c
rects = ''.join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{hexc(g[y][x])}"/>'
                for y in range(N) for x in range(N) if g[y][x] != BG)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" shape-rendering="crispEdges">'
       f'<rect width="16" height="16" fill="{hexc(BG)}"/>{rects}</svg>\n')
open(os.path.join(OUT, 'favicon.svg'), 'w', encoding='utf-8', newline='\n').write(svg)
img(3).save(os.path.join(OUT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
img(11, pad=2).save(os.path.join(OUT, 'apple-touch-icon.png'))   # 180x180

# preview: large + actual tab sizes
prev = Image.new('RGB', (420, 280), (40, 42, 54))
prev.paste(img(16), (12, 12))
prev.paste(img(2), (300, 40))
prev.paste(img(1), (300, 110))
if PREVIEW:
    prev.save(os.path.join(PREVIEW, 'icon-preview.png'))
print('ok')
