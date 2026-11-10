import sys, subprocess
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
from shimmer_style import _mask, _with_shadow
W, H, FPS = 720, 1280, 30
def wcaps(text, size, tr):
    m = _mask(text, caps_font(size, 500), tr); f = Image.new('RGBA', m.size, WHITE + (0,)); f.putalpha(m)
    return _with_shadow(f, m, (1, 2), size * 0.06, 0.6, (30, 24, 18))
yy = np.arange(H, dtype=np.float32)[:, None]
shade = np.clip((yy - H * 0.66) / (H * 0.34), 0, 1) ** 1.3 * 0.45      # soft shade only behind the lower text
def block(caps, script, y):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c = wcaps(caps, 28, 5); paste(lay, c, W / 2, y, anchor='center')
    paste(lay, gold_text(script, script_font(86)), W / 2, y + ink_size(c)[1] + 14, anchor='center')
    a = np.asarray(lay, np.float32); return a[..., :3], a[..., 3:4] / 255
TX = [(0.5, 4.1, block('BEM-VINDA À SHIMMER', 'sua joia começa aqui', 1030)),
      (21.0, 27.3, block('ATENDIMENTO PERSONALIZADO', 'no seu tempo', 1030))]
def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
src, out = sys.argv[1], sys.argv[2]; prev = sys.argv[3:]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = None if prev else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', out], stdin=subprocess.PIPE)
n = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    t = n / FPS; f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    for a, z, (rgb, al) in TX:
        k = min(ease((t - a) / 0.6), 1 - ease((t - (z - 0.5)) / 0.5)) if a <= t < z else 0
        if k > 0:
            f = f * (1 - shade[..., None] * k)
            f = f * (1 - al * k) + rgb * al * k
    f = np.clip(f, 0, 255).astype(np.uint8)
    if prev and any(abs(t - float(p)) < 0.017 for p in prev): Image.fromarray(f).save(S + f'lc_{t:.1f}.jpg', quality=88)
    elif enc: enc.stdin.write(f.tobytes())
    n += 1
if enc: enc.stdin.close(); enc.wait()
print('frames', n)
