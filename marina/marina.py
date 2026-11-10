import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '.')
from shimmer_style import *
OUT = '/home/user/print/marina/'
SRC = Image.open(OUT + 'foto-original.jpg').convert('RGB')
iw, ih = SRC.size
INK = (74, 59, 46); BR = (132, 101, 46); IV = (244, 239, 231)
M = 64
MODE = sys.argv[1] if len(sys.argv) > 1 else 'all'

def title(img, caps, name, x, y, size=210, center=False):
    c = solid_text(caps, caps_font(40, 500), INK, 3); n = gold_text(name, script_font(size))
    cw, ch = ink_size(c); nw, nh = ink_size(n)
    if center:
        left = img.width / 2 - nw / 2; paste(img, c, left + nw * 0.06, y); paste(img, n, left, y + ch + 4)
    else:
        paste(img, c, x + 6, y); paste(img, n, x - 4, y + ch + 4)
    return y + ch + 4 + nh

def lines(img, rows, x, y, size, color, gap, font='caps', anchor='left', tracking=2):
    for r in rows:
        f = caps_font(size, 600 if size < 26 else 500) if font == 'caps' else sans(size, 500)
        lay = solid_text(r, f, color, tracking if font == 'caps' else 0)
        paste(img, lay, x, y, anchor=anchor); y += ink_size(lay)[1] + gap
    return y

# ---------- FEED 1: produto (4:5, native crop) ----------
if MODE in ('all', 'feed'):
    H = round(iw * 5 / 4)
    f1 = crop_native(SRC, iw, H, oy=45).convert('RGBA')
    title(f1, 'ANEL SOLITÁRIO', 'Marina', M, 70)
    bottom_fade(f1, 0.66)   # approved light fade, starts below the ring
    y = lines(f1, ['Profundo como o mar.', 'Feito para durar.'], M, 1000, 34, INK, 14, tracking=1)
    sp = solid_text('OURO 18K · GARANTIA VITALÍCIA', caps_font(18, 600), BR, 2); paste(f1, sp, M, y + 10); y += 10 + ink_size(sp)[1]
    pr = solid_text('Condições especiais', sans(44, 600), PRICE_COLOR); paste(f1, pr, M + 1, y + 26)
    y += 26 + ink_size(pr)[1] + 16
    paste(f1, solid_text('10x sem juros · 10% OFF no PIX', sans(22, 500), PARCEL_COLOR), M + 2, y)
    sw = solid_text('ARRASTE PARA O LADO  →', sans(17, 700), LABEL_COLOR, 2)
    paste(f1, sw, iw - M - ink_size(sw)[0], H - 70)
    save_hq(f1, OUT + '01-marina-produto.jpg')

    # ---------- FEED 2: significado ----------
    f2 = Image.new('RGBA', (iw, H), IV + (255,))
    b = title(f2, 'POR QUE SE CHAMA', 'Marina', M, 70)
    det = SRC.crop((510 - 260, 850 - 230, 510 + 260, 850 + 290))          # native-pixel detail of the ring, no resize
    mk = Image.new('L', det.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, det.width - 1, det.height - 1], radius=26, fill=255)
    fr = Image.new('L', (iw, H), 0); x0, y0 = (iw - det.width) // 2, int(b) + 40
    ImageDraw.Draw(fr).rounded_rectangle([x0 - 3, y0 - 3, x0 + det.width + 2, y0 + det.height + 2], radius=28, fill=255)
    f2.alpha_composite(gold_fill(fr)); d = det.convert('RGBA'); d.putalpha(mk); f2.alpha_composite(d, (x0, y0))
    y = y0 + det.height + 50
    y = lines(f2, ['Do latim marinus,', '“aquela que vem do mar”.'], iw / 2, y, 34, INK, 12, anchor='center', tracking=1)
    lines(f2, ['A PEDRA AZUL PROFUNDA É O OCEANO,', 'E AS PEDRAS AO REDOR, O BRILHO DAS ONDAS.'], iw / 2, y + 22, 19, BR, 14, anchor='center')
    save_hq(f2, OUT + '02-marina-significado.jpg')

# ---------- 9:16 canvas (Story and Reels): photo native at the bottom, ivory band on top ----------
W9 = iw; H9 = round(W9 * 16 / 9) // 2 * 2; TOP = H9 - ih
ph = np.asarray(SRC, np.float32); IVa = np.array(IV, np.float32)
BG9 = np.empty((H9, W9, 3), np.float32); BG9[:] = IVa; BG9[TOP:] = ph
yy = np.arange(H9, dtype=np.float32)[:, None, None]
A = np.clip((yy - TOP) / 230, 0, 1) ** 1.2
BG9 = IVa + (BG9 - IVa) * A
FB = np.clip((yy - H9 * 0.78) / (H9 * 0.22), 0, 1) ** 1.15 * 0.92          # light fade at the base, below the ring
BG9 = BG9 + (np.array([250, 248, 244], np.float32) - BG9) * FB
def L(): return Image.new('RGBA', (W9, H9), (0, 0, 0, 0))
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def comp(f, arr, k, dy=16):
    if k <= 0: return f
    lay = np.roll(arr, int(round((1 - k) * dy)), axis=0); al = lay[..., 3:4] / 255 * k
    return f * (1 - al) + lay[..., :3] * al
def encode(path, frames, n, fps=30):
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W9}x{H9}', '-r', str(fps), '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuv420p',
        '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', path], stdin=subprocess.PIPE)
    for i in range(n): enc.stdin.write(np.clip(frames(i / fps), 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()

# ---------- STORY: por que se chama Marina (10 s) ----------
if MODE in ('all', 'story', 'prev'):
    S1 = L(); b = title(S1, 'POR QUE SE CHAMA', 'Marina', 0, 90, 180, center=True)
    S2 = L(); lines(S2, ['DO LATIM MARINUS:', '“AQUELA QUE VEM DO MAR”'], W9 / 2, b + 30, 25, BR, 14, anchor='center', tracking=3)
    S3 = L(); lines(S3, ['A pedra azul profunda é o oceano,', 'e as pedras ao redor, o brilho das ondas.'], W9 / 2, TOP + ih - 330, 31, INK, 16, anchor='center', tracking=1)
    S4 = L(); lines(S4, ['OURO 18K · GARANTIA VITALÍCIA'], W9 / 2, TOP + ih - 200, 21, BR, 0, anchor='center', tracking=3)
    SL = [(np.asarray(x, np.float32), t) for x, t in ((S1, .3), (S2, 1.2), (S3, 2.6), (S4, 3.8))]
    def sframe(t):
        f = BG9.copy()
        for arr, t0 in SL: f = comp(f, arr, ease((t - t0) / .9))
        return f
    if MODE == 'prev':
        Image.fromarray(np.clip(sframe(9), 0, 255).astype(np.uint8)).save(S + 'mar_story.jpg', quality=90)
    else:
        encode(OUT + 'story-por-que-marina.mp4', sframe, 300)

# ---------- REELS motion (15 s) ----------
if MODE in ('all', 'reels', 'prev'):
    def wave_layer(y, amp, length, phase=0):
        m = Image.new('L', (W9 * 2, 60 * 2), 0); d = ImageDraw.Draw(m)
        pts = [(x * 2, (30 + amp * math.sin(x / length * 2 * math.pi + phase)) * 2) for x in range(0, W9 + 1, 4)]
        d.line(pts, fill=255, width=5, joint='curve')
        m = m.resize((W9, 60), Image.LANCZOS); g = gold_fill(m); lay = L(); lay.alpha_composite(g, (0, int(y - 30))); return lay
    WAVE = np.asarray(wave_layer(TOP - 40 + 60, 9, 260), np.float32)
    xx = np.arange(W9, dtype=np.float32)[None, :, None]
    R1 = L(); lines(R1, ['TEM ANÉIS QUE', 'LEMBRAM O MAR'], W9 / 2, 150, 46, INK, 22, anchor='center', tracking=4)
    R2 = L(); title(R2, 'ANEL SOLITÁRIO', 'Marina', 0, 90, 190, center=True)
    R3 = L(); lines(R3, ['DO LATIM MARINUS:', '“AQUELA QUE VEM DO MAR”'], W9 / 2, 360, 25, BR, 14, anchor='center', tracking=3)
    R4 = L(); lines(R4, ['O azul profundo do oceano,', 'com o brilho das ondas ao redor.'], W9 / 2, TOP + ih - 330, 31, INK, 16, anchor='center', tracking=1)
    R5 = L()
    y = lines(R5, ['OURO 18K · GARANTIA VITALÍCIA'], W9 / 2, TOP + ih - 360, 22, BR, 0, anchor='center', tracking=3)
    pr = solid_text('Condições especiais', sans(46, 600), PRICE_COLOR); paste(R5, pr, W9 / 2, y + 24, anchor='center')
    y += 24 + ink_size(pr)[1] + 16
    paste(R5, solid_text('10x sem juros · 10% OFF no PIX', sans(24, 500), PARCEL_COLOR), W9 / 2, y, anchor='center')
    paste(R5, solid_text('PEÇA PELO NOME: MARINA', sans(22, 700), LABEL_COLOR, 3), W9 / 2, y + 60, anchor='center')
    RA = {k: np.asarray(v, np.float32) for k, v in dict(R1=R1, R2=R2, R3=R3, R4=R4, R5=R5).items()}
    IVF = np.empty((H9, W9, 3), np.float32); IVF[:] = IVa
    def win(t, a, b, fi=.8, fo=.6):
        return min(ease((t - a) / fi), 1 - ease((t - (b - fo)) / fo)) if t < b else 0
    def rframe(t):
        # photo reveals from the bottom like a rising tide (mask wipe), never zoomed
        rev = ease((t - 0.9) / 1.6)
        edge = H9 - rev * (H9 - TOP + 250)
        m = np.clip((yy - edge) / 160, 0, 1)
        f = IVF + (BG9 - IVF) * m
        # gold wave drawn left to right along the top of the photo
        dw = ease((t - 2.0) / 1.4); wm = (xx <= dw * W9).astype(np.float32)
        f = comp(f, WAVE * np.concatenate([np.ones((1, 1, 3)), wm[..., :1]], axis=2) if False else WAVE * np.dstack([np.ones((H9, W9, 3)), np.broadcast_to(wm[..., 0], (H9, W9))]), 1, 0)
        f = comp(f, RA['R1'], win(t, 0.2, 3.4))
        f = comp(f, RA['R2'], win(t, 3.3, 15.5, fo=.01))
        f = comp(f, RA['R3'], win(t, 4.4, 15.5, fo=.01))
        f = comp(f, RA['R4'], win(t, 6.0, 10.4))
        f = comp(f, RA['R5'], win(t, 10.4, 15.5, fo=.01))
        return f
    if MODE == 'prev':
        for t in (1.5, 2.8, 7.5, 13):
            Image.fromarray(np.clip(rframe(t), 0, 255).astype(np.uint8)).save(S + f'mar_r_{t}.jpg', quality=88)
    else:
        encode(OUT + 'reels-marina-motion.mp4', rframe, 450)
print('ok')
