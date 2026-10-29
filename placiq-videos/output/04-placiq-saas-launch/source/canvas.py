"""Placiq engine v2 - resolution-aware drawing primitives (vertical 1080x1920 shorts + 1920x1080 desktop).
Extends engine/core.py (fonts, easing, cached text rendering) instead of replacing it."""
import os, sys, math, random, subprocess
import numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from core import (hexc, clamp, prog, eo, eo5, eio, eback, lerp, font, text_img, tsize, fade, ROOT, FONTS)  # noqa

FPS = 30


class G:  # current output geometry (set per job)
    W, H = 1080, 1920
    U = 1.0          # unit scale: 1.0 == 1080px short edge
    vertical = True


def set_geometry(w, h):
    G.W, G.H = w, h
    G.U = min(w, h) / 1080
    G.vertical = h > w


# ------------------------------------------------------------------ palettes (brand: royal blue / black / white + restrained accents)
def pal(name):
    P = {
        'ink':    dict(bg='#0B0C10', bg2='#15171E', fg='#F5F2EC', card='#1A1D26', a1='#3151EE', a2='#FF533B', a3='#D6FF38', muted='#6E7385', line='#262A35', dark=True),
        'paper':  dict(bg='#F5F2EC', bg2='#E9E4DA', fg='#0F1117', card='#FFFFFF', a1='#3151EE', a2='#FF533B', a3='#1DB954', muted='#8A877F', line='#D8D2C6', dark=False),
        'royal':  dict(bg='#3151EE', bg2='#2741CC', fg='#FFFFFF', card='#FFFFFF', a1='#0F1117', a2='#D6FF38', a3='#FF533B', muted='#A9B6FF', line='#4A66F2', dark=True),
        'mono':   dict(bg='#050505', bg2='#121212', fg='#FFFFFF', card='#161616', a1='#FFFFFF', a2='#3151EE', a3='#FF533B', muted='#6A6A6A', line='#222222', dark=True),
        'term':   dict(bg='#06080A', bg2='#0D1114', fg='#D6FF38', card='#0E1316', a1='#D6FF38', a2='#FF533B', a3='#6E86FF', muted='#4F6B3A', line='#18211A', dark=True),
        'edit':   dict(bg='#F2EEE6', bg2='#E6E0D4', fg='#111111', card='#FFFFFF', a1='#FF533B', a2='#3151EE', a3='#111111', muted='#8C877C', line='#D5CEC0', dark=False),
        'white':  dict(bg='#FFFFFF', bg2='#F1F3F8', fg='#0F1117', card='#FFFFFF', a1='#3151EE', a2='#FF533B', a3='#D6FF38', muted='#8B90A0', line='#E3E6EE', dark=False),
    }[name]
    C = {k: (hexc(v) if isinstance(v, str) else v) for k, v in P.items()}
    C['name'] = name
    C['on_a1'] = hexc('#FFFFFF') if name not in ('term', 'mono') else hexc('#0B0C10')
    if name == 'royal':
        C['on_a1'] = hexc('#FFFFFF')
    return C


def rgb(c):
    return tuple(c[:3])


def mix(c1, c2, x):
    return tuple(int(lerp(c1[i], c2[i], x)) for i in range(3)) + (255,)


@lru_cache(maxsize=16)
def background(name, kind, w, h):
    C = pal(name)
    im = Image.new('RGB', (w, h), rgb(C['bg']))
    d = ImageDraw.Draw(im)
    step = int(54 * G.U)
    if kind == 'dots':
        for y in range(step // 2, h, step):
            for x in range(step // 2, w, step):
                r = 1.7 * G.U
                d.ellipse((x - r, y - r, x + r, y + r), fill=rgb(C['line']))
    elif kind == 'grid':
        for x in range(0, w, step):
            d.line((x, 0, x, h), fill=rgb(C['line']))
        for y in range(0, h, step):
            d.line((0, y, w, y), fill=rgb(C['line']))
    elif kind == 'scan':
        for y in range(0, h, 4):
            d.line((0, y, w, y), fill=rgb(C['bg2']))
    elif kind == 'noise':
        rnd = np.random.default_rng(3)
        a = np.asarray(im).astype(np.int16)
        a = a + rnd.integers(-7, 8, (h, w, 1))
        im = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    return im


# ------------------------------------------------------------------ text
def T(img, txt, x, y, fname, size, color, anchor='l', a=1.0, vanchor='t'):
    """Text at (x,y). anchor l/c/r horizontally; vanchor t/m vertically."""
    size = max(6, int(size))
    im = text_img(txt, fname, size, tuple(color))
    w, h = im.size
    if anchor == 'c':
        x -= w / 2
    elif anchor == 'r':
        x -= w
    if vanchor == 'm':
        y -= h / 2
    if a >= .999:
        img.paste(im, (int(x), int(y)), im)
    elif a > .003:
        s = fade(im, a)
        img.paste(s, (int(x), int(y)), s)
    return w, h


def Tmask(img, txt, x, y, fname, size, color, p, anchor='l'):
    """Masked slide-up reveal."""
    size = max(6, int(size))
    im = text_img(txt, fname, size, tuple(color))
    w, h = im.size
    if anchor == 'c':
        x -= w / 2
    elif anchor == 'r':
        x -= w
    if p <= 0:
        return w, h
    dy = int((1 - eo5(p)) * h)
    if h - dy > 0:
        crop = im.crop((0, 0, w, h - dy))
        img.paste(crop, (int(x), int(y + dy)), crop)
    return w, h


def wrap(txt, fname, size, maxw):
    words, lines, cur = txt.split(' '), [], ''
    for w in words:
        nx = (cur + ' ' + w).strip()
        if tsize(nx, fname, int(size))[0] > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = nx
    if cur:
        lines.append(cur)
    return lines


def fit(txt, fname, size, maxw):
    w = tsize(txt, fname, int(size))[0]
    return int(size * min(1, maxw / max(1, w)))


def para(img, txt, x, y, fname, size, color, maxw, lh=1.25, anchor='l', a=1.0):
    ls = wrap(txt, fname, size, maxw)
    for i, l in enumerate(ls):
        T(img, l, x, y + i * size * lh, fname, size, color, anchor, a)
    return len(ls) * size * lh


# ------------------------------------------------------------------ shapes
def rrect(d, box, fill=None, r=0, outline=None, width=1):
    x0, y0, x1, y1 = box
    if x1 - x0 < 1 or y1 - y0 < 1:
        return
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
    d.rounded_rectangle((x0, y0, x1, y1), int(r), fill=fill, outline=outline, width=int(width))


def layer(img, fn, box, a):
    """Draw with alpha: fn(draw, offx, offy) onto a transparent layer of size box then composite."""
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = max(1, x1 - x0), max(1, y1 - y0)
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    fn(ImageDraw.Draw(L), -x0, -y0, L)
    if a < .999:
        L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    img.paste(L, (x0, y0), L)


@lru_cache(maxsize=128)
def shadow(w, h, r, blur, alpha):
    pad = blur * 3
    im = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad + blur // 2, pad + w, pad + h + blur // 2), r, fill=(0, 0, 0, alpha))
    return im.filter(ImageFilter.GaussianBlur(blur)), pad


def drop(img, box, r=20, blur=24, alpha=80):
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    if w < 4 or h < 4:
        return
    # quantize to keep cache hits
    qw, qh = (w // 8) * 8 + 8, (h // 8) * 8 + 8
    s, pad = shadow(qw, qh, int(r), int(blur), alpha)
    img.paste(s, (x0 - pad, y0 - pad + int(blur * .4)), s)


def card(img, d, box, C, fill=None, r=None, sh=True, outline=None):
    r = 22 * G.U if r is None else r
    if sh and not C['dark']:
        drop(img, box, int(r), int(22 * G.U), 55)
    rrect(d, box, fill or C['card'], r, outline=outline or (C['line'] if C['dark'] else None), width=max(1, int(2 * G.U)))


def chip(img, d, txt, x, y, bg, fg, size=30, fname='mono', anchor='l', a=1.0, padx=None):
    size = int(size)
    tw, th = tsize(txt, fname, size)
    px = padx if padx is not None else size * .7
    w, h = tw + px * 2, size * 1.55
    if anchor == 'c':
        x -= w / 2
    elif anchor == 'r':
        x -= w
    if a < .999:
        layer(img, lambda dd, ox, oy, L: dd.rounded_rectangle((x + ox, y + oy, x + w + ox, y + h + oy), h / 2, fill=tuple(bg[:3]) + (255,)),
              (x, y, x + w + 1, y + h + 1), a)
    else:
        d.rounded_rectangle((x, y, x + w, y + h), h / 2, fill=bg)
    T(img, txt, x + px, y + h / 2, fname, size, fg, a=a, vanchor='m')
    return w, h


def arrow(d, p0, p1, col, w=4, head=16):
    d.line((p0, p1), fill=col, width=int(w))
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (-1, 1):
        a2 = ang + math.pi + s * .45
        d.line((p1, (p1[0] + head * math.cos(a2), p1[1] + head * math.sin(a2))), fill=col, width=int(w))


def bezier(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, n)]


def partial(pts, p):
    if p <= 0:
        return pts[:1]
    k = max(2, int(len(pts) * clamp(p)))
    return pts[:k]


def glitch(img, amount, seed=0):
    if amount <= 0:
        return img
    W, H = img.size
    rnd = random.Random(seed)
    out = img.copy()
    for _ in range(int(5 + 12 * amount)):
        y = rnd.randint(0, H - 20); h = rnd.randint(6, int(20 + 120 * amount * G.U))
        dx = int(rnd.uniform(-1, 1) * 140 * amount * G.U)
        out.paste(img.crop((0, y, W, min(H, y + h))), (dx, y))
    if amount > .3:
        r, g, b = out.split(); off = int(16 * amount * G.U)
        r = r.transform(r.size, Image.AFFINE, (1, 0, off, 0, 1, 0))
        b = b.transform(b.size, Image.AFFINE, (1, 0, -off, 0, 1, 0))
        out = Image.merge('RGB', (r, g, b))
    return out


def shake(t, amt, seed=1):
    return (math.sin(t * 91 + seed) * amt, math.cos(t * 77 + seed * 2) * amt)


# ------------------------------------------------------------------ real product footage (clips extracted from the official Placiq demo)
CLIPS = os.path.join(ROOT, 'assets/real-product/clips')
STILLS = os.path.join(ROOT, 'assets/real-product')


class Clip:
    """Sequential frame reader over a real product clip (ffmpeg pipe). Random access reopens the pipe."""
    _cache = {}

    def __init__(self, name):
        self.name, self.path = name, os.path.join(CLIPS, name + '.mp4')
        self.w, self.h = 1280, 720
        self.proc, self.idx, self.frame = None, -1, None

    @classmethod
    def get(cls, name):
        if name not in cls._cache:
            cls._cache[name] = Clip(name)
        return cls._cache[name]

    def _open(self, start):
        if self.proc:
            self.proc.kill()
        self.proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', '%.3f' % (start / FPS), '-i', self.path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                     stdout=subprocess.PIPE)
        self.idx = start - 1

    def at(self, t):
        f = max(0, int(t * FPS))
        if self.proc is None or f < self.idx or f > self.idx + 90:
            self._open(f)
        while self.idx < f:
            buf = self.proc.stdout.read(self.w * self.h * 3)
            if len(buf) < self.w * self.h * 3:
                break  # clip ended: hold last frame
            self.frame = Image.frombuffer('RGB', (self.w, self.h), buf, 'raw', 'RGB', 0, 1)
            self.idx += 1
        if self.frame is None:
            self.frame = Image.new('RGB', (self.w, self.h), (240, 236, 228))
        return self.frame


@lru_cache(maxsize=24)
def still(name):
    return Image.open(os.path.join(STILLS, name + '.png')).convert('RGB')


def screen(img, d, src, crop, box, C, r=None, chrome='learn.placiq.in', a=1.0):
    """Place a crop of a real product frame into box, inside a browser-chrome card."""
    r = int((r or 26) * G.U)
    x0, y0, x1, y1 = [int(v) for v in box]
    bar = int(46 * G.U) if chrome else 0
    w, h = x1 - x0, y1 - y0 - bar
    cx, cy, cw = crop  # crop centre (0..1) and width fraction
    sw, sh_ = src.size
    pw = cw * sw; ph = pw * h / w
    if ph > sh_:
        ph = sh_; pw = ph * w / h
    left = clamp(cx * sw - pw / 2, 0, sw - pw); top = clamp(cy * sh_ - ph / 2, 0, sh_ - ph)
    im = src.crop((int(left), int(top), int(left + pw), int(top + ph))).resize((w, h), Image.BILINEAR)
    cardim = Image.new('RGB', (w, h + bar), (255, 255, 255) if not C['dark'] else (24, 26, 33))
    if chrome:
        cd = ImageDraw.Draw(cardim)
        for i, c in enumerate(('#FF5F57', '#FEBC2E', '#28C840')):
            ox = int((22 + i * 28) * G.U); oy = int(bar / 2)
            cd.ellipse((ox - 7 * G.U, oy - 7 * G.U, ox + 7 * G.U, oy + 7 * G.U), fill=c)
        uw = int(330 * G.U)
        cd.rounded_rectangle((w / 2 - uw / 2, bar * .2, w / 2 + uw / 2, bar * .8), int(bar * .3), fill=(238, 235, 229) if not C['dark'] else (40, 43, 54))
        lab = text_img(chrome, 'monor', int(19 * G.U), (110, 108, 104, 255) if not C['dark'] else (160, 166, 180, 255))
        cardim.paste(lab, (int(w / 2 - lab.size[0] / 2), int(bar / 2 - lab.size[1] / 2)), lab)
    cardim.paste(im, (0, bar))
    m = round_mask(w, h + bar, r)
    if not C['dark']:
        drop(img, (x0, y0, x1, y1), r, int(30 * G.U), 70)
    if a < .999:
        m = m.point(lambda v: int(v * a))
    img.paste(cardim, (x0, y0), m)
    return (x0, y0 + bar, x1, y1)


@lru_cache(maxsize=64)
def round_mask(w, h, r):
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return m


def crop_to_screen(crop, box, src_size, pt):
    """Map a source-normalised point (0..1) to output pixel coords given a crop+box (for callouts)."""
    cx, cy, cw = crop
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sw, sh_ = src_size
    pw = cw * sw; ph = pw * h / w
    if ph > sh_:
        ph = sh_; pw = ph * w / h
    left = clamp(cx * sw - pw / 2, 0, sw - pw); top = clamp(cy * sh_ - ph / 2, 0, sh_ - ph)
    return (x0 + (pt[0] * sw - left) / pw * w, y0 + (pt[1] * sh_ - top) / ph * h)
