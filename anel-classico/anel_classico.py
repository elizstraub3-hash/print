"""Carrossel 'Anel clássico' (2 slides) + post editorial 'Joias que ficam' with the 3 photos Eliz sent.
Photos are only cropped / downscaled, never upscaled. Gold = brand texture (escovado)."""
import sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *

D = '/home/user/print/anel-classico/'
W, H = 1080, 1350
INK = (58, 45, 34); BR = (118, 88, 38); SOFT = (96, 86, 76); IV = (247, 243, 236)


def shadowed(lay_bb, blur=6, alpha=0.30, dy=3, col=(70, 50, 20)):
    lay, bb = lay_bb
    a = lay.getchannel('A')
    sh = Image.new('RGBA', lay.size, col + (0,)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha)))
    out = Image.new('RGBA', lay.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, dy)); out.alpha_composite(lay)
    return out, bb


def C(im, lay, y): paste(im, lay, im.width / 2, y, anchor='center'); return y + ink_size(lay)[1]


def rule(im, y, half=50):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).line([(im.width / 2 - half, y), (im.width / 2 + half, y)], fill=255, width=3); im.alpha_composite(gold_fill(m))


def photo_slide(name, kicker, script, line, top=150):
    src = Image.open(D + name).convert('RGB')
    im = src.crop((3, 0, 3 + W, H)).convert('RGBA')          # native pixels: 1086x1448 -> 1080x1350 (crop only)
    y = C(im, solid_text(kicker, caps_font(30, 700), BR, 10), top)
    rule(im, y + 24)
    y = C(im, shadowed(gold_text(script, script_font(140))), y + 46)
    C(im, solid_text(line, sans(36, 600), INK), y + 14)
    return im


def editorial():
    """'Something different': magazine layout, photo inset in an ivory passe-partout, title below."""
    im = Image.new('RGBA', (W, H), IV + (255,))
    src = Image.open(D + 'menina-brinco.png').convert('RGB')
    pw, ph = 960, 1010
    k = pw / src.width                                         # 0.885: downscale only
    s = src.resize((pw, round(src.height * k)), Image.LANCZOS).crop((0, 20, pw, 20 + ph))
    x0, y0 = (W - pw) // 2, 60
    fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rectangle([x0 - 10, y0 - 10, x0 + pw + 9, y0 + ph + 9], outline=255, width=2); im.alpha_composite(gold_fill(fr))
    im.paste(s, (x0, y0))
    y = C(im, solid_text('TENDÊNCIAS PASSAM.', caps_font(30, 700), BR, 10), y0 + ph + 34)
    y = C(im, shadowed(gold_text('Joias ficam.', script_font(118))), y + 6)
    C(im, solid_text('use joias que durem · garantia vitalícia', sans(30, 600), SOFT), y + 8)
    return im


if __name__ == '__main__':
    photo_slide('classico-1.png', 'ANEL CLÁSSICO', 'Para sempre', 'algumas escolhas a gente faz uma vez só').convert('RGB').save(D + '01-anel-classico.jpg', quality=95, subsampling=0)
    photo_slide('classico-2.png', 'ANEL CLÁSSICO', 'Delicado', 'no dedo, eterno na história').convert('RGB').save(D + '02-anel-classico.jpg', quality=95, subsampling=0)
    editorial().convert('RGB').save(D + 'joias-que-ficam.jpg', quality=95, subsampling=0)
    print('ok')
