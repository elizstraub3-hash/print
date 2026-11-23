"""Story motion 60 s: 'Tá procurando onde comprar...?' -> equipe pronta -> como funciona -> direct/link -> end card.
Background: attendance footage (bg.mp4) under a soft white fade from the top. Product photos slide in as cards
(crop + downscale only). Sound: synthesized whooshes on every entrance + soft ambient pad."""
import sys, subprocess, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *

D = '/home/user/print/stories/equipe-motion/'
P = '/home/user/print/'
W, H, FPS, DUR = 1080, 1920, 30, 60.0
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
PREV = [float(x) for x in sys.argv[1:]]
WHOOSH = []                                     # (time, strength)


def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def smooth(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def back(x):
    x = min(max(x, 0), 1); c = 1.4; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def fit_script(text, size, maxw=840):
    while True:
        lay = gold_text(text, script_font(size))
        if ink_size(lay)[0] <= maxw or size < 60: return lay
        size -= 4


# ---------- text blocks: list of (layer, y, t_in, t_out) ----------
TEXT = []


def block(lines, t0, t1, y=270, gap=16, stagger=0.35):
    for i, (kind, txt, sz) in enumerate(lines):
        if kind == 'caps': lay = solid_text(txt, caps_font(sz, 600), INK, max(3, sz // 6))
        elif kind == 'sub': lay = solid_text(txt, caps_font(sz, 600), BR, 3)
        elif kind == 'script': lay = fit_script(txt, sz)
        TEXT.append((lay, y, t0 + i * stagger, t1))
        if i == 0: WHOOSH.append((t0, 0.6))
        y += ink_size(lay)[1] + gap
    return y


block([('caps', 'TÁ PROCURANDO ONDE COMPRAR', 34), ('script', 'a sua aliança?', 140)], 0.4, 8.6)
block([('caps', 'OU UM SOLITÁRIO PARA', 34), ('script', 'pedir ela em casamento?', 120)], 9.2, 17.6)
block([('caps', 'OU UM PRESENTE ESPECIAL,', 34), ('script', 'anel de formatura?', 130)], 18.2, 25.6)
y = block([('caps', 'AQUI A GENTE', 34), ('script', 'faz pra você', 140)], 26.2, 35.6)
block([('sub', 'ATENDIMENTO ESPECIALIZADO', 30), ('sub', 'NOSSA EQUIPE ESTÁ PRONTA', 26), ('sub', 'PARA TE ATENDER COM CALMA', 26)], 28.2, 35.6, y=y + 30, gap=14, stagger=0.5)
block([('caps', 'É SIMPLES ASSIM', 34), ('script', 'como funciona', 130)], 36.2, 46.6)
y = block([('caps', 'GOSTOU DE ALGUMA?', 34), ('script', 'é só chamar', 140)], 47.2, 53.6)
block([('sub', 'MANDE NO DIRECT', 28), ('sub', 'OU PELO LINK NA BIO', 28)], 48.6, 53.6, y=y + 30, gap=14, stagger=0.4)

# ---------- product cards ----------
def card(path, w=380, h=480, ang=0):
    im = Image.open(P + path).convert('RGB')
    iw, ih = im.size; r = w / h
    cw, ch = (iw, int(iw / r)) if iw / ih < r else (int(ih * r), ih)
    im = im.crop(((iw - cw) // 2, (ih - ch) // 2, (iw - cw) // 2 + cw, (ih - ch) // 2 + ch)).resize((w, h), Image.LANCZOS)  # downscale only
    b = 10; pad = 40
    out = Image.new('RGBA', (w + 2 * b + 2 * pad, h + 2 * b + 2 * pad), (0, 0, 0, 0))
    m = Image.new('L', out.size, 0); ImageDraw.Draw(m).rounded_rectangle([pad, pad, pad + w + 2 * b, pad + h + 2 * b], 26, fill=255)
    sh = Image.new('RGBA', out.size, (60, 40, 20, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.35)))
    out.alpha_composite(sh, (0, 10))
    fr = Image.new('RGBA', out.size, (255, 253, 249, 0)); fr.putalpha(m); out.alpha_composite(fr)
    pm = Image.new('L', (w, h), 0); ImageDraw.Draw(pm).rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=255)
    ph = im.convert('RGBA'); ph.putalpha(pm); out.alpha_composite(ph, (pad + b, pad + b))
    return out


CARDS = []   # (img, cx, cy, final_angle, t_in, t_out)


def fan(paths, t0, t1, cy=1100):
    xs = [W / 2 - 300, W / 2, W / 2 + 300] if len(paths) == 3 else [W / 2 - 170, W / 2 + 170]
    angs = [-7, 0, 7] if len(paths) == 3 else [-5, 5]
    order = [0, 2, 1] if len(paths) == 3 else [0, 1]          # middle card lands last, on top
    for k, i in enumerate(order):
        CARDS.append((card(paths[i]), xs[i], cy + (0 if angs[i] == 0 else 30), angs[i], t0 + 0.45 * k, t1))
        WHOOSH.append((t0 + 0.45 * k, 1.0))
    WHOOSH.append((t1, 0.7))


fan(['aliancas-revestidas/fotos/51.webp', 'black-friday-kit/fotos/64_orig.jpg', 'aliancas-revestidas/fotos/55.webp'], 1.6, 8.6)
fan(['solitario-helena/fotos/57.webp', 'solitario-retoque/2382.png', 'solitario-7-5mm/fotos/45.webp'], 10.4, 17.6)
fan(['anel-classico/classico-1.png', 'anel-classico/classico-2.png'], 19.4, 25.6)

# ---------- 'como funciona' steps on an ivory panel ----------
STEPS = []
PANEL = Image.new('RGBA', (W, H), (0, 0, 0, 0))
pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).rounded_rectangle([90, 700, W - 90, 1330], 36, fill=255)
pl = Image.new('RGBA', (W, H), IV + (0,)); pl.putalpha(pm.point(lambda v: int(v * 0.93))); PANEL.alpha_composite(pl)
fm = Image.new('L', (W, H), 0); ImageDraw.Draw(fm).rounded_rectangle([90, 700, W - 90, 1330], 36, outline=255, width=3); PANEL.alpha_composite(gold_fill(fm))
for i, (a, b) in enumerate([('AGENDE O SEU HORÁRIO', 'pelo direct ou link na bio'), ('VENHA ATÉ A LOJA', 'Al. Dr. Muricy, 650 · 8º andar · Centro'),
                            ('ESCOLHA COM CALMA', 'entre as diversas opções que temos')]):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); yb = 760 + i * 190
    n = gold_text(str(i + 1), script_font(120)); paste(lay, n, 160, yb)
    paste(lay, solid_text(a, caps_font(32, 700), INK, 4), 280, yb + 18)
    paste(lay, solid_text(b, sans(28, 500), PARCEL_COLOR), 282, yb + 78)
    STEPS.append((np.asarray(lay, np.float32), 38.0 + i * 1.6)); WHOOSH.append((38.0 + i * 1.6, 0.8))
PANELA = np.asarray(PANEL, np.float32); WHOOSH.append((37.4, 0.6))

# ---------- end card ----------
END0 = 54.0
END = []
# official logo, untouched, at its native size (500 px); only a soft shadow behind it, allowed by the brand rules
LOGO = Image.open(P + 'marca/logo-oficial.png').convert('RGBA')
lg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); lx, ly = (W - LOGO.width) // 2, 430
sh = Image.new('RGBA', (W, H), (60, 45, 25, 0)); a = Image.new('L', (W, H), 0); a.paste(LOGO.getchannel('A'), (lx, ly + 3))
sh.putalpha(a.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))); lg.alpha_composite(sh); lg.alpha_composite(LOGO, (lx, ly))
END.append((np.asarray(lg, np.float32), END0 + 0.2))
e = Image.new('RGBA', (W, H), (0, 0, 0, 0)); y = 640
y = 640; t = solid_text('A SUA PRÓXIMA JOIA', caps_font(36, 600), INK, 6); paste(e, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 18
t = gold_text('te espera aqui', script_font(150)); paste(e, t, W / 2, y, anchor='center'); y += ink_size(t)[1]
END.append((np.asarray(e, np.float32), END0 + 0.4))
e = Image.new('RGBA', (W, H), (0, 0, 0, 0))
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y + 50), (W / 2 + 60, y + 50)], fill=255, width=3); e.alpha_composite(gold_fill(m))
y += 96
for txt, f, col in [('AGENDE SUA VISITA · LINK NA BIO', caps_font(32, 600), BR), ('Al. Dr. Muricy, 650 · 8º andar · Centro · Curitiba', sans(28, 500), PARCEL_COLOR),
                    ('Ouro 18k · garantia vitalícia · 10x sem juros', sans(28, 500), PARCEL_COLOR)]:
    t = solid_text(txt, f, col, 4 if col == BR else 0); paste(e, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 24
END.append((np.asarray(e, np.float32), END0 + 1.1)); WHOOSH.append((END0, 0.9))

# white fade from the top (requested) + light overall veil
IVA = np.array(IV, np.float32)
# white panel present through the whole video; footage behind it darkened (lower contrast, deeper blacks)
PX0, PY0, PX1, PY1 = 60, 200, W - 60, 1410
WP = Image.new('RGBA', (W, H), (0, 0, 0, 0))
pm = Image.new('L', (W, H), 0); ImageDraw.Draw(pm).rounded_rectangle([PX0, PY0, PX1, PY1], 40, fill=255)
shd = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shd.putalpha(pm.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.45))); WP.alpha_composite(shd, (0, 14))
pw = Image.new('RGBA', (W, H), IV + (0,)); pw.putalpha(pm.point(lambda v: int(v * 0.97))); WP.alpha_composite(pw)
om = Image.new('L', (W, H), 0); ImageDraw.Draw(om).rounded_rectangle([PX0 + 18, PY0 + 18, PX1 - 18, PY1 - 18], 30, outline=255, width=2); WP.alpha_composite(gold_fill(om))
WPA = np.asarray(WP, np.float32)
WX0, WY0, WX1, WY1 = 130, 740, W - 130, 1340
_wm = Image.new('L', (WX1 - WX0, WY1 - WY0), 0); ImageDraw.Draw(_wm).rounded_rectangle([0, 0, WX1 - WX0 - 1, WY1 - WY0 - 1], 26, fill=255)
WMASK = (np.asarray(_wm, np.float32) / 255)[..., None]


def comp_layer(f, arr, k, dy):
    if k <= 0.003: return f
    a = np.roll(arr, int(dy), axis=0); al = a[..., 3:4] / 255 * k
    return f * (1 - al) + a[..., :3] * al


TEXTA = []
for lay, y0, t0, t1 in TEXT:
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); paste(im, lay, W / 2, y0, anchor='center'); TEXTA.append((np.asarray(im, np.float32), t0, t1))


def frame(bgf, t):
    f = bgf.astype(np.float32)
    f = ((f - 128) * 0.72 + 128) * 0.42                      # low contrast + dark: the footage reads as a moody backdrop
    f = comp_layer(f, WPA, smooth(t / 0.6), (1 - smooth(t / 0.6)) * 40)
    for arr, t0, t1 in TEXTA:
        kin = ease_out((t - t0) / 0.7); kout = 1 - smooth((t - t1) / 0.45)
        k = kin * kout
        if k > 0: f = comp_layer(f, arr, k, (1 - kin) * 24 - (1 - kout) * 16)
    # panel + steps
    kp = smooth((t - 37.4) / 0.6) * (1 - smooth((t - 46.6) / 0.45))
    if kp > 0:
        for arr, t0 in STEPS:
            k = ease_out((t - t0) / 0.6) * (1 - smooth((t - 46.6) / 0.45))
            if k > 0: f = comp_layer(f, arr, k, 0) if False else _slide(f, arr, k, t, t0)
    # bright 'window' with the attendance footage inside the white panel (scenes without cards)
    for w0, w1 in ((26.8, 35.6), (47.8, 53.6)):
        kw = smooth((t - w0) / 0.6) * (1 - smooth((t - w1) / 0.45))
        if kw > 0:
            src = bgf.astype(np.float32)
            win = src[WY0 - 40:WY1 - 40, WX0:WX1] if False else src[(H - (WY1 - WY0)) // 2:(H - (WY1 - WY0)) // 2 + (WY1 - WY0), WX0:WX1]
            a = WMASK * kw
            f[WY0:WY1, WX0:WX1] = f[WY0:WY1, WX0:WX1] * (1 - a) + win * a
    img = Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).convert('RGBA')
    for c, cx, cy, ang, t0, t1 in CARDS:
        if t < t0 or t > t1 + 0.6: continue
        kin = back((t - t0) / 0.75); kout = smooth((t - t1) / 0.5)
        a = ang + (1 - kin) * 14 - kout * 10
        px = cx + (1 - kin) * 760 - kout * 900
        r = c.rotate(a, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(r, (int(px - r.width / 2), int(cy - r.height / 2)))
    f = np.asarray(img.convert('RGB'), np.float32)
    ke = smooth((t - END0) / 0.7)
    if ke > 0:
        f = f * (1 - ke) + IVA * ke
        for arr, t0 in END:
            k = ease_out((t - t0) / 0.7)
            if k > 0: f = comp_layer(f, arr, k, (1 - k) * 22)
    return np.clip(f, 0, 255).astype(np.uint8)


def _slide(f, arr, k, t, t0):
    dx = int((1 - ease_out((t - t0) / 0.6)) * 120)
    a = np.roll(arr, dx, axis=1); al = a[..., 3:4] / 255 * k
    return f * (1 - al) + a[..., :3] * al


# ---------- audio ----------
def audio(path):
    sr = 48000; n = int(sr * DUR); out = np.zeros(n, np.float32); rng = np.random.default_rng(7)
    for t0, s in WHOOSH:                                   # filtered-noise swoosh, pitch sweeping up then down
        L = int(sr * 0.75); i0 = int((t0 - 0.12) * sr)
        if i0 < 0 or i0 + L > n: continue
        noise = rng.standard_normal(L).astype(np.float32)
        tt = np.linspace(0, 1, L)
        env = np.sin(np.pi * np.clip(tt / 0.85, 0, 1)) ** 2 * np.exp(-2.2 * tt)
        y = np.zeros(L, np.float32); lp = 0.0; bp = 0.0
        fc = 400 + 2600 * np.sin(np.pi * tt) ** 1.5             # state-variable filter sweep
        q = 0.35
        for j in range(L):
            fq = 2 * math.sin(math.pi * fc[j] / sr)
            hp = noise[j] - lp - q * bp; bp += fq * hp; lp += fq * bp; y[j] = bp
        out[i0:i0 + L] += y * env * 0.16 * s
    t = np.arange(n) / sr                                     # soft pad: Cmaj9 / Am9 / Fmaj9 / G6, 3.75 s each
    chords = [[261.6, 329.6, 392.0, 493.9, 587.3], [220.0, 261.6, 329.6, 392.0, 493.9], [174.6, 220.0, 261.6, 329.6, 392.0], [196.0, 246.9, 293.7, 329.6, 392.0]]
    pad = np.zeros(n, np.float32); seg = 3.75
    for k in range(int(DUR / seg) + 1):
        a0 = int(k * seg * sr); a1 = min(n, int((k + 1) * seg * sr) + int(0.8 * sr))
        if a0 >= n: break
        tt = t[a0:a1] - k * seg
        env = np.clip(tt / 1.2, 0, 1) * np.clip((seg + 0.8 - tt) / 1.0, 0, 1)
        for fr in chords[k % 4]:
            pad[a0:a1] += (np.sin(2 * np.pi * fr * tt) + 0.3 * np.sin(2 * np.pi * fr * 2.003 * tt)) * env * 0.018
        # gentle pluck on the chord root an octave up
        pl = np.sin(2 * np.pi * chords[k % 4][0] * 2 * tt) * np.exp(-3.5 * tt) * 0.05
        pad[a0:a1] += pl
    out += pad * np.clip(t / 2, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1)
    out = np.tanh(out * 1.2) * 0.8
    st = (np.stack([out, out], 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes())


dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', D + 'bg.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
if not PREV:
    audio(D + 'som.wav')
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-i', D + 'som.wav', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', D + 'story-equipe-60s.mp4'], stdin=subprocess.PIPE)
last = None
for n in range(int(DUR * FPS)):
    b = dec.stdout.read(W * H * 3)
    if len(b) == W * H * 3: last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    t = n / FPS
    if PREV:
        if any(abs(t - p) < 0.5 / FPS for p in PREV):
            Image.fromarray(frame(last, t)).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/em_{t:05.1f}.jpg', quality=85)
        if t > max(PREV): break
        continue
    enc.stdin.write(frame(last, t).tobytes())
dec.kill()
if not PREV: enc.stdin.close(); enc.wait()
print('ok')
