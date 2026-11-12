import sys, subprocess
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
from shimmer_style import _mask, _with_shadow
SRC = '/home/user/print/aliancas-revestidas/fotos/62.webp'
OUT = '/home/user/print/stories/story-vai-pedir-em-casamento'
ph = np.asarray(Image.open(SRC).convert('RGB'), np.float32)            # native pixels, no resize
ih, iw = ph.shape[:2]; W = iw; H = round(W * 16 / 9) // 2 * 2; TOP = H - ih
IV = np.array([246, 242, 235], np.float32)
BG = np.empty((H, W, 3), np.float32); BG[:] = IV; BG[TOP:] = ph
yy = np.arange(H, dtype=np.float32)[:, None, None]
BG = IV + (BG - IV) * (np.clip((yy - TOP) / 220, 0, 1) ** 1.2)       # soft top transition only
INK = (74, 59, 46); BR = (132, 101, 46)
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def wcaps(text, size, tr):
    m = _mask(text, caps_font(size, 600), tr); f = Image.new('RGBA', m.size, WHITE + (0,)); f.putalpha(m)
    return _with_shadow(f, m, (1, 2), size * 0.08, 0.7, (10, 15, 40))
LAY = []
a = L(); paste(a, solid_text('VAI PEDIR ELA', caps_font(54, 500), INK, 6), W / 2, 205, anchor='center'); LAY.append((a, 0.2))
a = L(); paste(a, gold_text('em casamento?', script_font(160)), W / 2, 285, anchor='center'); LAY.append((a, 0.7))
a = L(); y = 500
for t in ['A GENTE TE AJUDA A ESCOLHER', 'O SOLITÁRIO E AS ALIANÇAS']:
    lay = solid_text(t, caps_font(26, 600), BR, 4); paste(a, lay, W / 2, y, anchor='center'); y += ink_size(lay)[1] + 16
LAY.append((a, 1.4))
a = L()
t1 = solid_text('ATENDIMENTO COM HORA MARCADA', caps_font(26, 600), INK, 4); t2 = solid_text('Agende pelo WhatsApp · link na bio', sans(28, 500), PARCEL_COLOR)
bw = max(ink_size(t1)[0], ink_size(t2)[0]) + 90; y0 = 1585; bh = ink_size(t1)[1] + ink_size(t2)[1] + 70
x0 = (W - bw) / 2
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=24, fill=255)
card = Image.new('RGBA', (W, H), (255, 253, 249, 0)); card.putalpha(m.point(lambda v: int(v * 0.96))); a.alpha_composite(card)
fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=24, outline=255, width=3); a.alpha_composite(gold_fill(fr))
paste(a, t1, W / 2, y0 + 26, anchor='center'); paste(a, t2, W / 2, y0 + 26 + ink_size(t1)[1] + 18, anchor='center')
LAY.append((a, 2.2))
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
Image.fromarray(frame(9)).save(OUT + '.jpg', quality=100, subsampling=0)
if len(sys.argv) > 1:
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '13', '-pix_fmt', 'yuv420p',
        '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', OUT + '.mp4'], stdin=subprocess.PIPE)
    for n in range(270): enc.stdin.write(frame(n / 30).tobytes())
    enc.stdin.close(); enc.wait()
Image.open(OUT + '.jpg').resize((405, 720)).save(S + 'ped_prev.jpg')
print('ok', W, H, TOP)
