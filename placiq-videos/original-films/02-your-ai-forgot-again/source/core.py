"""Placiq motion engine - drawing primitives (PIL, 1920x1080 @ 30fps)."""
import math, os, random
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = {
    'black': os.path.join(ROOT, 'assets/fonts/ArchivoBlack-Regular.ttf'),
    'mono': os.path.join(ROOT, 'assets/fonts/SpaceMono-Bold.ttf'),
    'monor': os.path.join(ROOT, 'assets/fonts/SpaceMono-Regular.ttf'),
    'serif': os.path.join(ROOT, 'assets/fonts/InstrumentSerif-Italic.ttf'),
    'sans': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
}
SHOTS = os.path.join(ROOT, 'assets/real-product')


def hexc(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def prog(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else float(t >= start)


def eo(x):  # ease out cubic
    x = clamp(x); return 1 - (1 - x) ** 3


def eo5(x):
    x = clamp(x); return 1 - (1 - x) ** 5


def eio(x):
    x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def eback(x, s=1.9):
    x = clamp(x); c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def lerp(a, b, x):
    return a + (b - a) * x


@lru_cache(maxsize=256)
def font(name, size):
    return ImageFont.truetype(FONTS[name], int(size))


@lru_cache(maxsize=6000)
def text_img(txt, fname, size, color):
    f = font(fname, size)
    bb = f.getbbox(txt)
    asc, desc = f.getmetrics()
    w = max(1, bb[2] - min(0, bb[0]) + 4)
    h = asc + desc + 4
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - min(0, bb[0]), 2), txt, font=f, fill=color)
    return im


def tsize(txt, fname, size):
    im = text_img(txt, fname, size, (0, 0, 0, 255))
    return im.size


def fade(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    al = im.getchannel('A').point(lambda v: int(v * a))
    im.putalpha(al)
    return im


def paste(dst, src, x, y, a=1.0):
    if a <= 0.003:
        return
    s = fade(src, a)
    dst.paste(s, (int(x), int(y)), s)


def text(dst, txt, x, y, fname, size, color, anchor='l', a=1.0):
    im = text_img(txt, fname, int(size), color)
    w, h = im.size
    if anchor == 'c':
        x -= w / 2
    elif anchor == 'r':
        x -= w
    paste(dst, im, x, y, a)
    return w, h


def text_mask_up(dst, txt, x, y, fname, size, color, p, anchor='l'):
    """Masked slide-up reveal: text rises out of an invisible baseline slot."""
    if p <= 0:
        return tsize(txt, fname, size)
    im = text_img(txt, fname, int(size), color)
    w, h = im.size
    if anchor == 'c':
        x -= w / 2
    elif anchor == 'r':
        x -= w
    e = eo5(p)
    dy = int((1 - e) * h)
    if h - dy > 0:
        crop = im.crop((0, 0, w, h - dy))
        dst.paste(crop, (int(x), int(y + dy)), crop)
    return w, h


def rect(d, box, fill, r=0, outline=None, width=1):
    x0, y0, x1, y1 = box
    if x1 <= x0 or y1 <= y0:
        return
    if r:
        d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)
    else:
        d.rectangle(box, fill=fill, outline=outline, width=width)


@lru_cache(maxsize=64)
def shadow(w, h, r, blur, alpha):
    pad = blur * 3
    im = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((pad, pad + blur // 2, pad + w, pad + h + blur // 2), r, fill=(0, 0, 0, alpha))
    return im.filter(ImageFilter.GaussianBlur(blur)), pad


@lru_cache(maxsize=64)
def round_mask(w, h, r):
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    return m


@lru_cache(maxsize=32)
def shot(name):
    im = Image.open(os.path.join(SHOTS, name + '.png')).convert('RGB')
    w, h = im.size
    # trim the blue desktop edge of the demo capture
    return im.crop((int(w * .012), int(h * .015), int(w * .988), int(h * .985)))


def window(dst, name, cx, cy, width, zoom=1.0, focus=(.5, .5), a=1.0, r=22, chrome=True, dark=False):
    """Real product screenshot in a browser-window card with soft shadow + optional zoom crop."""
    src = shot(name)
    sw, sh = src.size
    width = int(width)
    height = int(width * sh / sw)
    if zoom > 1.001:
        cw, ch = sw / zoom, sh / zoom
        fx = clamp(focus[0] * sw - cw / 2, 0, sw - cw)
        fy = clamp(focus[1] * sh - ch / 2, 0, sh - ch)
        src = src.crop((int(fx), int(fy), int(fx + cw), int(fy + ch)))
    bar = 34 if chrome else 0
    im = src.resize((width, height), Image.BILINEAR)
    card = Image.new('RGBA', (width, height + bar), hexc('#1A1C24' if dark else '#FFFFFF'))
    if chrome:
        cd = ImageDraw.Draw(card)
        for i, c in enumerate(('#FF5F57', '#FEBC2E', '#28C840')):
            cd.ellipse((16 + i * 22, 11, 28 + i * 22, 23), fill=c)
        cd.rounded_rectangle((width // 2 - 170, 7, width // 2 + 170, 27), 9, fill=hexc('#2A2D38' if dark else '#EFECE6'))
        lab = text_img('learn.placiq.in', 'monor', 14, hexc('#9AA0AE' if dark else '#6B6A66'))
        card.paste(lab, (width // 2 - lab.size[0] // 2, 7), lab)
    card.paste(im, (0, bar))
    card.putalpha(round_mask(width, height + bar, r))
    sh_im, pad = shadow(width, height + bar, r, 28, 90)
    x, y = int(cx - width / 2), int(cy - (height + bar) / 2)
    paste(dst, sh_im, x - pad, y - pad + 10, a)
    paste(dst, card, x, y, a)
    return (x, y, x + width, y + height + bar)


def pill(dst, d, txt, x, y, bg, fg, size=22, fname='mono', pad=(18, 9), a=1.0, anchor='l'):
    tw, th = tsize(txt, fname, size)
    w, h = tw + pad[0] * 2, th + pad[1] * 2 - 6
    if anchor == 'c':
        x -= w / 2
    if a < 1:
        layer = Image.new('RGBA', (int(w) + 2, int(h) + 2), (0, 0, 0, 0))
        ImageDraw.Draw(layer).rounded_rectangle((0, 0, w, h), h / 2, fill=bg)
        paste(dst, layer, x, y, a)
    else:
        d.rounded_rectangle((x, y, x + w, y + h), h / 2, fill=bg)
    text(dst, txt, x + pad[0], y + pad[1] - 5, fname, size, fg, a=a)
    return w, h


def glitch(img, amount, seed=0):
    """Horizontal slice displacement + RGB split."""
    if amount <= 0:
        return img
    rnd = random.Random(seed)
    out = img.copy()
    for _ in range(int(6 + 14 * amount)):
        y = rnd.randint(0, H - 20)
        h = rnd.randint(6, int(20 + 90 * amount))
        dx = int(rnd.uniform(-1, 1) * 160 * amount)
        band = img.crop((0, y, W, min(H, y + h)))
        out.paste(band, (dx, y))
    if amount > .3:
        r, g, b = out.split()
        off = int(18 * amount)
        r = r.transform(r.size, Image.AFFINE, (1, 0, off, 0, 1, 0))
        b = b.transform(b.size, Image.AFFINE, (1, 0, -off, 0, 1, 0))
        out = Image.merge('RGB', (r, g, b))
    return out


def bg_texture(color, dot, step=48, kind='dots'):
    im = Image.new('RGB', (W, H), color)
    d = ImageDraw.Draw(im)
    if kind == 'dots':
        for y in range(step // 2, H, step):
            for x in range(step // 2, W, step):
                d.ellipse((x - 1.6, y - 1.6, x + 1.6, y + 1.6), fill=dot)
    else:
        for x in range(0, W, step):
            d.line((x, 0, x, H), fill=dot)
        for y in range(0, H, step):
            d.line((0, y, W, y), fill=dot)
    return im
