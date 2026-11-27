"""Reels 'Imagina uma data tão especial que vira joia' — anel 01·12·07 (vídeos IMG_7275/7278, 4K 60fps).
Recorte 9:16 que exclui a marca d'água do compressor (canto inferior direito), só reduz para 1080x1920.
Legendas no estilo preferido da Eliz: branco grosso com contorno preto. Fecho com pattern + logo original. Trilha suave."""
import sys, subprocess, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/data-especial/'
U = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/'
V1, V2 = U + '2d9b1531-img-7275_7rszqe1l.mp4', U + 'd2e47ddb-img-7278_befG0v0x.mp4'
W, H, FPS = 1080, 1920, 30
SLOW = 1.2
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
PREV = [float(x) for x in sys.argv[1:]]
# (arquivo, início, duração na fonte, legendas [(t_rel, linhas, emoji)])
CL = [
    (V1, 0.0, 7.4, [(0.2, ['Imagina uma data', 'tão especial...'], None), (4.4, ['...que ela merece', 'virar joia'], '💍')]),
    (V2, 1.0, 7.0, [(0.2, ['O dia em que', 'tudo mudou'], '🤍'), (4.4, ['agora no dedo,', 'todos os dias'], None)]),
    (V1, 9.0, 4.2, [(0.2, ['Qual data você', 'eternizaria?'], '✨')]),
]
END = 3.8


def outline(lines, size=68, y=320, em=None):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(out); fnt = sans(size, 800)
    for i, ln in enumerate(lines):
        w = fnt.getlength(ln); e = emoji(em, int(size * 1.05)) if (em and i == len(lines) - 1) else None
        ew = (e.width + 12) if e else 0; x = (W - w - ew) / 2
        d.text((x, y), ln, font=fnt, fill=(255, 255, 255, 255), stroke_width=max(4, size // 12), stroke_fill=(0, 0, 0, 255))
        if e: out.alpha_composite(e, (int(x + w + 12), int(y + size * 0.05)))
        y += int(size * 1.22)
    return np.asarray(out, np.float32)


# fecho: pattern + logo
P = Image.open('/home/user/print/assets/pattern-logo.jpg').convert('RGB')
sc = H / P.height; P = P.resize((round(P.width * sc), H), Image.LANCZOS); P = P.crop(((P.width - W) // 2, 0, (P.width - W) // 2 + W, H))
a = np.asarray(P, np.float32); yy = np.arange(H, dtype=np.float32)[:, None, None]; xx = np.arange(W, dtype=np.float32)[None, :, None]
g = np.exp(-(((xx - W / 2) / 520) ** 2 + ((yy - 860) / 480) ** 2)) * 0.8
E = Image.fromarray((a * (1 - g) + np.array(IV, np.float32) * g).astype(np.uint8)).convert('RGBA')
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA'); E.alpha_composite(LOGO, ((W - LOGO.width) // 2, 480))
y = 720
t = solid_text('SUA DATA.', caps_font(48, 600), INK, 8); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 16
t = gold_text('Sua joia.', script_font(180)); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 40
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 44
for txt, f, col, tr in [('PERSONALIZADO COM A SUA DATA · OURO 18K', caps_font(32, 600), INK, 4), ('CHAME NO DIRECT · LINK NA BIO', caps_font(34, 700), BR, 4),
                        ('atendimento na loja ou online', sans(32, 500), PARCEL_COLOR, 0)]:
    t = solid_text(txt, f, col, tr); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 24
ENDA = np.asarray(E.convert('RGB'), np.float32)


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def frames(f, s, d):
    # 2160x3840 -> recorte 2025x3600 (topo, centro), sem a marca d'água (y>3600), reduz p/ 1080x1920
    vf = f"trim=start={s}:duration={d},setpts=(PTS-STARTPTS)*{SLOW},fps={FPS},crop=2025:3600:67:0,scale={W}:{H}:flags=lanczos"
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', f, '-vf', vf, '-an', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


XF = 10
CAPS = [[(t0, outline(ln, em=em)) for t0, ln, em in c[3]] for c in CL]
enc = None if PREV else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-an', D + '_v.mp4'], stdin=subprocess.PIPE)
n_out = 0; prev_tail = None
for ci, (f, s, d, _) in enumerate(CL):
    fr = list(frames(f, s, d))
    caps = CAPS[ci]
    for j, x in enumerate(fr):
        t = j / FPS; tg = n_out / FPS
        img = x.astype(np.float32)
        if prev_tail is not None and j < XF:
            k = (j + 1) / (XF + 1); img = prev_tail * (1 - k) + img * k
        for i, (t0, cap) in enumerate(caps):
            t1 = caps[i + 1][0] if i + 1 < len(caps) else len(fr) / FPS
            if not (t0 <= t < t1): continue
            kk = ease((t - t0) / 0.35) * (1 - ease((t - (t1 - 0.25)) / 0.25))
            al = cap[..., 3:4] / 255 * kk; capr = np.roll(cap, int((1 - min(kk, 1)) * 18), axis=0)
            img = img * (1 - al) + capr[..., :3] * al
        o = np.clip(img, 0, 255).astype(np.uint8)
        if PREV:
            if any(abs(tg - p) < 0.5 / FPS for p in PREV): Image.fromarray(o).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/rd_{tg:05.2f}.jpg', quality=85)
        else: enc.stdin.write(o.tobytes())
        n_out += 1
    prev_tail = fr[-1].astype(np.float32)
for j in range(int(END * FPS)):
    k = ease(j / 14); o = np.clip(prev_tail * (1 - k) + ENDA * k, 0, 255).astype(np.uint8); tg = n_out / FPS
    if PREV:
        if any(abs(tg - p) < 0.5 / FPS for p in PREV): Image.fromarray(o).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/rd_{tg:05.2f}.jpg', quality=85)
    else: enc.stdin.write(o.tobytes())
    n_out += 1
TOTAL = n_out / FPS
if PREV: print('prev ok', TOTAL); sys.exit()
enc.stdin.close(); enc.wait()

# trilha suave (pad + sininhos), discreta
SR = 44100; Ls = int(TOTAL * SR); tt = np.arange(Ls) / SR
pad = np.zeros(Ls)
for fr_, a_ in [(220.0, .5), (277.18, .35), (329.63, .35), (415.3, .18)]:
    pad += a_ * np.sin(2 * np.pi * fr_ * tt) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.07 * tt + fr_))
pad *= 0.05 * np.minimum(1, tt / 2) * np.minimum(1, (TOTAL - tt) / 2)
fx = np.zeros(Ls)
def chime(f0, d=1.6, amp=0.05):
    x = np.arange(int(d * SR)) / SR; return amp * np.exp(-x * 3) * (np.sin(2 * np.pi * f0 * x) + 0.3 * np.sin(2 * np.pi * f0 * 3.01 * x))
for t0, f0 in [(0.3, 880), (5.6, 1046.5), (8.9, 880), (14.3, 1174.7), (17.6, 1318.5), (TOTAL - END + 0.2, 659.25), (TOTAL - END + 0.7, 987.77)]:
    c = chime(f0); i = int(t0 * SR); n = min(len(c), Ls - i)
    if n > 0: fx[i:i + n] += c[:n]
mix = np.clip(pad + fx, -1, 1); st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
with wave.open(D + '_a.wav', 'wb') as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes(st.tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_v.mp4', '-i', D + '_a.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', D + 'reels-anel-data-especial.mp4'], check=True)
os.remove(D + '_v.mp4'); os.remove(D + '_a.wav')
print('ok', TOTAL)
