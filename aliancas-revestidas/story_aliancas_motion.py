import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '.')
from shimmer_style import *
D = '/home/user/print/aliancas-revestidas/'
W, H, FPS = 1080, 1920, 30
INK = (74, 59, 46); BR = (132, 101, 46); IV = np.array([246, 242, 235], np.float32)
PY = 240
yy = np.arange(H, dtype=np.float32)[:, None, None]
TOPF = np.clip(1 - (yy - 0) / 640, 0, 1) ** 1.3 * 0.82          # light fade behind the top text
def plate(n):
    src = Image.open(D + f'fotos/{n}.webp').convert('RGB')
    crisp = np.asarray(src.crop((3, 4, 1083, 1444)), np.float32)              # native pixels
    bg = src.resize((1440, 1920), Image.BICUBIC).crop((180, 0, 1260, 1920)).filter(ImageFilter.GaussianBlur(40))   # soft filler for the edges only
    f = np.asarray(bg, np.float32) * 0.92 + IV * 0.08
    m = np.clip((yy - PY) / 40, 0, 1) * np.clip((PY + 1440 - yy) / 40, 0, 1)
    full = np.empty((H, W, 3), np.float32); full[:] = f; full[PY:PY + 1440] = crisp
    f = f * (1 - m) + full * m
    return f + (IV - f) * TOPF
def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def head(caps, script, y=300, size=190):
    a = L(); c = solid_text(caps, caps_font(46, 500), INK, 5); s = gold_text(script, script_font(size))
    sw = ink_size(s)[0]; left = W / 2 - sw / 2
    paste(a, c, left + sw * 0.06, y); paste(a, s, left, y + ink_size(c)[1] + 4); return a
def line(text, y, size=26, color=BR, tr=3):
    a = L(); paste(a, solid_text(text, caps_font(size, 600), color, tr), W / 2, y, anchor='center'); return a
def pill(text, y):
    a = L(); t = solid_text(text, sans(34, 600), PRICE_COLOR); tw, th = ink_size(t)
    x0, x1 = W / 2 - tw / 2 - 40, W / 2 + tw / 2 + 40; y1 = y + th + 44
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([x0, y, x1, y1], radius=(y1 - y) // 2, fill=255)
    card = Image.new('RGBA', (W, H), (255, 253, 249, 0)); card.putalpha(m.point(lambda v: int(v * 0.96))); a.alpha_composite(card)
    fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle([x0, y, x1, y1], radius=(y1 - y) // 2, outline=255, width=3); a.alpha_composite(gold_fill(fr))
    paste(a, t, W / 2, y + 22, anchor='center'); return a
def price_card(y0):
    b = L(); x0, x1, y1 = 140, 940, y0 + 345
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], radius=26, fill=255)
    card = Image.new('RGBA', (W, H), (255, 253, 249, 0)); card.putalpha(m.point(lambda v: int(v * 0.97))); b.alpha_composite(card)
    fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle([x0, y0, x1, y1], radius=26, outline=255, width=3); b.alpha_composite(gold_fill(fr))
    lab = solid_text('À VISTA NO PIX', sans(28, 700), LABEL_COLOR, 3); paste(b, lab, W / 2, y0 + 34, anchor='center')
    pr = solid_text('R$ 2.250', sans(124, 600), PRICE_COLOR); paste(b, pr, W / 2, y0 + 34 + ink_size(lab)[1] + 22, anchor='center')
    yp = y0 + 34 + ink_size(lab)[1] + 22 + ink_size(pr)[1] + 26
    pc = solid_text('ou 10x de R$ 250,00 sem juros', sans(36, 500), PARCEL_COLOR); paste(b, pc, W / 2, yp, anchor='center')
    yl = yp + ink_size(pc)[1] + 28
    m2 = Image.new('L', (W, H), 0); ImageDraw.Draw(m2).line([(W / 2 - 70, yl), (W / 2 + 70, yl)], fill=255, width=2); b.alpha_composite(gold_fill(m2))
    paste(b, solid_text('REVESTIDAS · 4 MM · GARANTIA VITALÍCIA', caps_font(21, 600), BR, 3), W / 2, yl + 20, anchor='center')
    return b
def end_plate():
    f = np.empty((H, W, 3), np.float32); f[:] = IV; return f
def end_layers():
    a = L(); paste(a, gold_text('Agende sua visita', script_font(118)), W / 2, 640, anchor='center')
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 90, 830), (W / 2 + 90, 830)], fill=255, width=4); a.alpha_composite(gold_fill(m))
    b = L(); paste(b, solid_text('ATENDIMENTO COM HORA MARCADA', caps_font(30, 600), INK, 4), W / 2, 880, anchor='center')
    paste(b, solid_text('pelo WhatsApp · link na bio', sans(34, 500), PARCEL_COLOR), W / 2, 945, anchor='center')
    c = L(); y = 1080
    for t in ['AL. DR. MURICY, 650 · 8º ANDAR', 'CENTRO · CURITIBA – PR']:
        lay = solid_text(t, caps_font(26, 600), BR, 4); paste(c, lay, W / 2, y, anchor='center'); y += ink_size(lay)[1] + 20
    d = L(); paste(d, solid_text('SHIMMER JOIAS', caps_font(34, 500), INK, 8), W / 2, 1300, anchor='center')
    return [(a, 0.2), (b, 0.6), (c, 1.0), (d, 1.4)]
# scenes: (start, end, plate, [(layer, t_in)])
SC = [
 (0.0, 3.4, plate(53), [(head('PAR DE', 'Alianças'), -1.0), (pill('R$ 2.250 no PIX ou 10x de R$ 250', 560), 0.9)]),
 (3.4, 6.2, plate(55), [(head('FEITAS SOB MEDIDA', 'para o casal', size=150), 0.35)]),
 (6.2, 9.0, plate(52), [(head('AQUI VOCÊ TEM', 'garantia vitalícia', size=140), 0.35)]),
 (9.0, 12.8, plate(54), [(price_card(1150), 0.45)]),
 (12.8, 16.0, end_plate(), end_layers()),
]
SCA = [(a, b, p, [(np.asarray(l, np.float32), t) for l, t in ls]) for a, b, p, ls in SC]
DUR = SC[-1][1]; TR = 0.45
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_io(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def scene_frame(i, lt):
    a, b, p, ls = SCA[i]; f = p.copy()
    for arr, t0 in ls:
        k = ease((lt - t0) / 0.7)
        if k <= 0: continue
        lay = np.roll(arr, int(round((1 - k) * 20)), axis=0); al = lay[..., 3:4] / 255 * k
        f = f * (1 - al) + lay[..., :3] * al
    return f
def frame(t):
    for i, (a, b, p, ls) in enumerate(SCA):
        if a <= t < b or (i == len(SCA) - 1 and t >= a): break
    f = scene_frame(i, t - a)
    if i > 0 and t - a < TR:                      # previous scene slides out to the left, the new one comes in from the right
        sft = int(round(ease_io((t - a) / TR) * W))
        prev = scene_frame(i - 1, t - SCA[i - 1][0])
        out = prev.copy()
        if sft > 0:
            out[:, :W - sft] = prev[:, sft:]
            out[:, W - sft:] = f[:, :sft]
        f = out
    return np.clip(f, 0, 255).astype(np.uint8)
if len(sys.argv) > 1 and sys.argv[1] == 'prev':
    for t in map(float, sys.argv[2:]): Image.fromarray(frame(t)).save(S + f'sam_{t}.jpg', quality=88)
    sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', D + 'story-aliancas-venda.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
