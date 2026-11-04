"""Shimmer visual identity.

Rules from the brand owner:
- caps: Cinzel, tight spacing, white, subtle shadow
- highlight word: Parisienne filled with the brand gold texture (pure, unaltered), discreet shadow
- caps sit left-aligned on top of the script word, forming one block
- no sparkles, shines or other artificial effects
- photos arrive already edited: no sharpening, no colour changes, no heavy crops; export at top quality
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
IMG = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/images/'
GOLD_TEX = Image.open(IMG + '12.webp').convert('RGB')
WHITE = (255, 253, 248)
CHAMPAGNE = np.array([212, 178, 108], np.float32)


def script_font(size):
    return ImageFont.truetype(S + 'fonts/Parisienne.ttf', size)


def caps_font(size, wght=500):
    # Cinzel is part of the brand identity (owner's call)
    f = ImageFont.truetype(S + 'fonts/Cinzel.ttf', size)
    f.set_variation_by_axes([wght])
    return f


FEAT = ['lnum']  # lining figures: Cormorant's old-style 1 reads as 'i'


def _mask(text, fnt, tracking=0):
    if tracking:
        tw = sum(fnt.getlength(c, features=FEAT) for c in text) + tracking * (len(text) - 1)
    else:
        tw = fnt.getlength(text, features=FEAT)
    asc, desc = fnt.getmetrics()
    pad = int(fnt.size * 0.6)
    m = Image.new('L', (int(tw) + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(m)
    if tracking:
        x = pad
        for c in text:
            d.text((x, pad), c, font=fnt, fill=255, features=FEAT)
            x += fnt.getlength(c, features=FEAT) + tracking
    else:
        d.text((pad, pad), text, font=fnt, fill=255, features=FEAT)
    return m


def _with_shadow(fill, m, offset, blur, alpha, color):
    """Compose fill over a soft offset shadow; returns layer cropped to the ink box (+ shadow)."""
    w, h = m.size
    out = Image.new('RGBA', (w + offset[0] + 4, h + offset[1] + 4), (0, 0, 0, 0))
    sh = m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
    s_ = Image.new('RGBA', (w, h), color + (0,))
    s_.putalpha(sh)
    out.alpha_composite(s_, offset)
    out.alpha_composite(fill, (0, 0))
    bb = m.getbbox()
    return out, bb  # bb = ink box inside the layer


def gold_text(text, fnt, tracking=0):
    """Text clipped inside the brand gold texture, like a PowerClip: the whole texture spans the
    lettering, so each part of the word catches a different band (highlight, mid gold, darker gold)."""
    m = _mask(text, fnt, tracking)
    w, h = m.size
    x0, y0, x1, y1 = m.getbbox()
    iw, ih = x1 - x0, y1 - y0
    # the ink box covers ~0.15-0.85 of the texture height and its full width
    th = int(ih / 0.70) + 1
    tex = GOLD_TEX.resize((iw, th), Image.LANCZOS)
    top = int(th * 0.15)
    fill = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    fill.paste(tex.crop((0, top, iw, top + ih)).convert('RGBA'), (x0, y0))
    fill.putalpha(m)
    off = (max(2, int(fnt.size * 0.025)), max(2, int(fnt.size * 0.035)))
    return _with_shadow(fill, m, off, max(1.5, fnt.size * 0.02), 0.45, (55, 45, 35))


def white_text(text, fnt, tracking=0, color=WHITE):
    m = _mask(text, fnt, tracking)
    fill = Image.new('RGBA', m.size, color + (0,))
    fill.putalpha(m)
    # tight, faint shadow: a wide one reads as haze over the client's photo
    off = (1, max(1, int(fnt.size * 0.02)))
    return _with_shadow(fill, m, off, max(0.8, fnt.size * 0.012), 0.28, (40, 32, 24))


def paste(base, layer_bb, x, y, alpha=1.0, anchor='left'):
    """Paste so the ink box's top-left (or top-centre) lands at (x, y)."""
    if alpha <= 0.01:
        return
    lay, bb = layer_bb
    if alpha < 1:
        lay = lay.copy()
        lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    ink_w = bb[2] - bb[0]
    dx = x - bb[0] - (ink_w / 2 if anchor == 'center' else 0)
    base.alpha_composite(lay, (int(round(dx)), int(round(y - bb[1]))))


def ink_size(layer_bb):
    bb = layer_bb[1]
    return bb[2] - bb[0], bb[3] - bb[1]


def title_block(base, caps, script, cx, top, alpha=1.0, overlap=0.04, indent=0.09):
    """Caps left-aligned over the script word (indented a little into it), block centred on cx."""
    cw, ch = ink_size(caps)
    sw, sh = ink_size(script)
    bw = max(sw, cw + sw * indent)
    left = cx - bw / 2
    paste(base, caps, left + sw * indent, top, alpha)
    paste(base, script, left, top + ch + sh * 0.02 - sh * overlap, alpha)
    return top + ch - sh * overlap + sh  # bottom of the block


def cover(src, W, H, focus, ty, zoom=1.0):
    """Cover-fit src to W x H (Lanczos only), placing `focus` at (W/2, ty) when there is room."""
    iw, ih = src.size
    z = max(W / iw, H / ih) * zoom
    ox = min(max(focus[0] - W / 2 / z, 0), iw - W / z)
    oy = min(max(focus[1] - ty / z, 0), ih - H / z)
    fr = src.transform((W, H), Image.AFFINE, (1 / z, 0, ox, 0, 1 / z, oy), resample=Image.BICUBIC) \
        if zoom != 1.0 else src.resize((int(iw * z + 0.5), int(ih * z + 0.5)), Image.LANCZOS).crop(
            (int(ox * z), int(oy * z), int(ox * z) + W, int(oy * z) + H))
    return fr


def crop_native(src, W, H, oy=None, ox=None):
    """Crop to W x H at the photo's own resolution: no resampling at all."""
    iw, ih = src.size
    ox = (iw - W) // 2 if ox is None else ox
    oy = (ih - H) // 2 if oy is None else oy
    return src.crop((ox, oy, ox + W, oy + H))


def save_hq(img, path):
    img = img.convert('RGB')
    if path.lower().endswith('.png'):
        img.save(path, optimize=True)
    else:
        img.save(path, quality=100, subsampling=0)


def gold_fill(mask):
    """Fill any L mask (icon, shape) with the gold texture spanning its ink box, PowerClip style."""
    w, h = mask.size
    x0, y0, x1, y1 = mask.getbbox()
    iw, ih = x1 - x0, y1 - y0
    th = int(ih / 0.70) + 1
    tex = GOLD_TEX.resize((iw, th), Image.LANCZOS)
    top = int(th * 0.15)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.paste(tex.crop((0, top, iw, top + ih)).convert('RGBA'), (x0, y0))
    out.putalpha(mask)
    return out
