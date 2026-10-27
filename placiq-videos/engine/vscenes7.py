from vscenes6 import *

# ------------------------------------------------------------- role <-> skill graph
def vroles(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    roles = p.get('roles', [('AI Engineer', 260, 360), ('Data Scientist', 820, 360)])
    skills = p.get('skills', [('Python', 'both'), ('Statistics', 1), ('LLM APIs', 0), ('SQL', 1), ('MLOps', 0), ('Experiment design', 1), ('System design', 0), ('Linear algebra', 'both')])
    for i, (nm, x, y) in enumerate(roles):
        q = eback(prog(t, .1 + i * .3, .4))
        r = 150 * min(1, q)
        d.ellipse((x - r, y - r * .6, x + r, y + r * .6), fill=C['a1'] if i == 0 else C['a2'])
        if q > .8:
            for j, ln in enumerate(wrap(nm, 'black', 44, 260)):
                text(img, ln, x, y - 40 + j * 48, 'black', 44, C['fg_on_a1'] if i == 0 else C['bg'], anchor='c')
    for k, (s, who) in enumerate(skills):
        st = .8 + k * (dur * .6 / len(skills))
        q = eback(prog(t, st, .3))
        if q <= 0:
            continue
        x = 540 + (-300 if who == 0 else 300 if who == 1 else 0) + ((k % 2) * 2 - 1) * 60
        y = 700 + k * 100
        for ri, (nm, rx, ry) in enumerate(roles):
            if who == 'both' or who == ri:
                d.line((x, y + 30, rx, ry + 90), fill=C['a1'] if ri == 0 else C['a2'], width=3)
        tw, _ = tsize(s, 'mono', 32)
        pill(img, d, s, x - (tw + 36) / 2, y, C['fg'] if who == 'both' else C['card'], C['bg'] if who == 'both' else C['fg'], 32, a=min(1, q))
    if t > dur * .8:
        text(img, p.get('foot', 'shared skills in the middle'), W / 2, 1560, 'mono', 34, C['muted'], anchor='c')


# ------------------------------------------------------------- random skill pile -> sorted under chosen role
def vsort(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    chips = p.get('chips', ['Flutter', 'Rust', 'Docker', 'SQL', 'Figma', 'Kotlin', 'Pandas', 'React', 'AWS', 'Go', 'Excel', 'Unity', 'Spark', 'Java', 'GraphQL', 'Linux'])
    keep = set(p.get('keep', ['SQL', 'Pandas', 'Excel', 'Spark', 'Linux']))
    role = p.get('role', 'Target: Data Analyst')
    sq = eio(prog(t, dur * .5, .9)); rnd = random.Random(7)
    kept = [c for c in chips if c in keep]; later = [c for c in chips if c not in keep]
    if sq > 0:
        rect(d, (60, 230, W - 60, 330), C['a1'], r=20)
        text(img, role, W / 2, 248, 'black', 56, C['fg_on_a1'], anchor='c', a=min(1, sq * 2))
        text(img, 'NOW', 120, 380, 'mono', 34, C['a1'], a=sq); text(img, 'LATER (maybe)', 600, 380, 'mono', 34, C['muted'], a=sq)
    for i, c in enumerate(chips):
        fq = eback(prog(t, .05 + i * .12, .35), 1.3)
        if fq <= 0:
            continue
        px = rnd.uniform(80, 760); py = 1450 - (i // 4) * 90 - rnd.uniform(0, 40)
        py = lerp(-100, py, fq)
        if c in keep:
            k = kept.index(c); tx, ty = 120, 450 + k * 110
        else:
            k = later.index(c); tx, ty = 600 + (k % 2) * 200, 450 + (k // 2) * 90
        x = lerp(px, tx, sq); y = lerp(py, ty, sq)
        big = c in keep and sq > .5
        pill(img, d, c, x, y, C['a1'] if big else C['card'], C['fg_on_a1'] if big else (C['muted'] if sq > .5 else C['fg']), 40 if big else 30)


# ------------------------------------------------------------- overwhelming word landscape -> top 3
def vcloud(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    words = p.get('words', ['Kubernetes', 'DP', 'React', 'LLMs', 'System design', 'GraphQL', 'Rust', 'SQL', 'OS', 'CN', 'DBMS', 'Next.js', 'AWS', 'Tries', 'Spring', 'Kafka', 'Go', 'Docker', 'TypeScript', 'ML', 'Graphs', 'Redis'])
    top = p.get('top', [('1', 'Graphs (your weakest DSA area)'), ('2', 'SQL joins (role needs it)'), ('3', 'Ship project M2')])
    cq = eio(prog(t, dur * .45, .7)); rnd = random.Random(5)
    for i, w in enumerate(words):
        sz = int(rnd.uniform(36, 96)); x = rnd.uniform(40, 800); y = rnd.uniform(240, 1450)
        q = prog(t, i * .07, .3)
        if q <= 0:
            continue
        x += math.sin(t * 1.5 + i) * 20; y += math.cos(t * 1.3 + i) * 20 + cq * 1600 * (1 if i % 2 else -1)
        text(img, w, x, y, 'black', sz, C['fg'] if i % 3 else C['muted'], a=q * (1 - cq))
    for i, (n, s) in enumerate(top):
        q = eback(prog(t, dur * .55 + i * .3, .35))
        if q <= 0:
            continue
        y = 420 + i * 300
        text(img, n, 90, y - 20, 'black', 180, C['a1'], a=min(1, q))
        for j, ln in enumerate(wrap(s, 'black', 54, 680)):
            text_mask_up(img, ln, 300, y + 20 + j * 62, 'black', 54, C['fg'], q)


# ------------------------------------------------------------- comparison feed (fictional, humorous)
def vfeed(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    posts = p.get('posts', [('Rohan (fictional)', 'Thrilled to announce I woke up at 4 AM and solved 47 Hards'), ('Ananya (fictional)', 'Built an AGI startup over the weekend. Humbled.'),
                            ('Dev (fictional)', 'Day 1 of college: offer from 6 FAANGs'), ('Ishita (fictional)', 'Leaving my 3rd internship to start my 4th'),
                            ('Kunal (fictional)', 'My cat just merged a PR to the Linux kernel'), ('Sana (fictional)', 'Grateful to share: 12 certificates this week')])
    scroll = t * 420 * (1 - .8 * prog(t, dur * .7, .5))
    for i, (who, txt) in enumerate(posts * 2):
        y = 260 + i * 420 - scroll
        if y < -400 or y > H:
            continue
        rect(d, (60, y, W - 60, y + 380), C['card'], r=24)
        d.ellipse((90, y + 30, 170, y + 110), fill=C['a1'] if i % 2 else C['a2'])
        text(img, who, 190, y + 45, 'black', 36, C['fg'])
        for j, ln in enumerate(wrap(txt, 'sans', 40, 860)):
            text(img, ln, 90, y + 140 + j * 52, 'sans', 40, C['fg'])
        text(img, '%dk reactions' % (3 + i * 7), 90, y + 320, 'monor', 26, C['muted'])
    if t > dur * .72:
        rect(d, (60, 1300, W - 60, 1560), C['fg'], r=30)
        head(img, p.get('verdict', 'Compare with last-month you. Not their highlight reel.'), 1335, t, dur * .72, 54, C['bg'], C, maxw=900)


# ------------------------------------------------------------- deadline multiverse calendar
def vcal(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    evs = p.get('evs', [('DBMS assignment', 2, 1), ('OA: 10 AM', 2, 2), ('Project review', 2, 3), ('TPO: resume due', 2, 0), ('Mid-sem', 3, 1), ('Hackathon', 2, 4)])
    cw, ch = 140, 170; x0, y0 = 50, 330
    days = 'MON TUE WED THU FRI SAT SUN'.split()
    for i, dn in enumerate(days):
        text(img, dn, x0 + i * cw + cw / 2, y0 - 60, 'mono', 26, C['muted'], anchor='c')
    for r in range(5):
        for c in range(7):
            d.rectangle((x0 + c * cw, y0 + r * ch, x0 + (c + 1) * cw - 6, y0 + (r + 1) * ch - 6), outline=C['line'], width=2)
            text(img, str(r * 7 + c + 1), x0 + c * cw + 10, y0 + r * ch + 8, 'monor', 22, C['muted'])
    col_t = dur * .4
    for i, (nm, dc, row) in enumerate(evs):
        q = eback(prog(t, .2 + i * .25, .35))
        if q <= 0:
            continue
        tx, ty = x0 + dc * cw + 10, y0 + 2 * ch + 40
        sx, sy = x0 + (i % 7) * cw + 10, y0 + row * ch + 50
        cq = eio(prog(t, col_t + i * .1, .5))
        x = lerp(sx, tx, cq) + math.sin(t * 30 + i) * 8 * cq; y = lerp(sy, ty + i * 14, cq)
        rect(d, (x, y, x + 300, y + 66), [C['a1'], C['a2'], C['fg']][i % 3], r=12)
        text(img, nm, x + 14, y + 16, 'mono', 26, C['fg_on_a1'] if i % 3 == 0 else C['bg'])
    if t > dur * .75:
        head(img, p.get('verdict', 'Same Wednesday. Every deadline.'), 1250, t, dur * .75, 70, C['fg'], C)


# ------------------------------------------------------------- diverging paths -> choose one
def vpaths(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    paths = p.get('paths', ['Web dev', 'ML engineer', 'Data analyst', 'DevOps', 'Android', 'Cybersec'])
    pick = p.get('pick', 2); ch = prog(t, dur * .55, .6)
    sx, sy = W / 2, 1480
    for i, nm in enumerate(paths):
        ex = 90 + i * (900 / (len(paths) - 1)); ey = 380
        q = eo(prog(t, .1 + i * .12, .7))
        pts = [(lerp(sx, ex, k / 30), lerp(sy, ey, k / 30) - math.sin(k / 30 * math.pi) * (i - 2.5) * 30) for k in range(int(30 * q) + 1)]
        on = i == pick and ch > 0
        col = C['a1'] if on else (C['line'] if ch > .5 else C['muted'])
        if len(pts) > 1:
            d.line(pts, fill=col, width=18 if on else 8)
        if q > .9:
            tw, _ = tsize(nm, 'mono', 28)
            pill(img, d, nm, max(30, min(W - tw - 70, ex - tw / 2 - 18)), ey - 80 - (i % 2) * 60, C['a1'] if on else C['card'], C['fg_on_a1'] if on else C['fg'], 28)
    d.ellipse((sx - 40, sy - 40, sx + 40, sy + 40), fill=C['fg'])
    text(img, 'YOU', sx, sy + 50, 'black', 44, C['fg'], anchor='c')
    if ch > .6:
        pill(img, d, p.get('label', 'one focus. depth beats breadth.'), W / 2, 1600, C['fg'], C['bg'], 36, anchor='c')


# ------------------------------------------------------------- data packet dropped at each tool handoff
def vpacket(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    tools = p.get('tools', ['DSA site', 'Notes app', 'AI chat', 'Resume doc', 'Job portal'])
    fixed = t > dur * .6
    for i, tl in enumerate(tools):
        y = 280 + i * 250
        rect(d, (260, y, 820, y + 150), C['card'] if not fixed else C['a1'], r=24, outline=C['fg'], width=3)
        text(img, tl if not fixed else ['Placiq: DSA', 'Placiq: PCME', 'Placiq: Copilot', 'Placiq: Resume', 'Placiq: Passport'][i], W / 2, y + 48, 'black', 48, C['fg'] if not fixed else C['fg_on_a1'], anchor='c')
    seg = (dur * .6) / len(tools)
    if not fixed:
        i = min(len(tools) - 1, int(t / seg)); lt = (t - i * seg) / seg
        y = 280 + i * 250 + 75 + lt * 250
        drop = lt > .55
        x = 900 + (lt - .55) * 400 * drop
        yy = y + (lt - .55) ** 2 * 900 * drop
        rect(d, (x - 50, yy - 30, x + 50, yy + 30), C['a2'], r=10)
        text(img, 'ctx', x, yy - 20, 'mono', 28, C['bg'], anchor='c')
        if drop:
            text(img, 'LOST', 900, 280 + i * 250 + 40, 'black', 44, C['a2'], anchor='c')
    else:
        lt = ((t - dur * .6) * 1.2) % 1
        y = 355 + lt * 1000
        rect(d, (W / 2 + 330, y - 30, W / 2 + 430, y + 30), C['a2'], r=10)
        d.line((W / 2 + 380, 355, W / 2 + 380, 1355), fill=C['a2'], width=6)


# ------------------------------------------------------------- five tools, five versions of one student
def vconflict(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    rows = p.get('rows', [('DSA site', 'Level: Beginner'), ('Course app', 'Level: Advanced'), ('Resume', 'Skills: 14'), ('AI chat', 'Who are you?'), ('Spreadsheet', 'Progress: 63%?')])
    for i, (tool, val) in enumerate(rows):
        q = eback(prog(t, .1 + i * .3, .35))
        if q <= 0:
            continue
        y = 300 + i * 220; sh = math.sin(t * 18 + i) * 6 * (t < dur * .7)
        rect(d, (60 + sh, y, 60 + 960 * min(1, q) + sh, y + 180), C['card'], r=24)
        text(img, tool.upper(), 100 + sh, y + 24, 'mono', 30, C['muted'])
        text(img, 'Aarav (fictional): ' + val, 100 + sh, y + 80, 'black', 46, C['fg'])
    if t > dur * .7:
        rect(d, (60, 1420, 1020, 1580), C['a1'], r=24)
        head(img, p.get('verdict', 'Five tools. Five different Aaravs.'), 1455, t, dur * .7, 60, C['fg_on_a1'], C)


# ------------------------------------------------------------- comic panels (fictional narrative)
def vcomic(img, d, t, S, C):
    p = S['p']; dur = S['dur']; panels = p['panels']
    seg = dur / len(panels)
    for i, (tag, line, icon) in enumerate(panels):
        st = i * seg
        q = eo5(prog(t, st, .35))
        if q <= 0:
            continue
        x = 60 + (i % 2) * 490; y = 240 + (i // 2) * 440
        w, h = 470, 420
        rect(d, (x, y + (1 - q) * 60, x + w, y + h + (1 - q) * 60), C['card'], outline=C['fg'], width=6)
        text(img, tag, x + 20, y + 16, 'mono', 26, C['a2'])
        # stick figure + icon
        fx, fy = x + 110, y + 150 + math.sin(t * 3 + i) * 6
        d.ellipse((fx - 36, fy - 110, fx + 36, fy - 38), outline=C['fg'], width=6)
        d.line((fx, fy - 38, fx, fy + 60), fill=C['fg'], width=6)
        d.line((fx - 50, fy, fx + 50, fy - 20 if i % 2 else fy + 10), fill=C['fg'], width=6)
        d.line((fx, fy + 60, fx - 40, fy + 130), fill=C['fg'], width=6); d.line((fx, fy + 60, fx + 40, fy + 130), fill=C['fg'], width=6)
        rect(d, (x + 200, y + 110, x + 440, y + 250), C['a1'] if i == len(panels) - 1 else C['bg2'], r=14)
        text(img, icon, x + 320, y + 140, 'black', 60, C['fg_on_a1'] if i == len(panels) - 1 else C['fg'], anchor='c')
        for j, ln in enumerate(wrap(line, 'sans', 30, 420)[:3]):
            text(img, ln, x + 20, y + 300 + j * 38, 'sans', 30, C['fg'])


# ------------------------------------------------------------- the Placiq loop (vertical)
def vloop7(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    steps = ['Diagnose', 'Prioritize', 'Learn', 'Build', 'Evidence', 'Present', 'Reassess']
    rts = disp_reveal_times(S, len(steps)) if S.get('vo') is not None else [.3 + i * dur * .1 for i in range(7)]
    cx, cy, R = W / 2, 820, 380
    cur = max([i for i, r in enumerate(rts) if t >= r] or [-1])
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=C['line'], width=8)
    if cur >= 0:
        frac = (cur + eo(prog(t, rts[cur], .3))) / 7
        if cur == 6 and t > rts[6] + .4:
            frac = 1 + ((t - rts[6] - .4) * .4) % 1
        d.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * min(frac, 1), fill=C['a1'], width=20)
        if frac > 1:
            a = math.radians(-90 + 360 * (frac - 1)); d.ellipse((cx + R * math.cos(a) - 24, cy + R * math.sin(a) - 24, cx + R * math.cos(a) + 24, cy + R * math.sin(a) + 24), fill=C['a2'])
    for i, s in enumerate(steps):
        a = math.radians(-90 + 360 * i / 7); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        on = i <= cur
        d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=C['a1'] if on else C['card'], outline=C['fg'], width=4)
        lx = x + (50 if math.cos(a) > .1 else -50 if math.cos(a) < -.1 else 0)
        anc = 'l' if math.cos(a) > .1 else 'r' if math.cos(a) < -.1 else 'c'
        ly = y - 22 + (-70 if abs(math.cos(a)) <= .1 else 0)
        text(img, s.upper(), lx, ly, 'mono', 32, C['fg'] if on else C['muted'], anchor=anc)
    if cur >= 0:
        text_mask_up(img, steps[cur].upper(), cx, cy - 60, 'black', 90 if len(steps[cur]) < 9 else 74, C['fg'], prog(t, rts[cur], .25), anchor='c')
    text(img, p.get('center', 'one connected loop'), cx, cy + 50, 'serif', 50, C['a2'], anchor='c')


# ------------------------------------------------------------- continuous match-cut morph: tab -> card -> node -> passport
def vmorph(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    stages = p.get('stages', [('tab', 'a browser tab'), ('card', 'a practice card'), ('node', 'a connected node'), ('passport', 'a readiness record')])
    seg = dur / len(stages); i = min(len(stages) - 1, int(t / seg)); lt = (t - i * seg) / seg
    k = eio(clamp((lt - .6) / .4))
    shapes = {'tab': (700, 110, 20), 'card': (600, 360, 30), 'node': (300, 300, 150), 'passport': (620, 820, 40)}
    a = shapes[stages[i][0]]; b = shapes[stages[min(i + 1, len(stages) - 1)][0]]
    w, h, r = [lerp(a[j], b[j], k) for j in range(3)]
    cx, cy = W / 2, 800
    rot = math.sin(t * 1.5) * 4
    col = [C['card'], C['a2'], C['a1'], C['a1']][i]
    layer = Image.new('RGBA', (int(w) + 4, int(h) + 4), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle((2, 2, w, h), max(1, min(r, w / 2 - 8, h / 2 - 8)), fill=col, outline=C['fg'], width=5)
    layer = layer.rotate(rot, expand=True, resample=Image.BILINEAR)
    paste(img, layer, cx - layer.size[0] / 2, cy - layer.size[1] / 2)
    if k < .2:
        lab = {'tab': 'LeetCode - Two Sum', 'card': 'Hashing 14/20', 'node': 'DSA', 'passport': 'SKILL PASSPORT'}[stages[i][0]]
        text(img, lab, cx, cy - 30, 'black', 46, C['fg'] if i == 0 else C['fg_on_a1'], anchor='c')
        if stages[i][0] == 'node':
            for j in range(5):
                an = math.radians(j * 72 + t * 40); ex, ey = cx + 340 * math.cos(an), cy + 340 * math.sin(an)
                d.line((cx + 150 * math.cos(an), cy + 150 * math.sin(an), ex, ey), fill=C['a1'], width=5)
                d.ellipse((ex - 34, ey - 34, ex + 34, ey + 34), fill=C['card'], outline=C['fg'], width=3)
    head(img, stages[i][1], 1350, lt * seg, .05, 72, C['fg'], C, 'serif')


VSCENES.update(vroles=vroles, vsort=vsort, vcloud=vcloud, vfeed=vfeed, vcal=vcal, vpaths=vpaths, vpacket=vpacket, vconflict=vconflict,
               vcomic=vcomic, vloop7=vloop7, vmorph=vmorph)
