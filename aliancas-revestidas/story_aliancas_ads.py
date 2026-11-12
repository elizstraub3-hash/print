import sys, subprocess
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
D = '/home/user/print/aliancas-revestidas/'
W, H = 1080, 1920
INK = (74, 59, 46); BR = (132, 101, 46); IV = np.array([246, 242, 235], np.float32)
src = Image.open(D + 'fotos/53.webp').convert('RGB')
ph = np.asarray(src.crop((3, 420, 1083, 1180)), np.float32)        # native pixels, 1080 x 860, no resize
PY = 470
BG = np.empty((H, W, 3), np.float32); BG[:] = IV; BG[PY:PY + ph.shape[0]] = ph
yy = np.arange(H, dtype=np.float32)[:, None, None]
A = np.clip((yy - PY) / 70, 0, 1) * np.clip((PY + ph.shape[0] - yy) / 70, 0, 1)
BG = IV + (BG - IV) * A
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
LAY = []
a = L(); c = solid_text('PAR DE', caps_font(46, 500), INK, 5); s = gold_text('Alianças', script_font(180))
sw = ink_size(s)[0]; left = W / 2 - sw / 2
paste(a, c, left + sw * 0.06, 272); paste(a, s, left, 272 + ink_size(c)[1] + 4); LAY.append((a, 0.2))
a = L(); y = 1252
sp = solid_text('REVESTIDAS · 4 MM DE LARGURA', caps_font(24, 600), BR, 3); paste(a, sp, W / 2, y, anchor='center'); LAY.append((a, 1.0))
b = L(); price_block(b, W / 2, y + ink_size(sp)[1] + 30, 'R$ 2.250', 'ou 10x de R$ 250,00 sem juros', size=74, anchor='center'); LAY.append((b, 1.6))
c2 = L(); paste(c2, solid_text('AGENDE SUA VISITA PELO WHATSAPP', sans(24, 700), LABEL_COLOR, 3), W / 2, 1500, anchor='center'); LAY.append((c2, 2.4))
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
Image.fromarray(frame(10)).save(D + 'story-aliancas-preco.jpg', quality=100, subsampling=0)
if len(sys.argv) > 1 and sys.argv[1] == 'video':
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p',
        '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', D + 'story-aliancas-preco.mp4'], stdin=subprocess.PIPE)
    for n in range(240): enc.stdin.write(frame(n / 30).tobytes())
    enc.stdin.close(); enc.wait()
# check with the ad-safe zones drawn on top
chk = Image.open(D + 'story-aliancas-preco.jpg').convert('RGBA'); o = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
d.rectangle([0, 0, W, int(H * 0.14)], fill=(255, 0, 0, 70)); d.rectangle([0, int(H * 0.80), W, H], fill=(255, 0, 0, 70))
chk.alpha_composite(o); chk.convert('RGB').resize((540, 960)).save(S + 'sta_chk.jpg', quality=88)
print('ok')
