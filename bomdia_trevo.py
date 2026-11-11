import sys, subprocess
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
W, H, FPS = 720, 1280, 30
INK = (74, 59, 46); BR = (132, 101, 46)
yy = np.arange(H, dtype=np.float32)[:, None]
fade = (np.clip(1 - yy / (H * 0.30), 0, 1) ** 1.3 * 0.82)[..., None]       # light fade at the top only
IV = np.array([246, 243, 238], np.float32)
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
LAY = []
a = L(); paste(a, solid_text('BOM DIA,', caps_font(36, 500), INK, 6), W / 2, 80, anchor='center'); LAY.append((a, 0.3))
a = L(); paste(a, gold_text('e muita sorte hoje', script_font(84)), W / 2, 130, anchor='center'); LAY.append((a, 0.8))
a = L(); paste(a, solid_text('QUE O SEU DIA SEJA DE BOAS ESCOLHAS', caps_font(19, 600), BR, 3), W / 2, 262, anchor='center'); LAY.append((a, 1.5))
LA = [(np.asarray(l, np.float32), t) for l, t in LAY]
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
src, out = sys.argv[1], sys.argv[2]; prev = sys.argv[3:]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = None if prev else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '13', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', out], stdin=subprocess.PIPE)
n = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    t = n / FPS; f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    f = f + (IV - f) * fade
    for arr, t0 in LA:
        k = ease((t - t0) / 0.9)
        if k > 0:
            lay = np.roll(arr, int(round((1 - k) * 14)), axis=0); al = lay[..., 3:4] / 255 * k
            f = f * (1 - al) + lay[..., :3] * al
    f = np.clip(f, 0, 255).astype(np.uint8)
    if prev and any(abs(t - float(p)) < 0.017 for p in prev): Image.fromarray(f).save(S + f'tv_{t:.1f}.jpg', quality=88)
    elif enc: enc.stdin.write(f.tobytes())
    n += 1
if enc: enc.stdin.close(); enc.wait()
print('frames', n)
