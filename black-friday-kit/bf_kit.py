import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *

D = '/home/user/print/black-friday-kit/'
BLK = np.array([13, 11, 9], np.float32)
IVT = (246, 240, 228); SOFT = (196, 186, 170)
RING_TOP = {63: 633, 64: 691, 65: 806, 66: 729}     # top of the rings at 1080 px width


def photo(n):
    im = Image.open(D + f'fotos/{n}_x2.png').convert('RGB')
    return np.asarray(im.resize((1080, round(im.height * 1080 / im.width)), Image.LANCZOS), np.float32)


def base(W, H, n, top, ring_y, fade=150, z=1.0):
    """Black canvas; photo from `top` down, rings landing at `ring_y`, soft fade into the black above."""
    ph = photo(n)
    if z != 1.0:
        ph = np.asarray(Image.fromarray(ph.astype(np.uint8)).resize((round(1080 * z), round(ph.shape[0] * z)), Image.LANCZOS), np.float32)
        cx = (ph.shape[1] - 1080) // 2; ph = ph[:, cx:cx + 1080]
    src0 = int(RING_TOP[n] * z - (ring_y - top))
    f = np.empty((H, W, 3), np.float32); f[:] = BLK
    win = ph[src0:src0 + (H - top)]
    f[top:top + len(win)] = win
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    a = np.clip((yy - top) / fade, 0, 1) ** 1.6
    end = top + len(win)
    if end < H: a = a * np.clip((end - 20 - yy) / 140, 0, 1)          # soft fade where the photo runs out
    f = BLK * (1 - a) + f * a
    return f


def C(img, layer, y, x=None):
    paste(img, layer, img.width / 2 if x is None else x, y, anchor='center'); return y + ink_size(layer)[1]


def rule(img, y, half=60):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).line([(img.width / 2 - half, y), (img.width / 2 + half, y)], fill=255, width=3)
    img.alpha_composite(gold_fill(m))


def kicker(img, y):
    return C(img, gold_text('BLACK FRIDAY', caps_font(40, 600), 12), y)


def to_img(f): return Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).convert('RGBA')


# ---------------- carrossel 1080x1350 ----------------
def slide1():
    im = to_img(base(1080, 1350, 66, 470, 650))
    y = kicker(im, 92); rule(im, y + 30)
    y = C(im, solid_text('COMPRE O PAR DE ALIANÇAS', caps_font(50, 600), IVT, 3), y + 70)
    C(im, gold_text('e ganhe o solitário', script_font(124)), y + 18)
    return im


def slide2():
    im = to_img(base(1080, 1350, 63, 560, 700))
    y = kicker(im, 80); rule(im, y + 28)
    y = C(im, solid_text('PAR DE ALIANÇAS TRADICIONAIS', caps_font(40, 600), IVT, 3), y + 64)
    y = C(im, solid_text('abauladas · 3 mm de largura', sans(34, 500), SOFT), y + 16)
    y = C(im, gold_text('+ Solitário de brinde', script_font(96)), y + 34)
    y = C(im, solid_text('moissanite de 3 mm · cor da pedra personalizável', sans(31, 500), SOFT), y + 10)
    return im


def price(im, y, big=128):
    y = C(im, solid_text('R$ 3.199,00', sans(big, 600), IVT), y)
    y = C(im, solid_text('em até 10x de R$ 319,90 sem juros', sans(36, 500), SOFT), y + 26)
    y = C(im, gold_text('ou R$ 2.879,10 à vista · 10% OFF', sans(38, 700)), y + 16)
    return y


def slide3():
    im = to_img(base(1080, 1350, 64, 640, 640, fade=150))
    y = kicker(im, 80); rule(im, y + 28)
    y = price(im, y + 62)
    y = C(im, solid_text('+ SOLITÁRIO DE BRINDE · GARANTIA VITALÍCIA', caps_font(25, 600), SPEC_COLOR, 3), y + 30)
    return im


# ---------------- story 1080x1920 ----------------
def story_layers(im):
    """Text kept between 14% (269 px) and 80% (1536 px) of the height."""
    y = kicker(im, 285); rule(im, y + 26)
    y = C(im, solid_text('COMPRE O PAR DE ALIANÇAS', caps_font(46, 600), IVT, 3), y + 56)
    C(im, gold_text('e ganhe o solitário', script_font(104)), y + 10)


def price_card(im, y0=1314):
    x0, x1, y1 = 120, 960, y0 + 220
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], radius=28, fill=255)
    card = Image.new('RGBA', im.size, (13, 11, 9, 0)); card.putalpha(m.point(lambda v: int(v * 0.86))); im.alpha_composite(card)
    fr = Image.new('L', im.size, 0); ImageDraw.Draw(fr).rounded_rectangle([x0, y0, x1, y1], radius=28, outline=255, width=3); im.alpha_composite(gold_fill(fr))
    y = C(im, solid_text('R$ 3.199,00', sans(84, 600), IVT), y0 + 24)
    y = C(im, solid_text('em até 10x de R$ 319,90 sem juros', sans(32, 500), SOFT), y + 20)
    C(im, gold_text('ou R$ 2.879,10 à vista · 10% OFF', sans(34, 700)), y + 12)
    assert y1 < 1536


def story(z=1.0):
    im = to_img(base(1080, 1920, 66, 540, 650, fade=90, z=z))
    story_layers(im); price_card(im)
    return im


if __name__ == '__main__':
    for i, f in enumerate([slide1, slide2, slide3], 1):
        f().convert('RGB').save(D + f'0{i}-black-friday.jpg', quality=95, subsampling=0)
    story().convert('RGB').save(D + 'story-black-friday-aliancas.jpg', quality=95, subsampling=0)
    if 'video' in sys.argv:
        W, H, FPS, DUR = 1080, 1920, 30, 7.0
        txt = to_img(np.zeros((H, W, 3), np.float32)); txt.putalpha(0)
        enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + 'story-black-friday-aliancas.mp4'], stdin=subprocess.PIPE)
        def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
        # layers rendered once on transparent canvases
        L1 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); story_layers(L1)
        L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); price_card(L2)
        A1, A2 = np.asarray(L1, np.float32), np.asarray(L2, np.float32)
        for n in range(int(DUR * FPS)):
            t = n / FPS
            f = base(W, H, 66, 540, 650, fade=90, z=1.0 + 0.05 * t / DUR)
            for arr, t0 in ((A1, 0.0), (A2, 1.2)):
                k = 1.0 if t0 == 0 else ease((t - t0) / 0.7)
                if k <= 0: continue
                lay = np.roll(arr, int(round((1 - k) * 24)), axis=0); al = lay[..., 3:4] / 255 * k
                f = f * (1 - al) + lay[..., :3] * al
            enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
        enc.stdin.close(); enc.wait()
    print('ok')
