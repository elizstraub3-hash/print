import sys, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, '.')
from shimmer_style import *
OUT = sys.argv[1]; PREV = sys.argv[2:]
src = Image.open('/home/user/shimmer-joias-/images/SH-1061.jpg').convert('RGB')
iw, ih = src.size
W, H = 716, 1272
BG = np.asarray(crop_native(src, W, H, oy=0, ox=(iw - W) // 2), np.float32)  # native pixels, no resize
INK = (74, 59, 46)
IV = np.array([250, 248, 244], np.float32)
yy = np.arange(H, dtype=np.float32)[:, None]; xx = np.arange(W, dtype=np.float32)[None, :]
top = np.clip(1 - yy / (H * 0.215), 0, 1) ** 0.9 * 0.88                       # approved light fade, above the ring head
d = np.sqrt(((xx - 150) / 330) ** 2 + ((yy - 1030) / 230) ** 2)              # soft patch behind the price block only
blob = np.clip(1 - d, 0, 1) ** 1.4 * 0.78
A = np.maximum(top, blob)[..., None]
BG = BG * (1 - A) + IV * A
DUR, FPS = 10.0, 30

def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
L = []  # (layer, t_in, slide_px)
a = layer(); paste(a, solid_text('O MAIS DESEJADO DA SHIMMER', caps_font(19, 600), (132, 101, 46), 3), W / 2, 48, anchor='center'); L.append((a, 0.3, 14))
a = layer()
caps = solid_text('SOLITÁRIO', caps_font(36, 500), INK, 2); scr = gold_text('Serena', script_font(132))
cw, ch = ink_size(caps); sw, sh = ink_size(scr); left = W / 2 - sw / 2
paste(a, caps, left + sw * 0.07, 98); paste(a, scr, left, 98 + ch + 4)
print('header bottom', 98 + ch + 4 + sh)
L.append((a, 0.7, 20))
X = 40
a = layer(); y = 905
for t in ['PEDRA CENTRAL 5 MM', '12 MOISSANITES LATERAIS', 'OURO 18K']:
    lay = solid_text(t, caps_font(21, 600), (132, 101, 46), 2); paste(a, lay, X, y); y += ink_size(lay)[1] + 13
L.append((a, 2.0, 16))
a = layer(); yb = price_block(a, X, y + 26, 'R$ 1.799,10', 'ou 10x de R$ 199,90 sem juros', size=50)
print('price bottom', yb)
L.append((a, 3.4, 16))
a = layer(); paste(a, solid_text('GARANTIA VITALÍCIA', caps_font(18, 700), INK, 3), X, yb + 26)
L.append((a, 5.0, 12))
LA = [(np.asarray(l, np.float32), t, s) for l, t, s in L]

def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def frame(t):
    f = BG.copy()
    for arr, t0, s in LA:
        k = ease((t - t0) / 0.8)
        if k <= 0: continue
        dy = int(round((1 - k) * s))
        lay = np.roll(arr, dy, axis=0)
        al = lay[..., 3:4] / 255 * k
        f = f * (1 - al) + lay[..., :3] * al
    return f.astype(np.uint8)

if PREV:
    for t in map(float, PREV): Image.fromarray(frame(t)).save(f'ss_{t}.jpg', quality=92)
    sys.exit()
enc = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
    '-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-shortest','-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p',
    '-profile:v','high','-movflags','+faststart','-c:a','aac','-b:a','128k',OUT], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
