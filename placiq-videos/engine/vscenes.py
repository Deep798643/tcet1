"""Vertical (1080x1920) scene library for the 60-day campaign. fn(img, d, t, S, C)."""
import math, random, subprocess
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw
from core import *
from scenes import disp_reveal_times


def wrap(txt, fname, size, maxw):
    out, cur = [], ''
    for w in txt.split(' '):
        if cur and tsize(cur + w, fname, size)[0] > maxw:
            out.append(cur.strip()); cur = ''
        cur += w + ' '
    out.append(cur.strip())
    return out


def head(img, txt, y, t, st=0.1, size=96, col=None, C=None, fname='black', maxw=960, x=None):
    lines = wrap(txt, fname, size, maxw)
    for i, ln in enumerate(lines):
        if x is None:
            text_mask_up(img, ln, W / 2, y + i * size * 1.08, fname, size, col, prog(t, st + i * .1, .4), anchor='c')
        else:
            text_mask_up(img, ln, x, y + i * size * 1.08, fname, size, col, prog(t, st + i * .1, .4))
    return y + len(lines) * size * 1.08


def vhud(img, d, t, S, C):
    text(img, 'PLACIQ', 60, 70, 'mono', 26, C['muted'])
    text(img, S.get('daytag', ''), W - 60, 70, 'mono', 26, C['muted'], anchor='r')


# ------------------------------------------------------------- kinetic type (word synced, block reveals)
def vtype(img, d, t, S, C):
    p = S['p']; lines = p['lines']
    toks = [(li, w) for li, ln in enumerate(lines) for w in ln.split(' ')]
    rts = disp_reveal_times(S, len(toks))
    size = p.get('size', 130)
    widest = max(sum(tsize(w.strip('*~_'), 'black', size)[0] for w in ln.split(' ')) + size * .25 * len(ln.split(' ')) for ln in lines)
    if widest > 960:
        size = int(size * 960 / widest)
    lh = size * 1.15
    y0 = H * .42 - lh * len(lines) / 2 + p.get('dy', 0)
    k = 0
    for li, ln in enumerate(lines):
        ws = ln.split(' ')
        wd = [tsize(w.strip('*~_'), 'black', size)[0] for w in ws]
        gap = size * .25
        x = W / 2 - (sum(wd) + gap * (len(ws) - 1)) / 2
        y = y0 + li * lh
        for wi, w in enumerate(ws):
            rt = rts[k]; k += 1
            pr = prog(t, rt, .26)
            col = C['fg']
            if w.startswith('*') and pr > 0:
                rect(d, (x - 12, y + size * .06, x - 12 + (wd[wi] + 24) * eo5(prog(t, rt, .2)), y + lh * .95), C['a1'])
                col = C['fg_on_a1']
            if w.startswith('_'):
                col = C['muted']
            if p.get('slam') and pr > 0:
                sc = 1 + .7 * (1 - eback(pr)); sz = int(size * round(sc * 30) / 30)
                tw, _ = tsize(w.strip('*~_'), 'black', sz)
                text(img, w.strip('*~_'), x + wd[wi] / 2 - tw / 2, y + (size - sz) * .5, 'black', sz, col, a=min(1, pr * 3))
            else:
                text_mask_up(img, w.strip('*~_'), x, y, 'black', size, col, pr)
            if w.startswith('~') and t > rt + .35:
                sp = eo(prog(t, rt + .35, .25)); yy = y + lh * .5
                d.rectangle((x - 8, yy - 8, x - 8 + (wd[wi] + 16) * sp, yy + 8), fill=C['a2'])
            x += wd[wi] + gap
    if p.get('sub'):
        st = rts[-1] + .3
        for i, ln in enumerate(wrap(p['sub'], 'serif', 70, 900)):
            text_mask_up(img, ln, W / 2, y0 + len(lines) * lh + 40 + i * 74, 'serif', 70, C['a2'], prog(t, st + i * .1, .4), anchor='c')


# ------------------------------------------------------------- tabs multiplying -> merge into one workflow
TABS = ['LeetCode', 'GitHub', 'resume_v6.pdf', 'Striver sheet', 'ChatGPT', 'YT: DP in 1 shot', 'Notion', 'Course 14/83', 'StackOverflow',
        'jobs.xlsx', 'LinkedIn', 'GfG arrays', 'React docs', 'new chat', 'Udemy', 'notes.md', 'Codeforces', 'roadmap.sh', 'Kaggle',
        'portfolio-v2', 'mock test 3', 'system design?', 'assignment.pdf', 'HackerRank', 'Discord', 'interview Qs', 'Medium', 'TPO notice']


def vtabs(img, d, t, S, C):
    p = S['p']; N = p.get('n', 37); dur = S['dur']
    rnd = random.Random(p.get('seed', 3))
    mt = dur * p.get('merge', 2)  # merge start fraction (2 = never)
    mq = eio(prog(t, mt, .8))
    cnt = 0
    for i in range(N):
        st = .05 + dur * .6 * (i / N) ** 1.25
        pr = prog(t, st, .3)
        if pr <= 0:
            continue
        cnt += 1
        tx = 60 + (i % 3) * 330 + rnd.uniform(-20, 20)
        ty = 220 + (i // 3) * 92 + rnd.uniform(-8, 8)
        tx = lerp(tx, W / 2 - 150, mq); ty = lerp(ty, 900, mq)
        yy = lerp(-100, ty, eback(pr, 1.2))
        fill = C['card'] if i % 6 else C['a1']
        if mq < .98:
            d.rounded_rectangle((tx, yy, tx + 300, yy + 70), 14, fill=fill, outline=C['line'], width=2)
            d.ellipse((tx + 18, yy + 24, tx + 40, yy + 46), fill=C['a2'] if i % 4 == 0 else C['muted'])
            text(img, TABS[i % len(TABS)][:15], tx + 52, yy + 18, 'monor', 26, C['fg_on_a1'] if i % 6 == 0 else C['fg'])
    if mq <= 0:
        rect(d, (60, 1300, 60 + 960 * eo(prog(t, .1, .3)), 1520), C['fg'])
        if t > .3:
            text(img, str(cnt), 100, 1305, 'black', 170, C['bg'])
            text(img, p.get('label', 'TABS OPEN'), 460, 1350, 'mono', 40, C['a1'])
            text(img, p.get('label2', '0 CONNECTED'), 460, 1410, 'mono', 40, C['a2'])
    else:
        q = eback(prog(t, mt + .6, .5))
        if q > 0:
            w = 860 * min(1, q)
            rect(d, (W / 2 - w / 2, 760, W / 2 + w / 2, 1140), C['a1'], r=36)
            if q > .7:
                text(img, p.get('merged', 'ONE WORKFLOW'), W / 2, 800, 'black', 84, C['fg_on_a1'], anchor='c')
                steps = ['DSA', 'Projects', 'Resume', 'GitHub']
                for j, s in enumerate(steps):
                    pill(img, d, s, 130 + j * 215, 1000, C['fg_on_a1'], C['a1'], 30, a=eo(prog(t, mt + 1 + j * .15, .3)))


# ------------------------------------------------------------- activity vs progress meters
def vmeters(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    cx, cy, R = W / 2, 560, 300
    hours = p.get('hours', 11) * eo(prog(t, .1, dur * .6))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=C['fg'], width=10)
    for k in range(12):
        a = math.radians(k * 30)
        d.line((cx + (R - 40) * math.sin(a), cy - (R - 40) * math.cos(a), cx + (R - 12) * math.sin(a), cy - (R - 12) * math.cos(a)), fill=C['fg'], width=8)
    am = math.radians(hours * 360 * 2); ah = math.radians(hours * 30)
    d.line((cx, cy, cx + 230 * math.sin(am), cy - 230 * math.cos(am)), fill=C['a2'], width=8)
    d.line((cx, cy, cx + 150 * math.sin(ah), cy - 150 * math.cos(ah)), fill=C['fg'], width=14)
    d.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill=C['a1'])
    text(img, '%.1f h' % hours, cx, cy + R + 30, 'black', 90, C['fg'], anchor='c')
    for j, (lab, val, col) in enumerate([(p.get('l1', 'ACTIVITY'), 1.0, C['a2']), (p.get('l2', 'PROGRESS'), p.get('prog', .18), C['a1'])]):
        y = 1080 + j * 170
        q = eo(prog(t, .4 + j * .3, dur * .5))
        text(img, lab, 80, y, 'mono', 38, C['fg'])
        rect(d, (80, y + 60, 1000, y + 110), C['line'], r=25)
        rect(d, (80, y + 60, 80 + 920 * val * q, y + 110), col, r=25)
        text(img, '%d%%' % int(val * q * 100), 1000, y, 'mono', 38, col, anchor='r')
    chips = p.get('chips', ['37 videos watched', '120 problems tried', '4 courses started', '0 shipped projects'])
    for i, c in enumerate(chips):
        q = eback(prog(t, dur * .45 + i * .25, .3))
        if q > 0:
            pill(img, d, c, 80 + (i % 2) * 470, 1420 + (i // 2) * 90, C['card'], C['fg'], 30, a=min(1, q))


# ------------------------------------------------------------- roadmap revisions piling up
def vpile(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    items = p.get('items', ['roadmap_v%d.pdf' % i for i in range(1, 15)])
    rnd = random.Random(5)
    col_t = dur * p.get('collapse', .72)
    cq = prog(t, col_t, .7)
    base = 1450
    for i, it in enumerate(items):
        st = .05 + i * (col_t * .9 / len(items))
        q = eback(prog(t, st, .3), 1.3)
        if q <= 0:
            continue
        y = lerp(-120, base - i * 78, q)
        x = W / 2 - 330 + rnd.uniform(-40, 40) + math.sin(t * 3 + i) * (i * 1.5)
        if cq > 0:
            y += cq * cq * (1200 + i * 50); x += (i - len(items) / 2) * 50 * cq
        rect(d, (x, y, x + 660, y + 72), C['card'] if i % 3 else C['a1'], r=10, outline=C['fg'], width=3)
        text(img, it, x + 28, y + 14, 'mono', 34, C['fg_on_a1'] if i % 3 == 0 else C['fg'])
        text(img, 'edited' if i % 2 else 'NEW', x + 630, y + 18, 'monor', 26, C['muted'] if i % 3 else C['fg_on_a1'], anchor='r')
    if cq > .3:
        q = eback(prog(t, col_t + .4, .4))
        rect(d, (90, 820, 990, 1100), C['fg'], r=30)
        d.rounded_rectangle((150, 900, 250, 1000), 14, outline=C['bg'], width=8)
        if t > col_t + .9:
            d.line((168, 950, 195, 980, 235, 915), fill=C['a2'], width=12)
        text(img, p.get('done', 'Step 1: actually do it'), 290, 915, 'black', 56, C['bg'], a=min(1, q))
