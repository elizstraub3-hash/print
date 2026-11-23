"""Reels 'No GTA x na vida real' (~15 s) com o vídeo da bancada do ourives (WhatsApp 720x1280, versão sem legenda queimada).
Referência ao jogo só no texto (sem logo/arte/música do jogo). Áudio: som da bancada baixinho; o áudio em alta entra no app.
1) NO GTA: um clique e a joia é dela 🎮  2) NA VIDA REAL: (punch-in) alguém faz à mão, com carinho
3) aliança pronta: 'Feita pra ela.'  4) fecho com pattern + logo: 'No jogo é virtual. Aqui é pra sempre.'"""
import sys, subprocess, wave, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/reels/gta-vida-real/'
SRC = D + 'original-WA0014.mp4'
W, H, FPS = 1080, 1920, 30
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
PREV = [float(x) for x in sys.argv[1:]]
TL = [('clip', 0.3, 3.6), ('clip', 5.0, 4.4), ('clip', 28.4, 3.8), ('end', None, 3.8)]


def label(text, size=44, pad=(32, 18), em=None):
    t = solid_text(text, caps_font(size, 700), INK, 3); w, h = ink_size(t)
    e = emoji(em, int(size * 1.15)) if em else None
    ew = (e.width + 14) if e else 0
    im = Image.new('RGBA', (w + ew + 2 * pad[0], h + 2 * pad[1] + 12), (0, 0, 0, 0))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 13], 18, fill=255)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * 0.35))); im.alpha_composite(sh, (0, 6))
    bg = Image.new('RGBA', im.size, IV + (0,)); bg.putalpha(m.point(lambda v: int(v * 0.96))); im.alpha_composite(bg)
    paste(im, t, pad[0], pad[1])
    if e: im.alpha_composite(e, (pad[0] + w + 14, pad[1] + (h - e.height) // 2))
    return im


def gold_label(text, size):
    g = gold_text(text, script_font(size)); w, h = ink_size(g)
    im = Image.new('RGBA', (w + 90, h + 60), (0, 0, 0, 0))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], 26, fill=255)
    bg = Image.new('RGBA', im.size, IV + (0,)); bg.putalpha(m.point(lambda v: int(v * 0.96))); im.alpha_composite(bg)
    paste(im, g, 45, 30); return im


def stack(*lines, y=260, gap=14):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for l in lines:
        out.alpha_composite(l, (int((W - l.width) / 2), int(y))); y += l.height + gap
    return np.asarray(out, np.float32)


CAP = {
    0: [(stack(label('NO GTA:', 52, em='🎮')), 0.15), (stack(label('UM CLIQUE E A JOIA É DELA', 40), y=380), 0.6)],
    1: [(stack(label('NA VIDA REAL:', 52)), 0.0), (stack(label('ALGUÉM FAZ ELA À MÃO,', 40), label('COM CARINHO', 40), y=380), 0.7)],
    2: [(stack(gold_label('Feita pra ela.', 170), y=250), 0.2), (stack(label('OURO 18K · GARANTIA VITALÍCIA', 34), y=520), 0.9)],
}
# end card: logo pattern + official logo
P = Image.open('/home/user/print/assets/pattern-logo.jpg').convert('RGB')
sc = H / P.height; P = P.resize((round(P.width * sc), H), Image.LANCZOS); P = P.crop(((P.width - W) // 2, 0, (P.width - W) // 2 + W, H))
a = np.asarray(P, np.float32); yy = np.arange(H, dtype=np.float32)[:, None, None]; xx = np.arange(W, dtype=np.float32)[None, :, None]
g = np.exp(-(((xx - W / 2) / 520) ** 2 + ((yy - 860) / 480) ** 2)) * 0.8
E = Image.fromarray((a * (1 - g) + np.array(IV, np.float32) * g).astype(np.uint8)).convert('RGBA')
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')
lx = (W - LOGO.width) // 2; al = Image.new('L', (W, H), 0); al.paste(LOGO.getchannel('A'), (lx, 483))
shd = Image.new('RGBA', (W, H), (60, 45, 25, 0)); shd.putalpha(al.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))); E.alpha_composite(shd); E.alpha_composite(LOGO, (lx, 480))
y = 720
t = solid_text('NO JOGO É VIRTUAL.', caps_font(46, 600), INK, 6); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 20
t = gold_text('Aqui é pra sempre.', script_font(128)); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 40
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 44
for txt, f, col, tr in [('JOIAS FEITAS À MÃO · OURO 18K', caps_font(34, 600), INK, 4), ('AGENDE SUA VISITA · LINK NA BIO', caps_font(34, 700), BR, 4),
                        ('atendimento na loja ou online', sans(32, 500), PARCEL_COLOR, 0)]:
    t = solid_text(txt, f, col, tr); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 24
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


enc = None
if not PREV:
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', D + '_video.mp4'], stdin=subprocess.PIPE)
T = 0.0; AUD = []; EV = []
for i, (kind, s, d) in enumerate(TL):
    n = int(round(d * FPS))
    if kind == 'clip': AUD.append((T, s, d)); gen = clip_frames(s, d); last = None
    EV.append(T)
    for j in range(n):
        t = j / FPS; tg = T + t
        if kind == 'clip':
            fr = next(gen, None); last = fr if fr is not None else last
            if PREV and not any(abs(tg - p) < 0.5 / FPS for p in PREV): continue
            if i == 1: f = zoom(last, 1.0 + 0.45 * ease(t / 0.25), W * 0.56, H * 0.47)
            elif i == 2: f = zoom(last, 1.0 + 0.10 * t / d, W * 0.5, H * 0.55)
            else: f = zoom(last, 1.0 + 0.04 * t / d)
            for arr, t0 in CAP.get(i, []):
                k = ease((t - t0) / 0.35)
                if k > 0: f = over(f, arr, k, (1 - k) * 20)
        else:
            if PREV and not any(abs(tg - p) < 0.5 / FPS for p in PREV): continue
            f = ENDA
        out = np.clip(f, 0, 255).astype(np.uint8)
        if PREV: Image.fromarray(out).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/gt_{tg:05.2f}.jpg', quality=85)
        else: enc.stdin.write(out.tobytes())
    if kind == 'clip':
        for _ in gen: pass
    T += d
if PREV: print('prev ok'); sys.exit()
enc.stdin.close(); enc.wait()
sr = 48000; n = int(sr * T); mix = np.zeros((n, 2), np.float32)
for t0, s, d in AUD:                     # bench sound, low, so the trending audio can go on top in the app
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(s), '-t', str(d), '-i', SRC, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2) * 0.35; i0 = int(t0 * sr); L = min(len(a), n - i0)
    fd = np.ones(L, np.float32); fl = int(0.03 * sr); fd[:fl] = np.linspace(0, 1, fl); fd[-fl:] = np.linspace(1, 0, fl)
    mix[i0:i0 + L] += a[:L] * fd[:, None]
with wave.open(D + '_som.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_video.mp4', '-i', D + '_som.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', D + 'reels-gta-vida-real.mp4'], check=True)
print('ok', T)
