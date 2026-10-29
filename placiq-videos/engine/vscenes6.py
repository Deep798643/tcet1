from vscenes5 import *

# ------------------------------------------------------------- vertical contribution grid explodes -> what matters
def vgrid(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    cols, rows, cs = 7, 26, 40
    x0 = W / 2 - cols * (cs + 8) / 2 - 200; y0 = 230
    rnd = random.Random(12)
    ex = eo(prog(t, dur * .45, .9))
    greens = [(14, 68, 41), (0, 109, 50), (38, 166, 65), (57, 211, 83)]
    for r in range(rows):
        for c in range(cols):
            lv = rnd.random(); a = rnd.uniform(0, 6.28); sp = rnd.uniform(300, 1200)
            on = t > (r / rows) * dur * .35
            col = greens[int(lv * 3.99)] if on and lv > .15 else C['line']
            x = x0 + c * (cs + 8) + math.cos(a) * sp * ex; y = y0 + r * (cs + 8) + math.sin(a) * sp * ex
            d.rounded_rectangle((x, y, x + cs, y + cs), 7, fill=col)
    if ex < .3:
        text(img, '365 days', x0 + cols * (cs + 8) + 40, y0, 'mono', 34, C['muted'])
        text(img, 'all green.', x0 + cols * (cs + 8) + 40, y0 + 50, 'black', 64, C['fg'])
    items = p.get('items', ['What did you build?', 'Why that design?', 'What broke, how you fixed it', 'Can someone run it?'])
    for i, it in enumerate(items):
        q = eback(prog(t, dur * .55 + i * .3, .3))
        if q > 0:
            rect(d, (80, 520 + i * 200, 80 + 920 * min(1, q), 680 + i * 200), C['a1'] if i % 2 == 0 else C['card'], r=24)
            if q > .8:
                text(img, it, 120, 570 + i * 200, 'black', 54, C['fg_on_a1'] if i % 2 == 0 else C['fg'])


# ------------------------------------------------------------- project printed as a receipt
def vreceipt(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    items = p.get('items', [('ARCHITECTURE.md', '1'), ('commits', '61'), ('tests passing', '18'), ('decisions logged', '7'), ('bugs fixed', '12'), ('live demo', '1')])
    q = eo(prog(t, .2, dur * .65))
    h = 300 + 900 * q
    x0 = 190; w = 700
    rect(d, (x0 - 40, 230, x0 + w + 40, 300), C['fg'], r=20)  # printer
    rect(d, (x0 - 10, 270, x0 + w + 10, 290), C['muted'])
    paper = Image.new('RGBA', (w, int(h)), (250, 248, 242, 255)); pd = ImageDraw.Draw(paper)
    ink = (20, 20, 20)
    text(paper, p.get('shop', 'PROJECT: SplitIt'), w / 2, 30, 'mono', 40, ink, anchor='c')
    text(paper, '--------------------------------', w / 2, 90, 'monor', 28, ink, anchor='c')
    for i, (k, v) in enumerate(items):
        y = 150 + i * 110
        if y > h - 120:
            break
        text(paper, k, 40, y, 'mono', 34, ink); text(paper, v, w - 40, y, 'mono', 34, ink, anchor='r')
    if h > 150 + len(items) * 110 + 100:
        y = 150 + len(items) * 110
        text(paper, 'TOTAL', 40, y + 20, 'black', 56, ink)
        text(paper, 'EVIDENCE', w - 40, y + 20, 'black', 56, (49, 81, 238), anchor='r')
    for zx in range(0, w, 30):  # zigzag edge
        pd.polygon([(zx, h - 1), (zx + 15, h - 16), (zx + 30, h - 1)], fill=C['bg'])
    paste(img, paper, x0, 290)


# ------------------------------------------------------------- messy repo -> README walkthrough
def vreadme(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    sw = dur * .35
    rect(d, (60, 230, W - 60, 1460), C['bg2'], r=24)
    if t < sw:
        files = ['final.py', 'final2.py', 'test (1).py', 'app_old.js', 'new folder/', 'node_modules/', 'README.md  (empty)']
        for i, f in enumerate(files):
            text(img, ('  ' if i else '') + f, 100, 290 + i * 80, 'mono', 40, C['a2'] if 'empty' in f else C['fg'], a=prog(t, i * .1, .2))
        head(img, '"what does this do?"', 1000, t, .8, 64, C['muted'], C, 'serif')
        return
    secs = p.get('secs', [('# SplitIt', 'Split bills in hostel groups.'), ('## Run it', 'docker compose up'), ('## How it works', 'API -> ledger -> Postgres'),
                          ('## Decisions', 'Why Postgres, not Mongo'), ('## Tests', 'pytest  (18 passing)')])
    for i, (h_, b) in enumerate(secs):
        q = eo5(prog(t, sw + i * .4, .35))
        if q <= 0:
            continue
        y = 280 + i * 230
        text_mask_up(img, h_, 100, y, 'black', 60, C['a1'] if i == 0 else C['fg'], q)
        rect(d, (100, y + 90, 100 + 860 * q, y + 170), C['card'], r=12)
        text(img, b, 130, y + 108, 'mono', 36, C['fg'], a=q)


# ------------------------------------------------------------- certificate mountain vs working demo
def vmountain(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    N = 26; rnd = random.Random(3)
    for i in range(N):
        q = eback(prog(t, i * .12, .3), 1.2)
        if q <= 0:
            continue
        row = 0; k = i; cnt = 7
        while k >= cnt:
            k -= cnt; cnt -= 1; row += 1
        x = 60 + row * 32 + k * 132 + rnd.uniform(-8, 8)
        y = 1380 - row * 110 - (1 - q) * 600
        rect(d, (x, y, x + 120, y + 90), C['card'], outline=C['a3'] if not C['dark'] else C['muted'], width=3)
        d.ellipse((x + 44, y + 50, x + 76, y + 82), fill=C['a2'])
        d.line((x + 14, y + 20, x + 106, y + 20), fill=C['muted'], width=4)
    dq = eo5(prog(t, dur * .55, .5))
    if dq > 0:
        rect(d, (W - 60 - 520 * dq, 260, W - 60, 760), C['fg'], r=24)
        if dq > .9:
            text(img, 'localhost:3000', W - 540, 290, 'mono', 26, C['muted'])
            rect(d, (W - 540, 340, W - 100, 420), C['a1'], r=12)
            text(img, 'SplitIt  -  live', W - 520, 358, 'black', 36, C['fg_on_a1'])
            for k in range(3):
                rect(d, (W - 540, 450 + k * 90, W - 140 - k * 60, 510 + k * 90), C['muted'], r=10)
    if t > dur * .75:
        head(img, p.get('verdict', 'Certificates show you learned. Demos show you can build.'), 860, t, dur * .75, 58, C['fg'], C, maxw=520, x=500)


# ------------------------------------------------------------- winding evidence trail
def vtrail(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    nodes = p.get('nodes', ['DSA: hashing 14/20', 'Project M1: auth', 'commit: rate limiter', 'tests: 18 passing', 'resume: new bullet', 'mock: explained design'])
    rts = disp_reveal_times(S, len(nodes))
    pts = [(250 if i % 2 == 0 else 830, 300 + i * 220) for i in range(len(nodes))]
    for i in range(1, len(pts)):
        q = eo(prog(t, rts[i] - .3, .35))
        if q <= 0:
            continue
        a, b = pts[i - 1], pts[i]
        segs = 20
        pts_ = [(lerp(a[0], b[0], k / segs), lerp(a[1], b[1], k / segs) + math.sin(k / segs * math.pi) * 40) for k in range(int(segs * q) + 1)]
        for k in range(0, len(pts_) - 1, 2):
            d.line(pts_[k] + pts_[k + 1], fill=C['a1'], width=10)
    for i, (x, y) in enumerate(pts):
        q = eback(prog(t, rts[i], .3))
        if q <= 0:
            continue
        d.ellipse((x - 30 * q, y - 30 * q, x + 30 * q, y + 30 * q), fill=C['a2'])
        tw, _ = tsize(nodes[i], 'mono', 34)
        lx = min(max(60, x - tw / 2), W - tw - 60)
        pill(img, d, nodes[i], lx, y + 44, C['fg'], C['bg'], 34, a=min(1, q))


# ------------------------------------------------------------- interview: candidate rewinds own commit history
def vrewind(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    rect(d, (60, 230, W - 60, 470), C['a1'], r=30)
    text(img, 'INTERVIEWER', 100, 255, 'mono', 28, C['fg_on_a1'])
    head(img, p.get('q', '"Why did you add a queue here?"'), 310, t, .1, 56, C['fg_on_a1'], C, 'black', 880, x=100)
    commits = p.get('commits', [('a1f3', 'add retry queue for payments'), ('9c2e', 'fix: duplicate charge on timeout'), ('77b0', 'bench: sync calls p95 2.4s'),
                                ('3d18', 'design note: why async'), ('e5aa', 'initial payment API')])
    rw = prog(t, dur * .3, dur * .5)
    for i, (h_, m) in enumerate(commits):
        q = eo(prog(t, .5 + i * .12, .3))
        y = 560 + i * 150
        act = rw > 0 and int(rw * len(commits)) == i
        rect(d, (100, y, 100 + 880 * q, y + 120), C['a2'] if act else C['card'], r=16)
        d.ellipse((60, y + 40, 100, y + 80), fill=C['a1'] if rw * len(commits) > i else C['line'])
        text(img, h_, 130, y + 14, 'mono', 28, C['bg'] if act else C['muted'], a=q)
        text(img, m, 130, y + 56, 'sans', 36, C['bg'] if act else C['fg'], a=q)
    if rw > 0 and rw < 1:
        text(img, '<< rewinding', W - 80, 500, 'mono', 32, C['a2'], anchor='r')
    if t > dur * .82:
        pill(img, d, p.get('label', 'answers from your own history'), W / 2, 1400, C['fg'], C['bg'], 38, anchor='c')


# ------------------------------------------------------------- skill passport stamps
def vpassport(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    op = eio(prog(t, .1, .6))
    rect(d, (90, 260, 990, 1460), C['a1'], r=36)
    if op < 1:
        text(img, 'SKILL', W / 2, 600, 'black', 120, C['fg_on_a1'], anchor='c', a=1 - op)
        text(img, 'PASSPORT', W / 2, 740, 'black', 120, C['fg_on_a1'], anchor='c', a=1 - op)
    rect(d, (120, 290, 120 + 840 * op, 1430), (250, 248, 242), r=24)
    stamps = p.get('stamps', [('DSA', 'patterns'), ('PROJECT', 'shipped'), ('RESUME', 'reviewed'), ('GITHUB', 'evidence'), ('MOCK', 'practised'), ('READY', '+ trending')])
    rts = disp_reveal_times(S, len(stamps)) if S.get('vo') is not None else [.8 + i * (dur * .6 / len(stamps)) for i in range(len(stamps))]
    for i, (a, b) in enumerate(stamps):
        q = prog(t, rts[i], .25)
        if q <= 0 or op < 1:
            continue
        sc = 1.6 - .6 * eo5(q)
        col = [C['a1'], C['a2'], (29, 185, 84), (15, 17, 23), C['a1'], C['a2']][i % 6]
        st = Image.new('RGBA', (360, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((6, 6, 354, 194), 20, outline=col, width=10)
        text(st, a, 180, 30, 'black', 64, col, anchor='c'); text(st, b, 180, 120, 'mono', 32, col, anchor='c')
        st = st.rotate([-8, 6, -4, 9, -6, 4][i], expand=True, resample=Image.BILINEAR)
        sw_, sh_ = int(st.size[0] * sc), int(st.size[1] * sc)
        st = st.resize((sw_, sh_))
        cx = 330 + (i % 2) * 420; cy = 470 + (i // 2) * 330
        paste(img, st, cx - sw_ / 2, cy - sh_ / 2, min(1, q * 2))


VSCENES.update(vgrid=vgrid, vreceipt=vreceipt, vreadme=vreadme, vmountain=vmountain, vtrail=vtrail, vrewind=vrewind, vpassport=vpassport)
