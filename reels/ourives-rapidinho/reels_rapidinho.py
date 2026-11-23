"""Reels engraçado 'É só um anelzinho' (~22 s) from the goldsmith bench video (WhatsApp, 720x1280 60 fps).
Meme structure: ELA: 'é só um anelzinho, rapidinho' -> O OURIVES: (punch-in + stinger) -> 'UMA HORA DEPOIS...'
-> still on the same detail -> the finished band -> 'Rapidinho não. Perfeito.' -> end card with the official logo.
Captions: Cinzel on ivory labels (brand), punchlines in Parisienne gold. Original bench sound kept underneath."""
import sys, subprocess, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *

D = '/home/user/print/reels/ourives-rapidinho/'
SRC = D + 'original-WA0014.mp4'
W, H, FPS = 1080, 1920, 30
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
PREV = [float(x) for x in sys.argv[1:]]

# (kind, src_start, dur) ; card = full ivory interstitial
TL = [('clip', 0.3, 3.4), ('clip', 4.0, 4.6), ('card', None, 1.6), ('clip', 18.5, 4.2), ('clip', 28.4, 3.6), ('end', None, 3.6)]


def label(text, size=36, pad=(30, 18)):
    t = solid_text(text, caps_font(size, 700), INK, 3); w, h = ink_size(t)
    im = Image.new('RGBA', (w + 2 * pad[0], h + 2 * pad[1] + 12), (0, 0, 0, 0))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 13], 18, fill=255)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * 0.35))); im.alpha_composite(sh, (0, 6))
    bg = Image.new('RGBA', im.size, IV + (0,)); bg.putalpha(m.point(lambda v: int(v * 0.96))); im.alpha_composite(bg)
    paste(im, t, pad[0], pad[1])
    return im


def place(lay, y, x=None):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); out.alpha_composite(lay, (int((W - lay.width) / 2 if x is None else x), int(y))); return np.asarray(out, np.float32)


def gold_line(text, size, y):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); paste(out, gold_text(text, script_font(size)), W / 2, y, anchor='center'); return np.asarray(out, np.float32)


def gold_label(text, size, y):
    g = gold_text(text, script_font(size)); w, h = ink_size(g)
    im = Image.new('RGBA', (w + 90, h + 60), (0, 0, 0, 0))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 26, fill=255)
    bg = Image.new('RGBA', im.size, IV + (0,)); bg.putalpha(m.point(lambda v: int(v * 0.96))); im.alpha_composite(bg)
    paste(im, g, 45, 30)
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); out.alpha_composite(im, ((W - im.width) // 2, y)); return np.asarray(out, np.float32)


def stack(*lines, y=300, gap=14):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for l in lines:
        out.alpha_composite(l, (int((W - l.width) / 2), int(y))); y += l.height + gap
    return np.asarray(out, np.float32)


CAP = {
    0: [(stack(label('ELA:', 46), label('“É SÓ UM ANELZINHO,', 40), label('DEVE SER RAPIDINHO”', 40), y=260), 0.25)],
    1: [(stack(label('O OURIVES:', 52), y=260), 0.0)],
    3: [(stack(label('AINDA NO MESMO', 40), label('DETALHE...', 40), y=260), 0.3)],
    4: [(stack(label('RAPIDINHO NÃO.', 46), y=240), 0.2), (gold_label('Perfeito.', 170, 380), 1.1)],
}
# interstitial card
CARD = Image.new('RGBA', (W, H), IV + (255,))
paste(CARD, solid_text('UMA HORA DEPOIS...', caps_font(52, 700), INK, 8), W / 2, 900, anchor='center')
CARD = np.asarray(CARD.convert('RGB'), np.float32)
# end card
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')      # official, untouched
E = Image.new('RGBA', (W, H), IV + (255,))
a = Image.new('L', (W, H), 0); a.paste(LOGO.getchannel('A'), ((W - LOGO.width) // 2, 520 + 3))
sh = Image.new('RGBA', (W, H), (60, 45, 25, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))); E.alpha_composite(sh)
E.alpha_composite(LOGO, ((W - LOGO.width) // 2, 520))
y = 760; t = solid_text('CADA JOIA FEITA À MÃO,', caps_font(34, 600), INK, 5); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 18
t = gold_text('sem pressa', script_font(150)); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 30
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 40
for txt, f, col, tr in [('OURO 18K · GARANTIA VITALÍCIA', caps_font(30, 600), BR, 4), ('AGENDE SUA VISITA · LINK NA BIO', caps_font(30, 600), BR, 4)]:
    t = solid_text(txt, f, col, tr); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 22
ENDA = np.asarray(E.convert('RGB'), np.float32)


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def smooth(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)


def over(f, arr, k, dy=0):
    if k <= 0.003: return f
    a = np.roll(arr, int(dy), axis=0) if dy else arr; al = a[..., 3:4] / 255 * k
    return f * (1 - al) + a[..., :3] * al


def clip_frames(s, d):
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', str(s), '-t', str(d), '-i', SRC, '-vf',
                            'fps=30,scale=1080:1920:flags=lanczos,hqdn3d=1.5:1:4:3,eq=contrast=1.04:saturation=1.05:gamma=1.03',
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


def zoom(fr, z, cx=W / 2, cy=H / 2):
    if z <= 1.001: return fr.astype(np.float32)
    cw, ch = W / z, H / z; x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
    return np.asarray(Image.fromarray(fr).crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS), np.float32)


EVENTS = []   # (time, kind) for the sound design
frames_out = []
enc = None
if not PREV:
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', D + '_video.mp4'], stdin=subprocess.PIPE)
T = 0.0; AUDIO_SEGS = []
for i, (kind, s, d) in enumerate(TL):
    n = int(round(d * FPS))
    if kind == 'clip':
        AUDIO_SEGS.append((T, s, d)); gen = clip_frames(s, d); last = None
    if i == 1: EVENTS.append((T, 'hit'))
    if kind in ('card', 'end'): EVENTS.append((T, 'whoosh'))
    for j in range(n):
        t = j / FPS; tg = T + t
        if kind == 'clip':
            fr = next(gen, None); last = fr if fr is not None else last
            if PREV and not any(abs(tg - p) < 0.5 / FPS for p in PREV): continue
            if i == 1:   # punch-in on the hands, a little shake
                z = 1.0 + 0.55 * ease(t / 0.18); sx = math.sin(t * 60) * 6 * max(0, 1 - t / 0.5)
                f = zoom(last, z, W * 0.56 + sx, H * 0.47)
            elif i == 4:
                f = zoom(last, 1.0 + 0.12 * t / d, W * 0.5, H * 0.52)
            else:
                f = zoom(last, 1.0 + 0.05 * t / d)
            for arr, t0 in CAP.get(i, []):
                k = ease((t - t0) / 0.35)
                if k > 0: f = over(f, arr, k, (1 - k) * 20)
            fo = 1 - smooth((t - (d - 0.12)) / 0.12) * 0  # hard cuts (meme rhythm)
        elif kind == 'card':
            if PREV and not any(abs(tg - p) < 0.5 / FPS for p in PREV): continue
            f = CARD.copy()
        else:
            if PREV and not any(abs(tg - p) < 0.5 / FPS for p in PREV): continue
            k = smooth(t / 0.5); f = ENDA * k + 0 * (1 - k) if False else ENDA
        out = np.clip(f, 0, 255).astype(np.uint8)
        if PREV:
            Image.fromarray(out).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/rr_{tg:05.2f}.jpg', quality=85)
        else:
            enc.stdin.write(out.tobytes())
    if kind == 'clip':
        for _ in gen: pass
    T += d
TOTAL = T
if PREV: print('prev ok'); sys.exit()
enc.stdin.close(); enc.wait()

# ---- sound: original bench audio per clip (ducked a bit) + hit, whooshes, soft end chord ----
sr = 48000; n = int(sr * TOTAL); mix = np.zeros((n, 2), np.float32)
for t0, s, d in AUDIO_SEGS:
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(s), '-t', str(d), '-i', SRC, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2) * 0.7
    i0 = int(t0 * sr); L = min(len(a), n - i0)
    fade = np.ones(L, np.float32); fl = int(0.02 * sr); fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
    mix[i0:i0 + L] += a[:L] * fade[:, None]
rng = np.random.default_rng(3)
for t0, kind in EVENTS:
    i0 = int(t0 * sr)
    if kind == 'hit':     # dramatic 'dun': low sine drop + noise burst
        L = int(sr * 1.2); tt = np.arange(L) / sr
        boom = np.sin(2 * np.pi * (70 * tt - 15 * tt ** 2)) * np.exp(-3 * tt) * 0.9
        hit = rng.standard_normal(L) * np.exp(-30 * tt) * 0.25
        s = (boom + hit).astype(np.float32)
    else:                 # whoosh
        L = int(sr * 0.6); tt = np.linspace(0, 1, L)
        no = rng.standard_normal(L)
        k = np.exp(-((np.arange(-200, 201)) / 60.0) ** 2); k /= k.sum()
        s = (np.convolve(no, k, 'same') * 6 * np.sin(np.pi * tt) ** 2 * 0.3).astype(np.float32)
    L = min(len(s), n - i0); mix[i0:i0 + L] += s[:L, None]
# end chord
e0 = int((TOTAL - TL[-1][2]) * sr); tt = np.arange(n - e0) / sr
ch = sum(np.sin(2 * np.pi * f * tt) for f in (261.6, 329.6, 392.0, 523.3)) * 0.05 * np.minimum(tt / 0.4, 1) * np.exp(-0.6 * tt)
mix[e0:] += ch[:, None].astype(np.float32)
mix = np.tanh(mix * 1.1) * 0.9
with wave.open(D + '_som.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_video.mp4', '-i', D + '_som.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', D + 'reels-so-um-anelzinho.mp4'], check=True)
print('ok', TOTAL)
