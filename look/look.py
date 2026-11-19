import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
from story_nativo_lib import emoji

SRC = '/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/gp/full/'
D = '/home/user/print/look/'
IV = (247, 243, 236); INK = (58, 45, 34); BR = (132, 101, 46); SOFT = (112, 103, 93)


def cover(n, w, h, fx=0.5, fy=0.5):
    """Downscale-only cover crop of a 12 MP original."""
    im = Image.open(SRC + f'{n:03d}.jpg').convert('RGB')
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x = int((im.width - w) * fx); y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def C(img, lay, y, x=None): paste(img, lay, img.width / 2 if x is None else x, y, anchor='center'); return y + ink_size(lay)[1]


def rule(img, y, half=56):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).line([(img.width / 2 - half, y), (img.width / 2 + half, y)], fill=255, width=3)
    img.alpha_composite(gold_fill(m))


BAND = 320


def slide(n, kicker, script, sub, fx=0.5, fy=0.5, ssize=120):
    W, H = 1080, 1350
    im = Image.new('RGBA', (W, H), IV + (255,))
    im.paste(cover(n, W, H - BAND, fx, fy), (0, BAND))
    y = C(im, solid_text(kicker, caps_font(26, 600), BR, 8), 58)
    y = C(im, gold_text(script, script_font(ssize)), y + 6)
    C(im, solid_text(sub, sans(30, 500), SOFT), y + 12)
    return im


def cta():
    W, H = 1080, 1350
    im = Image.new('RGBA', (W, H), IV + (255,))
    y = C(im, gold_text('Qual você levaria?', script_font(118)), 110)
    for i, (n, fx, fy) in enumerate([(209, 0.35, 0.3), (205, 0.6, 0.5), (214, 0.5, 0.3)]):
        ph = cover(n, 300, 560, fx, fy); x = 60 + i * 330
        m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 299, 559], radius=26, fill=255)
        fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle([x - 5, 395, x + 305, 965], radius=30, outline=255, width=4); im.alpha_composite(gold_fill(fr))
        im.paste(ph, (x, 400), m)
        c = Image.new('L', (W, H), 0); ImageDraw.Draw(c).ellipse([x + 150 - 38, 925, x + 150 + 38, 1001], fill=255); im.alpha_composite(gold_fill(c))
        paste(im, solid_text(str(i + 1), sans(44, 700), (255, 253, 248)), x + 150, 940, anchor='center')
    t = solid_text('Comenta 1, 2 ou 3', sans(42, 700), INK); y2 = C(im, t, 1060)
    e = emoji('💬', 46); im.alpha_composite(e, (int(W / 2 + ink_size(t)[0] / 2 + 12), 1058))
    C(im, solid_text('ATENDIMENTO COM HORA MARCADA · LINK NA BIO', caps_font(22, 600), BR, 3), y2 + 34)
    return im


SLIDES = [
    lambda: slide(207, 'SHIMMER JOIAS', 'Monte seu look', 'pulseira · mix de anéis · colar', fy=0.35),
    lambda: slide(209, '01', 'Pulseira trevo', 'o detalhe que aparece em toda foto', fy=0.3),
    lambda: slide(205, '02', 'Mix de anéis', 'um fino, um com pedra, um diferente', fy=0.45),
    lambda: slide(214, '03', 'Colar delicado', 'pra usar todo dia, com qualquer decote', fy=0.25),
    cta,
]


# ---------------- stories 1080x1920 ----------------
def story_poll():
    W, H = 1080, 1920
    im = Image.new('RGBA', (W, H), IV + (255,))
    y = C(im, solid_text('ENQUETE', caps_font(28, 600), BR, 10), 300)
    y = C(im, gold_text('Pulseira ou anéis?', script_font(116)), y + 8)
    for i, (n, fx, fy, lab) in enumerate([(209, 0.4, 0.3, 'PULSEIRA'), (205, 0.6, 0.5, 'ANÉIS')]):
        ph = cover(n, 470, 700, fx, fy); x = 60 + i * 490
        m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, ph.width - 1, ph.height - 1], radius=30, fill=255)
        im.paste(ph, (x, 560), m)
        lb = solid_text(lab, caps_font(26, 700), INK, 6); paste(im, lb, x + 235, 1280, anchor='center')
    return im   # space 1340-1520 left free for the poll sticker


def story_box():
    W, H = 1080, 1920
    im = Image.new('RGBA', (W, H), IV + (255,))
    ph = cover(214, W, 1250, 0.5, 0.2); im.paste(ph, (0, 0))
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    a = np.clip((yy - 1050) / 200, 0, 1); a = a * a * (3 - 2 * a)
    f = np.asarray(im.convert('RGB'), np.float32); f = f * (1 - a) + np.array(IV, np.float32) * a
    im = Image.fromarray(f.astype(np.uint8)).convert('RGBA')
    y = C(im, gold_text('Qual peça não pode', script_font(96)), 1270)
    C(im, gold_text('faltar no seu look?', script_font(96)), y + 4)
    return im   # space ~1480-1540 for the question sticker


def story_teaser(cover_img):
    W, H = 1080, 1920
    im = Image.new('RGBA', (W, H), IV + (255,))
    y = C(im, solid_text('NOVIDADE NO FEED', caps_font(30, 600), BR, 10), 300)
    t = gold_text('Monte seu look', script_font(118)); C(im, t, y + 8)
    cv = cover_img.convert('RGB').resize((640, 800), Image.LANCZOS)
    fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle([214, 584, 866, 1396], radius=34, outline=255, width=4); im.alpha_composite(gold_fill(fr))
    m = Image.new('L', cv.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 639, 799], radius=28, fill=255)
    im.paste(cv, (220, 590), m)
    t2 = solid_text('arrasta pro lado e me conta qual você levaria', sans(30, 500), SOFT); C(im, t2, 1440)
    e = emoji('👆', 70); im.alpha_composite(e, (W // 2 - 35, 1500))
    return im


if __name__ == '__main__':
    imgs = [f() for f in SLIDES]
    for i, im in enumerate(imgs, 1): im.convert('RGB').save(D + f'0{i}-monte-seu-look.jpg', quality=95, subsampling=0)
    story_poll().convert('RGB').save(D + 'story-1-enquete.jpg', quality=95, subsampling=0)
    story_box().convert('RGB').save(D + 'story-2-caixinha.jpg', quality=95, subsampling=0)
    story_teaser(imgs[0]).convert('RGB').save(D + 'story-3-novidade-feed.jpg', quality=95, subsampling=0)
    print('ok')
