"""Post + Story 'Detalhes que fazem o look' from the photo Eliz edited (native 1086x1449)."""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/look/'
SRC = Image.open(D + 'detalhes-original.webp').convert('RGB')
IV = (247, 243, 236); INK = (58, 45, 34); BR = (132, 101, 46); SOFT = (112, 103, 93)
# numbered markers, placed beside each piece (never on it), in photo coordinates
MARK = [(1, (492, 512), 'Brinco ponto de luz'), (2, (636, 636), 'Meia aliança cravejada'),
        (3, (884, 868), 'Anel com pedra amarela'), (4, (1012, 752), 'Aros finos')]


def dot(img, n, x, y, k=1.0):
    if k <= 0.01: return
    r = 27 * (0.6 + 0.4 * k)
    sh = Image.new('L', img.size, 0); ImageDraw.Draw(sh).ellipse([x - r - 3, y - r - 3, x + r + 3, y + r + 3], fill=int(110 * k))
    img.alpha_composite(Image.merge('RGBA', [Image.new('L', img.size, 0)] * 3 + [sh.filter(ImageFilter.GaussianBlur(4))]))
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse([x - r, y - r, x + r, y + r], fill=int(255 * k)); img.alpha_composite(gold_fill(m))
    t = solid_text(str(n), sans(int(34 * (0.6 + 0.4 * k)), 700), (255, 253, 248))
    if k > 0.5: paste(img, t, x, y - ink_size(t)[1] / 2 - 1, anchor='center')


def legend(img, top, ks=(1, 1, 1, 1)):
    W = img.width
    for i, (n, _, lab) in enumerate(MARK):
        k = ks[i]
        if k <= 0.01: continue
        cx = W / 4 + (i % 2) * W / 2; y = top + (i // 2) * 70
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        t = solid_text(lab, sans(31, 600), INK); tw = ink_size(t)[0]
        x0 = cx - (tw + 56) / 2
        m = Image.new('L', img.size, 0); ImageDraw.Draw(m).ellipse([x0, y + 2, x0 + 40, y + 42], fill=255); lay.alpha_composite(gold_fill(m))
        paste(lay, solid_text(str(n), sans(24, 700), (255, 253, 248)), x0 + 20, y + 10, anchor='center')
        paste(lay, t, x0 + 56, y + 6)
        a = lay.getchannel('A').point(lambda v: int(v * k)); lay.putalpha(a)
        img.alpha_composite(lay)


def title(img, x, y, color=(255, 253, 248)):
    s = white_text('Detalhes', script_font(130)); paste(img, s, x, y)
    paste(img, white_text('QUE FAZEM O LOOK', caps_font(30, 600), 6), x + 14, y + ink_size(s)[1] + 6)


def feed():
    W, H, PH, Y0 = 1080, 1350, 1110, 50
    im = Image.new('RGBA', (W, H), IV + (255,))
    im.paste(SRC.crop((3, Y0, 3 + W, Y0 + PH)), (0, 0))
    title(im, 46, 40)
    for n, (x, y), _ in MARK: dot(im, n, x - 3, y - Y0)
    legend(im, PH + 34)
    paste(im, solid_text('QUAL É O SEU FAVORITO? COMENTA O NÚMERO', caps_font(22, 600), BR, 3), W / 2, H - 50, anchor='center')
    return im


# ---------------- story video ----------------
W, H, FPS, DUR = 1080, 1920, 30, 9.0
PY = (H - SRC.height) // 2
IVa = np.array(IV, np.float32)


def story_plate():
    iw, ih = SRC.size
    crisp = np.asarray(SRC.crop((3, 0, 3 + W, ih)), np.float32)
    k = H / ih; bg = SRC.resize((int(iw * k), H), Image.BICUBIC)
    bg = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(40))
    fb = np.asarray(bg, np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    m = np.clip((yy - PY) / 140, 0, 1) * np.clip((PY + ih - yy) / 140, 0, 1); m = m * m * (3 - 2 * m)
    full = fb.copy(); full[PY:PY + ih] = crisp
    f = fb * (1 - m) + full * m
    # soft ivory veil only on the bottom band for the legend
    v = np.clip((yy - 1560) / 160, 0, 1); v = v * v * (3 - 2 * v) * 0.9
    return f * (1 - v) + IVa * v


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


PLATE = story_plate()


def story_frame(t):
    z = 1.0 + 0.03 * t / DUR
    base = Image.fromarray(np.clip(PLATE, 0, 255).astype(np.uint8))
    if z > 1:
        cw, ch = W / z, H / z; base = base.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.BICUBIC)
    im = base.convert('RGBA')
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); title(lay, 56, 280)
    a = lay.getchannel('A').point(lambda v: int(v * ease(t / 0.6))); lay.putalpha(a); im.alpha_composite(lay)
    ks = [ease((t - (1.0 + 1.2 * i)) / 0.45) for i in range(4)]
    for (n, (x, y), _), k in zip(MARK, ks):
        cx = W / 2 + (x - 3 - W / 2) * z; cy = H / 2 + (y + PY - H / 2) * z
        dot(im, n, cx, cy, k)
    legend(im, 1650, ks)
    kc = ease((t - 6.2) / 0.5)
    if kc > 0.01:
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        paste(c, solid_text('QUAL É O SEU FAVORITO? RESPONDE AQUI', caps_font(24, 600), BR, 3), W / 2, 1810, anchor='center')
        c.putalpha(c.getchannel('A').point(lambda v: int(v * kc))); im.alpha_composite(c)
    return np.asarray(im.convert('RGB'))


if __name__ == '__main__':
    feed().convert('RGB').save(D + 'detalhes-feed.jpg', quality=95, subsampling=0)
    Image.fromarray(story_frame(8.5)).save(D + 'detalhes-story.jpg', quality=95, subsampling=0)
    if 'video' in sys.argv:
        enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + 'detalhes-story.mp4'], stdin=subprocess.PIPE)
        for n in range(int(DUR * FPS)): enc.stdin.write(story_frame(n / FPS).tobytes())
        enc.stdin.close(); enc.wait()
    print('ok')
