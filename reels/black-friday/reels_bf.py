"""Reels Black Friday Shimmer (20 s, 120 BPM): abertura preto/dourado, Clássico e Serena (anéis do tráfego) com preço,
fecho com pattern + logo original. Fotos editadas em pixels nativos (sem ampliar), bordas fundindo no preto.
Cortes e textos na batida; trilha eletrônica original gerada aqui."""
import sys, subprocess, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *

D = '/home/user/print/reels/black-friday/'
W, H, FPS = 1080, 1920, 30
BPM = 120; B = 60 / BPM
T_CL, T_SE, T_END, TOTAL = 8 * B, 20 * B, 32 * B, 40 * B      # 4s, 10s, 16s, 20s
BLK = np.array((14, 10, 8), np.float32)
IVORY = (238, 228, 212); SOFT = (198, 186, 168)
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
PREV = [float(x) for x in sys.argv[1:]]
yy = np.arange(H, dtype=np.float32)[:, None, None]; xx = np.arange(W, dtype=np.float32)[None, :, None]


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def C(im, lay, y): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]
def glow(lay_bb, blur=10, alpha=0.55, col=(0, 0, 0)):
    lay, bb = lay_bb; a = lay.getchannel('A'); s = Image.new('RGBA', lay.size, col + (0,)); s.putalpha(a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha)))
    o = Image.new('RGBA', lay.size, (0, 0, 0, 0)); o.alpha_composite(s, (0, 3)); o.alpha_composite(lay); return o, bb


# ---------- fundo preto quente com vinheta ----------
vig = np.exp(-(((xx - W / 2) / 900) ** 2 + ((yy - H * 0.45) / 1200) ** 2))
DARK = BLK + np.array((30, 22, 14), np.float32) * vig


def scene_bg(path, oy, crop_w=1080):
    ph = Image.open(path).convert('RGB')
    if ph.width > crop_w: ph = ph.crop(((ph.width - crop_w) // 2, 0, (ph.width - crop_w) // 2 + crop_w, ph.height))
    a = np.asarray(ph, np.float32); h, w = a.shape[:2]
    out = DARK.copy(); ox = (W - w) // 2
    y0, y1 = max(oy, 0), min(oy + h, H)
    region = a[y0 - oy:y1 - oy]
    # máscara: funde topo, base e laterais no preto
    ly = np.arange(y0, y1, dtype=np.float32)[:, None, None]
    m = np.clip((ly - oy) / 320, 0, 1) * np.clip((oy + h - ly) / 340, 0, 1)
    lx = np.arange(w, dtype=np.float32)[None, :, None]
    m = m * np.clip(lx / 40, 0, 1) * np.clip((w - lx) / 40, 0, 1)
    m = m * m * (3 - 2 * m)
    out[y0:y1, ox:ox + w] = out[y0:y1, ox:ox + w] * (1 - m) + region * m
    # escurece o topo da foto para o texto (nunca sobre a joia)
    top = np.clip(1 - (yy - oy) / 620, 0, 1); top = (top * top * (3 - 2 * top)) * 0.8
    out = out * (1 - top) + BLK * top
    return out


SC_CL1 = scene_bg('/home/user/print/serena-classico/fotos/classico-cetim-2.png', 330)
SC_CL2 = scene_bg('/home/user/print/serena-classico/fotos/classico-cetim-1.png', 330)
SC_SE = scene_bg('/home/user/print/serena-classico/fotos/serena-editada.png', 430, crop_w=1055)

# ---------- textos ----------
INTRO = []
a = L(); C(a, glow(gold_text('BLACK', caps_font(170, 700), 18)), 560); INTRO.append((a, 0 * B))
b = L(); C(b, glow(gold_text('FRIDAY', caps_font(170, 700), 18)), 760); INTRO.append((b, 2 * B))
c = L(); C(c, glow(gold_text('Shimmer', script_font(210))), 950); INTRO.append((c, 4 * B))
d = L(); y = C(d, solid_text('10% OFF NO PIX', caps_font(52, 700), IVORY, 8), 1250)
C(d, solid_text('ou até 10x sem juros no cartão', sans(36, 500), SOFT), y + 22); INTRO.append((d, 6 * B))


def product_layers(name, pix, parc):
    out = []
    a = L(); y = C(a, solid_text('ANEL SOLITÁRIO', caps_font(46, 600), IVORY, 8), 262); out.append((a, 0.5 * B))
    b = L(); y = C(b, glow(gold_text(name, script_font(200))), y + 4); out.append((b, 1 * B))
    c = L(); y = C(c, solid_text(pix, sans(64, 700), IVORY), y + 20)
    C(c, solid_text(parc, sans(34, 500), SOFT), y + 14); out.append((c, 2 * B))
    return out


CL_TX = product_layers('Clássico', 'R$ 1.350 no PIX', 'ou 10x de R$ 150,00 sem juros')
SE_TX = product_layers('Serena', 'R$ 1.799,10 no PIX', 'ou 10x de R$ 199,90 sem juros')
TAG = L(); C(TAG, solid_text('OURO 18K · GARANTIA VITALÍCIA', caps_font(30, 600), SOFT, 5), 1835)

# ---------- fecho: pattern + logo ----------
P = Image.open('/home/user/print/assets/pattern-logo.jpg').convert('RGB')
sc = H / P.height; P = P.resize((round(P.width * sc), H), Image.LANCZOS); P = P.crop(((P.width - W) // 2, 0, (P.width - W) // 2 + W, H))
pat = np.asarray(P, np.float32)
g = np.exp(-(((xx - W / 2) / 520) ** 2 + ((yy - 860) / 500) ** 2)) * 0.82
E = Image.fromarray((pat * (1 - g) + np.array(IV, np.float32) * g).astype(np.uint8)).convert('RGBA')
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA'); E.alpha_composite(LOGO, ((W - LOGO.width) // 2, 470))
y = 700
t = solid_text('BLACK FRIDAY', caps_font(50, 600), INK, 10); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 16
t = gold_text('é hoje', script_font(190)); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 40
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 44
for txt, f, col, tr in [('OURO 18K · GARANTIA VITALÍCIA', caps_font(34, 600), INK, 4), ('CHAME NO WHATSAPP · LINK NA BIO', caps_font(34, 700), BR, 4),
                        ('atendimento na loja ou online', sans(32, 500), PARCEL_COLOR, 0)]:
    t = solid_text(txt, f, col, tr); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 24
ENDA = np.asarray(E.convert('RGB'), np.float32)


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def easeio(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)


def pulse(t):   # leve "respiro" a cada batida (kick)
    ph = (t % B) / B
    return 0.010 * np.exp(-ph * 6)


def zoom(arr, z, cy=0.55):
    if z <= 1.0005: return arr
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); cw, ch = W / z, H / z
    return np.asarray(im.crop(((W - cw) / 2, (H - ch) * cy, (W + cw) / 2, (H - ch) * cy + ch)).resize((W, H), Image.LANCZOS), np.float32)


def put_layers(f, layers, lt):
    for lay, t0 in layers:
        k = ease((lt - t0) / 0.35)
        if k <= 0: continue
        arr = np.asarray(lay, np.float32)
        s = 1.0 + 0.06 * (1 - k)                      # pop leve na batida
        if s > 1.001:
            im = Image.fromarray(arr.astype(np.uint8), 'RGBA'); cw, ch = W / s, H / s
            arr = np.asarray(im.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H - ch) / 2 + ch)).resize((W, H), Image.LANCZOS), np.float32)
        al = arr[..., 3:4] / 255 * k
        f = f * (1 - al) + arr[..., :3] * al
    return f


def flash(f, t, t0, dur=0.18, amt=0.55):
    k = (t - t0) / dur
    if 0 <= k < 1: f = f * (1 - amt * (1 - k)) + 255 * amt * (1 - k)
    return f


def frame(t):
    if t < T_CL:
        f = put_layers(DARK.copy(), INTRO, t)
        f = zoom(f, 1 + pulse(t) * (1 if t >= 4 * B else 0.4))
    elif t < T_SE:
        lt = t - T_CL
        base = SC_CL1 if lt < 6 * B else SC_CL2
        f = zoom(base, 1.0 + 0.035 * lt / (T_SE - T_CL) + pulse(t))
        f = put_layers(f, CL_TX, lt)
        f = flash(f, t, T_CL); f = flash(f, t, T_CL + 6 * B, amt=0.35)
    elif t < T_END:
        lt = t - T_SE
        f = zoom(SC_SE, 1.0 + 0.04 * lt / (T_END - T_SE) + pulse(t))
        f = put_layers(f, SE_TX, lt)
        f = flash(f, t, T_SE)
    else:
        lt = t - T_END
        k = easeio(lt / (1.5 * B))
        prev = zoom(SC_SE, 1.04)
        f = prev * (1 - k) + ENDA * k
        f = flash(f, t, T_END, amt=0.3)
    return np.clip(f, 0, 255).astype(np.uint8)


N = int(round(TOTAL * FPS))
if PREV:
    for p in PREV: Image.fromarray(frame(p)).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/bf_{p:05.2f}.jpg', quality=85)
    print('prev ok', TOTAL); sys.exit()

enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-an', D + '_v.mp4'], stdin=subprocess.PIPE)
for n in range(N): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait()

# ---------- trilha eletrônica original 120 BPM ----------
SR = 44100; Ls = int(TOTAL * SR); tt = np.arange(Ls) / SR
mix = np.zeros((Ls, 2)); rng = np.random.default_rng(11)
def put(t0, sig, pan=0.0, amp=1.0):
    i = int(t0 * SR); n = min(len(sig), Ls - i)
    if n > 0: mix[i:i + n, 0] += sig[:n] * amp * (1 - pan); mix[i:i + n, 1] += sig[:n] * amp * (1 + pan)
def kick():
    x = np.arange(int(0.35 * SR)) / SR; fr = 46 + 100 * np.exp(-x * 30)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-x * 8)
def hat(d=0.05):
    n = int(d * SR); z = rng.standard_normal(n); z = z - np.convolve(z, np.ones(6) / 6, 'same'); return z * np.exp(-np.arange(n) / SR * 70)
def clap():
    n = int(0.2 * SR); z = np.convolve(rng.standard_normal(n), np.ones(3) / 3, 'same'); return z * np.exp(-np.arange(n) / SR * 20)
def bass(f0, d):
    x = np.arange(int(d * SR)) / SR; s = np.tanh(2.2 * np.sin(2 * np.pi * f0 * x)); return s * np.exp(-x * 5)
def chord(fs, d):
    x = np.arange(int(d * SR)) / SR; s = sum(np.sin(2 * np.pi * f * x) + 0.25 * np.sin(2 * np.pi * f * 2.004 * x) for f in fs) / len(fs)
    return s * np.minimum(1, x / 0.2) * np.minimum(1, (d - x) / 0.3)
def riser(d):
    n = int(d * SR); z = np.convolve(rng.standard_normal(n), np.ones(10) / 10, 'same'); return z * np.linspace(0, 1, n) ** 2.2
def crash(d=1.5):
    n = int(d * SR); z = rng.standard_normal(n); z = z - np.convolve(z, np.ones(4) / 4, 'same'); return z * np.exp(-np.arange(n) / SR * 3)
def chime(f0, d=1.4):
    x = np.arange(int(d * SR)) / SR; return np.exp(-x * 3.5) * (np.sin(2 * np.pi * f0 * x) + 0.3 * np.sin(2 * np.pi * f0 * 3.01 * x))
PROG = [(110.0, [220.0, 261.63, 329.63]), (87.31, [174.61, 220.0, 261.63]), (130.81, [261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66])]
BAR = 4 * B
for bi in range(int(TOTAL / BAR) + 1):
    t0 = bi * BAR; root, ch = PROG[bi % 4]
    put(t0, chord(ch, BAR), amp=0.10)
    for q in range(4):
        tb = t0 + q * B
        if tb >= TOTAL: break
        if tb < T_CL:                       # intro: só batida nas palavras + hats
            if q % 2 == 0: put(tb, kick(), amp=0.40)
            put(tb + B / 2, hat(0.03), pan=0.3, amp=0.06)
        elif tb < T_END:                    # drop
            put(tb, kick(), amp=0.62)
            put(tb + B / 2, hat(), pan=0.25, amp=0.12); put(tb + B / 4, hat(0.02), pan=-0.25, amp=0.05); put(tb + 3 * B / 4, hat(0.02), pan=-0.25, amp=0.05)
            if q in (1, 3): put(tb, clap(), amp=0.18)
            put(tb + B / 2, bass(root, B / 2), amp=0.16)
put(T_CL - 2 * B, riser(2 * B), amp=0.14)
for tc in (T_CL, T_SE): put(tc, crash(), amp=0.10)
put(T_CL + 6 * B, crash(0.8), amp=0.05)
put(T_END, chime(659.25, 2.6), amp=0.12); put(T_END + B, chime(987.77, 2.4), amp=0.09); put(T_END + 2 * B, chime(1318.5, 2.0), amp=0.06)
mix *= np.minimum(1, tt / 0.3)[:, None] * np.minimum(1, (TOTAL - tt) / 1.2)[:, None]
mix = mix / np.abs(mix).max() * 0.88
with wave.open(D + '_a.wav', 'wb') as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_v.mp4', '-i', D + '_a.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', D + 'reels-black-friday-shimmer.mp4'], check=True)
os.remove(D + '_v.mp4'); os.remove(D + '_a.wav')
print('ok', TOTAL)
