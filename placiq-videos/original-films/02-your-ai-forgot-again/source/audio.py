"""Procedural music + SFX synthesis and mixing (NumPy/SciPy). Everything here is generated from scratch."""
import numpy as np
from scipy import signal

SR = 48000


def env_ad(n, a=0.002, dcy=0.2, sr=SR):
    t = np.arange(n) / sr
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(dcy, 1e-4))
    return e


def lp(x, fc, order=2):
    b, a = signal.butter(order, min(fc / (SR / 2), .99), 'low'); return signal.lfilter(b, a, x)


def hp(x, fc, order=2):
    b, a = signal.butter(order, min(fc / (SR / 2), .99), 'high'); return signal.lfilter(b, a, x)


def bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), min(hi / (SR / 2), .99)], 'band'); return signal.lfilter(b, a, x)


def peaking(x, f0, gain_db, q=1.0):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


def saw(f, n, ph=0):
    t = np.arange(n) / SR
    return 2 * ((f * t + ph) % 1) - 1


def note_hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def place(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(x) <= 0:
        return
    if i < 0:
        x = x[-i:]; i = 0
    n = min(len(x), len(buf) - i)
    buf[i:i + n] += x[:n] * g


rng = np.random.default_rng(42)


# --------------------------------------------------------------- drums
def kick(style='house'):
    n = int(SR * (.55 if style == 'trap' else .35))
    t = np.arange(n) / SR
    f = 45 + 160 * np.exp(-t * 32) if style != 'trap' else 38 + 130 * np.exp(-t * 26)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * (7 if style != 'trap' else 3.5))
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t * 300) * .5
    return np.tanh((body + click) * 2.2) * .9


def snare(tone=190):
    n = int(SR * .28); t = np.arange(n) / SR
    nz = bp(rng.standard_normal(n), 1200, 9000) * np.exp(-t * 18)
    tn = np.sin(2 * np.pi * tone * t) * np.exp(-t * 30)
    return np.tanh((nz * .8 + tn * .7) * 1.6) * .7


def clap():
    n = int(SR * .3); t = np.arange(n) / SR
    nz = bp(rng.standard_normal(n), 900, 6000)
    e = np.zeros(n)
    for o in (0, .011, .022, .034):
        e += np.where(t >= o, np.exp(-(t - o) * (90 if o < .03 else 16)), 0)
    return nz * e * .5


def hat(open_=False):
    n = int(SR * (.25 if open_ else .05)); t = np.arange(n) / SR
    nz = hp(rng.standard_normal(n), 7000, 4)
    return nz * np.exp(-t * (14 if open_ else 90)) * (.28 if open_ else .3)


# --------------------------------------------------------------- tonal
def bass_note(m, dur, kind='saw', cutoff=900):
    n = int(SR * dur); t = np.arange(n) / SR
    f = note_hz(m)
    if kind == 'reese':
        x = saw(f, n) + saw(f * 1.007, n, .3) + saw(f * .993, n, .6)
        x = lp(x / 3, cutoff + 400 * np.sin(t[0] + 1), 4)
    elif kind == '808':
        fs = f * (1 + .5 * np.exp(-t * 40))
        x = np.tanh(np.sin(2 * np.pi * np.cumsum(fs) / SR) * 2.5)
    else:
        x = lp(saw(f, n) * .6 + np.sign(np.sin(2 * np.pi * f * t)) * .3, cutoff, 4) + np.sin(2 * np.pi * f / 2 * t) * .5
    e = np.minimum(1, t / .004) * np.minimum(1, (dur - t) / .02).clip(0, 1)
    if kind == '808':
        e = e * np.exp(-t * 1.2)
    return x * e * .55


def supersaw(ms, dur, cutoff=3000, dec=0.35):
    n = int(SR * dur); t = np.arange(n) / SR
    x = np.zeros(n)
    for m in ms:
        for dt in (-.012, -.005, 0, .006, .013):
            x += saw(note_hz(m) * (1 + dt), n, rng.random())
    x = lp(x / (len(ms) * 5), cutoff, 2)
    return x * env_ad(n, .003, dec) * .9


def pad(ms, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    x = np.zeros(n)
    for m in ms:
        for dt in (-.004, .004):
            x += saw(note_hz(m) * (1 + dt), n, rng.random())
    x = lp(x / (len(ms) * 2), 1400, 2)
    e = np.minimum(1, t / (dur * .3)) * np.minimum(1, (dur - t) / (dur * .3))
    return x * e * .35


def pluck(m, dur=.18):
    n = int(SR * dur); t = np.arange(n) / SR
    x = saw(note_hz(m), n) * .5 + np.sin(2 * np.pi * note_hz(m) * 2 * t) * .3
    return lp(x, 4000, 2) * env_ad(n, .001, .07) * .5


# --------------------------------------------------------------- sfx
def whoosh(dur=.55, up=True):
    n = int(SR * dur); t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    x = t / dur if up else 1 - t / dur
    low, mid, high = lp(nz, 700), bp(nz, 900, 3500), bp(nz, 3500, 11000)
    out = low * (1 - x) ** 2 + mid * np.sin(np.pi * x) + high * x ** 2
    e = np.sin(np.pi * np.clip(t / dur, 0, 1) ** (0.6 if up else 1.6))
    return out * e * .8


def impact():
    n = int(SR * 1.6); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(30 + 90 * np.exp(-t * 9)) / SR) * np.exp(-t * 2.2)
    crack = bp(rng.standard_normal(n), 200, 8000) * np.exp(-t * 14)
    tail = lp(rng.standard_normal(n), 900) * np.exp(-t * 3) * .25
    return np.tanh((sub * 1.2 + crack * .7 + tail) * 1.5) * .9


def bass_hit():
    n = int(SR * 1.0); t = np.arange(n) / SR
    return np.tanh(np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-t * 20)) / SR) * 3) * np.exp(-t * 3) * .8


def glitch_sfx(dur=.35):
    n = int(SR * dur); out = np.zeros(n); i = 0
    while i < n:
        L = int(rng.integers(300, 3000))
        kind = rng.integers(0, 3)
        tt = np.arange(L) / SR
        if kind == 0:
            seg = np.sign(np.sin(2 * np.pi * rng.uniform(80, 2000) * tt))
        elif kind == 1:
            seg = rng.standard_normal(L)
        else:
            seg = np.zeros(L)
        seg = np.round(seg * 4) / 4
        out[i:i + L] = seg[:max(0, min(L, n - i))]
        i += L
    return hp(out, 200) * .35


def click():
    n = int(SR * .03); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * .6 + hp(rng.standard_normal(n), 3000) * .5) * np.exp(-t * 260) * .7


def key_tap():
    n = int(SR * .04); t = np.arange(n) / SR
    return bp(rng.standard_normal(n), 1500, 7000) * np.exp(-t * rng.uniform(150, 260)) * rng.uniform(.25, .45)


def pop():
    n = int(SR * .12); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(500 + 900 * np.exp(-t * 40)) / SR) * np.exp(-t * 30) * .45


def riser(dur):
    n = int(SR * dur); t = np.arange(n) / SR
    x = t / dur
    nz = hp(rng.standard_normal(n), 800) * x ** 2 * .5
    tone = saw(1, n) * 0
    f = 200 + 1800 * x ** 2
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * x ** 2.5 * .25
    return lp(nz, 9000) + tone


def stinger(root=50):
    x = supersaw([root, root + 7, root + 12, root + 15, root + 19], 2.2, 5000, .9) * 1.4
    im = impact(); x[:len(im)] += im * .6
    return x


def tick():
    n = int(SR * .02); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 400) * .35


SFX = dict(whoosh=lambda: whoosh(), whoosh_down=lambda: whoosh(.5, False), impact=impact, bass=bass_hit,
           glitch=glitch_sfx, click=click, key=key_tap, pop=pop, stinger=stinger, tick=tick)


# --------------------------------------------------------------- music composer
STYLES = {
    'house': dict(prog=[[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]], bass='saw'),        # Dm Bb F C
    'trap': dict(prog=[[54, 57, 61], [50, 54, 57], [47, 50, 54], [49, 53, 56]], bass='808'),         # F#m D Bm C#
    'dnb': dict(prog=[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], bass='reese'),        # Am F C G
}


def compose(total, bpm, style, sections):
    """sections: list of (start, end, energy 0-3, drop_bool). Returns (music, meta)."""
    beat = 60 / bpm
    bar = beat * 4
    n = int(total * SR) + SR
    drums = np.zeros(n); bassb = np.zeros(n); keys = np.zeros(n); fx = np.zeros(n); duck = np.ones(n)
    S = STYLES[style]
    K, SN, CL, HC, HO = kick(style), snare(), clap(), hat(), hat(True)

    def energy_at(t):
        for s in sections:
            if s[0] <= t < s[1]:
                return s[2]
        return sections[-1][2]

    drops = [s[0] for s in sections if s[3]]
    nbars = int(total / bar) + 1
    for b in range(nbars):
        t0 = b * bar
        e = energy_at(t0 + .01)
        ch = S['prog'][(b // (2 if style == 'dnb' else 1)) % 4]
        pre_drop = any(0 < d - t0 <= bar + 1e-6 for d in drops)
        # chord bed
        if e >= 0:
            place(keys, pad([m + 12 for m in ch], bar + .3), t0, .9 if e < 2 else .5)
        for st in range(16):
            ts = t0 + st * beat / 4
            if ts >= total:
                break
            if pre_drop and st >= 12:
                continue  # one-beat breath before the drop
            if style == 'house':
                if e >= 1 and st % 4 == 0:
                    place(drums, K, ts, 1.0)
                    dl = int(beat * .5 * SR); i = int(ts * SR)
                    duck[i:i + dl] = np.minimum(duck[i:i + dl], 0.35 + 0.65 * np.linspace(0, 1, len(duck[i:i + dl])))
                if e >= 2 and st in (4, 12):
                    place(drums, CL, ts, .8)
                if e >= 1 and st % 4 == 2:
                    place(drums, HO, ts, .6)
                if e >= 2 and st % 2 == 1:
                    place(drums, HC, ts, .5)
                if e >= 1 and st % 4 == 2:
                    place(bassb, bass_note(ch[0] - 24, beat * .45, 'saw', 500 + 500 * e), ts, 1.0)
                if e >= 3 and st in (3, 6, 10, 14):
                    place(keys, supersaw([m + 12 for m in ch], beat * .5, 4200, .14), ts, .55)
                if e >= 2 and st % 2 == 0:
                    place(keys, pluck(ch[(st // 2) % 3] + 24), ts, .35)
            elif style == 'trap':
                kp = (0, 7, 10) if b % 2 == 0 else (0, 3, 10, 14)
                if e >= 1 and st in kp:
                    place(drums, K, ts, 1.0)
                    place(bassb, bass_note(ch[0] - 24 + (3 if st == 10 else 0), beat * 1.2, '808'), ts, .9)
                if e >= 2 and st == 8:
                    place(drums, SN, ts, .9); place(drums, CL, ts, .5)
                if e >= 1:
                    if st % 2 == 0:
                        place(drums, HC, ts, .45)
                    if e >= 2 and st in (13, 14, 15) and b % 2:
                        for r in range(3):
                            place(drums, HC, ts + r * beat / 12, .35)
                if e >= 2 and st % 4 == 0:
                    place(keys, pluck(ch[(st // 4) % 3] + 24, .3), ts, .45)
                    place(keys, pluck(ch[(st // 4 + 1) % 3] + 36, .2), ts + beat / 2, .3)
                if e >= 3 and st in (0, 6):
                    place(keys, supersaw([m + 12 for m in ch], beat * .8, 3000, .3), ts, .5)
            else:  # dnb, two-step
                if e >= 1 and st in (0, 10):
                    place(drums, K, ts, 1.0)
                if e >= 1 and st in (4, 12):
                    place(drums, SN, ts, 1.0)
                if e >= 2 and st in (7, 15) and b % 2:
                    place(drums, SN, ts, .35)
                if e >= 1 and st % 2 == 0:
                    place(drums, HC, ts, .4 if st % 4 else .25)
                if e >= 1 and st in (0, 6, 10):
                    place(bassb, bass_note(ch[0] - 24, beat * (1.4 if st == 0 else .9), 'reese', 300 + 300 * e), ts, .9)
                if e >= 2 and st % 2 == 0:
                    place(keys, pluck([ch[0], ch[1], ch[2], ch[1] + 12][(st // 2) % 4] + 24, .15), ts, .3)
                if e >= 3 and st in (0, 8):
                    place(keys, supersaw([m + 12 for m in ch], beat * 1.2, 2600, .5), ts, .4)
        if e == 0:
            place(drums, HC, t0, .3); place(drums, HC, t0 + beat * 2, .3)
            place(bassb, bass_note(ch[0] - 24, bar * .9, 'saw', 300), t0, .5)
    for d in drops:
        rl = min(bar * 2, d)
        place(fx, riser(rl), d - rl, .7)
        place(fx, impact(), d, .9)
        # snare roll over last bar
        for r in range(16):
            tt = d - bar + r * beat / 4
            if tt > 0:
                place(drums, SN * (.2 + .6 * r / 16), tt, 1.0)
    music = drums * .9 + bassb * duck * .9 + keys * duck * .8 + fx * .8
    music = hp(music, 28)
    music = np.tanh(music * 1.1) / 1.1
    return music[:int(total * SR)], beat


def compress(x, thr_db=-18, ratio=3.0, att=.005, rel=.12):
    env = np.abs(x)
    a1, r1 = np.exp(-1 / (att * SR)), np.exp(-1 / (rel * SR))
    # fast one-pole follower (vectorized approx via lfilter on rectified signal)
    e = signal.lfilter([1 - r1], [1, -r1], env)
    db = 20 * np.log10(e + 1e-9)
    over = np.maximum(0, db - thr_db)
    g = 10 ** (-(over - over / ratio) / 20)
    return x * g


def vo_chain(v):
    v = hp(v, 85, 2)
    v = peaking(v, 250, -2.5, 1.0)     # de-mud
    v = peaking(v, 3200, 3.5, 0.9)     # presence
    v = peaking(v, 9000, 2.0, 0.7)     # air
    v = compress(v, -22, 3.5)
    return v / (np.max(np.abs(v)) + 1e-9) * .9


def duck_env(vo, depth=.62):
    e = signal.lfilter([1 - np.exp(-1 / (.25 * SR))], [1, -np.exp(-1 / (.25 * SR))], np.abs(vo))
    e = np.convolve(e, np.ones(2400) / 2400, mode='same')
    k = np.clip(e / (np.max(e) * .15 + 1e-9), 0, 1)
    return 1 - depth * k
