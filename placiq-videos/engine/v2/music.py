"""Placiq engine v2 - procedural score composer. Builds on engine/audio.py voices (kick/snare/hat/bass/supersaw/pad/pluck + SFX)
and adds pattern-driven genres so every film gets its own composition. 100% locally synthesised; no samples."""
import os, sys
import numpy as np
from scipy import signal

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import audio as A  # noqa  (existing engine)
from audio import SR, place, lp, hp, bp, saw, note_hz, env_ad  # noqa


# ------------------------------------------------------------------ extra voices
def square(f, n, duty=.5):
    t = np.arange(n) / SR
    return np.where((f * t) % 1 < duty, 1.0, -1.0)


def chip_note(m, dur, duty=.25, vib=0.0):
    n = int(SR * dur); t = np.arange(n) / SR
    f = note_hz(m) * (1 + vib * np.sin(2 * np.pi * 6 * t))
    ph = np.cumsum(f) / SR
    x = np.where(ph % 1 < duty, 1.0, -1.0)
    e = np.minimum(1, t / .003) * np.clip((dur - t) / .02, 0, 1) * (0.7 + .3 * np.exp(-t * 6))
    return x * e * .18


def tri_bass(m, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    ph = (note_hz(m) * t) % 1
    x = 4 * np.abs(ph - .5) - 1
    return x * np.minimum(1, t / .003) * np.clip((dur - t) / .02, 0, 1) * .5


def fm_bell(m, dur, idx=3.0):
    n = int(SR * dur); t = np.arange(n) / SR
    f = note_hz(m)
    x = np.sin(2 * np.pi * f * t + idx * np.exp(-t * 4) * np.sin(2 * np.pi * f * 3.5 * t))
    return x * env_ad(n, .002, dur * .5) * .3


def slap_bass(m, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    f = note_hz(m)
    x = saw(f, n) * .5 + np.sin(2 * np.pi * f * t) * .6
    fc = 300 + 2600 * np.exp(-t * 22)
    # time-varying filter approximation: blend bright/dark
    bright, dark = lp(x, 3000, 2), lp(x, 300, 2)
    w = np.exp(-t * 22)
    y = bright * w + dark * (1 - w)
    return np.tanh(y * 2.2) * np.clip((dur - t) / .02, 0, 1) * np.minimum(1, t / .002) * .5


def clav(m, dur=.16):
    n = int(SR * dur); t = np.arange(n) / SR
    x = square(note_hz(m), n, .3) * .5 + saw(note_hz(m) * 2, n) * .2
    return bp(x, 500, 5000) * env_ad(n, .001, .05) * .45


def metal_hit():
    n = int(SR * .5); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) for f in (317, 563, 891, 1349, 2011)) / 5
    nz = bp(A.rng.standard_normal(n), 2000, 9000) * np.exp(-t * 40)
    return np.tanh((x * np.exp(-t * 9) + nz * .5) * 2.5) * .45


def tom(m=45):
    n = int(SR * .7); t = np.arange(n) / SR
    f = note_hz(m) * (1 + .6 * np.exp(-t * 18))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    nz = lp(A.rng.standard_normal(n), 1500) * np.exp(-t * 25) * .3
    return np.tanh((x + nz) * 1.8) * .8


def taiko():
    n = int(SR * 1.2); t = np.arange(n) / SR
    f = 55 * (1 + .9 * np.exp(-t * 25))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    nz = lp(A.rng.standard_normal(n), 900) * np.exp(-t * 16) * .6
    return np.tanh((x * 1.3 + nz) * 1.6) * .9


def rim():
    n = int(SR * .05); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1700 * t) + bp(A.rng.standard_normal(n), 2000, 8000) * .6) * np.exp(-t * 160) * .35


def shaker():
    n = int(SR * .07); t = np.arange(n) / SR
    return hp(A.rng.standard_normal(n), 6000, 2) * np.minimum(1, t / .01) * np.exp(-t * 60) * .18


def bitcrush(x, bits=6, ds=4):
    y = np.repeat(x[::ds], ds)[:len(x)]
    q = 2 ** bits
    return np.round(y * q) / q


def sub(m, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    return np.sin(2 * np.pi * note_hz(m) * t) * np.minimum(1, t / .005) * np.clip((dur - t) / .03, 0, 1) * .6


def strings(ms, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    x = np.zeros(n)
    for m in ms:
        for dt in (-.006, 0, .006):
            f = note_hz(m) * (1 + dt) * (1 + .003 * np.sin(2 * np.pi * 5 * t))
            x += saw(1, n) * 0 + (2 * ((np.cumsum(f) / SR) % 1) - 1)
    x = lp(x / (len(ms) * 3), 1800, 2)
    e = np.minimum(1, t / (dur * .25)) * np.minimum(1, (dur - t) / (dur * .25))
    return x * e * .32


# ------------------------------------------------------------------ genre patterns (16 steps per bar; 'x' strong, 'o' soft, '.' rest)
G = {
 'house':      dict(k='x...x...x...x...', s='....x.......x...', h='..x...x...x...x.', oh='..o...o...o...o.', bass='saw',  bstep='..x...x...x...x.', lead='supersaw', bpm=(120, 126), drive=1.1),
 'dnb':        dict(k='x.........x.....', s='....x.......x...', h='x.x.x.x.x.x.x.x.', bass='reese', bstep='x.....x...x.....', lead='pluck', bpm=(170, 176), drive=1.2),
 'breakbeat':  dict(k='x.....x...x.....', s='....x..o.o..x...', h='x.xox.x.x.xox.x.', bass='saw',  bstep='x..x..x...x..x..', lead='pluck', bpm=(128, 136), drive=1.25),
 'trap':       dict(k='x......x..x.....', s='........x.......', h='x.x.x.x.x.xxx.x.', bass='808',  bstep='x......x..x.....', lead='bell', bpm=(138, 146), drive=1.1),
 'arcade':     dict(k='x...x...x...x...', s='....x.......x...', h='x.x.x.x.x.x.x.x.', bass='tri',  bstep='x.x.x.x.x.x.x.x.', lead='chip', bpm=(140, 152), drive=1.0),
 'industrial': dict(k='x..x..x...x..x..', s='....x.......x...', h='.x.x.x.x.x.x.x.x', bass='reese', bstep='x..x..x...x..x..', lead='metal', bpm=(118, 126), drive=1.6),
 'cinematic':  dict(k='x.......x.......', s='........x.......', h='................', bass='sub',  bstep='x...............', lead='strings', bpm=(84, 96), drive=1.0),
 'funk':       dict(k='x..x......x..x..', s='....x.......x...', h='xoxoxoxoxoxoxoxo', bass='slap', bstep='x..x.x....x.xx..', lead='clav', bpm=(104, 112), drive=1.1),
 'glitchhop':  dict(k='x.....x.x.......', s='....x.......x..o', h='x.xx.x.xx.x.xx.x', bass='reese', bstep='x.....x.x...x...', lead='chip', bpm=(108, 114), drive=1.3),
 'minimal':    dict(k='x...x...x...x...', s='................', h='..o...o...o...o.', bass='sub',  bstep='x..x...x..x.....', lead='bell', bpm=(122, 128), drive=1.0),
 'garage':     dict(k='x......x..x.....', s='....x.......x...', h='..x.x..x..x.x..x', bass='saw',  bstep='x......x..x...x.', lead='supersaw', bpm=(130, 134), drive=1.15),
 'phonk':      dict(k='x.....x...x.....', s='....x.......x...', h='x.x.x.x.x.x.x.x.', bass='808',  bstep='x.....x...x...x.', lead='bell', bpm=(128, 140), drive=1.4),
}

# chord progressions as scale degrees (minor-key friendly); root chosen per film
PROGS = [[0, 5, 3, 7], [0, 8, 3, 10], [0, 3, 8, 7], [0, 10, 8, 7], [0, 5, 10, 3], [0, 7, 8, 5]]
MINOR = [0, 2, 3, 5, 7, 8, 10]


def triad(root, deg):
    # minor-ish voicing on chromatic offset
    r = root + deg
    third = 3 if deg in (0, 5, 7) else 4
    return [r, r + third, r + 7]


def compose(total, style, seed, sections, bpm=None, key=50):
    """sections: [(t0, t1, energy 0..3, drop)]. Returns (music, bpm). Deterministic per seed."""
    rng = np.random.default_rng(seed)
    g = G[style]
    bpm = bpm or int(rng.integers(g['bpm'][0], g['bpm'][1] + 1))
    beat = 60 / bpm; st16 = beat / 4; bar = beat * 4
    n = int(total * SR) + SR * 2
    drums, bass, keys, fx = (np.zeros(n) for _ in range(4))
    duck = np.ones(n)
    kst = 'trap' if g['bass'] in ('808',) else ('house' if style != 'cinematic' else 'trap')
    K = A.kick(kst)
    if style == 'industrial':
        K = np.tanh(K * 3) * .8
    SN = A.snare(int(rng.integers(170, 230))); CL = A.clap(); HC = A.hat(); HO = A.hat(True)
    if style in ('arcade', 'glitchhop'):
        SN = bitcrush(SN, 5, 3); HC = bitcrush(HC, 6, 2)
    prog = PROGS[int(rng.integers(0, len(PROGS)))]
    mel_seed = rng.integers(0, 7, 64)
    swing = .12 if style in ('garage', 'funk') else 0.0

    def energy(t):
        for s in sections:
            if s[0] <= t < s[1]:
                return s[2]
        return sections[-1][2] if sections else 2
    drops = [s[0] for s in sections if s[3] and s[0] > .5]
    nbars = int(total / bar) + 2
    for b in range(nbars):
        t0 = b * bar
        e = energy(t0 + .01)
        ch = triad(key, prog[b % 4])
        pre = any(0 < dd - t0 <= bar + 1e-6 for dd in drops)
        # bed
        if g['lead'] == 'strings' or e <= 1:
            place(keys, strings([m + 12 for m in ch], bar + .25) if style == 'cinematic' else A.pad([m + 12 for m in ch], bar + .3), t0, .8 if e <= 1 else .45)
        for s in range(16):
            ts = t0 + s * st16 + (swing * st16 if s % 2 else 0)
            if ts >= total:
                break
            if pre and s >= 12:
                continue
            ks, ss, hs = g['k'][s], g['s'][s], g['h'][s]
            if e >= 1 and ks != '.':
                place(drums, K, ts, 1.0 if ks == 'x' else .6)
                dl = int(beat * .45 * SR); i = int(ts * SR)
                seg = duck[i:i + dl]; duck[i:i + len(seg)] = np.minimum(seg, .4 + .6 * np.linspace(0, 1, len(seg)))
            if e >= 2 and ss != '.':
                place(drums, SN if style not in ('house', 'garage', 'minimal') else CL, ts, .9 if ss == 'x' else .35)
            if style == 'minimal' and e >= 2 and s in (4, 12):
                place(drums, rim(), ts, .9)
            if e >= 1 and hs != '.':
                place(drums, HC, ts, .4 if hs == 'x' else .22)
            if e >= 2 and g.get('oh') and g['oh'][s] != '.':
                place(drums, HO, ts, .35)
            if style in ('funk', 'minimal', 'cinematic') and e >= 2 and s % 2:
                place(drums, shaker(), ts, .8)
            if style == 'cinematic' and e >= 1 and s in (0, 6, 10):
                place(drums, taiko() if s == 0 else tom(40 + s), ts, .9 if s == 0 else .5)
            if style == 'industrial' and e >= 2 and s in (6, 14):
                place(drums, metal_hit(), ts, .6)
            # bass
            if e >= 1 and g['bstep'][s] != '.':
                m = ch[0] - 24 + (12 if style in ('funk',) and s in (5, 13) else 0)
                L = st16 * (3 if g['bass'] in ('808', 'sub') else 1.8)
                bk = g['bass']
                if bk == '808':
                    x = A.bass_note(m, beat * 1.1, '808')
                elif bk == 'reese':
                    x = A.bass_note(m, L * 1.6, 'reese', 300 + 300 * e)
                elif bk == 'tri':
                    x = tri_bass(m + 12, st16 * .9)
                elif bk == 'sub':
                    x = sub(m, L * 1.5)
                elif bk == 'slap':
                    x = slap_bass(m, st16 * 1.6)
                else:
                    x = A.bass_note(m, L, 'saw', 400 + 450 * e)
                place(bass, x, ts, .85)
            # lead / hook
            if e >= 2:
                lk = g['lead']
                deg = MINOR[mel_seed[(b * 4 + s // 4) % 64]]
                if lk == 'chip' and s % 2 == 0 and mel_seed[(b * 16 + s) % 64] % 3:
                    place(keys, chip_note(key + 24 + deg, st16 * 1.8, .25 if b % 2 else .125, .004), ts, .7)
                elif lk == 'pluck' and s % 2 == 0:
                    place(keys, A.pluck([ch[0], ch[1], ch[2], ch[1] + 12][(s // 2) % 4] + 24, .16), ts, .32)
                elif lk == 'bell' and s in (0, 3, 6, 10, 12) and (b + s) % 3:
                    place(keys, fm_bell(key + 24 + deg, beat * 1.2), ts, .4)
                elif lk == 'clav' and g['h'][s] == 'x' and s % 4 in (1, 2):
                    place(keys, clav(ch[(s // 2) % 3] + 24), ts, .5)
                elif lk == 'metal' and s in (2, 10):
                    place(keys, A.supersaw([m + 12 for m in ch], st16 * 2, 2200, .12), ts, .35)
                elif lk == 'supersaw' and s in (3, 6, 10, 14) and e >= 3:
                    place(keys, A.supersaw([m + 12 for m in ch], beat * .5, 4200, .14), ts, .5)
                elif lk == 'strings' and s == 0:
                    place(keys, fm_bell(key + 36 + deg, bar), ts, .25)
            if e >= 3 and s in (0, 8) and g['lead'] in ('pluck', 'bell', 'chip', 'clav'):
                place(keys, A.supersaw([m + 12 for m in ch], beat * 1.1, 3000, .35), ts, .28)
        if e == 0:
            place(bass, sub(ch[0] - 24, bar * .95), t0, .5)
            place(drums, HC, t0 + beat * 2, .2)
    for dd in drops:
        rl = min(bar * 2, dd)
        place(fx, A.riser(rl), dd - rl, .6)
        place(fx, A.impact(), dd, .8)
        for r in range(8):
            tt = dd - beat * 2 + r * beat / 4
            if tt > 0:
                place(drums, SN * (.2 + .7 * r / 8), tt, 1.0)
    music = drums * .9 + bass * duck * .9 + keys * duck * .8 + fx * .7
    if style in ('arcade',):
        music = music * .8 + bitcrush(music, 8, 2) * .2
    music = hp(music, 30)
    music = np.tanh(music * g['drive']) / g['drive']
    # gentle master EQ: tame 250Hz mud, lift air
    music = A.peaking(music, 250, -1.5, .9)
    music = A.peaking(music, 10000, 1.5, .7)
    out = music[:int(total * SR)]
    return out / (np.max(np.abs(out)) + 1e-9) * .9, bpm


# ------------------------------------------------------------------ extra SFX
def typing_burst(dur, rate=14, seed=0):
    r = np.random.default_rng(seed)
    out = np.zeros(int(dur * SR) + SR // 10)
    t = 0
    while t < dur:
        place(out, A.key_tap(), t, r.uniform(.7, 1.1)); t += r.uniform(.6, 1.4) / rate
    return out


def swoosh_short():
    return A.whoosh(.32)


def boom():
    return A.impact() * .9


def notif():
    n = int(SR * .25); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 1318 * t) * (t < .09) + np.sin(2 * np.pi * 1760 * t) * (t >= .09)
    return x * np.exp(-t * 14) * .35


def error_buzz():
    n = int(SR * .3); t = np.arange(n) / SR
    return np.tanh(square(110, n) * .7 + square(116, n) * .5) * np.exp(-t * 6) * .25


def success():
    out = np.zeros(int(SR * .6))
    for i, m in enumerate((72, 76, 79, 84)):
        place(out, fm_bell(m, .4, 1.5), i * .07, .6)
    return out


def tick_tock():
    return A.tick()


def stamp():
    n = int(SR * .4); t = np.arange(n) / SR
    thud = np.sin(2 * np.pi * np.cumsum(70 + 120 * np.exp(-t * 40)) / SR) * np.exp(-t * 12)
    return np.tanh((thud + lp(A.rng.standard_normal(n), 2500) * np.exp(-t * 35) * .6) * 2) * .7


def scratch():
    n = int(SR * .35); t = np.arange(n) / SR
    nz = bp(A.rng.standard_normal(n), 800, 5000)
    return nz * (0.5 + .5 * np.sin(2 * np.pi * 18 * t)) * np.exp(-t * 4) * .35


def clock_tick():
    n = int(SR * .05); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2600 * t) + np.sin(2 * np.pi * 900 * t) * .5) * np.exp(-t * 200) * .4


def zap():
    n = int(SR * .25); t = np.arange(n) / SR
    f = 2400 * np.exp(-t * 14) + 120
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * .3


SFX = dict(A.SFX)
SFX.update(type=lambda: typing_burst(.6), swoosh=swoosh_short, boom=boom, notif=notif, error=error_buzz, success=success,
           stamp=stamp, scratch=scratch, clock=clock_tick, zap=zap, metal=metal_hit, taiko=taiko)
