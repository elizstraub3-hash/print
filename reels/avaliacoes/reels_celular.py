"""Reels 'Avaliações no celular' — feed de avaliações rolando dentro de um celular; 10 destaques
saem da tela com zoom (toque no tempo da batida), com a resposta da Shimmer; as outras 10 só passam no feed.
Trilha eletrônica original 120 BPM gerada aqui (sem direitos autorais); eventos alinhados à grade de batidas."""
import sys, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print/reels/avaliacoes')
from _common import *   # R, card, star, wrap, BGI, pat, yy, sans, caps_font, script_font, gold_text, solid_text, paste, ...

OUT = D + 'reels-avaliacoes-celular.mp4'
BPM = 120; BEAT = 60 / BPM; SEG = 8 * BEAT          # 2 compassos por destaque
INTRO, OUTRO = 8 * BEAT, 8 * BEAT
NAMES = [r[0] for r in R]
ORDER = ['Emanuelle V.', 'Diogo B.', 'Jean L.', 'Fábio', 'Nayara B.', 'Stephany T.', 'Paola B.', 'Baruc', 'Erika D.', 'Géssica P.',
         'Kelen S.', 'Victor L.', 'Allan L.', 'Luana A.', 'Brendo S.', 'João S.', 'Sifarlei C.', 'Jackson D.', 'Jessica M.', 'Patrick B.']
FEAT = ['Emanuelle V.', 'Jean L.', 'Nayara B.', 'Paola B.', 'Erika D.', 'Kelen S.', 'Allan L.', 'Brendo S.', 'Sifarlei C.', 'Jessica M.']
NF = len(FEAT)
TOTAL = INTRO + NF * SEG + OUTRO

# ---------- phone geometry ----------
PW, PH = 660, 1290; PX, PY = (W - PW) // 2, 350
BEZ = 20; SX, SY, SW, SH = PX + BEZ, PY + BEZ, PW - 2 * BEZ, PH - 2 * BEZ
HEAD = 250                                   # app header inside screen
SC = 0.6                                     # feed card scale

PHONE = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dp = ImageDraw.Draw(PHONE)
sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle([PX + 10, PY + 30, PX + PW - 10, PY + PH + 20], 90, fill=120)
shadow = Image.new('RGBA', (W, H), (40, 28, 14, 0)); shadow.putalpha(sh.filter(ImageFilter.GaussianBlur(30)))
dp.rounded_rectangle([PX, PY, PX + PW, PY + PH], 86, fill=(28, 24, 22, 255))
dp.rounded_rectangle([PX + 4, PY + 4, PX + PW - 4, PY + PH - 4], 82, outline=(90, 80, 70, 255), width=2)
SCREEN_MASK = Image.new('L', (W, H), 0); ImageDraw.Draw(SCREEN_MASK).rounded_rectangle([SX, SY, SX + SW, SY + SH], 68, fill=255)
PHONE.putalpha(Image.fromarray(np.maximum(np.asarray(PHONE.getchannel('A')) - np.asarray(SCREEN_MASK), 0).astype(np.uint8)))
ISLAND = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ISLAND).rounded_rectangle([W // 2 - 90, SY + 18, W // 2 + 90, SY + 62], 22, fill=(12, 10, 10, 255))

# app header (screen-local)
APPH = Image.new('RGBA', (SW, HEAD), (255, 255, 255, 255)); da = ImageDraw.Draw(APPH)
da.text((44, 30), '9:41', font=sans(26, 700), fill=(30, 30, 30))
for k in range(4): da.rectangle([SW - 120 + k * 9, 44 - k * 4, SW - 114 + k * 9, 50], fill=(30, 30, 30))
da.rounded_rectangle([SW - 76, 34, SW - 36, 52], 5, outline=(30, 30, 30), width=2); da.rectangle([SW - 72, 38, SW - 46, 48], fill=(30, 30, 30))
da.text((44, 96), 'Shimmer Joias', font=sans(38, 700), fill=(32, 28, 24))
for k in range(5): star(da, 58 + k * 34, 172, 14, STAR)
da.text((44 + 5 * 34 + 14, 172), 'mais de 40 avaliações', font=sans(24, 500), fill=GREY, anchor='lm')
da.line([(0, HEAD - 2), (SW, HEAD - 2)], fill=(232, 226, 216), width=2)

# feed strip
FEED_BG = (246, 242, 235)
small = []
for nm in ORDER:
    c = card(NAMES.index(nm), False)
    small.append(c.resize((int(c.width * SC), int(c.height * SC)), Image.LANCZOS))
GAP = 8
ys, y = [], 24
for c in small: ys.append(y); y += c.height - int(60 * SC) + GAP
STRIP = Image.new('RGBA', (SW, y + SH), FEED_BG + (255,))
for c, y0 in zip(small, ys): STRIP.alpha_composite(c, ((SW - c.width) // 2, y0))
BIG = {nm: card(NAMES.index(nm), True) for nm in FEAT}

# scroll targets: featured card top lands ~110 px below header
TGT = [max(0, ys[ORDER.index(nm)] - 110) for nm in FEAT]


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def easeio(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def eback(x):
    x = min(max(x, 0), 1); c1 = 1.4; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def scroll_at(t):
    if t < INTRO: return 0.0
    i = min(int((t - INTRO) // SEG), NF - 1); lt = t - INTRO - i * SEG
    prev = TGT[i - 1] if i > 0 else 0.0
    return prev + (TGT[i] - prev) * easeio(lt / (2 * BEAT))


def comp(base, L, dx, dy, alpha=1.0):
    tmp = Image.new('RGBA', base.size, (0, 0, 0, 0)); tmp.paste(L, (int(dx), int(dy)), L)
    if alpha < 1: tmp.putalpha(tmp.getchannel('A').point(lambda v: int(v * max(alpha, 0))))
    base.alpha_composite(tmp)


# intro + header text
def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
I1 = layer(); t = solid_text('OBRIGADA', caps_font(88, 600), INK, 14); paste(I1, t, W / 2, 610, anchor='center')
I2 = layer(); t = gold_text('por cada', script_font(190)); paste(I2, t, W / 2, 700, anchor='center')
t = gold_text('palavra', script_font(190)); paste(I2, t, W / 2, 860, anchor='center')
I3 = layer(); d3 = ImageDraw.Draw(I3)
for k in range(5): star(d3, W / 2 - 120 + k * 60, 1150, 24, STAR)
t = solid_text('MAIS DE 40 AVALIAÇÕES', caps_font(44, 600), BR, 4); paste(I3, t, W / 2, 1210, anchor='center')
t = solid_text('REAIS NO GOOGLE', caps_font(44, 600), BR, 4); paste(I3, t, W / 2, 1272, anchor='center')
t = solid_text('separamos algumas delas', sans(36, 500), PARCEL_COLOR); paste(I3, t, W / 2, 1350, anchor='center')
TOPH = layer(); t = solid_text('O QUE NOSSOS CLIENTES DIZEM', caps_font(42, 600), INK, 5); paste(TOPH, t, W / 2, 232, anchor='center')

# end card (pattern + logo original)
g = np.exp(-(((np.arange(W, dtype=np.float32)[None, :, None] - W / 2) / 520) ** 2 + ((yy - 860) / 500) ** 2)) * 0.82
E = Image.fromarray((pat * (1 - g) + np.array(IV, np.float32) * g).astype(np.uint8)).convert('RGBA')
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA'); E.alpha_composite(LOGO, ((W - LOGO.width) // 2, 470))
y = 700
t = solid_text('SUA HISTÓRIA TAMBÉM', caps_font(46, 600), INK, 6); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 16
t = gold_text('merece brilhar', script_font(170)); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 44
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 44
for txt, f, c, tr in [('OURO 18K · GARANTIA VITALÍCIA', caps_font(34, 600), INK, 4), ('CHAME NO DIRECT · LINK NA BIO', caps_font(34, 700), BR, 4),
                      ('atendimento na loja ou online', sans(32, 500), PARCEL_COLOR, 0)]:
    t = solid_text(txt, f, c, tr); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 24
ENDA = np.asarray(E.convert('RGB'), np.float32)


def phone_frame(t, rise=0.0):
    """renders BG + header + phone with feed; rise in [0,1] = slide-in from bottom."""
    f = BGI.copy()
    off = int((1 - ease(rise)) * 900)
    s = scroll_at(t)
    scr = Image.new('RGBA', (SW, SH), FEED_BG + (255,))
    crop = STRIP.crop((0, int(s), SW, int(s) + SH - HEAD)); scr.paste(crop, (0, HEAD))
    scr.paste(APPH, (0, 0))
    full = Image.new('RGBA', (W, H), (0, 0, 0, 0)); full.paste(scr, (SX, SY))
    full.putalpha(Image.fromarray(np.minimum(np.asarray(full.getchannel('A')), np.asarray(SCREEN_MASK))))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); lay.alpha_composite(shadow); lay.alpha_composite(full); lay.alpha_composite(PHONE); lay.alpha_composite(ISLAND)
    comp(f, lay, 0, off, alpha=min(1, rise * 1.5))
    return f, s, off


def frame(t):
    if t < INTRO:
        out_k = easeio((t - (INTRO - 2.5 * BEAT)) / BEAT)
        if t >= INTRO - 1.5 * BEAT:
            f, _, _ = phone_frame(INTRO, rise=(t - (INTRO - 1.5 * BEAT)) / (1.5 * BEAT))
            return np.asarray(f.convert('RGB'))
        f = BGI.copy()
        for L, t0 in [(I1, 0.15), (I2, 0.55), (I3, 1.1)]:
            k = ease((t - t0) / 0.7)
            if k > 0: comp(f, L, 0, int((1 - k) * 24 - out_k * 60), alpha=k * (1 - out_k))
        return np.asarray(f.convert('RGB'))
    if t >= INTRO + NF * SEG:
        k = easeio((t - INTRO - NF * SEG) / (2 * BEAT))
        pf, _, _ = phone_frame(INTRO + NF * SEG - 1e-3)
        comp(pf, TOPH, 0, 0)
        base = np.asarray(pf.convert('RGB'), np.float32)
        return np.clip(base * (1 - k) + ENDA * k, 0, 255).astype(np.uint8)
    f, s, off = phone_frame(t, 1.0)
    comp(f, TOPH, 0, 0, alpha=ease((t - INTRO) / BEAT))
    i = int((t - INTRO) // SEG); lt = t - INTRO - i * SEG; nm = FEAT[i]
    j = ORDER.index(nm); sm = small[j]
    sx_ = SX + (SW - sm.width) // 2; sy_ = SY + HEAD + ys[j] - s
    T_TAP, T_POP, T_LAND, T_BACK, T_HOME = 2 * BEAT, 2.5 * BEAT, 3 * BEAT, 6.5 * BEAT, 7.5 * BEAT
    # tap ripple on the card (on the beat)
    cx, cy = int(sx_ + sm.width * 0.72), int(sy_ + sm.height * 0.45)
    ph = lt - (T_TAP - 0.3)
    if 0 <= ph < 0.9 and lt < T_LAND:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
        if ph < 0.3:
            a_ = ease(ph / 0.3); r = 30
            do.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, int(210 * a_)), outline=(120, 90, 40, int(170 * a_)), width=3)
        else:
            p = (ph - 0.3) / 0.6; r = 30 + 70 * ease(p); a_ = 1 - p
            do.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(214, 165, 52, int(230 * a_)), width=6)
        f.alpha_composite(ov)
    # pop out / hold / return
    if T_POP <= lt < T_HOME:
        big = BIG[nm]
        if lt < T_LAND: k = eback((lt - T_POP) / (T_LAND - T_POP))
        elif lt < T_BACK: k = 1.0 + 0.012 * np.sin((lt - T_LAND) / BEAT * np.pi)   # leve pulsar na batida
        else: k = 1 - easeio((lt - T_BACK) / (T_HOME - T_BACK))
        k0 = min(max(k, 0), 1.06)
        s0 = SC; s1 = 1.0; sc = s0 + (s1 - s0) * k0
        bx0, by0 = sx_ + sm.width / 2, sy_ + sm.height / 2
        bx1, by1 = W / 2, 330 + 640
        cxp, cyp = bx0 + (bx1 - bx0) * min(k0, 1), by0 + (by1 - by0) * min(k0, 1)
        im = big.resize((max(1, int(big.width * sc)), max(1, int(big.height * sc))), Image.LANCZOS)
        dim = Image.new('RGBA', (W, H), (40, 30, 18, int(55 * min(k0, 1)))); f.alpha_composite(dim)
        comp(f, im, cxp - im.width / 2, cyp - im.height / 2)
    return np.asarray(f.convert('RGB'))


N = int(round(TOTAL * FPS))
if PREV:
    for p in PREV:
        Image.fromarray(frame(p)).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/cel_{p:05.2f}.jpg', quality=85)
    print('prev ok', TOTAL); sys.exit()

enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', D + '_cel_video.mp4'], stdin=subprocess.PIPE)
for n in range(N): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait()

# ---------- trilha eletrônica original 120 BPM ----------
SR = 44100; L = int(TOTAL * SR); tt = np.arange(L) / SR
mix = np.zeros((L, 2))
rng = np.random.default_rng(7)
def put(t0, sig, pan=0.0, amp=1.0):
    i = int(t0 * SR); n = min(len(sig), L - i)
    if n <= 0 or i < 0: return
    mix[i:i + n, 0] += sig[:n] * amp * (1 - pan) ; mix[i:i + n, 1] += sig[:n] * amp * (1 + pan)
def kick():
    x = np.arange(int(0.35 * SR)) / SR; fr = 48 + 90 * np.exp(-x * 28)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-x * 9)
def hat(d=0.05):
    n = int(d * SR); z = rng.standard_normal(n); z = z - np.convolve(z, np.ones(6) / 6, 'same')
    return z * np.exp(-np.arange(n) / SR * 70)
def clap():
    n = int(0.18 * SR); z = rng.standard_normal(n); z = np.convolve(z, np.ones(3) / 3, 'same')
    env = np.exp(-np.arange(n) / SR * 22); return z * env
def pluck(f0, d=0.4):
    x = np.arange(int(d * SR)) / SR
    s = np.sign(np.sin(2 * np.pi * f0 * x)) * 0.5 + np.sin(2 * np.pi * f0 * x)
    s = np.convolve(s, np.ones(8) / 8, 'same'); return s * np.exp(-x * 7)
def chord(freqs, d):
    x = np.arange(int(d * SR)) / SR; s = sum(np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * f * 2.003 * x) for f in freqs)
    env = np.minimum(1, x / 0.3) * np.minimum(1, (d - x) / 0.4); return s * env / len(freqs)
def chime(f0, d=1.0):
    x = np.arange(int(d * SR)) / SR; return np.exp(-x * 4) * (np.sin(2 * np.pi * f0 * x) + 0.35 * np.sin(2 * np.pi * f0 * 3.01 * x))
def riser(d):
    n = int(d * SR); z = rng.standard_normal(n); k = np.linspace(4, 60, n).astype(int)
    out = np.array([z[max(0, i - k[i]):i + 1].mean() for i in range(0, n)]) if False else np.convolve(z, np.ones(12) / 12, 'same')
    return out * np.linspace(0, 1, n) ** 2
# Am - F - C - G (1 compasso cada)
PROG = [(220.0, [220.0, 261.63, 329.63]), (174.61, [174.61, 220.0, 261.63]), (130.81, [261.63, 329.63, 392.0]), (196.0, [196.0, 246.94, 293.66])]
BAR = 4 * BEAT; nbars = int(np.ceil(TOTAL / BAR))
DROP, END = INTRO, INTRO + NF * SEG
for b in range(nbars):
    t0 = b * BAR; root, ch = PROG[b % 4]
    put(t0, chord(ch, BAR), amp=0.10)
    for q in range(4):
        tb = t0 + q * BEAT
        if DROP <= tb < END:
            put(tb, kick(), amp=0.55)
            put(tb + BEAT / 2, hat(), pan=0.25, amp=0.10)
            if q in (1, 3): put(tb, clap(), pan=-0.1, amp=0.16)
            for e in range(2): put(tb + e * BEAT / 2, pluck(root / 2 if e == 0 else root), amp=0.10)
        elif tb < DROP:
            put(tb + BEAT / 2, hat(0.03), pan=0.25, amp=0.05)
put(DROP - 2 * BEAT, riser(2 * BEAT), amp=0.10)
for i in range(NF):
    s0 = INTRO + i * SEG
    put(s0 + 2 * BEAT, chime(1760, 0.4), pan=0.2, amp=0.07)            # tap
    put(s0 + 2.5 * BEAT, riser(0.5 * BEAT), amp=0.07)                   # swoosh into pop
    put(s0 + 3 * BEAT, chime(1318.5, 1.2), pan=-0.2, amp=0.08)          # land
put(END, chime(659.25, 2.5), amp=0.09); put(END + BEAT, chime(987.77, 2.5), amp=0.07)
mix *= np.minimum(1, tt / 0.8)[:, None] * np.minimum(1, (TOTAL - tt) / 1.5)[:, None]
mix = mix / max(1e-6, np.abs(mix).max()) * 0.85
with wave.open(D + '_cel_audio.wav', 'wb') as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_cel_video.mp4', '-i', D + '_cel_audio.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', OUT], check=True)
import os; os.remove(D + '_cel_video.mp4'); os.remove(D + '_cel_audio.wav')
print('ok', TOTAL)
