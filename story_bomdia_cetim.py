import sys, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, '.')
from shimmer_style import *
SRC, OUT = sys.argv[1], sys.argv[2]; PREV = sys.argv[3:]
ph = np.asarray(Image.open(SRC).convert('RGB'), np.float32)   # native pixels, no resize
ih, iw = ph.shape[:2]
W = iw; H = round(W * 16 / 9) // 2 * 2
TOP = H - ih - 70                                                # photo sits low, light band on top for the text
IV = np.array([241, 237, 229], np.float32)
BG = np.empty((H, W, 3), np.float32); BG[:] = IV
BG[TOP:TOP + ih] = ph
# soft blend of the photo edges into the ivory band (no hard line), far from the ring
y = np.arange(H, dtype=np.float32)[:, None, None]
a_top = np.clip((y - TOP) / 230, 0, 1) ** 1.2
a_bot = np.clip((TOP + ih - y) / 70, 0, 1)
A = np.minimum(a_top, a_bot)
BG = IV + (BG - IV) * A
INK = (74, 59, 46)
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
LAY = []
a = L(); paste(a, solid_text('BOM DIA,', caps_font(52, 500), INK, 6), W / 2, 150, anchor='center'); LAY.append((a, 0.3))
a = L(); paste(a, gold_text('boa semana', script_font(170)), W / 2, 225, anchor='center'); LAY.append((a, 0.8))
a = L(); paste(a, solid_text('QUE ELA SEJA LEVE E CHEIA DE BRILHO', caps_font(25, 600), (132, 101, 46), 4), W / 2, 440, anchor='center'); LAY.append((a, 1.6))
LA = [(np.asarray(l, np.float32), t) for l, t in LAY]
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def frame(t):
    f = BG.copy()
    for arr, t0 in LA:
        k = ease((t - t0) / 0.9)
        if k <= 0: continue
        lay = np.roll(arr, int(round((1 - k) * 16)), axis=0); al = lay[..., 3:4] / 255 * k
        f = f * (1 - al) + lay[..., :3] * al
    return np.clip(f, 0, 255).astype(np.uint8)
if PREV:
    for t in map(float, PREV): Image.fromarray(frame(t)).save(f'bd_{t}.jpg', quality=92)
    print(W, H, TOP); sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', OUT], stdin=subprocess.PIPE)
for n in range(240): enc.stdin.write(frame(n / 30).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
