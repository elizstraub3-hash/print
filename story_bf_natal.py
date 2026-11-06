import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '.')
from shimmer_style import *
OUT = sys.argv[1]; PREV = sys.argv[2:]
W, H, FPS, DUR = 1080, 1920, 30, 13.0
BLACK = np.array([14, 12, 10], np.float32)
CHAMP = (214, 186, 128); CREAM = (240, 232, 218); MUTED = (170, 158, 140)
SITE = '/home/user/shimmer-joias-/images/'
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
glow = np.clip(1 - np.sqrt(((xx - W / 2) / 900) ** 2 + ((yy - 380) / 700) ** 2), 0, 1) ** 2 * 18   # very soft warm light behind the title
BG = BLACK + glow[..., None] * np.array([1.0, 0.8, 0.5], np.float32)

def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
LAY = []

def gift():
    C = 1200; m = Image.new('L', (C, C), 0); d = ImageDraw.Draw(m); lw = 44
    d.rounded_rectangle([200, 520, 1000, 1080], radius=30, outline=255, width=lw)        # box
    d.rounded_rectangle([150, 400, 1050, 540], radius=30, outline=255, width=lw)         # lid
    d.line([(600, 400), (600, 1080)], fill=255, width=lw)                                # ribbon
    d.ellipse([330, 150, 600, 410], outline=255, width=lw)                               # bow loops
    d.ellipse([600, 150, 870, 410], outline=255, width=lw)
    m = m.crop((120, 120, 1080, 1100)).resize((150, 153), Image.LANCZOS)
    return gold_fill(m)
a = L(); g = gift(); a.alpha_composite(g, (W // 2 - g.width // 2, 95)); LAY.append((a, 0.2))
a = L(); paste(a, solid_text('BLACK FRIDAY', caps_font(92, 600), CREAM, 10), W / 2, 290, anchor='center'); LAY.append((a, 0.5))
a = L(); s = gold_text('de Natal', script_font(190)); paste(a, s, W / 2, 380, anchor='center'); LAY.append((a, 0.8))
a = L(); paste(a, solid_text('SOLITÁRIOS EM OURO 18K PARA PRESENTEAR', caps_font(27, 600), CHAMP, 4), W / 2, 590, anchor='center'); LAY.append((a, 1.2))

CARDS = [  # (file, focus x, focus y, name, pix, parcel)
 ('img7030.png', .45, .55, 'Maria', 'R$ 855', 'ou 10x de R$ 95,00'),
 (SITE + 'SH-1061.jpg', .5, .42, 'Serena', 'R$ 1.799,10', 'ou 10x de R$ 199,90'),
 (SITE + 'SH-1084.jpg', .5, .45, 'Céu da Noite', 'R$ 1.350', 'ou 10x de R$ 150,00'),
 (IMG + '18.webp', .5, .6, 'Ariel', 'R$ 1.440', 'ou 10x de R$ 160,00'),
]
CW, PHh = 450, 340
for i, (f, fx, fy, name, pix, parc) in enumerate(CARDS):
    src = Image.open(f).convert('RGB'); iw, ih = src.size
    cw = iw * 0.62; ch = cw * PHh / CW                    # crop region in source pixels, then downscale only
    x0 = min(max(iw * fx - cw / 2, 0), iw - cw); y0 = min(max(ih * fy - ch / 2, 0), ih - ch)
    ph = src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((CW, PHh), Image.LANCZOS)
    mk = Image.new('L', (CW, PHh), 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, CW - 1, PHh - 1], radius=22, fill=255)
    cx = 70 + (i % 2) * (CW + 40); cy = 650 + (i // 2) * 545
    a = L()
    fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle([cx - 2, cy - 2, cx + CW + 1, cy + PHh + 1], radius=24, fill=255)
    a.alpha_composite(gold_fill(fr))
    p = ph.convert('RGBA'); p.putalpha(mk); a.alpha_composite(p, (cx, cy))
    mid = cx + CW / 2
    paste(a, gold_text(name, script_font(72)), mid, cy + PHh + 12, anchor='center')
    paste(a, solid_text(pix + ' NO PIX', sans(31, 600), CHAMP), mid, cy + PHh + 92, anchor='center')
    paste(a, solid_text(parc, sans(22, 500), MUTED), mid, cy + PHh + 134, anchor='center')
    LAY.append((a, 1.8 + i * 0.45))
a = L()
paste(a, solid_text('GARANTIA VITALÍCIA · 10X SEM JUROS · 10% OFF NO PIX', caps_font(23, 600), CREAM, 3), W / 2, 1772, anchor='center')
paste(a, solid_text('Chame no direct e garanta o seu presente', sans(29, 500), CHAMP), W / 2, 1822, anchor='center')
LAY.append((a, 4.2))
LA = [(np.asarray(l, np.float32), t) for l, t in LAY]

def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def frame(t):
    f = BG.copy()
    for arr, t0 in LA:
        k = ease((t - t0) / 0.8)
        if k <= 0: continue
        lay = np.roll(arr, int(round((1 - k) * 18)), axis=0)
        al = lay[..., 3:4] / 255 * k
        f = f * (1 - al) + lay[..., :3] * al
    return np.clip(f, 0, 255).astype(np.uint8)

if PREV:
    for t in map(float, PREV): Image.fromarray(frame(t)).save(f'bfn_{t}.jpg', quality=92)
    sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', OUT], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
