"""Shimmer visual identity: white serif caps, Parisienne script filled with the gold texture, small caps details."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
IMG = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/images/'
GOLD_TEX = Image.open(IMG + '12.webp').convert('RGB')
WHITE = (255, 253, 248)


def script_font(size):
    return ImageFont.truetype(S + 'fonts/Parisienne.ttf', size)


def caps_font(size, wght=500):
    f = ImageFont.truetype(S + 'fonts/Cinzel.ttf', size)
    f.set_variation_by_axes([wght])
    return f


def _mask(text, fnt, tracking=0):
    """Tight L mask of the text; tracking only applied to caps (script must stay joined)."""
    if tracking:
        tw = sum(fnt.getlength(c) for c in text) + tracking * (len(text) - 1)
    else:
        tw = fnt.getlength(text)
    asc, desc = fnt.getmetrics()
    pad = int(fnt.size * 0.6)
    m = Image.new('L', (int(tw) + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(m)
    if tracking:
        x = pad
        for c in text:
            d.text((x, pad), c, font=fnt, fill=255)
            x += fnt.getlength(c) + tracking
    else:
        d.text((pad, pad), text, font=fnt, fill=255)
    return m, pad


def gold_text(text, fnt, shine=None, tracking=0):
    """RGBA layer: text filled with the brushed-gold texture, soft drop shadow, optional moving highlight."""
    m, pad = _mask(text, fnt, tracking)
    w, h = m.size
    tex = GOLD_TEX.resize((max(w, int(h * GOLD_TEX.width / GOLD_TEX.height)), h), Image.LANCZOS).crop((0, 0, w, h))
    arr = np.asarray(tex, np.float32)
    if shine is not None:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        pos = (xx + yy * 0.5) / (w + h * 0.5)
        band = np.exp(-((pos - shine) / 0.06) ** 2)[..., None]
        arr = arr + (np.array([255, 250, 230]) - arr) * band * 0.75
    fill = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')
    fill.putalpha(m)
    out = Image.new('RGBA', (w, h + 12), (0, 0, 0, 0))
    sh = m.filter(ImageFilter.GaussianBlur(fnt.size * 0.05)).point(lambda v: int(v * 0.55))
    shadow = Image.new('RGBA', (w, h), (40, 26, 10, 0))
    shadow.putalpha(sh)
    out.alpha_composite(shadow, (0, int(fnt.size * 0.03) + 2))
    out.alpha_composite(fill, (0, 0))
    return out, pad


def white_text(text, fnt, tracking=0, color=WHITE, shadow=0.45):
    m, pad = _mask(text, fnt, tracking)
    w, h = m.size
    out = Image.new('RGBA', (w, h + 8), (0, 0, 0, 0))
    sh = m.filter(ImageFilter.GaussianBlur(max(2, fnt.size * 0.08))).point(lambda v: int(v * shadow))
    s_ = Image.new('RGBA', (w, h), (20, 14, 8, 0))
    s_.putalpha(sh)
    out.alpha_composite(s_, (0, 3))
    f_ = Image.new('RGBA', (w, h), color + (0,))
    f_.putalpha(m)
    out.alpha_composite(f_, (0, 0))
    return out, pad


def place(base, layer, pad, cx, top, alpha=1.0, dy=0):
    """Paste a text layer centered on cx with its glyph top at `top`."""
    if alpha <= 0.01:
        return
    lay = layer
    if alpha < 1:
        lay = layer.copy()
        lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    base.alpha_composite(lay, (int(cx - lay.width / 2), int(top - pad + dy)))


def sparkle(base, cx, cy, size, alpha):
    if alpha <= 0.01:
        return
    r = int(size * 1.3)
    g = Image.new('L', (2 * r, 2 * r), 0)
    d = ImageDraw.Draw(g)
    for ang, ln in ((0, 1.0), (90, 1.0), (45, 0.45), (135, 0.45)):
        a = math.radians(ang)
        dx, dy = math.cos(a) * size * ln, math.sin(a) * size * ln
        nx, ny = -math.sin(a) * size * 0.05, math.cos(a) * size * 0.05
        d.polygon([(r - dx, r - dy), (r + nx, r + ny), (r + dx, r + dy), (r - nx, r - ny)], fill=255)
    glow = g.filter(ImageFilter.GaussianBlur(size * 0.12)).point(lambda v: min(255, int(v * 1.6)))
    m = Image.fromarray(np.maximum(np.asarray(g), np.asarray(glow)))
    lay = Image.new('RGBA', g.size, (255, 252, 244, 0))
    lay.putalpha(m.point(lambda v: int(v * alpha)))
    base.alpha_composite(lay, (int(cx - r), int(cy - r)))


def cover(src, W, H, focus, ty, zoom=1.0):
    """Cover-crop src to W x H with `focus` placed at (W/2, ty)."""
    iw, ih = src.size
    z = max(W / iw, H / ih) * zoom
    ox = min(max(focus[0] - W / 2 / z, 0), iw - W / z)
    oy = min(max(focus[1] - ty / z, 0), ih - H / z)
    fr = src.transform((W, H), Image.AFFINE, (1 / z, 0, ox, 0, 1 / z, oy), resample=Image.BICUBIC)
    return fr, ((focus[0] - ox) * z, (focus[1] - oy) * z)


def top_shade(W, H, depth, strength=0.6, color=(48, 36, 26)):
    """Warm dark gradient behind the title block so white type reads on light photos."""
    y = np.arange(H, dtype=np.float32)[:, None]
    a = np.clip(1 - y / depth, 0, 1) ** 1.3 * strength
    lay = Image.new('RGBA', (W, H), color + (0,))
    lay.putalpha(Image.fromarray((np.broadcast_to(a, (H, W)) * 255).astype(np.uint8)))
    return lay
