"""Anel com a data especial (01·12·07): post de feed 4:5 no padrão Shimmer + Story 'como se a Eliz tivesse postado agora'.
Fotos do Drive (IMG_7272/7273, iPhone 3024x4032) só recortadas e reduzidas."""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/data-especial/'
INK = (58, 45, 34); BR = (118, 88, 38)


def C(im, lay, y, W): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]
def sh(lay_bb, blur=6, alpha=0.25):
    lay, bb = lay_bb; a = lay.getchannel('A'); s = Image.new('RGBA', lay.size, (70, 50, 20, 0)); s.putalpha(a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha)))
    o = Image.new('RGBA', lay.size, (0, 0, 0, 0)); o.alpha_composite(s, (0, 3)); o.alpha_composite(lay); return o, bb


# ---------- FEED 1080x1350 (IMG_7272: caixa + sacola verde da Shimmer ao fundo) ----------
ph = Image.open(D + 'fotos/IMG_7272.jpg').convert('RGB')          # 3024x4032
ch = int(3024 * 1350 / 1080)                                       # 3780
feed = ph.crop((0, 4032 - ch - 40, 3024, 4032 - 40)).resize((1080, 1350), Image.LANCZOS).convert('RGBA')
# véu claro só no topo (onde fica o texto; o anel está a partir de y~780)
W, H = feed.size
yy = np.arange(H, dtype=np.float32)[:, None]
veil = np.clip(1 - yy / 620, 0, 1) ** 1.2 * 0.80
vl = Image.new('RGBA', (W, H), (250, 246, 239, 0)); vl.putalpha(Image.fromarray((np.repeat(veil, W, 1) * 255).astype(np.uint8))); feed.alpha_composite(vl)
y = 92
y = C(feed, solid_text('A DATA QUE MUDOU TUDO', caps_font(40, 600), INK, 6), y, W)
y = C(feed, sh(gold_text('para sempre', script_font(168))), y + 4, W)
y = C(feed, solid_text('NO SEU DEDO', caps_font(40, 600), INK, 6), y + 6, W)
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 50, y + 26), (W / 2 + 50, y + 26)], fill=255, width=3); feed.alpha_composite(gold_fill(m))
y = C(feed, solid_text('PERSONALIZADO COM A SUA DATA · OURO 18K', caps_font(30, 700), BR, 4), y + 50, W)
print('feed texto termina em y', y)
feed.convert('RGB').save(D + 'feed-anel-data-especial.jpg', quality=100, subsampling=0)

# ---------- STORY nativo 1080x1920 (IMG_7273) ----------
W, H = 1080, 1920
ph2 = Image.open(D + 'fotos/IMG_7273.jpg').convert('RGB')         # 3:4 -> 9:16: recorta laterais
cw = int(4032 * 9 / 16)                                           # 2268
base = ph2.crop(((3024 - cw) // 2, 0, (3024 - cw) // 2 + cw, 4032)).resize((W, H), Image.LANCZOS)


def bubble(lines, em=None, size=52):
    fnt = sans(size, 700); lh = int(size * 1.28); px, py = 28, 16
    e = emoji(em, int(size * 1.05)) if em else None
    ws = [fnt.getlength(l) + ((e.width + 12) if (e and i == len(lines) - 1) else 0) for i, l in enumerate(lines)]
    out = Image.new('RGBA', (W, len(lines) * lh + py + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(out)
    for i, w in enumerate(ws):
        x = (W - w) / 2; d.rounded_rectangle([x - px, i * lh, x + w + px, i * lh + lh + py], 22, fill=(255, 255, 255, 255))
    for i, (l, w) in enumerate(zip(lines, ws)):
        x = (W - w) / 2; d.text((x, i * lh + py / 2 + 4), l, font=fnt, fill=(18, 18, 18))
        if e and i == len(lines) - 1: out.alpha_composite(e, (int(x + fnt.getlength(l) + 12), int(i * lh + py / 2 + 4)))
    return out


LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')
LOGO = LOGO.resize((300, round(LOGO.height * 300 / LOGO.width)), Image.LANCZOS)
PILL = Image.new('RGBA', (LOGO.width + 56, LOGO.height + 36), (0, 0, 0, 0))
ImageDraw.Draw(PILL).rounded_rectangle([0, 0, PILL.width - 1, PILL.height - 1], 22, fill=(255, 255, 255, 230)); PILL.alpha_composite(LOGO, (28, 18))
TX = [(0.3, bubble(['Ficou pronto hoje e eu', 'precisava mostrar'], '😍'), 300),
      (1.6, bubble(['Anel com a data mais', 'especial dela'], '🤍'), 470),
      (3.2, bubble(['Quer o seu com a sua data?', 'Chama no direct'], '📩', size=46), 1560)]
DUR, FPS = 8.0, 30


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def sframe(t):
    z = 1.0 + 0.04 * t / DUR; cw_, ch_ = W / z, H / z
    f = base.crop(((W - cw_) / 2, (H - ch_) * 0.55, (W + cw_) / 2, (H - ch_) * 0.55 + ch_)).resize((W, H), Image.LANCZOS).convert('RGBA') if z > 1.0005 else base.convert('RGBA')
    f.alpha_composite(PILL, ((W - PILL.width) // 2, 140))
    for t0, L_, y in TX:
        k = ease((t - t0) / 0.35)
        if k <= 0: continue
        s = 0.85 + 0.15 * k; Ls = L_.resize((int(L_.width * s), int(L_.height * s)), Image.LANCZOS)
        tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.paste(Ls, ((W - Ls.width) // 2, int(y + (L_.height - Ls.height) / 2)), Ls)
        if k < 1: tmp.putalpha(tmp.getchannel('A').point(lambda v: int(v * k)))
        f.alpha_composite(tmp)
    return np.asarray(f.convert('RGB'))


Image.fromarray(sframe(DUR - 0.1)).save(D + 'story-anel-data-especial.jpg', quality=100, subsampling=0)
if '--prev' in sys.argv: sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + 'story-anel-data-especial.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(sframe(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
