"""Placiq SaaS launch film (1920x1080 @ 30fps).

Pipeline: Kokoro TTS per sentence -> beat-quantised shot timeline -> procedural electronic score + SFX (audio2) ->
PIL frame compositor over REAL Placiq product footage (assets/real-product/clips) -> FFmpeg H.264 master.

Usage (inside the placiq-render image):
    python launch.py A            # full render of variant A
    python launch.py A --stills   # QA stills only
Variants share one visual timeline; they differ in voice + score so they can be A/B tested.
"""
import os, sys, json, math, time, subprocess, re
os.environ.pop('PLACIQ_FMT', None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'v2'))
import numpy as np, soundfile as sf
from functools import lru_cache
from scipy.signal import resample_poly
from PIL import Image, ImageDraw, ImageFilter
from core import hexc, clamp, prog, eo, eo5, eio, eback, lerp, text_img, tsize, fade, ROOT
import canvas as CV
CV.set_geometry(1920, 1080)
from canvas import Clip, screen, crop_to_screen, drop, rrect, round_mask
import audio2 as A2
import build as B

W, H, FPS = 1920, 1080, 30
SLUG = '04-placiq-saas-launch'
OUT = os.path.join(ROOT, 'output', SLUG)
CACHE = os.path.join(ROOT, 'build', SLUG)

# ------------------------------------------------------------------ brand
PAPER, INK, ROYAL, CORAL = hexc('#F5F2EC'), hexc('#0F1117'), hexc('#3151EE'), hexc('#FF5A3C')
MIST, SAND, MUTED, WHITE = hexc('#E8ECFB'), hexc('#ECE6DA'), hexc('#8A877F'), hexc('#FFFFFF')
SKY = hexc('#AFC0FF')
LIGHT = dict(dark=False, line=hexc('#D8D2C6'))
DARK = dict(dark=True, line=hexc('#2A2E3A'))

VARIANTS = {
    'A': dict(voice='am_michael', speed=1.1, style='electro', root=45, seed=11, title='Placiq - Your work, connected (Launch film, cut A)'),
    'B': dict(voice='af_heart', speed=1.1, style='house', root=43, seed=29, title='Placiq - Your work, connected (Launch film, cut B)'),
}

P = 'Place IQ'  # pronunciation hint; captions always say "Placiq"
# Each shot: kind, lines=[(say, caption)], visual params. Durations come from narration, quantised to the beat.
SHOTS = [
    dict(id='chaos', kind='chaos', bg=PAPER, energy=1, label='// the problem',
         lines=[("You learn in one place.", "You learn in one place."),
                ("Build in another.", "Build in another."),
                ("Track your progress... nowhere.", "Track your progress nowhere."),
                ("And every AI conversation starts from zero.", "And every AI conversation starts from zero.")]),
    dict(id='reveal', kind='reveal', bg=ROYAL, energy=3, drop=True, label='// introducing',
         lines=[(f"Meet {P}.", "Meet Placiq."),
                ("Your AI-native, Career Intelligence OS.", "Your AI-native Career Intelligence OS.")]),
    dict(id='workspace', kind='workspace', bg=PAPER, energy=2, label='// one workspace', clip='welcome', c0=.6,
         lines=[("One workspace, where everything you do... connects.", "One workspace, where everything you do connects.")]),
    dict(id='readiness', kind='product', bg=PAPER, energy=2, label='// 01  diagnose', clip='readiness_a', c0=1.2, side='right',
         head='Know where|you *stand.*', crop0=(.5, .5, .95), crop1=(.5, .62, .62),
         callouts=[(.42, (.31, .74), 'Readiness score'), (.62, (.57, .70), 'Competency gaps')], sub=('gapanalysis', 2.0),
         lines=[("It starts with where you stand.", "It starts with where you stand."),
                ("Career Readiness finds your gaps.", "Career Readiness finds your gaps.")]),
    dict(id='navigator', kind='product', bg=MIST, energy=2, label='// 02  prioritize', clip='navigator_a', c0=3.2, side='left',
         head='Do the *right*|thing next.', crop0=(.55, .5, .95), crop1=(.62, .55, .7),
         callouts=[(.35, (.55, .52), 'Recommended next')],
         lines=[("Career Navigator prioritizes what to do next.", "Career Navigator prioritizes what to do next.")]),
    dict(id='dsa', kind='product', bg=PAPER, energy=2, label='// 03  learn', clip='dsa_viz', c0=1.0, side='right',
         head='Watch the|concept *click.*', crop0=(.5, .5, .95), crop1=(.5, .4, .72),
         callouts=[(.35, (.45, .24), 'Step-by-step visualisation'), (.6, (.80, .2), 'Live code trace')],
         lines=[("Interactive D S A visualizations make concepts click.", "Interactive DSA visualizations make concepts click.")]),
    dict(id='builder', kind='split', bg=SAND, energy=2, label='// 04  build', clip='builder', c0=.6, clip2='roadmap_a', c2=.8,
         head='From idea to|*milestones.*',
         lines=[("And the AI Project Builder turns an idea... into guided, milestone by milestone development.",
                 "And the AI Project Builder turns an idea into guided, milestone-by-milestone development.")]),
    dict(id='proof', kind='statement', bg=INK, energy=1, drop=False, label='// from learning to proof',
         lines=[("Then, learning becomes proof.", "Then, learning becomes proof.")]),
    dict(id='github', kind='product', bg=INK, energy=3, label='// 05  evidence', clip='github', c0=.3, side='right',
         head='Commits become|*evidence.*', crop0=(.5, .5, .95), crop1=(.42, .45, .7), dark=True,
         callouts=[(.45, (.25, .3), 'Verified project evidence')],
         lines=[("Your GitHub work becomes project evidence.", "Your GitHub work becomes project evidence.")]),
    dict(id='resume', kind='product', bg=INK, energy=3, label='// 06  present', clip='resume', c0=.5, side='left',
         head='Every claim,|*checked.*', crop0=(.5, .5, .95), crop1=(.5, .4, .72), dark=True, sub=('resume_report', 1.0),
         callouts=[(.4, (.5, .3), 'Skills vs. claims')],
         lines=[("Resume Intelligence analyzes every skill, and every claim.", "Resume Intelligence analyzes every skill and every claim.")]),
    dict(id='passport', kind='product', bg=INK, energy=3, label='// 07  skill passport', clip='passport', c0=.2, side='right',
         head='Skills you can|*demonstrate.*', crop0=(.5, .5, .95), crop1=(.5, .45, .75), dark=True,
         lines=[("Your Skill Passport organizes what you can actually demonstrate.", "Your Skill Passport organizes what you can actually demonstrate.")]),
    dict(id='pcme', kind='pcme', bg=INK, energy=3, label='// PCME  persistent context & memory engine', clip='pcme_a', c0=.8, clip2='copilot_a', c2=1.0,
         lines=[("And P C M E ties it all together,", "And PCME ties it all together,"),
                ("remembering your progress and context, across every interaction.", "remembering your progress and context across every interaction.")]),
    dict(id='loop', kind='loop', bg=PAPER, energy=3, drop=True, label='// one connected loop',
         lines=[("Diagnose. Prioritize. Learn. Build. Evidence. Present. Reassess.", "Diagnose. Prioritize. Learn. Build. Evidence. Present. Reassess.")]),
    dict(id='resolve', kind='resolve', bg=PAPER, energy=2, label='// one system',
         lines=[("Every step feeds the next, in one connected system.", "Every step feeds the next, in one connected system.")]),
    dict(id='end', kind='end', bg=INK, energy=1, label='',
         lines=[(f"{P}. Your work, connected.", "Placiq. Your work, connected."),
                ("Start free, at learn dot place IQ dot in.", "Start free at learn.placiq.in")], hold=.5),
]
LOOP = [('Diagnose', 'readiness_a', 3), ('Prioritize', 'navigator_a', 3), ('Learn', 'dsa_viz', 4), ('Build', 'roadmap_a', 3),
        ('Evidence', 'github_a', 1), ('Present', 'resume_a', 3), ('Reassess', 'readiness', 2)]


# ------------------------------------------------------------------ timeline
def timeline(V):
    vd = os.path.join(CACHE, 'vo_%s_%.2f' % (V['voice'], V['speed'])); os.makedirs(vd, exist_ok=True)
    bpm = A2.STY[V['style']]['bpm']; beat = 60 / bpm; bar = beat * 4
    t, scs = 0.0, []
    for i, s in enumerate(SHOTS):
        S = dict(s); S['idx'] = i
        if S.get('drop') and scs:  # land drops on a bar line
            nb = math.ceil((t - 1e-6) / (beat * 2)) * beat * 2
            scs[-1]['dur'] += nb - t; t = nb
        lead = .55 if i == 0 else (.45 if S.get('drop') else .3)
        cur, vos, words, cues, chunks = lead, [], [], [], []
        for k, (say, cap) in enumerate(S['lines']):
            a, ws = B.tts(say, V['voice'], V['speed'], os.path.join(vd, f'{S["id"]}_{k}'))
            d = len(a) / 24000
            vos.append((cur, a)); cues.append(cur)
            ws = [[w, b + cur, e + cur] for w, b, e in ws]; words += ws
            chunks += [[c, s0, s1] for c, s0, s1 in split_caption(cap, ws, cur, cur + d)]
            cur += d + (.26 if S['kind'] == 'chaos' else .2)
        dur = math.ceil((cur + .35 + S.get('hold', 0)) / beat) * beat
        dur = max(dur, {'chaos': 9.4, 'reveal': 6.5, 'loop': 7.0, 'resolve': 4.8, 'end': 6.4}.get(S['kind'], 3.8))
        S.update(t0=t, dur=dur, vos=vos, words=words, cues=cues, chunks=chunks)
        scs.append(S); t += dur
    return scs, t, beat


def split_caption(cap, ws, s, e, maxw=8):
    toks = cap.split()
    if len(toks) <= maxw or not ws:
        return [[cap, s, e]]
    n = math.ceil(len(toks) / maxw); per = math.ceil(len(toks) / n); out = []
    for j in range(n):
        part = toks[j * per:(j + 1) * per]
        a = s + (e - s) * j * per / len(toks); b = s + (e - s) * min(len(toks), (j + 1) * per) / len(toks)
        # snap to nearest real word timings
        if ws:
            a = min(ws, key=lambda w: abs(w[1] - a))[1] if j else s
            b = e if j == n - 1 else min(ws, key=lambda w: abs(w[2] - b))[2]
        out.append([' '.join(part), a, b])
    return out


# ------------------------------------------------------------------ drawing helpers
def ink_on(bg):
    return WHITE if bg in (INK, ROYAL) else INK


def accent_on(bg):
    return SKY if bg == INK else (WHITE if bg == ROYAL else ROYAL)


def head(img, spec, x, y, size, t, t0, bg, anchor='l', stagger=.07, lh=1.05, maxw=None):
    """Editorial headline: '|' line break, *word* = italic serif accent. Masked word-by-word rise."""
    fg, ac = ink_on(bg), accent_on(bg)
    lines = spec.split('|'); k = 0; yy = y
    if maxw:
        wid = max(sum(tsize(w.strip('*'), 'serif' if w.startswith('*') else 'black', int(size * (1.22 if w.startswith('*') else 1)))[0] + size * .26 for w in ln.split(' ')) for ln in lines)
        size = int(size * min(1, maxw / wid))
    for ln in lines:
        toks = []
        for wd in ln.split(' '):
            it = wd.startswith('*')
            wd = wd.strip('*')
            toks.append((wd, 'serif' if it else 'black', int(size * (1.22 if it else 1)), ac if it else fg, it))
        sp = size * .26
        widths = [tsize(w, f, s)[0] for w, f, s, c, it in toks]
        tot = sum(widths) + sp * (len(toks) - 1)
        xx = x - (tot / 2 if anchor == 'c' else 0)
        for (w, f, s, c, it), wd_ in zip(toks, widths):
            dy = -size * .17 if it else 0
            CV.Tmask(img, w, xx, yy + dy, f, s, c, prog(t, t0 + k * stagger, .55))
            xx += wd_ + sp; k += 1
        yy += size * lh * 1.12
    return yy


def label(img, txt, t, bg, x=96, y=64):
    if not txt:
        return
    col = MUTED if bg != ROYAL else SKY
    if bg == INK:
        col = hexc('#7C8194')
    n = int(len(txt) * eo(prog(t, .05, .5)))
    CV.T(img, txt[:n], x, y, 'monor', 22, col)
    CV.T(img, 'PLACIQ', W - 96, y, 'mono', 22, col, anchor='r', a=eo(prog(t, .05, .4)))


@lru_cache(maxsize=64)
def still_frame(name, ct):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '%.2f' % ct, '-i', os.path.join(CV.CLIPS, name + '.mp4'), '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    return Image.frombuffer('RGB', (1280, 720), r.stdout, 'raw', 'RGB', 0, 1).copy()


@lru_cache(maxsize=256)
def card(name, ct, w, dark=False, chrome=True):
    """Pre-composited static browser card (RGBA incl. soft shadow) for multi-window choreography."""
    src = still_frame(name, ct)
    h = int(w * 0.56) + (int(w * .03) if chrome else 0)
    pad = int(w * .08)
    L = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad + w * .02, pad + w, pad + h + w * .02), int(w * .025), fill=(10, 12, 20, 70 if not dark else 140))
    L = Image.alpha_composite(L, sh.filter(ImageFilter.GaussianBlur(w * .03)))
    C = dict(dark=dark)
    tmp = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    CV.G.U, keep = w / 1700, CV.G.U
    screen(tmp, ImageDraw.Draw(tmp), src, (.5, .5, .94), (0, 0, w, h), C, chrome='learn.placiq.in' if chrome else None)
    CV.G.U = keep
    L.alpha_composite(tmp, (pad, pad))
    return L, pad


def put(img, cardpad, cx, cy, a=1.0, scale=1.0):
    c, pad = cardpad
    if scale != 1.0:
        c = c.resize((max(2, int(c.width * scale)), max(2, int(c.height * scale))), Image.BILINEAR); pad = int(pad * scale)
    if a < .999:
        c = fade(c, a)
    img.paste(c, (int(cx - c.width / 2), int(cy - c.height / 2)), c)


def live(img, name, ct, box, crop, dark=False, a=1.0, chrome='learn.placiq.in'):
    src = Clip.get(name).at(ct)
    return screen(img, ImageDraw.Draw(img), src, crop, box, dict(dark=dark), chrome=chrome, a=a)


def lerpbox(b0, b1, x):
    return tuple(lerp(p, q, x) for p, q in zip(b0, b1))


def callout(img, d, pt, txt, p, bg, side=1):
    if p <= 0:
        return
    x, y = pt
    e = eback(clamp(p * 2.2))
    r = 13 * e
    pulse = (p * 3) % 1
    d.ellipse((x - r, y - r, x + r, y + r), fill=CORAL)
    rr = 13 + 34 * pulse
    d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=CORAL[:3] + (int(255 * (1 - pulse)),), width=3)
    q = eo5(prog(p, .15, .4))
    if q <= 0:
        return
    lx = x + side * 150 * q; ly = y - 92
    d.line((x, y, x + side * 50 * q, ly + 26, lx, ly + 26), fill=INK if bg != INK else WHITE, width=3)
    fg, tc = (INK, WHITE) if bg != INK else (WHITE, INK)
    CV.chip(img, d, txt, lx, ly, fg, tc, 26, 'mono', anchor='l' if side > 0 else 'r', a=q)


def cam(img, t, dur, amt=.03, focus=(.5, .5)):
    z = 1 + amt * eio(clamp(t / max(dur, .1)))
    if z <= 1.0005:
        return img
    cw, ch = W / z, H / z
    x0 = (W - cw) * focus[0]; y0 = (H - ch) * focus[1]
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)


def bg_for(col):
    im = Image.new('RGB', (W, H), col[:3])
    if col in (PAPER, SAND, MIST):
        d = ImageDraw.Draw(im); dot = tuple(max(0, c - 18) for c in col[:3])
        for y in range(27, H, 54):
            for x in range(27, W, 54):
                d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=dot)
    elif col == INK:
        d = ImageDraw.Draw(im)
        for x in range(0, W, 96):
            d.line((x, 0, x, H), fill=(22, 25, 34))
    return im


BG = {}


def background(col):
    k = tuple(col)
    if k not in BG:
        BG[k] = bg_for(col)
    return BG[k].copy()


# ------------------------------------------------------------------ shots
CHAOS = [  # (clip, still time, cx, cy, width, cue index, delay)
    ('dsa_viz', 3, 560, 470, 760, 0, 0.0), ('dsa', 2, 1400, 330, 560, 0, .35),
    ('ide2', 3, 1330, 640, 720, 1, 0.0), ('github_a', 6, 520, 760, 600, 1, .3), ('editor', 4, 1500, 860, 520, 1, .55),
    ('project_catalog', 2, 900, 300, 560, 2, 0.0), ('resume_a', 2, 330, 330, 480, 2, .15), ('roadmap', 2, 1640, 470, 470, 2, .3),
    ('streaks', 2, 980, 820, 520, 2, .42), ('procoding', 3, 260, 600, 440, 2, .52), ('company', 3, 1180, 480, 480, 2, .62),
    ('analyzer', 2, 760, 620, 500, 2, .72),
]
STICKY = [('resume_FINAL_v7.pdf', 300, 905, 2), ('47 tabs open', 1560, 175, 2), ('project (unfinished)', 1280, 985, 2), ('streak lost', 240, 470, 2)]


def chaos_layout(S, t):
    out = []
    for i, (n, ct, cx, cy, w, cue, dl) in enumerate(CHAOS):
        ta = S['cues'][cue] + dl
        if t < ta:
            continue
        a = eo(prog(t, ta, .3)); s = .86 + .14 * eback(prog(t, ta, .45))
        drift = (t - ta)
        jit = max(0, t - S['cues'][3]) * 1.2
        x = cx + math.sin(drift * .7 + i) * 14 + math.sin(t * 23 + i * 3) * jit * 2
        y = cy + math.cos(drift * .6 + i * 2) * 10 + (1 - a) * 40
        out.append((n, ct, w, x, y, a, s))
    return out


def sh_chaos(img, d, t, S):
    bg = S['bg']
    for (n, ct, w, x, y, a, s) in chaos_layout(S, t):
        put(img, card(n, ct, w), x, y, a, s)
    for txt, x, y, cue in STICKY:
        p = prog(t, S['cues'][cue] + .2 + x / 4000, .3)
        if p > 0:
            CV.chip(img, d, txt, x, y, CORAL, WHITE, 24, 'mono', anchor='c', a=eo(p))
    # AI chat that starts from zero
    c3 = S['cues'][3]
    if t > c3 - .1:
        p = eo5(prog(t, c3 - .1, .4))
        bx, by, bw, bh = 1180, 160 + 60 * (1 - p), 620, 430
        drop(img, (bx, by, bx + bw, by + bh), 24, 30, 90)
        rrect(d, (bx, by, bx + bw, by + bh), WHITE, 24)
        CV.T(img, 'AI chat', bx + 30, by + 24, 'mono', 24, INK)
        CV.chip(img, d, 'New conversation', bx + bw - 30, by + 18, SAND, INK, 20, 'monor', anchor='r')
        d.line((bx, by + 76, bx + bw, by + 76), fill=SAND, width=2)
        q = 'Remember the project I showed you last week?'
        k = int(len(q) * clamp((t - c3 - .1) / 1.1))
        rrect(d, (bx + 120, by + 110, bx + bw - 30, by + 200), ROYAL, 20)
        for li, ln in enumerate(CV.wrap(q[:k], 'monor', 24, bw - 200)):
            CV.T(img, ln, bx + 145, by + 122 + li * 32, 'monor', 24, WHITE)
        if t > c3 + 1.4:
            pa = eo(prog(t, c3 + 1.4, .3))
            rrect(d, (bx + 30, by + 230, bx + bw - 120, by + 330), SAND, 20)
            r = "I don't have any memory of previous conversations."
            for li, ln in enumerate(CV.wrap(r, 'monor', 24, bw - 200)):
                CV.T(img, ln, bx + 55, by + 246 + li * 32, 'monor', 24, INK, a=pa)
            CV.T(img, 'context: 0', bx + 30, by + bh - 62, 'mono', 26, CORAL, a=pa)
    # kinetic statement card (bottom-left)
    words = ['Learn *here.*', 'Build *there.*', 'Progress: *nowhere.*', 'Context: *zero.*']
    ci = max([i for i, c in enumerate(S['cues']) if t >= c - .05] or [0])
    if t >= S['cues'][0] - .05:
        sw = sum(tsize(w.strip('*'), 'serif' if w.startswith('*') else 'black', int(88 * (1.22 if w.startswith('*') else 1)))[0] + 23 for w in words[ci].split(' '))
        rrect(d, (70, 860, 70 + sw + 80, 1020), INK, 26)
        head(img, words[ci], 110, 880, 88, t, S['cues'][ci] - .05, INK, stagger=.06)
    label(img, S['label'], t, bg)


def sh_reveal(img, d, t, S, prev=None):
    """Chaos collapses into one window on royal blue, then 'Meet Placiq.'"""
    C0 = SHOTS_T[0]
    tc = C0['dur']
    k = eio(prog(t, 0, .75))
    if k < 1:
        for (n, ct, w, x, y, a, s) in chaos_layout(C0, tc):
            put(img, card(n, ct, w), lerp(x, W / 2, k), lerp(y, H / 2 + 60, k), a * (1 - prog(t, .5, .25)), s * (1 - .85 * k))
    c1 = S['cues'][1] if len(S['cues']) > 1 else 2
    # logo + Meet
    p = prog(t, .7, .5)
    if p > 0:
        up = eio(prog(t, c1 - .25, .7))
        y = lerp(H / 2 - 110, 120, up); sz = lerp(1.0, .55, up)
        head(img, 'Meet *Placiq.*', W / 2, y, int(170 * sz), t, .72, ROYAL, anchor='c', stagger=.12)
    # window rises after second cue
    if t > c1 - .25:
        q = eo5(prog(t, c1 - .25, .9))
        bw = lerp(300, 1040, q); bh = bw * .6
        cy = lerp(H + 200, 670, q)
        live(img, 'welcome', .5 + (t - c1) * .9, (W / 2 - bw / 2, cy - bh / 2, W / 2 + bw / 2, cy + bh / 2), (.5, .5, .94))
    if t > c1 + .2:
        head(img, 'Your AI-native *Career Intelligence OS.*', W / 2, 250, 52, t, c1 + .2, ROYAL, anchor='c', stagger=.05)
    label(img, S['label'], t, ROYAL)


MODULES = [('DSA practice', -1, .2), ('Pro coding', -1, .38), ('Copilot', -1, .56), ('Memory', -1, .74),
           ('Resume', 1, .2), ('Portfolio', 1, .38), ('GitHub evidence', 1, .56), ('Career navigator', 1, .74)]


def sh_workspace(img, d, t, S):
    bg = S['bg']
    # window glides from reveal's position into a centred hero
    q = eio(prog(t, 0, .9))
    b0 = (W / 2 - 520, 670 - 312, W / 2 + 520, 670 + 312)
    b1 = (W / 2 - 500, 240, W / 2 + 500, 240 + 610)
    box = lerpbox(b0, b1, q)
    inner = live(img, 'welcome', S['c0'] + 1.5 + t * .8, box, (.5, .5, .94) if t < 1 else (.5, lerp(.5, .42, eio(prog(t, 1, 3))), lerp(.94, .8, eio(prog(t, 1, 3)))))
    head(img, 'Everything you do,|*connected.*', W / 2, 60, 66, t, .3, bg, anchor='c', stagger=.06, lh=.95)
    # module chips snap in from both sides with connector lines into the window
    for i, (nm, side, fy) in enumerate(MODULES):
        p = eo5(prog(t, .9 + i * .12, .5))
        if p <= 0:
            continue
        y = box[1] + (box[3] - box[1]) * fy + 30
        ex = box[0] if side < 0 else box[2]
        x = ex + side * (40 + 70 * p)
        d.line((ex, y + 20, x, y + 20), fill=ROYAL, width=3)
        d.ellipse((ex - 7, y + 13, ex + 7, y + 27), fill=CORAL)
        CV.chip(img, d, nm, x, y, INK, WHITE, 24, 'mono', anchor='r' if side < 0 else 'l', a=p)
    label(img, S['label'], t, bg)


def sh_product(img, d, t, S):
    bg, dark = S['bg'], S.get('dark', False)
    side = S['side']
    wl = (720, 180, 1840, 180 + 690) if side == 'right' else (80, 180, 1200, 180 + 690)
    # enter: window slides from centre-ish with a soft scale; crop push-in (precisely timed zoom)
    q = eo5(prog(t, 0, .7))
    sx = (W / 2 - (wl[0] + wl[2]) / 2) * (1 - q) * .35
    box = (wl[0] + sx, wl[1] + 40 * (1 - q), wl[2] + sx, wl[3] + 40 * (1 - q))
    z = eio(prog(t, .8, S['dur'] * .55))
    crop = tuple(lerp(a, b, z) for a, b in zip(S['crop0'], S['crop1']))
    sub = S.get('sub')
    if sub and len(S['cues']) > 1 or (sub and S['id'] == 'resume'):
        ts = S['cues'][-1] if len(S['cues']) > 1 else S['dur'] * .45
    else:
        ts = None
    inner = live(img, S['clip'], S['c0'] + t * .85, box, crop, dark)
    for (tp, pt, txt) in S.get('callouts', []):
        p = prog(t, S['dur'] * tp, 1.2)
        if p > 0 and (ts is None or t < ts + .2):
            sp = crop_to_screen(crop, inner, (1280, 720), pt)
            if inner[0] < sp[0] < inner[2] and inner[1] < sp[1] < inner[3]:
                callout(img, d, sp, txt, p, bg, side=1 if sp[0] < (inner[0] + inner[2]) / 2 + 200 else -1)
    if ts is not None and t > ts:
        p = eo5(prog(t, ts, .6))
        bw, bh = 760, 470
        if side == 'right':
            bx = lerp(W + 20, 600, p)
        else:
            bx = lerp(-bw - 20, 560, p)
        by = 520
        live(img, sub[0], sub[1] + (t - ts) * .9, (bx, by, bx + bw, by + bh), (.5, .5, .94), dark)
    tx = 120 if side == 'right' else 1290
    label(img, S['label'], t, bg)
    head(img, S['head'], tx, 400, 78, t, .25, bg, stagger=.07, maxw=540)
    cap = S['lines'][-1][1]
    for li, ln in enumerate(CV.wrap(cap, 'monor', 24, 500)):
        CV.T(img, ln, tx, 640 + li * 36, 'monor', 24, MUTED if bg != INK else hexc('#9AA0B4'), a=eo(prog(t, .7 + li * .1, .5)))


def sh_split(img, d, t, S):
    """Builder full window -> splits into idea | milestones roadmap."""
    bg = S['bg']
    sp = eio(prog(t, S['dur'] * .38, .9))
    full = (700, 200, 1840, 200 + 690)
    left = (100, 300, 940, 300 + 520)
    b1 = lerpbox(full, left, sp)
    live(img, S['clip'], S['c0'] + t * .8, b1, (lerp(.5, .42, sp), .45, lerp(.94, .7, sp)))
    if sp > 0:
        rx = lerp(W + 40, 980, sp)
        live(img, S['clip2'], S['c2'] + max(0, t - S['dur'] * .38) * .8, (rx, 260, rx + 840, 260 + 600), (.6, .4, .66))
        # milestone ticks travelling between both windows
        for i in range(4):
            p = prog(t, S['dur'] * .55 + i * .35, .35)
            if p > 0:
                y = 880 + 0
                x = 980 + i * 210
                d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=ROYAL if p >= 1 else SAND, outline=ROYAL, width=3)
                if p >= 1:
                    d.line((x - 6, y, x - 1, y + 6, x + 8, y - 6), fill=WHITE, width=3)
                if i:
                    d.line((x - 196, y, x - 196 + 182 * eo(p), y), fill=ROYAL, width=3)
                CV.T(img, ['Plan', 'Scaffold', 'Build', 'Ship'][i], x, y + 26, 'monor', 22, INK, anchor='c', a=eo(p))
        CV.chip(img, d, 'your idea', 120, 250, INK, WHITE, 22, 'mono', a=eo(prog(t, S['dur'] * .45, .4)))
        CV.chip(img, d, 'guided milestones', 1000, 205, ROYAL, WHITE, 22, 'mono', a=eo(prog(t, S['dur'] * .5, .4)))
    hx = lerp(120, 120, sp)
    hy = lerp(400, 880, sp)
    if sp < .05:
        head(img, S['head'], 110, 420, 74, t, .25, bg)
    else:
        head(img, 'From idea to *milestones.*', 120, 900, 56, 1, 0, bg)
    label(img, S['label'], t, bg)


def sh_statement(img, d, t, S):
    bg = S['bg']
    c = S['cues'][0]
    head(img, 'Learning', W / 2, 330, 170, t, c, bg, anchor='c')
    p = eo5(prog(t, c + .6, .5))
    tw = tsize('Learning', 'black', 170)[0]
    if p > 0:
        d.rectangle((W / 2 - tw / 2, 440, W / 2 - tw / 2 + tw * p, 452), fill=CORAL)
    head(img, 'becomes *proof.*', W / 2, 560, 170, t, c + .75, bg, anchor='c', stagger=.15)
    label(img, S['label'], t, bg)


def sh_pcme(img, d, t, S):
    bg = S['bg']
    q = eo5(prog(t, 0, .7))
    box = (140, 200 + 30 * (1 - q), 1160, 200 + 640 + 30 * (1 - q))
    z = eio(prog(t, .6, 3))
    inner = live(img, S['clip'], S['c0'] + t * .8, box, (lerp(.5, .45, z), lerp(.5, .55, z), lerp(.95, .7, z)), True)
    c1 = S['cues'][1] if len(S['cues']) > 1 else 2
    p = eo5(prog(t, c1 - .3, .7))
    if p > 0:
        bx = lerp(W + 20, 1000, p)
        live(img, S['clip2'], S['c2'] + (t - c1) * .9, (bx, 430, bx + 800, 430 + 500), (.5, .5, .94), True)
        # memory threads from memory list into the copilot conversation
        for i in range(3):
            pp = prog(t, c1 + .2 + i * .3, .8)
            if pp > 0:
                y0 = inner[1] + 150 + i * 90
                pts = CV.bezier((inner[0] + 600, y0), ((inner[0] + 600 + bx) / 2, y0 - 160), (bx + 120, 560 + i * 90), 30)
                pts = CV.partial(pts, eo(pp))
                if len(pts) > 1:
                    d.line(pts, fill=CORAL, width=4)
                    d.ellipse((pts[-1][0] - 8, pts[-1][1] - 8, pts[-1][0] + 8, pts[-1][1] + 8), fill=CORAL)
    head(img, 'Memory that *carries over.*', 140, 900, 64, t, .3, bg, stagger=.06)
    for k, txt in enumerate(['progress', 'context', 'goals']):
        a = eo(prog(t, c1 + .5 + k * .25, .4))
        CV.chip(img, d, '+ remembers ' + txt, 1820, 210 + k * 62, ROYAL, WHITE, 22, 'mono', anchor='r', a=a)
    label(img, S['label'], t, bg)


def loop_pos(i, rot=0.0):
    ang = -math.pi / 2 + i * 2 * math.pi / 7 + rot
    return W / 2 + 660 * math.cos(ang), 560 + 330 * math.sin(ang)


def loop_times(S):
    names = [n.lower() for n, _, _ in LOOP]; out = []; j = 0
    for w, b, e in S['words']:
        ww = re.sub(r'\W', '', w.lower())
        if j < 7 and ww.startswith(names[j][:5]):
            out.append(b); j += 1
    while len(out) < 7:
        out.append((out[-1] if out else .5) + .6)
    return out


def sh_loop(img, d, t, S):
    bg = S['bg']
    ts = loop_times(S)
    rot = .05 * max(0, t - ts[-1])
    pts = [loop_pos(i, rot) for i in range(7)]
    # path
    ring = [(W / 2 + 660 * math.cos(a), 560 + 330 * math.sin(a)) for a in np.linspace(-math.pi / 2 + rot, 1.5 * math.pi + rot, 140)]
    k = clamp((t - ts[0]) / max(.1, ts[-1] + .6 - ts[0]))
    part = ring[:max(2, int(len(ring) * k))]
    d.line(ring, fill=hexc('#DCD6CA'), width=3)
    if k > 0:
        d.line(part, fill=ROYAL, width=6)
        hx, hy = part[-1]
        d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=CORAL)
    for i, (nm, clip, ct) in enumerate(LOOP):
        p = prog(t, ts[i] - .1, .45)
        x, y = pts[i]
        if p <= 0:
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=hexc('#CFC8BA'))
            continue
        put(img, card(clip, ct, 300), x, y - 10, eo(p), .6 + .4 * eback(p))
        CV.chip(img, d, f'{i + 1:02d}  {nm}', x, y + 95, ROYAL if t < (ts[i + 1] if i < 6 else 99) else INK, WHITE, 24, 'mono', anchor='c', a=eo(p))
    a = eo(prog(t, ts[-1] + .4, .6))
    if a > 0:
        head(img, 'One *continuous* loop.', W / 2, 520, 70, t, ts[-1] + .4, bg, anchor='c')
    label(img, S['label'], t, bg)


def sh_resolve(img, d, t, S):
    bg = S['bg']
    L = SHOTS_T[[s['id'] for s in SHOTS_T].index('loop')]
    rot = .05 * max(0, L['dur'] - loop_times(L)[-1])
    k = eio(prog(t, 0, 1.1))
    big = (W / 2 - 640, 250, W / 2 + 640, 250 + 720)
    # thumbnails converge into the single workspace window
    for i, (nm, clip, ct) in enumerate(LOOP):
        x, y = loop_pos(i, rot)
        put(img, card(clip, ct, 300), lerp(x, W / 2, k), lerp(y - 10, 610, k), 1 - prog(t, .8, .4), 1 - .4 * k)
    if t > .8:
        q = eo5(prog(t, .8, .8))
        bw = lerp(300, 1280, q); bh = bw * .5625
        live(img, 'welcome', 3 + (t - .8) * .7, (W / 2 - bw / 2, 610 - bh / 2 + 0, W / 2 + bw / 2, 610 + bh / 2), (.5, .5, .94), a=min(1, q * 1.5))
    head(img, 'One *connected* system.', W / 2, 70, 84, t, .6, bg, anchor='c')
    label(img, S['label'], t, bg)


def sh_end(img, d, t, S):
    c1 = S['cues'][1] if len(S['cues']) > 1 else 3
    q = eback(prog(t, .15, .6))
    s = 170 * q
    lx = W / 2 - 330; ly = 300
    if s > 2:
        rrect(d, (lx + 85 - s / 2, ly + 85 - s / 2, lx + 85 + s / 2, ly + 85 + s / 2), WHITE, int(s * .24))
    if q > .7:
        CV.T(img, 'P', lx + 85, ly + 85, 'black', 120, INK, anchor='c', vanchor='m')
    CV.Tmask(img, 'Placiq', lx + 210, ly - 6, 'black', 170, WHITE, prog(t, .45, .6))
    u = eo5(prog(t, .9, .6))
    d.rectangle((lx, ly + 215, lx + 700 * u, ly + 223), fill=CORAL)
    head(img, 'Your work, *connected.*', W / 2, ly + 270, 88, t, 1.05, INK, anchor='c', stagger=.1)
    b = eback(prog(t, c1, .5))
    if b > 0:
        CV.chip(img, d, 'Start free at learn.placiq.in  ->', W / 2, ly + 470, ROYAL, WHITE, 38, 'mono', anchor='c', a=min(1, b))
        cx, cy = W / 2 + 250, ly + 560 + 50 * (1 - eo(prog(t, c1 + .3, .5)))
        d.polygon([(cx, cy), (cx, cy + 46), (cx + 13, cy + 34), (cx + 30, cy + 34)], fill=WHITE, outline=INK)
        if t > c1 + .8:
            r = 20 + 70 * prog(t, c1 + .8, .6)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=CORAL[:3], width=4)
    CV.T(img, 'AI-native Career Intelligence OS  ·  placiq.in', W / 2, H - 120, 'monor', 24, hexc('#7C8194'), anchor='c', a=eo(prog(t, 1.6, .6)))


SHOT_FN = dict(chaos=sh_chaos, reveal=sh_reveal, workspace=sh_workspace, product=sh_product, split=sh_split,
               statement=sh_statement, pcme=sh_pcme, loop=sh_loop, resolve=sh_resolve, end=sh_end)
CAM = dict(chaos=.06, reveal=.02, workspace=.035, product=.03, split=.02, statement=.05, pcme=.03, loop=.04, resolve=.02, end=.03)
SHOTS_T = []


def render_shot(S, lt):
    img = background(S['bg'])
    SHOT_FN[S['kind']](img, ImageDraw.Draw(img), lt, S)
    return cam(img, lt, S['dur'], CAM[S['kind']])


def frame(scs, g):
    si = max(i for i, S in enumerate(scs) if S['t0'] <= g + 1e-9)
    S = scs[si]; lt = g - S['t0']
    img = render_shot(S, lt)
    XF = .3
    if si > 0 and lt < XF and S['kind'] not in ('reveal',):
        P0 = scs[si - 1]
        prev = render_shot(P0, P0['dur'] + lt)
        a = eio(lt / XF)
        if S['bg'] != P0['bg']:  # colour change: directional wipe with a coral leading edge
            x = int(W * a)
            out = prev.copy(); out.paste(img.crop((0, 0, x, H)), (0, 0))
            if 0 < x < W:
                ImageDraw.Draw(out).rectangle((x - 10, 0, x, H), fill=CORAL[:3])
            img = out
        else:
            img = Image.blend(prev, img, a)
    if S['kind'] == 'reveal' and lt < .12:  # flash on the drop
        img = Image.blend(img, Image.new('RGB', (W, H), (255, 255, 255)), (1 - lt / .12) * .7)
    return img


# ------------------------------------------------------------------ audio
def sfx_events(scs, beat):
    ev = []
    for S in scs:
        t0, k, c = S['t0'], S['kind'], S['cues']
        if S['idx'] > 0 and S['kind'] != 'reveal':
            ev.append((t0 - .25, 'whoosh', .5))
        if k == 'chaos':
            for (n, ct, cx, cy, w, cue, dl) in CHAOS:
                ev.append((t0 + c[cue] + dl, 'pop', .45))
            for i in range(26):
                ev.append((t0 + c[3] + .1 + i * .045, 'key', .5))
            ev += [(t0 + c[3] + 1.4, 'notif', .5), (t0 + c[3] + 2.0, 'glitch', .55)]
        elif k == 'reveal':
            ev += [(t0, 'impact', .9), (t0 + .72, 'bass', .6), (t0 + c[1] - .2, 'whoosh', .6)]
        elif k == 'workspace':
            ev += [(t0 + .9 + i * .12, 'tick', .7) for i in range(8)]
        elif k == 'product':
            ev.append((t0 + .1, 'whoosh_down', .4))
            ev += [(t0 + S['dur'] * tp, 'click', .8) for tp, _, _ in S.get('callouts', [])]
            if S.get('sub'):
                ev.append((t0 + (c[-1] if len(c) > 1 else S['dur'] * .45), 'whoosh', .45))
        elif k == 'split':
            ev.append((t0 + S['dur'] * .38, 'whoosh', .6))
            ev += [(t0 + S['dur'] * .55 + i * .35 + .35, 'pop', .6) for i in range(4)]
        elif k == 'statement':
            ev += [(t0 + c[0] + .6, 'eraser', .5), (t0 + c[0] + .75, 'bass', .5)]
        elif k == 'pcme':
            ev += [(t0 + c[-1] + .2 + i * .3, 'notif', .3) for i in range(3)]
        elif k == 'loop':
            ev += [(t0 + x - .05, 'tick', 1.0) for x in loop_times(S)] + [(t0 + x - .05, 'click', .5) for x in loop_times(S)]
        elif k == 'resolve':
            ev += [(t0 + .8, 'impact', .5)]
        elif k == 'end':
            ev += [(t0 + .15, 'stinger', .6), (t0 + c[-1], 'pop', .6), (t0 + c[-1] + .8, 'click', 1.0)]
    return ev


def render_audio(V, scs, total, beat):
    SR = A2.SR; N = int(total * SR)
    vo = np.zeros(N)
    for S in scs:
        for at, a in S['vos']:
            A2.place(vo, resample_poly(a, 2, 1), S['t0'] + at)
    vo = A2.vo_chain(vo)
    secs = [(S['t0'], S['t0'] + S['dur'], S['energy'], bool(S.get('drop'))) for S in scs]
    music, _ = A2.compose2(total, V['style'], secs, seed=V['seed'], root=V['root'])
    music = A2.peaking(music, 2800, -3.0, .8)
    sfx = np.zeros(N); events = []
    for at, kind, g in sfx_events(scs, beat):
        if 0 <= at < total:
            A2.place(sfx, A2.SFX[kind](), at, g); events.append([round(at, 3), kind, g])
    sfx = np.tanh(sfx * .9)
    fd = np.ones(N); fl = int(SR * 1.6); fd[-fl:] = np.linspace(1, 0, fl) ** 2
    music *= fd
    duck = A2.duck_env(vo, .6)
    mix = vo + music * duck * .55 + sfx * .42
    mo = music * .75 + sfx * .42
    return vo, music, sfx, mix, mo, events


# ------------------------------------------------------------------ main
def srt(chunks, sep=','):
    pass


def main(vkey='A', stills=False):
    global SHOTS_T
    V = VARIANTS[vkey]
    scs, total, beat = timeline(V)
    SHOTS_T = scs
    print(f'timeline {total:.2f}s  shots={len(scs)}', flush=True)
    for S in scs:
        print(f"  {S['id']:10s} {S['t0']:6.2f} +{S['dur']:.2f}", flush=True)
    od = OUT if vkey == 'A' else os.path.join(OUT, 'ab-variant-B')
    for sub in ('audio', 'captions', 'thumbnails', 'source'):
        os.makedirs(os.path.join(od, sub), exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    if stills:
        qa = os.path.join(CACHE, 'qa'); os.makedirs(qa, exist_ok=True)
        for S in scs:
            for fr in (.15, .5, .9):
                g = S['t0'] + S['dur'] * fr
                frame(scs, g).save(f'{qa}/{S["idx"]:02d}_{S["id"]}_{int(fr * 100):02d}.jpg', quality=80)
        return
    # ---- audio
    vo, music, sfx, mix, mo, events = render_audio(V, scs, total, beat)
    SR = A2.SR; ad = os.path.join(od, 'audio')
    sf.write(CACHE + f'/mix_raw_{vkey}.wav', mix / (np.abs(mix).max() + 1e-9) * .8, SR)
    sf.write(CACHE + f'/mo_raw_{vkey}.wav', mo / (np.abs(mo).max() + 1e-9) * .8, SR)
    B.loudnorm(CACHE + f'/mix_raw_{vkey}.wav', ad + '/full_mix.wav', TP=-3.2)
    B.loudnorm(CACHE + f'/mo_raw_{vkey}.wav', CACHE + f'/mo_{vkey}.wav', TP=-3.2)
    sf.write(ad + '/narration.wav', (vo * .9).astype(np.float32), SR, subtype='PCM_24')
    B.loudnorm(ad + '/narration.wav', ad + '/narration.wav', tmp=True, I=-16)
    sf.write(ad + '/music.wav', (music / (np.abs(music).max() + 1e-9) * .89).astype(np.float32), SR, subtype='PCM_24')
    sf.write(ad + '/sfx.wav', (sfx / (np.abs(sfx).max() + 1e-9) * .89).astype(np.float32), SR, subtype='PCM_24')
    for k in ('narration', 'music', 'sfx', 'full_mix'):
        B.sh(f'ffmpeg -v error -y -i {ad}/{k}.wav -c:a libmp3lame -b:a 256k {ad}/{k}.mp3')
    # ---- video (variant B reuses A's picture: identical visual timeline, different voice/score)
    silent = os.path.join(CACHE, f'silent_{vkey}.mp4')
    if not os.path.exists(silent) or os.environ.get('FORCE') == '1':
        proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                 '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
                                 '-movflags', '+faststart', silent], stdin=subprocess.PIPE)
        nF = int(round(total * FPS)); t0 = time.time()
        for f in range(nF):
            proc.stdin.write(frame(scs, f / FPS).tobytes())
            if f % 150 == 0:
                print(f'  frame {f}/{nF}  {f / max(1e-3, time.time() - t0):.2f} fps', flush=True)
        proc.stdin.close(); proc.wait()
    final = os.path.join(od, f'{SLUG}{"" if vkey == "A" else "_B"}_FINAL.mp4')
    B.sh(f'ffmpeg -v error -y -i {silent} -i {ad}/full_mix.wav -map 0:v -map 1:a -c:v copy -af "aresample=192000,alimiter=limit=0.72:attack=0.3:release=40:level=false,aresample=48000" -c:a aac -b:a 256k -shortest -movflags +faststart {final}')
    B.sh(f'ffmpeg -v error -y -i {silent} -i {CACHE}/mo_{vkey}.wav -map 0:v -map 1:a -c:v copy -af "aresample=192000,alimiter=limit=0.72:attack=0.3:release=40:level=false,aresample=48000" -c:a aac -b:a 256k -shortest -movflags +faststart {od}/{SLUG}{"" if vkey == "A" else "_B"}_MUSIC_ONLY.mp4')
    B.sh(f'ffmpeg -v error -y -i {final} -c:v libvpx-vp9 -b:v 0 -crf 34 -deadline realtime -cpu-used 8 -row-mt 1 -vf scale=1280:-2 -c:a libopus -b:a 128k {final[:-10]}_preview.webm')
    # ---- captions
    s_, v_, k = [], ['WEBVTT', ''], 1
    for S in scs:
        for c, a0, a1 in S['chunks']:
            a0 += S['t0']; a1 = S['t0'] + a1 + .15
            s_ += [str(k), f'{B.srt_time(a0)} --> {B.srt_time(a1)}', c, '']
            v_ += [f'{B.srt_time(a0, ".")} --> {B.srt_time(a1, ".")}', c, '']; k += 1
    open(f'{od}/captions/{SLUG}.srt', 'w').write('\n'.join(s_))
    open(f'{od}/captions/{SLUG}.vtt', 'w').write('\n'.join(v_))
    open(f'{od}/captions/script.txt', 'w').write('\n'.join(c for S in scs for _, c in S['lines']) + '\n')
    # ---- stills
    th = od + '/thumbnails'
    rv = next(S for S in scs if S['id'] == 'reveal')
    B.sh(f'ffmpeg -v error -y -ss {rv["t0"] + rv["dur"] * .85:.2f} -i {final} -frames:v 1 {th}/thumbnail.png')
    en = scs[-1]
    B.sh(f'ffmpeg -v error -y -ss {en["t0"] + en["dur"] * .8:.2f} -i {final} -frames:v 1 {th}/end_card.png')
    B.sh(f'ffmpeg -v error -y -i {final} -vf "fps={16 / total:.5f},scale=480:-1,tile=4x4" -frames:v 1 {th}/storyboard.png')
    # ---- editable source
    tl = [dict(idx=S['idx'], id=S['id'], kind=S['kind'], start=round(S['t0'], 3), dur=round(S['dur'], 3), background='#%02X%02X%02X' % S['bg'][:3],
               label=S.get('label'), headline=S.get('head'), clip=S.get('clip'), clip2=S.get('clip2'),
               lines=[dict(say=a, caption=b, vo_start=round(S['t0'] + c, 3)) for (a, b), c in zip(S['lines'], S['cues'])],
               words=[[w, round(S['t0'] + b, 3), round(S['t0'] + e, 3)] for w, b, e in S['words']],
               energy=S['energy'], drop=bool(S.get('drop'))) for S in scs]
    json.dump(dict(title=V['title'], variant=vkey, resolution='1920x1080', fps=FPS, duration=round(total, 3), bpm=round(60 / beat, 2), style=V['style'],
                   voice=V['voice'], tts='Kokoro-82M (local, Apache-2.0)', shots=tl, sfx_events=events,
                   footage='Real Placiq product captures: placiq-videos/assets/real-product/clips'), open(f'{od}/source/timeline.json', 'w'), indent=1)
    B.sh(f'cp {HERE}/launch.py {HERE}/audio.py {HERE}/audio2.py {HERE}/core.py {HERE}/v2/canvas.py {od}/source/')
    open(f'{od}/source/README.md', 'w').write(
        f"# {V['title']}\n\nEditable source. `timeline.json` holds every shot (start, duration, layout, clip, headline), every narration line with word-level timings, and every SFX event.\n\n"
        "Re-render (from repo root):\n\n```\ndocker build --network host -t placiq-render placiq-videos/engine/docker\n"
        f"docker run --rm -v $PWD:/workspace -w /workspace/placiq-videos/engine placiq-render python launch.py {vkey}\n```\n\n"
        "Edit `SHOTS` in `launch.py` to change copy, layouts, clip choices or callouts; durations re-quantise to the beat automatically.\n")
    # ---- QA
    probe = json.loads(B.sh(f'ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,profile:format=duration -of json {final}').stdout)
    rep = dict(final=B.measure(final), probe=probe, duration=round(total, 3))
    json.dump(rep, open(f'{od}/verify.json', 'w'), indent=1)
    print('verify', json.dumps(rep['final']), round(total, 2), flush=True)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'A', '--stills' in sys.argv)
