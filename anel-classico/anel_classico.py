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


M = 64


def band_top(im, a0=0.02, a1=0.30, strength=0.6):
    """Approved light ivory band from the top (as in the Helena post) so the gold reads."""
    import numpy as np
    yy = np.arange(H, dtype=np.float32)[:, None] / H
    a = np.clip((a1 - yy) / (a1 - a0), 0, 1) ** 1.2 * strength
    lay = Image.new('RGBA', (W, H), (250, 248, 244, 0)); lay.putalpha(Image.fromarray((np.broadcast_to(a, (H, W)) * 255).astype('uint8')))
    im.alpha_composite(lay)


def photo_slide(name, caps, script, phrase, size=210):
    """Approved feed composition: Cinzel caps left-aligned right above the big Parisienne word, one block."""
    src = Image.open(D + name).convert('RGB')
    im = src.crop((3, 0, 3 + W, H)).convert('RGBA')          # native pixels, crop only
    band_top(im)
    y = 58
    c = solid_text(caps, caps_font(40, 500), INK, 3); paste(im, c, M + 6, y)
    sc = shadowed(gold_text(script, script_font(size))); paste(im, sc, M - 4, y + ink_size(c)[1] + 4)
    yp = y + ink_size(c)[1] + 4 + ink_size(sc)[1] + 18
    for line in phrase:
        t = solid_text(line, caps_font(24, 600), BR, 3); paste(im, t, M + 6, yp); yp += ink_size(t)[1] + 10
    return im


def editorial():
    """Full-bleed photo (crop only) with the approved light ivory fade rising from the base, dark text on it."""
    import numpy as np
    src = Image.open(D + 'menina-brinco.png').convert('RGB')
    im = src.crop((2, 0, 2 + W, H))                            # native pixels, crop only
    a = np.asarray(im, np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None] / H
    x = np.clip((yy - 0.64) / (0.83 - 0.64), 0, 1); f = x * x * (3 - 2 * x) * 0.95
    a = a * (1 - f) + np.array([250, 247, 241], np.float32) * f
    im = Image.fromarray(a.astype('uint8')).convert('RGBA')
    y = C(im, solid_text('TENDÊNCIAS PASSAM.', caps_font(32, 700), BR, 10), 1105)
    y = C(im, shadowed(gold_text('Joias ficam.', script_font(150))), y + 4)
    C(im, solid_text('USE JOIAS QUE DUREM · GARANTIA VITALÍCIA', caps_font(22, 600), BR, 3), y + 14)
    return im


def delicado_slide():
    """Slide 1: ANEL CLÁSSICO over 'Delicado'; 'NO DEDO,' beside it, 'ETERNO NA HISTÓRIA' below. Swipe hint."""
    src = Image.open(D + 'classico-2.png').convert('RGB')
    im = src.crop((3, 0, 3 + W, H)).convert('RGBA')
    band_top(im, a1=0.32)
    y = 58
    c = solid_text('ANEL CLÁSSICO', caps_font(40, 500), INK, 3); paste(im, c, M + 6, y)
    ys = y + ink_size(c)[1] + 4
    sc = shadowed(gold_text('Delicado', script_font(210))); paste(im, sc, M - 4, ys)
    sw, sh = ink_size(sc)
    nd = solid_text('NO DEDO,', caps_font(34, 600), BR, 4)
    paste(im, nd, M - 4 + sw + 26, ys + sh * 0.52 - ink_size(nd)[1] / 2)      # beside the script word
    et = solid_text('ETERNO NA HISTÓRIA', caps_font(34, 600), BR, 4)
    paste(im, et, M + 6, ys + sh + 16)                                         # right below
    hint = solid_text('ARRASTE PARA O LADO  →', sans(18, 700), LABEL_COLOR, 2)
    paste(im, hint, W - M - ink_size(hint)[0], H - 66)
    return im


def clean_slide():
    """Slide 2: the other photo, clean (no text), native crop."""
    src = Image.open(D + 'classico-1.png').convert('RGB')
    return src.crop((3, 0, 3 + W, H))


if __name__ == '__main__':
    delicado_slide().convert('RGB').save(D + 'carrossel-01-delicado.jpg', quality=100, subsampling=0)
    clean_slide().save(D + 'carrossel-02-foto.jpg', quality=100, subsampling=0)
    photo_slide('classico-1.png', 'ANEL CLÁSSICO', 'Para sempre', ['ALGUMAS ESCOLHAS', 'A GENTE FAZ UMA VEZ SÓ']).convert('RGB').save(D + '01-anel-classico.jpg', quality=100, subsampling=0)
    photo_slide('classico-2.png', 'ANEL CLÁSSICO', 'Delicado', ['NO DEDO,', 'ETERNO NA HISTÓRIA']).convert('RGB').save(D + '02-anel-classico.jpg', quality=100, subsampling=0)
    editorial().convert('RGB').save(D + 'joias-que-ficam.jpg', quality=100, subsampling=0)
    print('ok')
