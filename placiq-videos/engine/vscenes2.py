from vscenes import *

# ------------------------------------------------------------- platforms orbit & tug -> rewire into hub
def vorbit(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    names = p.get('names', ['LeetCode', 'GitHub', 'Resume', 'Courses', 'AI chat', 'Notion', 'LinkedIn', 'YouTube', 'Job portal', 'Sheets'])
    cx, cy = W / 2, 860
    hub_t = dur * p.get('hub', .62)
    hq = eio(prog(t, hub_t, .7))
    jit = 1 - hq
    sx = cx + math.sin(t * 9) * 26 * jit * (t > .5); sy = cy + math.cos(t * 7) * 18 * jit * (t > .5)
    pts = []
    for i, n in enumerate(names):
        a = 2 * math.pi * i / len(names) + t * .35
        r = 400 + 40 * math.sin(t * 2 + i)
        pts.append((cx + r * math.cos(a), cy + r * 1.25 * math.sin(a)))
    for i, (x, y) in enumerate(pts):
        q = prog(t, .05 + i * .12, .3)
        if q <= 0:
            continue
        if hq < 1:  # tug lines to the student
            d.line((x, y, sx, sy), fill=C['a2'], width=int(3 + 3 * abs(math.sin(t * 5 + i))))
        if hq > 0:
            j = (i + 1) % len(pts)
            d.line((x, y, lerp(x, pts[j][0], hq), lerp(y, pts[j][1], hq)), fill=C['a1'], width=5)
            d.line((x, y, lerp(x, cx, hq), lerp(y, cy, hq)), fill=C['a1'], width=3)
    for i, (x, y) in enumerate(pts):
        q = eback(prog(t, .05 + i * .12, .3))
        if q <= 0:
            continue
        tw, _ = tsize(names[i], 'mono', 30); w = (tw + 44) * q
        d.rounded_rectangle((x - w / 2, y - 34, x + w / 2, y + 34), 34, fill=C['card'], outline=C['fg'], width=3)
        if q > .8:
            text(img, names[i], x, y - 20, 'mono', 30, C['fg'], anchor='c')
    r = 70 + 60 * hq
    d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=C['a1'] if hq > .5 else C['fg'])
    text(img, p.get('hubtxt', 'YOU') if hq < .5 else 'Placiq', sx, sy - 30, 'black', 44 if hq > .5 else 48,
         C['fg_on_a1'] if hq > .5 else C['bg'], anchor='c')


# ------------------------------------------------------------- retro terminal
@lru_cache(maxsize=2)
def scanlines():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    for y in range(0, H, 4):
        dd.line((0, y, W, y), fill=(0, 0, 0, 70))
    return im


def vterm(img, d, t, S, C):
    p = S['p']; lines = p['lines']; dur = S['dur']
    rect(d, (40, 200, W - 40, 1500), C['bg2'], r=24, outline=C['a1'], width=3)
    text(img, p.get('title', 'bash  -  2:07 AM'), 80, 222, 'mono', 28, C['muted'])
    cps = p.get('cps', 40)
    t0 = .15; y = 300
    for ln in lines:
        txt, col = (ln, 'fg') if isinstance(ln, str) else ln
        n = int((t - t0) * cps)
        if n <= 0:
            break
        shown = txt[:n]
        for sub in wrap(shown, 'mono', 36, 920) if shown else ['']:
            text(img, sub, 80, y, 'mono', 36, C[col]); y += 54
        t0 += len(txt) / cps + p.get('pause', .25)
        if n < len(txt):
            break
    if int(t * 3) % 2 == 0:
        d.rectangle((80, y + 4, 104, y + 46), fill=C['a1'])
    img.paste(scanlines(), (0, 0), scanlines())
    if p.get('alert') and t > dur * p['alert'][1]:
        q = eback(prog(t, dur * p['alert'][1], .3))
        st = text_img(p['alert'][0], 'black', 110, C['a2']).rotate(-7, expand=True)
        paste(img, st, W / 2 - st.size[0] / 2, 1530, min(1, q))


# ------------------------------------------------------------- busy dashboard with hidden gap revealed by scanner
def vdash(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    bars = p.get('bars', [('Arrays', .92), ('Strings', .88), ('Hashing', .81), ('Trees', .74), ('SQL', .7), ('Graphs', .12)])
    gap_i = p.get('gap', len(bars) - 1)
    scan = prog(t, dur * .35, dur * .35)
    rect(d, (60, 230, W - 60, 1420), C['card'], r=30)
    text(img, p.get('title', 'MY PREP DASHBOARD'), 110, 270, 'mono', 34, C['muted'])
    text(img, 'streak 41 days', W - 110, 270, 'mono', 34, C['a1'], anchor='r')
    for i, (n, v) in enumerate(bars):
        y = 380 + i * 165
        hidden = i == gap_i
        q = eo(prog(t, .1 + i * .1, .6))
        fake = .9 if hidden else v
        rv = v if (hidden and scan * 1300 + 230 > y) else fake
        text(img, n, 110, y, 'black', 50, C['fg'])
        rect(d, (110, y + 75, 970, y + 120), C['line'], r=22)
        col = C['a2'] if (hidden and rv == v) else C['a1']
        rect(d, (110, y + 75, 110 + 860 * rv * q, y + 120), col, r=22)
        text(img, '%d%%' % int(rv * q * 100), 970, y, 'mono', 40, col, anchor='r')
        if hidden and rv == v:
            pill(img, d, p.get('flag', 'blind spot: never practised'), 110, y + 135, C['a2'], C['bg'], 28)
    if 0 < scan < 1:
        sy = 230 + scan * 1190
        d.rectangle((60, sy - 4, W - 60, sy + 4), fill=C['a2'])
        rect(d, (60, sy - 60, W - 60, sy), (C['a2'][0], C['a2'][1], C['a2'][2], 40))


# ------------------------------------------------------------- archetype trading cards
def vcards(img, d, t, S, C):
    p = S['p']; cards = p['cards']; dur = S['dur']
    seg = dur / len(cards)
    i = min(len(cards) - 1, int(t / seg)); lt = t - i * seg
    c = cards[i]
    flip = eio(prog(lt, 0, .45))
    w = int(860 * abs(math.cos(math.pi * (1 - flip) / 2 + math.pi / 2 * 0))) if flip < 1 else 860
    w = max(8, int(860 * flip))
    x0, y0 = W / 2 - w / 2, 300 + math.sin(t * 2.2) * 14
    rect(d, (x0, y0, x0 + w, y0 + 1180), C['a1'] if i % 2 == 0 else C['fg'], r=40)
    if flip > .9:
        fg = C['fg_on_a1'] if i % 2 == 0 else C['bg']
        text(img, 'CARD %d / %d' % (i + 1, len(cards)), x0 + 60, y0 + 50, 'mono', 30, fg)
        text(img, c['emoji'], x0 + w - 60, y0 + 40, 'black', 60, fg, anchor='r')
        for k, ln in enumerate(wrap(c['name'], 'black', 84, 740)):
            text_mask_up(img, ln, x0 + 60, y0 + 140 + k * 92, 'black', 84, fg, prog(lt, .4 + k * .1, .35))
        for k, (s, v) in enumerate(c['stats']):
            yy = y0 + 470 + k * 120
            text(img, s, x0 + 60, yy, 'mono', 32, fg)
            q = eo(prog(lt, .6 + k * .15, .5))
            rect(d, (x0 + 60, yy + 50, x0 + 800, yy + 80), C['muted'], r=15)
            rect(d, (x0 + 60, yy + 50, x0 + 60 + 740 * v * q, yy + 80), C['a2'], r=15)
        for k, ln in enumerate(wrap(c['ability'], 'serif', 54, 740)):
            text_mask_up(img, ln, x0 + 60, y0 + 900 + k * 60, 'serif', 54, fg, prog(lt, 1.0, .4))


# ------------------------------------------------------------- AI chat windows multiplying
def vchats(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    msg = p.get('msg', "Hi, I'm a 3rd-year CSE student preparing for placements. I know Java, some DSA...")
    n = int(1 + p.get('n', 12) * eo(prog(t, .8, dur * .7)))
    rnd = random.Random(8)
    for i in range(n):
        x = 80 + rnd.uniform(-40, 60) + (i % 3) * 20
        y = 260 + i * 95 if n < 14 else 260 + i * (1150 / n)
        rect(d, (x, y, x + 900, y + 300), C['card'], r=24, outline=C['line'], width=2)
        rect(d, (x, y, x + 900, y + 56), C['fg'], r=24)
        text(img, 'New chat #%d' % (i + 1), x + 28, y + 10, 'mono', 28, C['bg'])
        typed = msg if i < n - 1 else msg[:int((t - .1) * 45) if i == 0 else len(msg)]
        for k, ln in enumerate(wrap(typed, 'sans', 32, 820)[:3]):
            text(img, ln, x + 30, y + 80 + k * 44, 'sans', 32, C['fg'])
    if n > 3:
        rect(d, (60, 1420, 60 + 960 * eo(prog(t, dur * .5, .3)), 1560), C['a2'], r=20)
        if t > dur * .5 + .2:
            text(img, p.get('count', 'SAME INTRO x %d') % n if '%d' in p.get('count', '%d') else p['count'], W / 2, 1445, 'black', 70, C['bg'], anchor='c')
