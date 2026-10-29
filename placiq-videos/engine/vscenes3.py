from vscenes2 import *

# ------------------------------------------------------------- projects grow while chat context resets
def vreset(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    projs = p.get('projects', ['DSA: 140 solved', 'Chat app: M3', 'Resume v4', 'GitHub: 9 repos', 'SQL course 70%', 'Mock interview #2'])
    text(img, 'YOUR WORK', 70, 230, 'mono', 34, C['a1'])
    text(img, 'AI CHAT MEMORY', W - 70, 230, 'mono', 34, C['a2'], anchor='r')
    d.line((W / 2, 290, W / 2, 1450), fill=C['line'], width=4)
    k = 0
    for i, pr_ in enumerate(projs):
        q = eback(prog(t, .3 + i * dur * .12, .3))
        if q <= 0:
            continue
        k = i
        y = 300 + i * 180
        rect(d, (60, y, 60 + 450 * min(1, q), y + 150), C['card'], r=20, outline=C['a1'], width=3)
        for j, ln in enumerate(wrap(pr_, 'black', 40, 400)):
            text(img, ln, 85, y + 25 + j * 46, 'black', 40, C['fg'], a=min(1, q))
    # chat column: fills then resets on every new project
    seg_st = .3 + k * dur * .12
    fill = prog(t, seg_st, dur * .1)
    for j in range(min(4, int(1 + fill * 4))):
        y = 300 + j * 150
        rect(d, (W / 2 + 30, y, W - 60, y + 120), C['bg2'], r=20)
        text(img, ['I know Java...', 'I did 140 Qs', 'my project is...', 'my goal is SDE'][j], W / 2 + 55, y + 38, 'sans', 34, C['fg'])
    if prog(t, seg_st, .25) < 1 and t > .5:
        q = 1 - prog(t, seg_st, .25)
        rect(d, (W / 2 + 30, 300, W - 60, 1450), (C['a2'][0], C['a2'][1], C['a2'][2], 255))
        text(img, 'RESET', W * .75, 800, 'black', 90, C['bg'], anchor='c', a=q)
    pill(img, d, 'context lost x%d' % (k + 1), W / 2 + 40, 1480, C['a2'], C['bg'], 34)


# ------------------------------------------------------------- mentor's memory board being erased
def vboard(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    notes = p.get('notes', ['weak: DP', 'goal: backend SDE', 'project: expense API', 'resume: no metrics', 'strong: arrays', 'mock #1: nervous'])
    rect(d, (50, 240, W - 50, 1400), C['bg2'], r=16, outline=C['fg'], width=8)
    text(img, p.get('board', "MENTOR'S MEMORY BOARD"), 90, 270, 'mono', 32, C['muted'])
    cyc = p.get('cycles', 3); seg = dur * .8 / cyc
    c = min(cyc - 1, int(t / seg)); lt = t - c * seg
    er = prog(lt, seg * .6, seg * .3)
    for i, n in enumerate(notes):
        q = prog(lt, .1 + i * seg * .08, .25)
        x = 110 + (i % 2) * 450; y = 360 + (i // 2) * 300
        cut = 110 + er * 980
        if q <= 0 or x + 400 < cut and er > 0:
            continue
        for j, ln in enumerate(wrap(n, 'serif', 72, 400)):
            tw = text(img, ln, x, y + j * 74, 'serif', 72, C['fg'], a=q)
    if 0 < er < 1:
        ex = 110 + er * 980; ey = 700 + math.sin(er * 30) * 300
        rect(d, (ex - 90, ey - 60, ex + 90, ey + 60), C['a2'], r=14)
        rect(d, (ex - 90, ey + 30, ex + 90, ey + 60), C['fg'], r=8)
    text(img, 'session %d' % (c + 1), W / 2, 1440, 'black', 80, C['a2'], anchor='c')


# ------------------------------------------------------------- REAL product footage, vertical framing with pan
@lru_cache(maxsize=3)
def clip_frames(name):
    path = os.path.join(SHOTS, 'clips', name + '.mp4')
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280, 3)
    return a


def vclip(img, d, t, S, C):
    p = S['p']; dur = S['dur']
    if p.get('still'):
        src = shot(p['still']); fr = src.resize((1280, 720))
    else:
        fr_ = clip_frames(p['clip']); fr = Image.fromarray(fr_[min(len(fr_) - 1, int(t * 30 * p.get('speed', 1)) % len(fr_))])
    a, b = p.get('pan', ((0, 0), (.5, 0)))
    zw = p.get('cw', .5)  # crop width fraction of 1280
    ch = zw * 1280 / .82 / 720  # card aspect ~0.82
    ch = min(1, ch)
    k = eio(prog(t, .3, dur - .3))
    cx0 = lerp(a[0], b[0], k) * (1 - zw); cy0 = lerp(a[1], b[1], k) * (1 - ch)
    crop = fr.crop((int(cx0 * 1280), int(cy0 * 720), int((cx0 + zw) * 1280), int((cy0 + ch) * 720)))
    cw = 960; chh = int(cw * crop.size[1] / crop.size[0])
    enter = eo5(prog(t, 0, .5))
    y0 = p.get('y', 420) + (1 - enter) * 900
    rect(d, (60 - 18, y0 - 18, 60 + cw + 18, y0 + chh + 18), C['a1'], r=40)
    card = crop.resize((cw, chh), Image.BILINEAR).convert('RGBA'); card.putalpha(round_mask(cw, chh, 26))
    paste(img, card, 60, y0)
    text(img, 'REAL PLACIQ FOOTAGE' if not p.get('still') else 'REAL PLACIQ SCREEN', 60, y0 + chh + 34, 'mono', 26, C['muted'], a=enter)
    for c in p.get('callouts', []):
        txt, fx, fy, ft = c
        q = eback(prog(t, ft * dur, .3))
        if q <= 0:
            continue
        x = 60 + fx * cw; y = y0 + fy * chh
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=C['a2'])
        rr = 16 + 50 * prog(t, ft * dur, .6)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=C['a2'], width=4)
        tw, _ = tsize(txt, 'mono', 34)
        pill(img, d, txt, min(x + 30, W - tw - 90), y - 26, C['fg'], C['bg'], 34, a=min(1, q))
    if p.get('title'):
        head(img, p['title'], 170, t, .15, p.get('tsize', 84), C['fg'], C)


# ------------------------------------------------------------- big number
def vnumber(img, d, t, S, C):
    p = S['p']
    q = eo5(prog(t, .1, 1.4)); n = p['n']
    s = (p.get('pre', '') + '{:,}'.format(int(n * q)) + p.get('suffix', ''))
    for k in range(48):
        a = math.radians(k * 7.5 + t * 30); on = k / 48 < q
        r0 = 380; r1 = 410 if k % 4 else 440
        d.line((W / 2 + r0 * math.cos(a), 800 + r0 * math.sin(a), W / 2 + r1 * math.cos(a), 800 + r1 * math.sin(a)), fill=C['a1'] if on else C['line'], width=7)
    sz = 200 if len(s) < 6 else 160
    text(img, s, W / 2, 800 - sz * .62, 'black', sz, C['fg'], anchor='c')
    head(img, p.get('label', ''), 1280, t, .5, 54, C['a2'], C, 'mono')


# ------------------------------------------------------------- end cards (variants)
def vcta(img, d, t, S, C):
    p = S['p']; v = p.get('v', 'stack')
    url = p.get('url', 'learn.placiq.in')
    q = eback(prog(t, .05, .45))
    if v == 'stack':
        for i, w in enumerate(p.get('words', ['YOUR', 'WORK,', 'CONNECTED.'])):
            sz = min(150, int(150 * 920 / max(1, tsize(w, 'black', 150)[0])))
            text_mask_up(img, w, 80, 520 + i * 160, 'black', sz, C['a1'] if i == 2 else C['fg'], prog(t, .1 + i * .15, .35))
    else:
        r = 120 * q
        rect(d, (W / 2 - r, 560 - r, W / 2 + r, 560 + r), C['a1'], r=int(40 * q) + 1)
        if q > .7:
            text(img, 'P', W / 2, 470, 'black', 150, C['fg_on_a1'], anchor='c')
        text_mask_up(img, p.get('tag', 'Your work, connected.'), W / 2, 760, 'serif', 96, C['fg'], prog(t, .4, .4), anchor='c')
    text_mask_up(img, 'Placiq', W / 2 if v != 'stack' else 80, 1020, 'black', 130, C['fg'], prog(t, .5, .4), anchor='c' if v != 'stack' else 'l')
    bq = eback(prog(t, .9, .4))
    if bq > 0:
        pill(img, d, url + '  ->', W / 2, 1230, C['a1'], C['fg_on_a1'], 50, anchor='c', a=min(1, bq), pad=(40, 26))
    if p.get('foot'):
        text(img, p['foot'], W / 2, 1400, 'mono', 30, C['muted'], anchor='c', a=eo(prog(t, 1.2, .4)))


VSCENES = dict(vtype=vtype, vtabs=vtabs, vmeters=vmeters, vpile=vpile, vorbit=vorbit, vterm=vterm, vdash=vdash, vcards=vcards,
               vchats=vchats, vreset=vreset, vboard=vboard, vclip=vclip, vnumber=vnumber, vcta=vcta)
