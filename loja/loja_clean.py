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
shade = np.clip((yy - H * 0.60) / (H * 0.30), 0, 1) ** 1.1 * 0.62      # soft shade only behind the lower text
from story_nativo_lib import emoji
def arr(lay):
    a = np.asarray(lay, np.float32); return a[..., :3], a[..., 3:4] / 255
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def caps_lines(lay, rows, y, size, tr=5):
    for r in rows:
        c = wcaps(r, size, tr); paste(lay, c, W / 2, y, anchor='center'); y += ink_size(c)[1] + int(size * 0.45)
    return y
q = L(); caps_lines(q, ['A SHIMMER SÓ', 'ATENDE ONLINE?'], 980, 46)
no = L(); g = gold_text('Não', script_font(170)); gw, gh = ink_size(g); e = emoji('👎', 96)
x0 = W / 2 - (gw + 24 + e.width) / 2; paste(no, g, x0, 990); no.alpha_composite(e, (int(x0 + gw + 24), int(990 + gh / 2 - e.height / 2 + 10)))
hm = L(); y = caps_lines(hm, ['ATENDEMOS COM', 'HORA MARCADA'], 930, 38)
caps_lines(hm, ['AL. DR. MURICY, 650 · 8º ANDAR', 'CENTRO · CURITIBA – PR'], y + 18, 23, 3)
jo = L(); y = caps_lines(jo, ['AS JOIAS MAIS LINDAS,'], 940, 32)
gt = gold_text('com o melhor preço', script_font(78)); paste(jo, gt, W / 2, y + 2, anchor='center')
caps_lines(jo, ['E GARANTIA VITALÍCIA'], y + ink_size(gt)[1] + 22, 32)
TX = [(0.15, 2.0, arr(q)), (2.0, 3.4, arr(no)), (3.4, 7.7, arr(hm)), (26.5, 33.2, arr(jo))]
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
        k = min(ease((t - a) / 0.35), 1 - ease((t - (z - 0.3)) / 0.3)) if a <= t < z else 0
        if k > 0:
            f = f * (1 - shade[..., None] * k)
            f = f * (1 - al * k) + rgb * al * k
    f = np.clip(f, 0, 255).astype(np.uint8)
    if prev and any(abs(t - float(p)) < 0.017 for p in prev): Image.fromarray(f).save(S + f'lc_{t:.1f}.jpg', quality=88)
    elif enc: enc.stdin.write(f.tobytes())
    n += 1
if enc: enc.stdin.close(); enc.wait()
print('frames', n)
