import sys, subprocess
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
D = '/home/user/print/solitario-helena/'
W, H = 1080, 1920
INK = (74, 59, 46); BR = (132, 101, 46); IV = np.array([246, 242, 235], np.float32)
src = Image.open(D + 'fotos/58.webp').convert('RGB')
ph = np.asarray(src.crop((3, 420, 1083, 1220)), np.float32)        # native pixels, 1080 x 800, no resize
PY = 505
BG = np.empty((H, W, 3), np.float32); BG[:] = IV; BG[PY:PY + ph.shape[0]] = ph
yy = np.arange(H, dtype=np.float32)[:, None, None]
A = np.clip((yy - PY) / 60, 0, 1) * np.clip((PY + ph.shape[0] - yy) / 60, 0, 1)
BG = IV + (BG - IV) * A
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
LAY = []
a = L(); c = solid_text('ANEL SOLITÁRIO', caps_font(44, 500), INK, 5); s = gold_text('Helena', script_font(205))
sw = ink_size(s)[0]; left = W / 2 - sw / 2
paste(a, c, left + sw * 0.06, 255); paste(a, s, left, 255 + ink_size(c)[1] + 4); LAY.append((a, 0.2))
a = L(); sp = solid_text('OURO 18K · 7,5 MM · 4,35 G · GARANTIA VITALÍCIA', caps_font(24, 600), BR, 3); paste(a, sp, W / 2, 1335, anchor='center'); LAY.append((a, 0.9))
# price card: white card, thin gold frame, price large and centred
b = L(); x0, y0, x1, y1 = 150, 1395, 930, 1665
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], radius=26, fill=255)
card = Image.new('RGBA', (W, H), (255, 253, 249, 0)); card.putalpha(m.point(lambda v: int(v * 0.97))); b.alpha_composite(card)
fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle([x0, y0, x1, y1], radius=26, outline=255, width=3); b.alpha_composite(gold_fill(fr))
lab = solid_text('À VISTA NO PIX', sans(28, 700), LABEL_COLOR, 3); paste(b, lab, W / 2, y0 + 34, anchor='center')
pr = solid_text('R$ 4.050', sans(124, 600), PRICE_COLOR); paste(b, pr, W / 2, y0 + 34 + ink_size(lab)[1] + 22, anchor='center')
pc = solid_text('ou 10x de R$ 450,00 sem juros', sans(36, 500), PARCEL_COLOR); paste(b, pc, W / 2, y0 + 34 + ink_size(lab)[1] + 22 + ink_size(pr)[1] + 26, anchor='center')
LAY.append((b, 1.5))
LA = [(np.asarray(l, np.float32), t) for l, t in LAY]
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def frame(t):
    f = BG.copy()
    for arr, t0 in LA:
        k = ease((t - t0) / 0.8)
        if k <= 0: continue
        lay = np.roll(arr, int(round((1 - k) * 18)), axis=0); al = lay[..., 3:4] / 255 * k
        f = f * (1 - al) + lay[..., :3] * al
    return np.clip(f, 0, 255).astype(np.uint8)
Image.fromarray(frame(10)).save(D + 'story-helena-preco.jpg', quality=100, subsampling=0)
if len(sys.argv) > 1 and sys.argv[1] == 'video':
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p',
        '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', D + 'story-helena-preco.mp4'], stdin=subprocess.PIPE)
    for n in range(240): enc.stdin.write(frame(n / 30).tobytes())
    enc.stdin.close(); enc.wait()
# check with the ad-safe zones drawn on top
chk = Image.open(D + 'story-helena-preco.jpg').convert('RGBA'); o = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
d.rectangle([0, 0, W, int(H * 0.14)], fill=(255, 0, 0, 70)); d.rectangle([0, int(H * 0.80), W, H], fill=(255, 0, 0, 70))
chk.alpha_composite(o); chk.convert('RGB').resize((540, 960)).save(S + 'sta_chk.jpg', quality=88)
print('ok')
