"""Campaign score engine: pattern-sequenced styles, seeded motifs per video, extra SFX. Builds on audio.py instruments."""
import numpy as np
from audio import *

R = lambda s: [i for i, c in enumerate(s) if c == 'x']
STY = {
 'house':      dict(bpm=124, k='x...x...x...x...', s='....x.......x...', h='..x...x...x...x.', oh='', bass='saw', brh='..x...x...x...x.', lead='pluck', kick='house'),
 'dnb':        dict(bpm=172, k='x.........x.....', s='....x.......x...', h='x.x.x.x.x.x.x.x.', oh='', bass='reese', brh='x.....x...x.....', lead='pluck', kick='house'),
 'breakbeat':  dict(bpm=132, k='x.....x...x.....', s='....x..x.x..x...', h='xxxxxxxxxxxxxxxx', oh='', bass='saw', brh='x..x..x...x.x...', lead='square', kick='house'),
 'trap':       dict(bpm=145, k='x......x..x.....', s='........x.......', h='x.x.x.x.x.xxx.x.', oh='', bass='808', brh='x......x..x.....', lead='bell', kick='trap'),
 'arcade':     dict(bpm=150, k='x...x...x...x...', s='....x.......x...', h='x.x.x.x.x.x.x.x.', oh='', bass='square', brh='x.x.x.x.x.x.x.x.', lead='square', kick='house'),
 'industrial': dict(bpm=118, k='x..x..x...x..x..', s='....x.......x...', h='x.x.x.x.x.x.x.x.', oh='', bass='saw', brh='xxxxxxxxxxxxxxxx', lead='metal', kick='dist'),
 'cinematic':  dict(bpm=90,  k='x.....x.x.......', s='........x.......', h='x...x...x...x...', oh='', bass='saw', brh='x...............', lead='bell', kick='trap'),
 'funk':       dict(bpm=108, k='x..x..x...x.....', s='....x.......x...', h='xxxxxxxxxxxxxxxx', oh='......x.......x.', bass='slap', brh='x..x.x..x.xx..x.', lead='clav', kick='house'),
 'glitchhop':  dict(bpm=100, k='x.....x..x......', s='....x.......x...', h='x.xxx.x.x.xxx.x.', oh='', bass='wobble', brh='x.......x.......', lead='square', kick='house'),
 'minimal':    dict(bpm=120, k='x...x...x...x...', s='......x.......x.', h='.x.x.x.x.x.x.x.x', oh='', bass='sine', brh='x.....x.........', lead='bell', kick='house'),
 'electro':    dict(bpm=128, k='x...x...x...x...', s='....x.......x...', h='x.x.x.x.x.x.x.x.', oh='..x...x...x...x.', bass='saw', brh='x.xx.x.xx.x.x.xx', lead='pluck', kick='house'),
}
PROGS = [[0, 8, 3, 10], [0, 5, 8, 7], [0, 10, 8, 7], [0, 3, 8, 10], [0, 8, 5, 7], [0, 7, 8, 5]]


def tone(kind, m, dur):
    n = int(SR * dur); t = np.arange(n) / SR; f = note_hz(m)
    if kind == 'square':
        x = np.sign(np.sin(2 * np.pi * f * t)) * .35 * env_ad(n, .002, dur * .6)
    elif kind == 'bell':
        x = (np.sin(2 * np.pi * f * t + 2 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 6))) * env_ad(n, .002, .5) * .45
    elif kind == 'metal':
        x = np.sin(2 * np.pi * f * t + 4 * np.sin(2 * np.pi * f * 1.41 * t)) * env_ad(n, .001, .12) * .4
    elif kind == 'clav':
        x = lp(np.sign(np.sin(2 * np.pi * f * t)) * .5 + saw(f * 2, n) * .2, 3000) * env_ad(n, .001, .08)
    else:
        x = pluck(m, dur)
    return x


def bassn(kind, m, dur, e):
    n = int(SR * dur); t = np.arange(n) / SR; f = note_hz(m)
    if kind in ('saw', 'reese', '808'):
        return bass_note(m, dur, kind, 400 + 300 * e)
    if kind == 'square':
        x = np.sign(np.sin(2 * np.pi * f * t)) * .35
    elif kind == 'slap':
        x = np.tanh(np.sin(2 * np.pi * f * t) * 3 + saw(f, n) * np.exp(-t * 30)) * .5 * np.exp(-t * 5)
    elif kind == 'wobble':
        x = lp(saw(f, n) + saw(f * 1.01, n), 1200, 2) * (.6 + .4 * np.sin(2 * np.pi * 6 * t)) * .5
    else:
        x = np.sin(2 * np.pi * f * t) * .6
    e_ = np.minimum(1, t / .004) * np.clip((dur - t) / .02, 0, 1)
    return x * e_


def dist_kick():
    return np.tanh(kick('house') * 5) * .8


def compose2(total, style, sections, seed=0, root=45, bpm=None):
    st = STY[style]; bpm = bpm or st['bpm']; beat = 60 / bpm; bar = beat * 4
    rg = np.random.default_rng(seed)
    n = int(total * SR) + SR
    drums, bassb, keys, fx = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    duck = np.ones(n)
    K = dist_kick() if st['kick'] == 'dist' else kick(st['kick'])
    SN, CL, HC, HO = snare(150 + seed % 80), clap(), hat(), hat(True)
    prog_ = PROGS[seed % len(PROGS)]
    scale = [0, 2, 3, 5, 7, 8, 10]
    motif = [int(rg.integers(0, 7)) for _ in range(8)]
    rhythm = [int(rg.integers(0, 2)) for _ in range(16)]
    drops = [s[0] for s in sections if s[3]]

    def energy_at(t):
        for s in sections:
            if s[0] <= t < s[1]:
                return s[2]
        return sections[-1][2]

    for b in range(int(total / bar) + 1):
        t0 = b * bar; e = energy_at(t0 + .01)
        r = root + prog_[b % 4]
        ch = [r, r + 3, r + 7]
        pre = any(0 < dd - t0 <= bar + 1e-6 for dd in drops)
        place(keys, pad([m + 12 for m in ch], bar + .3), t0, .7 if e < 2 else .35)
        if style == 'cinematic' and e >= 1:
            place(keys, supersaw([r - 12, r - 5, r], bar, 900, 1.2), t0, .5)
        for s in range(16):
            ts = t0 + s * beat / 4 + (beat / 4 * .16 if style in ('funk', 'glitchhop') and s % 2 else 0)
            if ts >= total or (pre and s >= 12):
                continue
            if e >= 1 and s in R(st['k']):
                place(drums, K, ts, 1.0)
                i = int(ts * SR); dl = int(beat * .45 * SR)
                duck[i:i + dl] = np.minimum(duck[i:i + dl], np.linspace(.4, 1, len(duck[i:i + dl])))
            if e >= 2 and s in R(st['s']):
                place(drums, SN, ts, .9)
                if style in ('house', 'electro', 'funk'):
                    place(drums, CL, ts, .5)
            if e >= 1 and s in R(st['h']):
                place(drums, HC, ts, (.45 if s % 4 == 0 else .3) * (.6 if style == 'breakbeat' and s % 2 else 1))
            if e >= 2 and s in R(st['oh']):
                place(drums, HO, ts, .4)
            if style == 'glitchhop' and e >= 2 and s == 14 and b % 2:
                for q in range(4):
                    place(drums, SN * .4, ts + q * beat / 16, 1)
            if style == 'industrial' and e >= 2 and s in (6, 14):
                place(drums, tone('metal', root + 36 + (s // 6), .2), ts, .7)
            if e >= 1 and s in R(st['brh']):
                m = r - 24 + (12 if style == 'funk' and s % 5 == 0 else 0)
                place(bassb, bassn(st['bass'], m, beat * (.9 if st['bass'] in ('808', 'reese') else .4), e), ts, .9)
            if e >= 2 and rhythm[s] and s % 2 == 0:
                deg = motif[(s // 2 + b) % 8]
                place(keys, tone(st['lead'], r + 24 + scale[deg] - (r - root), beat * .5), ts, .35)
            if e >= 3 and s in (0, 6, 10) and style not in ('minimal',):
                place(keys, supersaw([m + 12 for m in ch], beat * .5, 3500, .18), ts, .35)
        if e == 0:
            place(drums, HC, t0 + beat, .3); place(drums, HC, t0 + beat * 3, .3)
            place(keys, tone('bell', r + 24, 1.0), t0, .3)
    for dd in drops:
        rl = min(bar * 2, dd)
        if rl > .3:
            place(fx, riser(rl), dd - rl, .6)
        place(fx, impact(), dd, .8)
    m = drums * .9 + bassb * duck * .9 + keys * duck * .8 + fx * .8
    m = np.tanh(hp(m, 28) * 1.1) / 1.1
    return m[:int(total * SR)], beat


def eraser():
    n = int(SR * .5); t = np.arange(n) / SR
    return bp(rng.standard_normal(n), 600, 4000) * (0.5 + .5 * np.abs(np.sin(2 * np.pi * 9 * t))) * np.sin(np.pi * t / .5) * .5


def stamp():
    return impact()[:int(SR * .5)] * .8 + click()[:] .__class__(click()) * 0 if False else impact()[:int(SR * .5)] * .8


def beep():
    n = int(SR * .18); t = np.arange(n) / SR
    return np.sign(np.sin(2 * np.pi * 880 * t)) * .25 * (t < .16)


def notif():
    n = int(SR * .35); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1320 * t) * (t < .12) + np.sin(2 * np.pi * 1760 * t) * (t >= .12)) * np.exp(-t * 8) * .35


SFX.update(eraser=eraser, stamp=stamp, beep=beep, notif=notif)
