from vscenes4 import *

# ------------------------------------------------------------- real-footage hero reel, cuts on beat between clips
def vreel(img, d, t, S, C):
    p = S['p']; dur = S['dur']; clips = p['clips']; labels = p.get('labels', [])
    seg = dur / len(clips); i = min(len(clips) - 1, int(t / seg)); lt = t - i * seg
    c = clips[i]
    fr_ = clip_frames(c[0]); fr = Image.fromarray(fr_[min(len(fr_) - 1, int((lt + .3) * 30)) % len(fr_)])
    zw = c[3] if len(c) > 3 else .5; ch = min(1, zw * 1280 / .62 / 720)
    k = eio(prog(lt, 0, seg))
    cx0 = lerp(c[1][0], c[2][0], k) * (1 - zw); cy0 = lerp(c[1][1], c[2][1], k) * (1 - ch)
    crop = fr.crop((int(cx0 * 1280), int(cy0 * 720), int((cx0 + zw) * 1280), int((cy0 + ch) * 720)))
    cw = 1000; chh = min(1280, int(cw * crop.size[1] / crop.size[0]))
    punch = 1 + .08 * (1 - eo(prog(lt, 0, .25)))
    cwp = int(cw * punch); chp = int(chh * punch)
    im = crop.resize((cwp, chp), Image.BILINEAR).convert('RGBA'); im.putalpha(round_mask(cwp, chp, 30))
    y0 = 330
    rect(d, (40 - 14, y0 - 14, 40 + cw + 14, y0 + chh + 14), C['a1'], r=40)
    paste(img, im, 40 + (cw - cwp) / 2, y0 + (chh - chp) / 2)
    text(img, 'REAL PLACIQ FOOTAGE  %02d/%02d' % (i + 1, len(clips)), 40, y0 + chh + 30, 'mono', 26, C['muted'])
    if i < len(labels):
        lab = labels[i]
        tw, _ = tsize(lab, 'black', 76)
        sz = min(76, int(76 * 960 / tw))
        rect(d, (40, 170, 40 + (tsize(lab, 'black', sz)[0] + 40) * eo5(prog(lt, .05, .25)), 170 + sz * 1.3), C['fg'])
        text_mask_up(img, lab, 60, 176, 'black', sz, C['bg'], prog(lt, .1, .3))


# ------------------------------------------------------------- tutorial windows vanish -> blank editor
def vvanish(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    names = p.get('names', ['React in 1 hr', 'MERN full course', 'Build Netflix clone', 'DSA in 30 days', 'Next.js crash', 'Docker basics', 'Spring Boot 4h'])
    rnd = random.Random(1); van = dur * .35
    rect(d, (60, 260, W - 60, 1450), C['bg2'], r=24)
    text(img, 'my-project/  main.py', 100, 290, 'mono', 30, C['muted'])
    for ln in range(14):
        text(img, '%2d' % (ln + 1), 100, 360 + ln * 70, 'monor', 30, C['line'])
    if t > van + len(names) * .3 and int(t * 2.5) % 2 == 0:
        d.rectangle((170, 360, 184, 400), fill=C['a1'])
    for i, nm in enumerate(names):
        x = 80 + rnd.uniform(0, 380); y = 300 + rnd.uniform(0, 900)
        q = eback(prog(t, .05 + i * .15, .3))
        gone = prog(t, van + i * .3, .25)
        if q <= 0 or gone >= 1:
            continue
        sc = 1 - eo(gone)
        w, h = 520 * sc, 320 * sc
        cx, cy = x + 260, y + 160
        rect(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), C['fg'], r=16)
        if sc > .6:
            d.polygon([(cx - 30, cy - 40), (cx - 30, cy + 40), (cx + 40, cy)], fill=C['a2'])
            text(img, nm, cx - w / 2 + 20, cy + h / 2 - 60, 'black', 34, C['bg'])
            rect(d, (cx - w / 2, cy + h / 2 - 12, cx - w / 2 + w * (.2 + .7 * ((i * 37) % 10) / 10), cy + h / 2), C['a2'])
    if t > van + len(names) * .3 + .3:
        head(img, p.get('end', 'Now build it. Alone.'), 1500, t, van + len(names) * .3 + .3, 80, C['fg'], C)


# ------------------------------------------------------------- todo clones pile, then a distinct idea
def vclones(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    clones = p.get('clones', ['todo-app', 'todo-app-2', 'weather-app', 'netflix-clone', 'todo-react', 'calculator', 'todo-final', 'tic-tac-toe'])
    idea_t = dur * .55
    for i, c in enumerate(clones):
        q = eback(prog(t, .1 + i * .3, .3), 1.4)
        if q <= 0:
            continue
        x = 90 + (i % 2) * 470; y = 260 + (i // 2) * 250
        fade_ = 1 - .75 * prog(t, idea_t, .4)
        layer = Image.new('RGBA', (430, 220), C['card']); ld = ImageDraw.Draw(layer)
        ld.rectangle((0, 0, 429, 219), outline=C['line'], width=3)
        for k in range(3):
            ld.rectangle((24, 80 + k * 40, 44, 100 + k * 40), outline=C['fg'], width=3)
            ld.line((60, 90 + k * 40, 300 - k * 40, 90 + k * 40), fill=C['line'], width=8)
        text(layer, c, 24, 18, 'mono', 32, C['fg'])
        text(layer, '#%d' % (i + 1), 400, 18, 'black', 32, C['a2'], anchor='r')
        paste(img, layer, x, y + (1 - q) * -300, fade_)
    if t > idea_t:
        q = eback(prog(t, idea_t + .3, .45))
        w = 940 * min(1, q)
        rect(d, (W / 2 - w / 2, 1050, W / 2 + w / 2, 1500), C['a1'], r=30)
        if q > .8:
            head(img, p.get('idea', 'Hostel mess-menu predictor with real feedback data'), 1100, t, idea_t + .6, 60, C['fg_on_a1'], C, maxw=840)
            pill(img, d, 'problem you actually have', W / 2, 1400, C['fg_on_a1'], C['a1'], 30, anchor='c')


# ------------------------------------------------------------- abandoned repo city -> one building completed
def vcity(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    rnd = random.Random(6)
    ground = 1380
    d.rectangle((0, ground, W, H), fill=C['bg2'])
    names = p.get('names', ['chat-app', 'ml-proj', 'portfolio', 'blog', 'game', 'api-v2', 'clone'])
    build_t = dur * .5
    for i, nm in enumerate(names):
        bw = 130; x = 30 + i * 148; full = rnd.uniform(500, 900); done = rnd.uniform(.25, .55)
        hero = i == p.get('hero', 3)
        frac = done if not hero else lerp(done, 1, eio(prog(t, build_t, dur * .35)))
        q = eo(prog(t, .1 + i * .1, .5))
        h = full * frac * q
        rect(d, (x, ground - h, x + bw, ground), C['a1'] if hero and frac > .95 else C['card'], outline=C['line'], width=2)
        for wy in range(int(ground - h + 30), ground - 30, 60):
            for wx in (x + 22, x + 76):
                lit = hero and frac > .95 or rnd.random() < .15
                d.rectangle((wx, wy, wx + 30, wy + 30), fill=C['a3'] if lit else C['bg'])
        # scaffolding on unfinished
        if frac < .95:
            top = ground - full * q
            for sy in range(int(top), int(ground - h), 40):
                d.line((x, sy, x + bw, sy + 40), fill=C['muted'], width=2)
            d.rectangle((x, top, x + bw, ground - h), outline=C['muted'], width=2)
        text(img, nm, x + bw / 2, ground + 20, 'monor', 22, C['fg'], anchor='c')
        if not hero:
            text(img, 'last commit: %d mo' % (2 + i), x + bw / 2, ground + 55, 'monor', 18, C['a2'], anchor='c')
    # crane
    if t > build_t - .5:
        hx = 30 + p.get('hero', 3) * 148 + 65
        d.line((hx + 200, 200, hx + 200, ground), fill=C['a2'], width=10)
        d.line((hx - 100, 220, hx + 380, 220), fill=C['a2'], width=10)
        yy = 230 + 200 * abs(math.sin(t * 2))
        d.line((hx, 220, hx, yy), fill=C['fg'], width=3); rect(d, (hx - 30, yy, hx + 30, yy + 40), C['fg'])
    if t > dur * .8:
        pill(img, d, p.get('label', 'finish one. ship it.'), W / 2, 1600, C['a1'], C['fg_on_a1'], 40, anchor='c')


# ------------------------------------------------------------- blank editor -> architecture + milestones
def vblank(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    tr = dur * .3
    rect(d, (60, 230, W - 60, 1500), C['bg2'], r=24)
    if t < tr:
        text(img, 'untitled.py', 100, 260, 'mono', 30, C['muted'])
        if int(t * 2.5) % 2 == 0:
            d.rectangle((110, 340, 124, 384), fill=C['a1'])
        head(img, 'where do I even start?', 760, t, .3, 60, C['muted'], C, 'serif')
        return
    boxes = p.get('boxes', [('Client', 200, 360), ('API', 540, 360), ('Auth', 200, 620), ('DB', 540, 620), ('Queue', 870, 620)])
    for (a, b) in p.get('edges', [(0, 1), (1, 2), (1, 3), (1, 4)]):
        if t > tr + 1.1:
            ax, ay = boxes[a][1:], None
            d.line((boxes[a][1], boxes[a][2], boxes[b][1], boxes[b][2]), fill=C['fg'], width=3)
    for i, (b, x, y) in enumerate(boxes):
        q = eback(prog(t, tr + i * .2, .35))
        if q <= 0:
            continue
        w, h = 260 * q, 140 * q
        rect(d, (x - w / 2, y - h / 2, x + w / 2, y + h / 2), C['a1'] if i == 1 else C['card'], r=18, outline=C['fg'], width=3)
        if q > .8:
            text(img, b, x, y - 28, 'black', 44, C['fg_on_a1'] if i == 1 else C['fg'], anchor='c')
    ms = p.get('milestones', ['M1  auth + user model', 'M2  core API endpoints', 'M3  frontend flows', 'M4  tests + deploy'])
    for i, m in enumerate(ms):
        q = prog(t, tr + 1.3 + i * .35, .3)
        if q <= 0:
            continue
        y = 840 + i * 150
        rect(d, (110, y, 110 + 860 * eo5(q), y + 120), C['card'], r=16, outline=C['line'], width=2)
        d.rounded_rectangle((135, y + 32, 191, y + 88), 10, outline=C['a1'], width=5)
        if i == 0 and t > tr + 2.6:
            d.line((147, y + 60, 160, y + 75, 182, y + 42), fill=C['a1'], width=8)
        text(img, m, 220, y + 34, 'black', 44, C['fg'], a=q)


# ------------------------------------------------------------- vertical pipeline: requirements -> tests
def vflow(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    nodes = p.get('nodes', [('Requirements', 'users can split bills'), ('Architecture', 'REST API + Postgres'), ('Modules', 'auth / groups / ledger'),
                            ('Implementation', 'ledger.balance()'), ('Tests', '24 passing')])
    rts = disp_reveal_times(S, len(nodes))
    x = 120
    for i, (n, sub) in enumerate(nodes):
        y = 260 + i * 250
        q = eback(prog(t, rts[i], .35))
        if i > 0:
            lq = eo(prog(t, rts[i] - .2, .3))
            d.line((x + 40, y - 150, x + 40, y - 150 + 150 * lq), fill=C['a1'], width=8)
        if q <= 0:
            continue
        rect(d, (x, y, x + 840 * min(1, q), y + 100), C['a1'] if i == len(nodes) - 1 and t > rts[i] + .4 else C['card'], r=20, outline=C['fg'], width=3)
        if q > .8:
            text(img, n, x + 30, y + 22, 'black', 50, C['fg_on_a1'] if i == len(nodes) - 1 and t > rts[i] + .4 else C['fg'])
            text(img, sub, x + 40, y + 115, 'mono', 32, C['muted'])
    # travelling token
    cur = max([i for i, r in enumerate(rts) if t >= r] or [0])
    ty = 260 + cur * 250 + 50 + 20 * math.sin(t * 6)
    d.ellipse((x + 900, ty - 22, x + 944, ty + 22), fill=C['a2'])


# ------------------------------------------------------------- AI asks first: question cards + checkpoints
def vasks(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    qs = p.get('qs', [('Who uses it?', 'Students splitting rent'), ('What breaks first?', 'Concurrent edits'), ('How will you test it?', 'Unit + one e2e flow')])
    seg = dur * .85 / len(qs)
    for i, (q_, a) in enumerate(qs):
        st = .1 + i * seg
        q = eback(prog(t, st, .35))
        if q <= 0:
            continue
        y = 250 + i * 390
        rect(d, (60, y, 60 + 760 * min(1, q), y + 150), C['a1'], r=26)
        if q > .8:
            text(img, 'TUTOR ASKS', 90, y + 16, 'mono', 26, C['fg_on_a1'])
            text(img, q_, 90, y + 58, 'black', 52, C['fg_on_a1'])
        aq = eo(prog(t, st + seg * .45, .3))
        if aq > 0:
            rect(d, (300, y + 175, 1020, y + 285), C['card'], r=26, outline=C['line'], width=2)
            text(img, a[:int(len(a) * aq)], 330, y + 205, 'sans', 40, C['fg'])
            if aq >= 1:
                d.ellipse((960, y + 205, 1010, y + 255), fill=C['a3'] if not C['dark'] else C['a2'])
                d.line((970, y + 232, 982, y + 245, 1000, y + 218), fill=C['bg'], width=6)
    if t > dur * .88:
        pill(img, d, p.get('label', 'checkpoint 1 / 4 passed'), W / 2, 1460, C['fg'], C['bg'], 38, anchor='c')


# ------------------------------------------------------------- resume modes
def vres(img, d, t, S, C):
    p = S['p']; dur = S['dur']; mode = p.get('mode', 'claim')
    def paper(x, y, w, h, lines, hl=None, messy=False, a=1):
        rect(d, (x, y, x + w, y + h), C['card'] if not C['dark'] else (245, 242, 236), r=10)
        ink = (15, 17, 23)
        text(img, p.get('name', 'Aarav S.'), x + 40, y + 36, 'black', 54 if not messy else 40, ink)
        text(img, 'B.Tech CSE  |  2026', x + 40, y + 110, 'monor', 26, (130, 130, 130))
        for i, ln in enumerate(lines):
            yy = y + 190 + i * (70 if not messy else 48)
            if hl == i:
                rect(d, (x + 26, yy - 8, x + w - 26, yy + 52), C['a1'])
            text(img, ln, x + 40, yy, 'sans' if not messy else 'monor', 30 if not messy else 24, (255, 255, 255) if hl == i else ink)
    if mode == 'claim':
        lines = ['EXPERIENCE', '- Built a scalable expense app', '- Improved performance', 'PROJECTS', '- Chat app (MERN)', 'SKILLS: React, Node, SQL']
        pq = eo5(prog(t, 0, .5))
        paper(60 - (1 - pq) * 800, 240, 960, 620, lines, hl=1 if t > .7 else None)
        if t > dur * .25:
            st = text_img('PROOF?', 'black', 120, C['a2']).rotate(8, expand=True)
            paste(img, st, 560, 640, min(1, eback(prog(t, dur * .25, .3))))
        ev = p.get('evidence', ['repo: expense-app  (61 commits)', 'tests/  18 passing', 'ARCHITECTURE.md', 'demo: live link', 'profiling: 2.1s -> 0.6s'])
        for i, e in enumerate(ev):
            q = eo5(prog(t, dur * .4 + i * dur * .1, .35))
            if q <= 0:
                continue
            y = 930 + i * 110
            d.line((540, 640, lerp(540, 120, q), y + 40), fill=C['a1'], width=4)
            rect(d, (100, y, 100 + 880 * q, y + 90), C['fg'], r=16)
            if q > .7:
                text(img, e, 130, y + 22, 'mono', 34, C['bg'])
    elif mode == 'stuff':
        kws = ['Python', 'Java', 'AI', 'ML', 'Cloud', 'Agile', 'Synergy', 'Docker', 'K8s', 'Blockchain', 'React', 'Leadership', 'NLP', 'SQL', 'DevOps', 'GenAI']
        k = int(prog(t, .3, dur * .5) * 60)
        words = ' '.join(kws[i % len(kws)] for i in range(k))
        lines = ['SKILLS'] + wrap(words, 'monor', 24, 880)[:16]
        paper(60, 240, 960, 1100, lines, messy=True)
        if t > dur * .7:
            rect(d, (60, 1380, 1020, 1560), C['a1'], r=24)
            head(img, p.get('fix', 'Match real skills to real evidence.'), 1405, t, dur * .7, 52, C['fg_on_a1'], C, maxw=900)
    elif mode == 'scan':
        clean = t > dur * .5
        lines = ['EXPERIENCE  Intern, FinCo (2025)', '- Cut API latency 40% (profiling)', 'PROJECTS', '- SplitIt: bill-splitting app, 3 users groups', 'SKILLS  Python, SQL, FastAPI'] if clean else \
            ['Objective: to obtain a challenging position in a reputed org where I can utilise my skills', 'Hobbies: reading, cricket', 'Skills: MS Office, C, C++, Java, Python, HTML, CSS, JS, React, AI', 'Projects: various web dev projects', 'Experience: worked on many things']
        paper(60, 240, 960, 900, lines, messy=not clean)
        rnd = random.Random(int(t * 3))
        path = [(540, 330), (300, 480), (700, 560), (400, 700), (800, 820)] if clean else [(rnd.uniform(100, 980), rnd.uniform(400, 1100)) for _ in range(5)]
        lt = (t % 1.5) / 1.5; k = int(lt * (len(path) - 1))
        x, y = path[k]
        d.ellipse((x - 40, y - 40, x + 40, y + 40), outline=C['a2'], width=8)
        head(img, 'Clear hierarchy: easy to scan.' if clean else 'Where does the eye go?', 1220, t, (.2 if not clean else dur * .5 + .1), 64, C['fg'], C)
    elif mode == 'rewrite':
        a = p.get('before', 'Worked on a web app project.')
        b = p.get('after', 'Built group-ledger API (FastAPI, Postgres); wrote 18 tests; deployed on Render.')
        paper(60, 240, 960, 380, ['PROJECT'], None)
        sw = t > dur * .4
        txt = a if not sw else b[:int(len(b) * prog(t, dur * .45, dur * .35))]
        for j, ln in enumerate(wrap(txt, 'sans', 40, 860)):
            text(img, ln, 100, 470 + j * 52, 'sans', 40, (15, 17, 23))
        if sw and t < dur * .45:
            d.rectangle((100, 490, 900, 500), fill=C['a2'])
        tags = ['what you built', 'tools', 'proof', 'outcome']
        for i, tg in enumerate(tags):
            q = eback(prog(t, dur * .8 + i * .12, .3))
            if q > 0:
                pill(img, d, tg, 80 + i * 240, 700, C['a1'], C['fg_on_a1'], 30, a=min(1, q))
    elif mode == 'compare':
        A = ['- Did a project on ML', '- Good team player', '- Knowledge of Python']
        Bn = ['- Trained churn model, F1 0.81', '- Led 3-person sprint, shipped v1', '- Python: pandas, sklearn, FastAPI']
        for j, (lab, L, col) in enumerate([('RESUME A', A, C['muted']), ('RESUME B', Bn, C['a1'])]):
            y = 240 + j * 640
            q = eo5(prog(t, .2 + j * dur * .3, .45))
            rect(d, (60, y, 60 + 960 * q, y + 580), (245, 242, 236), r=12)
            if q > .9:
                text(img, lab, 100, y + 30, 'mono', 32, col)
                text(img, 'same internship, same student', 980, y + 34, 'monor', 24, (130, 130, 130), anchor='r')
                for i, ln in enumerate(L):
                    text(img, ln, 100, y + 140 + i * 120, 'sans', 40, (15, 17, 23))
        if t > dur * .75:
            pill(img, d, 'Difference: specifics + evidence', W / 2, 1540, C['a2'], C['bg'], 38, anchor='c')


VSCENES.update(vreel=vreel, vvanish=vvanish, vclones=vclones, vcity=vcity, vblank=vblank, vflow=vflow, vasks=vasks, vres=vres)
