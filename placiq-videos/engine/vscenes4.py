from vscenes3 import *

# ------------------------------------------------------------- conveyor factory: different inputs -> identical outputs
def vfactory(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    ins = p.get('inputs', ['Riya - ECE, loves data', 'Kabir - CSE, backend', 'Meera - IT, ML research', 'Arjun - Mech -> SDE'])
    out = p.get('output', 'Generic roadmap: 1. Learn DSA 2. Build projects 3. Apply')
    belt_y = 980
    rect(d, (0, belt_y, W, belt_y + 40), C['fg'])
    for k in range(14):
        x = (k * 90 - t * 240) % (W + 90) - 45
        d.line((x, belt_y + 5, x + 30, belt_y + 35), fill=C['bg'], width=6)
    rect(d, (W / 2 - 170, belt_y - 380, W / 2 + 170, belt_y), C['a1'], r=20)
    text(img, p.get('machine', 'ADVICE-O-MATIC'), W / 2, belt_y - 330, 'mono', 32, C['fg_on_a1'], anchor='c')
    gear = t * 180
    for gx in (-70, 70):
        cx, cy = W / 2 + gx, belt_y - 190
        for a in range(0, 360, 45):
            r = math.radians(a + gear * (1 if gx < 0 else -1))
            d.line((cx, cy, cx + 60 * math.cos(r), cy + 60 * math.sin(r)), fill=C['fg_on_a1'], width=14)
        d.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=C['fg_on_a1'])
    period = dur * .8 / len(ins)
    for i, s in enumerate(ins):
        lt = t - i * period
        if lt < 0:
            continue
        x = -420 + lt * 520
        if x < W / 2 - 300:  # input card on belt
            rect(d, (x, belt_y - 160, x + 380, belt_y - 10), C['card'], r=16, outline=C['fg'], width=3)
            for j, ln in enumerate(wrap(s, 'black', 34, 340)):
                text(img, ln, x + 20, belt_y - 140 + j * 40, 'black', 34, C['fg'])
        elif x > W / 2 + 170:  # identical output
            ox = x - 100
            rect(d, (ox, belt_y - 170, ox + 420, belt_y - 10), C['a2'], r=16)
            for j, ln in enumerate(wrap(out, 'mono', 26, 380)[:4]):
                text(img, ln, ox + 18, belt_y - 155 + j * 34, 'mono', 26, C['bg'])
    q = prog(t, dur * .55, .4)
    if q > 0:
        head(img, p.get('verdict', 'Four students. One copy-paste roadmap.'), 1180, t, dur * .55, 70, C['fg'], C)


# ------------------------------------------------------------- split screen: N AI panes compete
def vsplit(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    msgs = p.get('msgs', ['Learn Rust!', 'Do 500 LC Qs', 'Build an LLM', 'Try Web3', 'Master DevOps'])
    win = dur * p.get('win', .7)
    wq = eio(prog(t, win, .6))
    for i, m in enumerate(msgs):
        q = eback(prog(t, .1 + i * .25, .3))
        if q <= 0:
            continue
        x = 60 + (i % 2) * 490; y = 230 + (i // 2) * 400
        if i == len(msgs) - 1 and len(msgs) % 2:
            x = W / 2 - 220
        sh = (math.sin(t * 23 + i * 2) * 10) * (1 - wq)
        a = 1 - wq * .8
        layer = Image.new('RGBA', (440, 360), C['card']); ld = ImageDraw.Draw(layer)
        ld.rectangle((0, 0, 440, 54), fill=C['a2'] if i % 2 else C['a1'])
        text(layer, 'AI tab %d' % (i + 1), 20, 10, 'mono', 28, C['bg'] if i % 2 else C['fg_on_a1'])
        for j, ln in enumerate(wrap(m, 'black', 52, 400)):
            text(layer, ln, 20, 90 + j * 58, 'black', 52, C['fg'])
        text(layer, 'trust me bro', 20, 300, 'serif', 36, C['muted'])
        paste(img, layer, x + sh, y, a * min(1, q))
    if wq > 0:
        w = 960 * wq
        rect(d, (W / 2 - w / 2, 800, W / 2 + w / 2, 1240), C['a1'], r=30)
        if wq > .8:
            head(img, p.get('win_txt', 'One tutor that knows your work.'), 860, t, win + .5, 74, C['fg_on_a1'], C, maxw=860)


# ------------------------------------------------------------- scattered chips snap into a vertical timeline
def vtimeline(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    items = p.get('items', [('Mon', 'solved 3 sliding-window Qs'), ('Tue', 'chat app: auth module'), ('Wed', 'resume: added metrics'),
                            ('Thu', 'mock: weak on DP'), ('Fri', 'DP: 4 problems'), ('Sat', 'GitHub: README pushed')])
    snap = dur * p.get('snap', .3)
    rnd = random.Random(2)
    d.line((180, 300, 180, 300 + (len(items) - 1) * 190 * eo(prog(t, snap, .8))), fill=C['a1'], width=8)
    for i, (dday, txt) in enumerate(items):
        sx, sy = rnd.uniform(100, 700), rnd.uniform(250, 1400)
        tx, ty = 230, 270 + i * 190
        q = eio(prog(t, snap + i * .18, .5))
        x, y = lerp(sx, tx, q), lerp(sy, ty, q)
        x += math.sin(t * 3 + i) * 20 * (1 - q); y += math.cos(t * 2 + i) * 20 * (1 - q)
        rect(d, (x, y, x + 780, y + 120), C['card'], r=18, outline=C['a1'] if q > .9 else C['line'], width=3)
        text(img, dday.upper(), x + 24, y + 14, 'mono', 28, C['a2'])
        text(img, txt, x + 24, y + 54, 'black', 40 if len(txt) < 26 else 34, C['fg'])
        if q > .9:
            d.ellipse((180 - 18, ty + 42, 180 + 18, ty + 78), fill=C['a1'])
    if t > snap + len(items) * .18 + .6:
        pill(img, d, p.get('label', 'PCME: one memory, every session'), W / 2, 1460, C['a1'], C['fg_on_a1'], 36, anchor='c')


# ------------------------------------------------------------- arrays: hashmap two-sum / chaos pointer / sliding window / binary search
def varr(img, d, t, S, C):
    p = S['p']; dur = S['dur']; mode = p.get('mode', 'hash')
    vals = p.get('vals', [2, 7, 11, 15, 1, 8]); target = p.get('target', 9)
    n = len(vals); bw = min(140, 900 // n - 14); gap = 14
    x0 = W / 2 - (n * bw + (n - 1) * gap) / 2; y0 = 520
    steps = p.get('steps', n)
    si = min(steps - 1, int(prog(t, .5, dur * .7) * steps))
    hl = set(); ptr = []
    if mode == 'hash':
        i = min(si, n - 1); hl = {i}; ptr = [('i', i, C['a2'])]
    elif mode == 'chaos':
        chaos = t < dur * .45
        i = random.Random(int(t * 4)).randint(0, n - 1) if chaos else min(n - 1, int(prog(t, dur * .5, dur * .4) * n))
        hl = {i}; ptr = [('p', i, C['a2'] if chaos else C['a1'])]
    elif mode == 'window':
        k = p.get('k', 3); i = min(n - k, si); hl = set(range(i, i + k)); ptr = [('L', i, C['a2']), ('R', i + k - 1, C['a1'])]
    elif mode == 'binary':
        lo, hi = 0, n - 1; tg = target; path = []
        while lo <= hi:
            mid = (lo + hi) // 2; path.append((lo, hi, mid))
            if vals[mid] == tg: break
            lo, hi = (mid + 1, hi) if vals[mid] < tg else (lo, mid - 1)
        lo, hi, mid = path[min(len(path) - 1, si)]
        hl = {mid}; ptr = [('lo', lo, C['a2']), ('mid', mid, C['a1']), ('hi', hi, C['muted'])]
    for k_, v in enumerate(vals):
        q = eback(prog(t, .04 * k_, .3)); x = x0 + k_ * (bw + gap)
        on = k_ in hl
        dim = mode == 'binary' and not (ptr[0][1] <= k_ <= ptr[2][1])
        rect(d, (x, y0 + (1 - q) * 150, x + bw, y0 + bw + (1 - q) * 150), C['a1'] if on else (C['bg2'] if dim else C['card']), r=16, outline=C['fg'], width=3)
        text(img, str(v), x + bw / 2, y0 + bw * .22, 'black', int(bw * .42), C['fg_on_a1'] if on else (C['muted'] if dim else C['fg']), anchor='c')
        text(img, str(k_), x + bw / 2, y0 + bw + 10, 'monor', 26, C['muted'], anchor='c')
    for j, (lab, idx, col) in enumerate(ptr):
        x = x0 + idx * (bw + gap) + bw / 2; yy = y0 - 40 - j * 0
        d.polygon([(x - 20, yy - 30), (x + 20, yy - 30), (x, yy)], fill=col)
        text(img, lab, x, yy - 100 - (j % 2) * 50, 'black', 48, col, anchor='c')
    yb = y0 + bw + 90
    if mode == 'hash':
        i = min(si, n - 1); seen = {vals[k_]: k_ for k_ in range(i)}
        need = target - vals[i]
        rect(d, (80, yb, 1000, yb + 110), C['fg'], r=16)
        text(img, 'need = %d - %d = %d' % (target, vals[i], need), 110, yb + 28, 'mono', 42, C['bg'])
        text(img, 'HASH MAP  (value -> index)', 80, yb + 150, 'mono', 32, C['muted'])
        for k_, (vv, ii) in enumerate(seen.items()):
            rect(d, (80 + k_ * 180, yb + 200, 240 + k_ * 180, yb + 300), C['a2'] if vv == need else C['card'], r=14, outline=C['fg'], width=2)
            text(img, '%d:%d' % (vv, ii), 160 + k_ * 180, yb + 225, 'black', 40, C['bg'] if vv == need else C['fg'], anchor='c')
        if need in seen:
            pill(img, d, 'FOUND [%d, %d]  in one pass, O(n)' % (seen[need], i), W / 2, yb + 360, C['a1'], C['fg_on_a1'], 38, anchor='c')
    elif mode == 'window':
        k = p.get('k', 3); i = min(n - k, si); s = sum(vals[i:i + k])
        rect(d, (80, yb, 1000, yb + 110), C['fg'], r=16)
        text(img, 'window sum = %d   (+in  -out)' % s, 110, yb + 28, 'mono', 40, C['bg'])
    elif mode == 'binary':
        rect(d, (80, yb, 1000, yb + 110), C['fg'], r=16)
        text(img, 'target %d  |  a[mid] = %d  |  halve it' % (target, vals[ptr[1][1]]), 110, yb + 28, 'mono', 36, C['bg'])
    elif mode == 'chaos':
        rect(d, (80, yb, 1000, yb + 110), C['a2'] if t < dur * .45 else C['a1'], r=16)
        text(img, 'p = ???  (random jumps)' if t < dur * .45 else 'p += 1  (one step, one rule)', 110, yb + 28, 'mono', 40, C['bg'] if t < dur * .45 else C['fg_on_a1'])
    if p.get('title'):
        head(img, p['title'], 200, t, .1, 80, C['fg'], C)


# ------------------------------------------------------------- loop maze with dry-run trace table
def vmaze(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    G = 9; cs = 100; ox, oy = 90, 260
    rnd = random.Random(9)
    for i in range(G + 1):
        for j in range(G):
            if rnd.random() < .55:
                d.line((ox + j * cs, oy + i * cs, ox + (j + 1) * cs, oy + i * cs), fill=C['fg'], width=8)
            if rnd.random() < .55:
                d.line((ox + i * cs, oy + j * cs, ox + i * cs, oy + (j + 1) * cs), fill=C['fg'], width=8)
    clear = dur * .45
    path = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (4, 3), (4, 4), (5, 4), (6, 4), (6, 5), (7, 5), (7, 6), (8, 6), (8, 7), (8, 8)]
    if t < clear:  # lost token wandering
        k = int(t * 6) % 6
        x, y = [(0, 0), (1, 0), (1, 1), (0, 1), (2, 0), (1, 1)][k]
        d.ellipse((ox + x * cs + 25, oy + y * cs + 25, ox + x * cs + 75, oy + y * cs + 75), fill=C['a2'])
        text(img, '?', ox + x * cs + 50, oy + y * cs - 40, 'black', 60, C['a2'], anchor='c')
    else:
        q = prog(t, clear, dur * .4); k = int(q * (len(path) - 1))
        pts = [(ox + x * cs + 50, oy + y * cs + 50) for x, y in path[:k + 1]]
        if len(pts) > 1:
            d.line(pts, fill=C['a1'], width=14)
        x, y = pts[-1]; d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=C['a1'])
        rows = [('i', 'sum', 'arr[i]')] + [(str(r), str(sum(range(r + 1)) * 2), str(r * 2)) for r in range(min(5, 1 + k // 3))]
        for r_, row in enumerate(rows):
            for c_, cell in enumerate(row):
                rect(d, (120 + c_ * 290, 1230 + r_ * 62, 400 + c_ * 290, 1288 + r_ * 62), C['fg'] if r_ == 0 else C['card'])
                text(img, cell, 260 + c_ * 290, 1236 + r_ * 62, 'mono', 34, C['bg'] if r_ == 0 else C['fg'], anchor='c')


# ------------------------------------------------------------- brute force vs optimised race
def vrace(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    q = prog(t, .3, dur * .75)
    nmax = 10000
    nn = int(10 + q * nmax)
    for j, (lab, ops, col, code) in enumerate([('BRUTE FORCE  O(n^2)', nn * nn / 2, C['a2'], 'for i: for j: check a[i]+a[j]'),
                                                ('HASH MAP  O(n)', nn, C['a1'], 'for x: if target-x in seen')]):
        y = 260 + j * 600
        rect(d, (60, y, W - 60, y + 520), C['card'], r=24)
        text(img, lab, 100, y + 30, 'black', 50, col)
        text(img, code, 100, y + 110, 'mono', 32, C['muted'])
        text(img, '{:,} ops'.format(int(ops)), 100, y + 190, 'black', 90, C['fg'])
        # growth curve
        pts = []
        for k in range(60):
            xx = k / 59 * q
            yy = (xx ** 2) if j == 0 else xx * .1
            pts.append((100 + k / 59 * 880, y + 480 - min(1, yy) * 160))
        d.line(pts, fill=col, width=8)
    text(img, 'n = {:,}'.format(nn), W / 2, 1420, 'black', 80, C['fg'], anchor='c')
    if t > dur * .75:
        pill(img, d, p.get('verdict', 'Both correct. One scales.'), W / 2, 1530, C['a1'], C['fg_on_a1'], 42, anchor='c')


# ------------------------------------------------------------- problem cards collapse into patterns
def vcollapse(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    pats = p.get('patterns', ['Two pointers', 'Sliding window', 'Hashing', 'BFS / DFS', 'Binary search', 'Dynamic prog.'])
    N = 180; rnd = random.Random(4)
    cq = eio(prog(t, dur * .4, dur * .35))
    for i in range(N):
        sx, sy = rnd.uniform(30, W - 110), rnd.uniform(220, 1500)
        b = i % len(pats); bx, by = 80 + (b % 2) * 480, 300 + (b // 2) * 380
        x = lerp(sx + math.sin(t * 2 + i) * 15, bx + rnd.uniform(0, 300), cq)
        y = lerp(sy + math.cos(t * 2 + i) * 15, by + 90 + rnd.uniform(0, 150), cq)
        if prog(t, i * .006, .2) > 0:
            d.rounded_rectangle((x, y, x + 80, y + 50), 8, fill=C['card'] if i % 7 else C['a2'], outline=C['line'])
            if cq < .3:
                text(img, '#%d' % (i * 7 % 1803 + 1), x + 6, y + 10, 'monor', 20, C['muted'])
    if cq > .5:
        for b, ptn in enumerate(pats):
            bx, by = 80 + (b % 2) * 480, 300 + (b // 2) * 380
            rect(d, (bx - 10, by, bx + 420, by + 70), C['a1'], r=14)
            text(img, ptn, bx + 14, by + 10, 'black', 42, C['fg_on_a1'], a=min(1, (cq - .5) * 2))


VSCENES.update(vfactory=vfactory, vsplit=vsplit, vtimeline=vtimeline, varr=varr, vmaze=vmaze, vrace=vrace, vcollapse=vcollapse)
