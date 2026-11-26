"""Story de anúncio Black Friday (10 s + jpg) sobre Shimmer_Anel_09 do Drive (solitário no cetim).
Texto no fundo claro de cima, nunca encostando nas joias (anéis a partir de y~950). Zona segura de anúncio: 250..1440."""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *
D = '/home/user/print/trafego/story-bf/'
# foto editada do Drive ainda não usada em Story: Shimmer_Anel_09 (cetim, 1086x1448). Pixels nativos; o topo do 9:16
# é completado com uma cópia desfocada da própria foto (fundo), com a emenda suavizada.
ph = Image.open(D + 'pulseira-trevo.webp').convert('RGB').crop((6, 0, 1086, 1448))   # pulseira trevo (foto enviada pela Eliz)
W, H = 1080, 1920; k = W / 1080; FPS, DUR = 30, 10.0
OY = H - ph.height
bg = ph.resize((int(1080 * 1.4), int(1448 * 1.4)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(28)).crop((216, 0, 216 + 1080, 1920))
bga = np.asarray(bg, np.float32) * 0.9 + np.array([250, 247, 241], np.float32) * 0.1
full = bga.copy(); full[OY:] = np.asarray(ph, np.float32)
yy = np.arange(H, dtype=np.float32)[:, None, None]; mm = np.clip((yy - OY) / 200, 0, 1); mm = mm * mm * (3 - 2 * mm)
src = Image.fromarray((bga * (1 - mm) + full * mm).astype(np.uint8))
INK = (58, 45, 34); BR = (118, 88, 38)
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def C(im, lay, y): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]
def sh(lay_bb, blur=6, alpha=0.28):
    lay, bb = lay_bb; a = lay.getchannel('A'); s = Image.new('RGBA', lay.size, (70, 50, 20, 0)); s.putalpha(a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha)))
    o = Image.new('RGBA', lay.size, (0, 0, 0, 0)); o.alpha_composite(s, (0, 3)); o.alpha_composite(lay); return o, bb
layers = []
a = L(); y = C(a, solid_text('BLACK FRIDAY SHIMMER', caps_font(int(40 * k), 600), INK, int(7 * k)), int(235 * k)); layers.append((a, 0.3))
b = L(); y = C(b, sh(gold_text('Pulseira Trevo', script_font(int(180 * k)))), y + int(14 * k)); layers.append((b, 0.8))
c = L(); y = C(c, solid_text('OURO 18K · GARANTIA VITALÍCIA', caps_font(int(30 * k), 600), BR, int(5 * k)), y + int(30 * k)); layers.append((c, 1.5))
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 55 * k, y + 34 * k), (W / 2 + 55 * k, y + 34 * k)], fill=255, width=3); c.alpha_composite(gold_fill(m))
d = L(); y2 = C(d, solid_text('10% OFF À VISTA', sans(int(54 * k), 700), PRICE_COLOR), y + int(70 * k))
y2 = C(d, solid_text('ou até 10x sem juros', sans(int(36 * k), 500), PARCEL_COLOR), y2 + int(14 * k)); layers.append((d, 2.4))
e = L(); t = solid_text('CHAME NO WHATSAPP', caps_font(int(34 * k), 700), BR, int(5 * k)); w, h = ink_size(t)
box = [W / 2 - w / 2 - 50 * k, y2 + 40 * k, W / 2 + w / 2 + 50 * k, y2 + 40 * k + h + 46 * k]
mk = Image.new('L', (W, H), 0); ImageDraw.Draw(mk).rounded_rectangle(box, radius=int((h + 46 * k) / 2), fill=255)
pl = Image.new('RGBA', (W, H), (255, 253, 249, 0)); pl.putalpha(mk.point(lambda v: int(v * 0.96))); e.alpha_composite(pl)
fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle(box, radius=int((h + 46 * k) / 2), outline=255, width=3); e.alpha_composite(gold_fill(fr))
paste(e, t, W / 2, y2 + 40 * k + 23 * k, anchor='center'); layers.append((e, 3.2))
print('cta bottom', box[3])
base = np.asarray(src, np.float32); LA = [(np.asarray(l, np.float32), t0) for l, t0 in layers]
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def frame(t):
    z = 1.0 + 0.05 * t / DUR; cw, ch = W / z, H / z
    f = np.asarray(src.crop(((W - cw) / 2, H - ch, (W + cw) / 2, H)).resize((W, H), Image.LANCZOS), np.float32) if z > 1.0005 else base.copy()
    for arr, t0 in LA:
        kk = ease((t - t0) / 0.7)
        if kk <= 0: continue
        a_ = np.roll(arr, int(round((1 - kk) * 20)), axis=0); al = a_[..., 3:4] / 255 * kk; f = f * (1 - al) + a_[..., :3] * al
    return np.clip(f, 0, 255).astype(np.uint8)
Image.fromarray(frame(DUR - 0.1)).save(D + 'story-anuncio-bf-pulseira-trevo.jpg', quality=100, subsampling=0)
if '--prev' in sys.argv: sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + 'story-anuncio-bf-pulseira-trevo.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
