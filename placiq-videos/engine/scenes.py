"""Scene library. Each scene: fn(img, d, t, S, C). t = local seconds, S = scene dict, C = palette."""
import math, random
from PIL import Image, ImageDraw
from core import *


def word_times(S):
    return [w[1] for w in S['words']] or [0.3]


def disp_reveal_times(S, n):
    """Map n display tokens onto the actual spoken word onsets (Kokoro timestamps)."""
    wt = word_times(S)
    if n <= 0:
        return []
    out = []
    for k in range(n):
        idx = min(len(wt) - 1, int(round(k * (len(wt) - 1) / max(1, n - 1)))) if n > 1 else 0
        out.append(wt[idx] - 0.06)
    return out


def hud(img, d, t, S, C):
    col = C['muted']
    text(img, 'PLACIQ', 56, 40, 'mono', 18, col)
    text(img, '/ ' + S.get('tag', ''), 140, 40, 'monor', 18, col)
    g = S['t0'] + t
    text(img, '%02d:%02d:%02d' % (int(g // 60), int(g % 60), int(g * 30 % 30)), W - 56, 40, 'monor', 18, col, anchor='r')
    text(img, '%02d' % (S['idx'] + 1) + ' / %02d' % S['n'], W - 56, H - 60, 'mono', 18, col, anchor='r')


# ---------------------------------------------------------------- kinetic type
def kinetic(img, d, t, S, C):
    p = S['p']
    lines = p['lines']
    toks = []
    for li, ln in enumerate(lines):
        for w in ln.split(' '):
            toks.append((li, w))
    rts = disp_reveal_times(S, len(toks))
    size = p.get('size', 150)
    # auto-fit
    widest = max(sum(tsize(w.strip('*~_'), 'black', size)[0] + size * .25 for w in ln.split(' ')) for ln in lines)
    if widest > 1680:
        size = int(size * 1680 / widest)
    push = 1 + 0.035 * prog(t, 0, S['dur'])
    size_q = int(size * round(push * 50) / 50)
    lh = size_q * 1.12
    y0 = H / 2 - lh * len(lines) / 2 + p.get('dy', 0)
    style = p.get('style', 'mask')
    k = 0
    for li, ln in enumerate(lines):
        ws = ln.split(' ')
        widths = [tsize(w.strip('*~_'), 'black', size_q)[0] for w in ws]
        gap = size_q * .25
        total = sum(widths) + gap * (len(ws) - 1)
        x = W / 2 - total / 2 if p.get('align', 'c') == 'c' else 140
        y = y0 + li * lh
        for wi, w in enumerate(ws):
            rt = rts[k]; k += 1
            pr = prog(t, rt, 0.28)
            clean = w.strip('*~_')
            accent = w.startswith('*')
            col = C['a1'] if accent else C['fg']
            if w.startswith('_'):
                col = C['muted']
            if accent and pr > 0:
                bw = widths[wi] * eo5(prog(t, rt, .22))
                rect(d, (x - 14, y + size_q * .08, x - 14 + bw + 28, y + lh * .92), C['a1'])
                col = C['bg'] if C.get('dark') else C['fg_on_a1']
            if style == 'slam' and pr > 0:
                sc = 1 + 0.6 * (1 - eback(pr))
                sz = int(size_q * round(sc * 40) / 40)
                tw, th = tsize(clean, 'black', sz)
                text(img, clean, x + widths[wi] / 2 - tw / 2, y + (size_q - sz) * .55, 'black', sz, col, a=min(1, pr * 3))
            else:
                text_mask_up(img, clean, x, y, 'black', size_q, col, pr)
            if w.startswith('~') and t > rt + .35:
                sp = eo(prog(t, rt + .35, .25))
                yy = y + lh * .52
                d.rectangle((x - 10, yy - 7, x - 10 + (widths[wi] + 20) * sp, yy + 7), fill=C['a2'])
            x += widths[wi] + gap
    if p.get('sub'):
        st = rts[-1] + .25
        text_mask_up(img, p['sub'], W / 2, y0 + len(lines) * lh + 30, 'serif', 72, C['a2'], prog(t, st, .4), anchor='c')


# ---------------------------------------------------------------- tab avalanche
TAB_NAMES = ['LeetCode', 'GitHub', 'resume_v4.pdf', 'Striver Sheet', 'ChatGPT', 'YouTube - DP', 'Notion', 'Course 14/83',
             'Stack Overflow', 'jobs.xlsx', 'LinkedIn', 'GfG Arrays', 'React docs', 'ChatGPT (new)', 'Udemy', 'notes.md',
             'Codeforces', 'roadmap.sh', 'Gemini', 'portfolio-v2', 'Glassdoor', 'mock test 3', 'Kaggle', 'Medium',
             'system design?', 'ChatGPT (again)', 'Discord', 'HackerRank', 'job portal', 'interview Qs']


def tabs(img, d, t, S, C):
    p = S['p']
    N = p.get('n', 47)
    rnd = random.Random(7)
    span = S['dur'] * .72
    shown = 0
    for i in range(N):
        st = 0.05 + span * (i / N) ** 1.3
        pr = prog(t, st, .35)
        if pr <= 0:
            continue
        shown += 1
        col, row = i % 6, i // 6
        tx = 120 + col * 285 + rnd.uniform(-30, 30)
        ty = 150 + row * 98 + rnd.uniform(-14, 14)
        yy = lerp(-120, ty, eback(pr, 1.2))
        tw = 262
        fill = C['card'] if i % 5 else C['a1']
        d.rounded_rectangle((tx, yy, tx + tw, yy + 58), 12, fill=fill, outline=C['line'], width=2)
        d.ellipse((tx + 16, yy + 20, tx + 34, yy + 38), fill=(C['a2'] if i % 3 == 0 else C['a3'] if i % 3 == 1 else C['muted']))
        name = TAB_NAMES[i % len(TAB_NAMES)]
        text(img, name[:16], tx + 46, yy + 16, 'monor', 19, C['fg'] if i % 5 else C['fg_on_a1'])
        text(img, 'x', tx + tw - 26, yy + 16, 'monor', 19, C['muted'])
    # counter block
    cp = eo(prog(t, .1, .3))
    bx = W - 640
    rect(d, (bx, H - 380, bx + 540 * cp, H - 140), C['fg'])
    if cp > .9:
        text(img, str(shown), bx + 40, H - 380, 'black', 170, C['bg'])
        text(img, 'OPEN TABS', bx + 44, H - 185, 'mono', 26, C['a1'])
        text(img, '0 CONTEXT', bx + 300, H - 185, 'mono', 26, C['a2'])


# ---------------------------------------------------------------- AI amnesia chat loop
def chat_panel(C, t, msg_user, msg_ai, session, typed_p):
    w, h = 1000, 560
    im = Image.new('RGBA', (w, h), C['card'])
    dd = ImageDraw.Draw(im)
    dd.rectangle((0, 0, w, 64), fill=C['fg'])
    text(im, 'AI CHAT  -  session #%d' % session, 28, 16, 'mono', 22, C['bg'])
    text(im, 'memory: none', w - 28, 18, 'monor', 20, C['a2'], anchor='r')
    n = int(len(msg_user) * clamp(typed_p))
    u = msg_user[:n]
    # wrap user msg
    lines, cur = [], ''
    for wd in u.split(' '):
        if tsize(cur + wd, 'sans', 30)[0] > 700:
            lines.append(cur); cur = ''
        cur += wd + ' '
    lines.append(cur)
    bh = 30 + 44 * len(lines)
    dd.rounded_rectangle((w - 780, 100, w - 30, 100 + bh), 24, fill=C['a1'])
    for i, l in enumerate(lines):
        text(im, l, w - 750, 112 + i * 44, 'sans', 30, C['fg_on_a1'])
    if typed_p >= 1:
        dd.rounded_rectangle((30, 140 + bh, 700, 230 + bh), 24, fill=C['bg2'])
        text(im, msg_ai, 60, 165 + bh, 'sans', 30, C['fg'])
    elif int(t * 4) % 2 == 0:
        x = w - 750 + tsize(lines[-1], 'sans', 30)[0]
        dd.rectangle((x, 116 + (len(lines) - 1) * 44, x + 4, 150 + (len(lines) - 1) * 44), fill=C['fg_on_a1'])
    return im


def chat(img, d, t, S, C):
    p = S['p']
    msg = p.get('msg', "Hi! I'm a 3rd-year CSE student preparing for placements...")
    reply = p.get('reply', 'Nice to meet you! Tell me about yourself.')
    typing = p.get('type_dur', min(2.2, S['dur'] * .45))
    base = p.get('session0', 1)
    rec = p.get('recursion', True)
    # recursive stack of past identical sessions shrinking behind
    reps = int(clamp((t - typing) / max(.1, S['dur'] - typing)) * 7) if rec else 0
    for r in range(reps, 0, -1):
        sc = 1 - r * 0.085
        pan = chat_panel(C, t, msg, reply, base + 99 - r, 1.0)
        pw, ph = int(pan.size[0] * sc), int(pan.size[1] * sc)
        pan = pan.resize((pw, ph), Image.BILINEAR)
        paste(img, pan, W / 2 - pw / 2 + r * 70, H / 2 - ph / 2 - r * 40, 0.35 + 0.08 * (7 - r))
    pan = chat_panel(C, t, msg, reply, base + (99 if rec and reps else 0), prog(t, .1, typing))
    sh, pad = shadow(pan.size[0], pan.size[1], 20, 26, 110)
    paste(img, sh, W / 2 - 500 - pad, H / 2 - 280 - pad + 12)
    pan.putalpha(round_mask(pan.size[0], pan.size[1], 20))
    paste(img, pan, W / 2 - 500, H / 2 - 280)
    if p.get('label'):
        text_mask_up(img, p['label'], 140, H - 230, 'black', 90, C['a2'], prog(t, typing + .2, .4))


# ---------------------------------------------------------------- project graveyard
def graveyard(img, d, t, S, C):
    p = S['p']
    files = p.get('files', ['project-final.zip', 'final-v2', 'final-FINAL', 'final-REAL-v3', 'todo-app (copy)', 'clone-netflix'])
    rts = disp_reveal_times(S, len(files))
    floor = H - 250
    d.line((100, floor, W - 100, floor), fill=C['fg'], width=4)
    for i, f in enumerate(files):
        pr = prog(t, rts[i], .4)
        if pr <= 0:
            continue
        x = 150 + i * 280
        y = lerp(-260, floor - 230, eback(pr, 1.4))
        tilt = (i % 2) * 8
        # folder
        d.rounded_rectangle((x, y + 10 + tilt, x + 90, y + 46 + tilt), 8, fill=C['a3'])
        d.rounded_rectangle((x, y + 30 + tilt, x + 220, y + 200 + tilt), 14, fill=C['a3'] if i % 2 else C['a1'])
        text(img, f, x + 4, y + 212 + tilt, 'mono', 21, C['fg'])
        if t > rts[i] + .5:
            sp = eo(prog(t, rts[i] + .5, .2))
            text(img, '0%' if i % 2 else '12%', x + 20, y + 80 + tilt, 'black', 70, C['fg_on_a1'], a=sp)
    if t > S['dur'] * .62:
        sp = eback(prog(t, S['dur'] * .62, .3))
        sz = int(140 * (2 - sp))
        stamp = text_img('ABANDONED', 'black', max(20, sz), C['a2'])
        stamp = stamp.rotate(-8, expand=True, resample=Image.BILINEAR)
        paste(img, stamp, W / 2 - stamp.size[0] / 2, 170, min(1, sp))


# ---------------------------------------------------------------- DSA array / pointers
def array(img, d, t, S, C):
    p = S['p']
    vals = p.get('vals', [2, 5, 8, 11, 15, 19, 23, 31, 42])
    target = p.get('target', 34)
    n = len(vals)
    bw, gap = 150, 22
    x0 = W / 2 - (n * bw + (n - 1) * gap) / 2
    y0 = 380
    dur = S['dur']
    broken = p.get('mode') == 'break'
    steps = [(0, 8), (0, 7), (1, 7), (2, 7), (3, 7), (3, 6)]
    si = min(len(steps) - 1, int(t / (dur * .75 / len(steps))))
    L, R = steps[si]
    bt = dur * .55
    for i, v in enumerate(vals):
        pr = eback(prog(t, .05 * i, .35))
        x = x0 + i * (bw + gap)
        y = y0 + (1 - pr) * 200
        if broken and t > bt:
            q = prog(t, bt + 0.03 * i, .7)
            y += q * q * 900
            x += (i - n / 2) * 60 * q
        active = i in (L, R)
        fill = C['a1'] if active else C['card']
        d.rounded_rectangle((x, y, x + bw, y + bw), 18, fill=fill, outline=C['line'], width=3)
        text(img, str(v), x + bw / 2, y + 36, 'black', 64, C['fg_on_a1'] if active else C['fg'], anchor='c', a=min(1, pr))
        text(img, '[%d]' % i, x + bw / 2, y + bw + 16, 'monor', 20, C['muted'], anchor='c')
    if not (broken and t > bt):
        for lab, idx, col in (('L', L, C['a2']), ('R', R, C['a3'])):
            x = x0 + idx * (bw + gap) + bw / 2
            d.polygon([(x - 18, y0 - 30), (x + 18, y0 - 30), (x, y0 - 6)], fill=col)
            text(img, lab, x, y0 - 90, 'black', 48, col, anchor='c')
        s = vals[L] + vals[R]
        code = 'while L < R:  sum = a[%d] + a[%d] = %d   %s %d' % (L, R, s, '==' if s == target else ('>' if s > target else '<'), target)
        rect(d, (x0, y0 + 260, x0 + 1400, y0 + 340), C['fg'], r=14)
        text(img, code, x0 + 30, y0 + 279, 'mono', 30, C['bg'])
        if s == target:
            pill(img, d, 'FOUND  invariant holds', x0 + 1000, y0 + 360, C['a3'], C['fg_on_a1'], 24)
    else:
        q = eback(prog(t, bt + .1, .3))
        text(img, 'ONE LINE CHANGED.', W / 2, 420, 'black', int(40 + 100 * q), C['a2'], anchor='c', a=min(1, q))
        text(img, 'a = sorted(a)  ->  a = a  # unsorted input', W / 2, 600, 'mono', 34, C['fg'], anchor='c', a=min(1, q))
    if p.get('title'):
        text_mask_up(img, p['title'], 140, 140, 'black', 84, C['fg'], prog(t, .1, .4))


# ---------------------------------------------------------------- big counter
def counter(img, d, t, S, C):
    p = S['p']
    n = p['n']
    q = eo5(prog(t, .1, min(1.8, S['dur'] * .6)))
    val = int(n * q)
    s = '{:,}'.format(val) + p.get('suffix', '')
    cx, cy = W / 2, H / 2 - 40
    rot = t * 40
    for k in range(72):
        a = math.radians(k * 5 + rot)
        on = k / 72 < q
        r0, r1 = 430, 455 if k % 6 else 480
        col = C['a1'] if on else C['line']
        d.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=col, width=5)
    text(img, s, cx, cy - 150, 'black', 250, C['fg'], anchor='c')
    text_mask_up(img, p.get('label', ''), cx, cy + 150, 'mono', 40, C['a2'], prog(t, .5, .4), anchor='c')


# ---------------------------------------------------------------- evidence graph
def graph(img, d, t, S, C):
    p = S['p']
    nodes = p['nodes']
    center = p.get('center', 'Placiq')
    rts = disp_reveal_times(S, len(nodes))
    cx, cy = W / 2 + p.get('dx', 0), H / 2 + 20
    rad = p.get('r', 360)
    pts = []
    for i, nm in enumerate(nodes):
        a = 2 * math.pi * i / len(nodes) + t * .18 - math.pi / 2
        pts.append((cx + rad * 1.35 * math.cos(a), cy + rad * .85 * math.sin(a)))
    # links
    for i, (x, y) in enumerate(pts):
        lp = eo(prog(t, rts[i] + .15, .4))
        if lp <= 0:
            continue
        ex, ey = lerp(x, cx, lp), lerp(y, cy, lp)
        d.line((x, y, ex, ey), fill=C['a1'], width=4)
        j = (i + 1) % len(pts)
        if p.get('mesh') and t > rts[j] + .4 and t > rts[i] + .4:
            d.line((x, y, pts[j][0], pts[j][1]), fill=C['line'], width=2)
        if lp >= 1:  # data pulse
            f = (t * 1.3 + i * .17) % 1
            px, py = lerp(x, cx, f), lerp(y, cy, f)
            d.ellipse((px - 8, py - 8, px + 8, py + 8), fill=C['a2'])
    # center
    cp = eback(prog(t, .05, .5))
    r = 110 * cp
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=C['fg'])
    if cp > .6:
        text(img, center, cx, cy - 34, 'black', 50, C['bg'], anchor='c')
    for i, (x, y) in enumerate(pts):
        pr = eback(prog(t, rts[i], .35))
        if pr <= 0:
            continue
        nm = nodes[i]
        tw, th = tsize(nm, 'mono', 30)
        w2 = (tw + 50) * pr
        fill = C['a1'] if i % 3 == 0 else C['card']
        d.rounded_rectangle((x - w2 / 2, y - 34, x + w2 / 2, y + 34), 34, fill=fill, outline=C['fg'], width=3)
        if pr > .8:
            text(img, nm, x, y - 20, 'mono', 30, C['fg_on_a1'] if i % 3 == 0 else C['fg'], anchor='c')
    if p.get('title'):
        text_mask_up(img, p['title'], 140, 120, 'black', 76, C['fg'], prog(t, .1, .4))


def notes(img, d, t, S, C):
    """Sticky notes of memory stitched together with a red thread (PCME)."""
    p = S['p']
    items = p['notes']
    rts = disp_reveal_times(S, len(items))
    rnd = random.Random(3)
    pos = []
    rect(d, (110, 150, W - 110, H - 170), C['bg2'], r=26)
    text(img, 'your career memory  -  PCME', 150, 175, 'serif', 46, C['muted'])
    for i, s in enumerate(items):
        x = 200 + (i % 3) * 540 + rnd.uniform(-40, 40)
        y = 290 + (i // 3) * 300 + rnd.uniform(-30, 30)
        pos.append((x + 180, y + 20))
    for i in range(1, len(items)):
        if t > rts[i] + .2:
            lp = eo(prog(t, rts[i] + .2, .3))
            a, b = pos[i - 1], pos[i]
            d.line((a[0], a[1], lerp(a[0], b[0], lp), lerp(a[1], b[1], lp)), fill=C['a2'], width=5)
    cols = [C['a1'], C['a3'], C['card'], C['a1'], C['card'], C['a3']]
    for i, s in enumerate(items):
        pr = eback(prog(t, rts[i], .35))
        if pr <= 0:
            continue
        x, y = pos[i][0] - 180, pos[i][1] - 20
        y -= (1 - pr) * 80
        note = Image.new('RGBA', (380, 170), cols[i % len(cols)])
        nd = ImageDraw.Draw(note)
        nd.rectangle((0, 0, 379, 169), outline=C['fg'], width=3)
        text(note, s, 20, 55, 'serif', 40, C['fg_on_a1'])
        note = note.rotate(rnd.uniform(-5, 5), expand=True, resample=Image.BILINEAR)
        paste(img, note, x, y, min(1, pr))
        d.ellipse((pos[i][0] - 12, pos[i][1] - 12, pos[i][0] + 12, pos[i][1] + 12), fill=C['a2'])


# ---------------------------------------------------------------- product screen reveal
def screen(img, d, t, S, C):
    p = S['p']
    dur = S['dur']
    lay = p.get('layout', 'right')
    enter = eo5(prog(t, 0, .55))
    z = lerp(1.0, p.get('zoom', 1.3), eio(prog(t, .9, dur - .9)))
    foc = p.get('focus', (.5, .4))
    if lay == 'right':
        cx = lerp(W + 700, 1220, enter); cy = H / 2 + 20; ww = 1160
    elif lay == 'left':
        cx = lerp(-700, 700, enter); cy = H / 2 + 20; ww = 1160
    else:
        cx = W / 2; cy = lerp(H + 600, H / 2 + 60, enter); ww = 1500
    # color slab behind
    sp = eo5(prog(t, 0, .4))
    if lay == 'right':
        rect(d, (1220 - 560 + 60, 120, 1220 - 560 + 60 + 1180 * sp, H - 100), C['a1'], r=30)
    elif lay == 'left':
        rect(d, (700 - 640 + 20 - 1180 * sp + 1180, 120, 700 + 620, H - 100), C['a1'], r=30)
    else:
        rect(d, (W / 2 - 790 * sp, 150, W / 2 + 790 * sp, H - 40), C['a1'], r=30)
    box = window(img, p['shot'], cx, cy, ww, zoom=z, focus=foc)
    # callouts
    for i, c in enumerate(p.get('callouts', [])):
        txt, fx, fy, ft = c
        st = ft * dur
        pr = eback(prog(t, st, .3))
        if pr <= 0:
            continue
        x = box[0] + fx * (box[2] - box[0]); y = box[1] + fy * (box[3] - box[1])
        d.ellipse((x - 14 * pr, y - 14 * pr, x + 14 * pr, y + 14 * pr), fill=C['a2'])
        ring = 14 + 40 * prog(t, st, .6)
        d.ellipse((x - ring, y - ring, x + ring, y + ring), outline=C['a2'], width=3)
        pill(img, d, txt, x + 30, y - 22, C['fg'], C['bg'], 24, a=min(1, pr))
    # title
    title = p.get('title')
    if title:
        tl = title.split('|')
        if lay in ('right', 'left'):
            tx = 120 if lay == 'right' else 1340
            for i, ln in enumerate(tl):
                text_mask_up(img, ln, tx, 260 + i * 92, 'black', 78 if len(ln) < 12 else 62, C['fg'], prog(t, .25 + i * .12, .45))
            if p.get('sub'):
                words_, lines_, cur = p['sub'].split(), [], ''
                for wd in words_:
                    if tsize(cur + wd, 'serif', 48)[0] > 470 and cur:
                        lines_.append(cur); cur = ''
                    cur += wd + ' '
                lines_.append(cur)
                for j, ln in enumerate(lines_):
                    text_mask_up(img, ln, tx, 280 + len(tl) * 92 + j * 52, 'serif', 48, C['a2'], prog(t, .7 + j * .1, .45))
            if p.get('tagline'):
                for i, tg in enumerate(p['tagline']):
                    pill(img, d, tg, tx, 600 + len(tl) * 40 + i * 64, C['card'], C['fg'], 22, a=eo(prog(t, 1.0 + i * .25, .3)))
        else:
            text_mask_up(img, tl[0], W / 2, 50, 'black', 70, C['fg'], prog(t, .2, .45), anchor='c')
    if p.get('real', True):
        text(img, 'REAL PRODUCT CAPTURE', box[0] + 14, box[3] + 14, 'monor', 16, C['muted'], a=enter)


# ---------------------------------------------------------------- beat montage
def montage(img, d, t, S, C):
    p = S['p']
    shots = p['shots']
    words = p['words']
    rts = disp_reveal_times(S, len(words))
    k = 0
    for i, rt in enumerate(rts):
        if t >= rt:
            k = i
    lt = t - rts[k]
    sh = shots[k % len(shots)]
    z = 1.15 + 0.12 * prog(lt, 0, 1.2)
    sc = 1.1 - 0.1 * eo5(prog(lt, 0, .3))
    window(img, sh, W / 2 + 230, H / 2 + 30, int(1200 * sc), zoom=z, focus=((k * .37) % 1, (.3 + k * .21) % 1), chrome=False)
    rect(d, (0, 0, 640, H), C['fg'])
    for i, w in enumerate(words):
        if t >= rts[i] - .05:
            col = C['a1'] if i == k else C['muted']
            text_mask_up(img, w, 90, 120 + i * (820 / len(words)), 'black', min(int(min(96, 760 / len(words))), int(60 * 480 / max(tsize(x, 'black', 60)[0] for x in words))), col, prog(t, rts[i] - .05, .25))


# ---------------------------------------------------------------- cycle loop
def loop(img, d, t, S, C):
    p = S['p']
    steps = p['steps']
    rts = disp_reveal_times(S, len(steps))
    cx, cy, R = W / 2, H / 2 + 30, 360
    cur = -1
    for i, rt in enumerate(rts):
        if t >= rt:
            cur = i
    cp = eo(prog(t, 0, .6))
    d.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * cp, fill=C['line'], width=6)
    if cur >= 0:
        ang = 360 * (cur + eo(prog(t, rts[cur], .3))) / len(steps)
        d.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + ang, fill=C['a1'], width=14)
    for i, s in enumerate(steps):
        a = math.radians(-90 + 360 * i / len(steps))
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        on = i <= cur
        r = 22 if not on else 22 + 10 * (1 - eo(prog(t, rts[i], .3)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=C['a1'] if on else C['card'], outline=C['fg'], width=3)
        lx = x + (60 if math.cos(a) >= -0.01 else -60)
        text(img, s.upper(), lx, y - 22, 'mono', 34, C['fg'] if on else C['muted'], anchor='l' if math.cos(a) >= -0.01 else 'r')
    if cur >= 0:
        w = steps[cur].upper()
        text_mask_up(img, w, cx, cy - 70, 'black', 96 if len(w) < 9 else 76, C['fg'], prog(t, rts[cur], .25), anchor='c')
    text(img, p.get('center', 'a loop, not a checklist'), cx, cy + 50, 'serif', 46, C['a2'], anchor='c')


# ---------------------------------------------------------------- resume claim -> evidence
def resume(img, d, t, S, C):
    p = S['p']
    dur = S['dur']
    pr = eo5(prog(t, 0, .5))
    x0, y0 = lerp(-700, 140, pr), 170
    rect(d, (x0, y0, x0 + 640, y0 + 760), C['card'], r=10, outline=C['line'], width=2)
    text(img, 'Deep M.', x0 + 40, y0 + 40, 'black', 46, C['fg'])
    text(img, 'Software Engineer  -  2026', x0 + 40, y0 + 110, 'monor', 20, C['muted'])
    for i in range(9):
        yy = y0 + 200 + i * 56
        if i == 3:
            continue
        rect(d, (x0 + 40, yy, x0 + 40 + (520 if i % 3 else 380), yy + 14), C['line'], r=7)
    hy = y0 + 200 + 3 * 56 - 18
    hp = eo(prog(t, .6, .35))
    rect(d, (x0 + 30, hy - 6, x0 + 30 + 590 * hp, hy + 50), C['a1'])
    text(img, '- Built a scalable app for 10k users', x0 + 40, hy, 'sans', 27, C['fg_on_a1'] if hp > .5 else C['fg'])
    if t > dur * .3:
        sp = eback(prog(t, dur * .3, .3))
        st = text_img('CLAIM?', 'black', max(10, int(110 * (2 - sp))), C['a2']).rotate(10, expand=True)
        paste(img, st, x0 + 330, y0 + 520, min(1, sp))
    ev = p.get('evidence', ['repo: placiq-chat/  42 commits', 'tests/  31 passing', 'architecture.md', 'load test: p95 180ms', 'deployed: live demo'])
    for i, e in enumerate(ev):
        st = dur * .42 + i * (dur * .45 / len(ev))
        q = eo5(prog(t, st, .4))
        if q <= 0:
            continue
        ex, ey = 1040, 210 + i * 150
        sx, sy = x0 + 620, hy + 22
        d.line((sx, sy, lerp(sx, ex, q), lerp(sy, ey + 40, q)), fill=C['a3'], width=4)
        if q > .6:
            rect(d, (ex, ey, ex + 700, ey + 84), C['fg'], r=16)
            d.ellipse((ex + 22, ey + 24, ex + 58, ey + 60), fill=C['a3'])
            text(img, 'OK', ex + 25, ey + 28, 'mono', 18, C['fg_on_a1'])
            text(img, e, ex + 80, ey + 22, 'mono', 30, C['bg'])


# ---------------------------------------------------------------- contribution grid
def grid(img, d, t, S, C):
    p = S['p']
    dur = S['dur']
    cols, rows, cs = 52, 7, 28
    x0, y0 = W / 2 - cols * (cs + 4) / 2, 300
    rnd = random.Random(11)
    ex = prog(t, dur * .55, .9)
    greens = ['#0E4429', '#006D32', '#26A641', '#39D353']
    for c in range(cols):
        for r in range(rows):
            lv = rnd.random()
            fill_t = (c / cols) * dur * .35
            on = t > fill_t
            col = hexc(greens[int(lv * 3.99)]) if on and lv > .18 else C['line']
            x, y = x0 + c * (cs + 4), y0 + r * (cs + 4)
            if ex > 0:
                a = rnd.uniform(0, 6.28); sp = rnd.uniform(200, 900) * eo(ex)
                x += math.cos(a) * sp; y += math.sin(a) * sp
            else:
                rnd.random(); rnd.random()
            d.rounded_rectangle((x, y, x + cs, y + cs), 5, fill=col)
    text(img, '1,248 contributions in the last year', x0, y0 - 60, 'monor', 26, C['muted'], a=1 - ex)
    if t > dur * .35:
        q = eback(prog(t, dur * .35, .3))
        text(img, 'SO WHAT?', W / 2, 620, 'black', int(60 + 120 * min(1, q)), C['a2'], anchor='c', a=min(1, q))
    if ex > .3:
        items = ['WHY this design?', 'WHAT broke?', 'HOW you tested', 'WHO uses it']
        for i, it in enumerate(items):
            q = eback(prog(t, dur * .6 + i * .25, .3))
            pill(img, d, it, 260 + i * 370, 860, C['a1'], C['fg_on_a1'], 30, a=min(1, q))


# ---------------------------------------------------------------- CTA end card
def cta(img, d, t, S, C):
    p = S['p']
    q = eback(prog(t, .05, .5))
    s = 1.0 * q
    # logo tile
    lx, ly = W / 2 - 330, 330
    rect(d, (lx, ly, lx + 150 * s, ly + 150 * s), C['fg'], r=int(32 * s) + 1)
    if q > .7:
        text(img, 'P', lx + 75, ly + 8, 'black', 110, C['bg'], anchor='c')
        text(img, 'Placiq', lx + 190, ly - 10, 'black', 150, C['fg'])
    u = prog(t, .5, .4)
    rect(d, (lx, ly + 190, lx + 690 * eo5(u), ly + 200), C['a2'])
    text_mask_up(img, p.get('tag', 'Your work, connected.'), W / 2, ly + 240, 'serif', 96, C['fg'], prog(t, .6, .45), anchor='c')
    bq = eback(prog(t, 1.1, .4))
    if bq > 0:
        w, h = pill(img, d, '  learn.placiq.in  ->  ', W / 2, ly + 400, C['a1'], C['fg_on_a1'], 44, anchor='c', a=min(1, bq), pad=(36, 22))
        # cursor click
        cx, cy = W / 2 + 160, ly + 470 + 40 * (1 - eo(prog(t, 1.4, .4)))
        d.polygon([(cx, cy), (cx, cy + 46), (cx + 13, cy + 34), (cx + 30, cy + 34)], fill=C['fg'], outline=C['bg'])
        if t > 1.8:
            r = 20 + 60 * prog(t, 1.8, .5)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=C['a2'], width=4)
    text(img, p.get('foot', 'AI-native Career Intelligence OS for engineers  -  placiq.in'), W / 2, H - 170, 'monor', 24, C['muted'], anchor='c', a=eo(prog(t, 1.4, .5)))


SCENES = dict(kinetic=kinetic, tabs=tabs, chat=chat, graveyard=graveyard, array=array, counter=counter,
              graph=graph, notes=notes, screen=screen, montage=montage, loop=loop, resume=resume, grid=grid, cta=cta)
