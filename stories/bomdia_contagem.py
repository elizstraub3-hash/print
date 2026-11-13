import sys, subprocess, datetime
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
SRC = '/home/user/print/solitario-helena/fotos/59.webp'
OUT = '/home/user/print/stories/story-bom-dia-contagem-virada'
DAYS = (datetime.date(2026, 12, 31) - datetime.date(2026, 11, 13)).days
ph = np.asarray(Image.open(SRC).convert('RGB'), np.float32)         # native pixels
ih, iw = ph.shape[:2]; W = iw; H = round(W * 16 / 9) // 2 * 2; TOP = H - ih
IV = np.array([246, 242, 235], np.float32)
BG = np.empty((H, W, 3), np.float32); BG[:] = IV; BG[TOP:] = ph
yy = np.arange(H, dtype=np.float32)[:, None, None]
BG = IV + (BG - IV) * (np.clip((yy - TOP - 120) / 560, 0, 1) ** 1.6)       # long, light transition into the satin
INK = (74, 59, 46); BR = (132, 101, 46)
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
LAY = []
a = L(); paste(a, solid_text('BOM DIA,', caps_font(50, 500), INK, 6), W / 2, 150, anchor='center')
paste(a, gold_text('ótima sexta-feira', script_font(128)), W / 2, 215, anchor='center'); LAY.append((a, 0.2))
a = L(); m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 80, 450), (W / 2 + 80, 450)], fill=255, width=3); a.alpha_composite(gold_fill(m))
paste(a, solid_text('FALTAM', caps_font(34, 600), INK, 8), W / 2, 500, anchor='center'); LAY.append((a, 1.0))
a = L(); n = gold_text(str(DAYS), caps_font(250, 600), 6); paste(a, n, W / 2, 560, anchor='center')
paste(a, solid_text('DIAS', caps_font(44, 600), INK, 10), W / 2, 560 + ink_size(n)[1] + 26, anchor='center'); LAY.append((a, 1.5))
a = L(); s = gold_text('para pedir ela em casamento', script_font(84)); paste(a, s, W / 2, 850, anchor='center')
paste(a, solid_text('NA VIRADA DO ANO', caps_font(32, 600), INK, 6), W / 2, 850 + ink_size(s)[1] + 22, anchor='center'); LAY.append((a, 2.3))
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
    for k in range(270): enc.stdin.write(frame(k / 30).tobytes())
    enc.stdin.close(); enc.wait()
Image.open(OUT + '.jpg').resize((405, 720)).save(S + 'bdc_prev.jpg')
print('days', DAYS, 'TOP', TOP)
