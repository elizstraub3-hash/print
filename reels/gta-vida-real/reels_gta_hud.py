"""Reels 'Missão: joia pra Lucia' (~19 s) com HUD de game desenhado do zero (inspirado em jogos de mundo aberto,
sem logo, fonte ou arte do GTA): minimapa com marcador da Shimmer, barras de vida/colete, saldo do jogo,
banner de 'NOVA MISSÃO', objetivo no rodapé e 'MISSÃO CUMPRIDA' no fim. Joia sempre nítida, texto nunca em cima dela.
Clipes: bancada do ourives (WhatsApp 720x1280) + meia aliança no cetim (IMG_2358)."""
import sys, subprocess, wave, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/reels/gta-vida-real/'
BENCH = D + 'original-WA0014.mp4'
ALI = '/home/user/print/videos-drive/IMG_2358.MOV'
W, H, FPS = 1080, 1920, 30
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
YEL = (247, 196, 22); GRN = (114, 196, 92); BLU = (86, 156, 220)
PREV = [float(x) for x in sys.argv[1:]]
SEG = [('bench', 0.3, 3.6), ('bench', 5.0, 4.4), ('ali', 1.0, 4.8), ('mission', None, 2.8), ('end', None, 3.8)]


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def outline(lines, size=64, y=300, em=None, color=(255, 255, 255), hl=None):
    """White bold letters with black outline; hl = word drawn in yellow."""
    out = L(); d = ImageDraw.Draw(out); fnt = sans(size, 800)
    for i, ln in enumerate(lines):
        words = ln.split(' '); total = fnt.getlength(ln)
        e = emoji(em, int(size * 1.05)) if (em and i == len(lines) - 1) else None
        ew = (e.width + 12) if e else 0; x = (W - total - ew) / 2
        for wi, wd in enumerate(words):
            txt = wd + (' ' if wi < len(words) - 1 else '')
            col = YEL if hl and wd.strip('.,:').lower() in hl else color
            d.text((x, y), txt, font=fnt, fill=col + (255,), stroke_width=max(4, size // 12), stroke_fill=(0, 0, 0, 255))
            x += fnt.getlength(txt)
        if e: out.alpha_composite(e, (int(x + 12), int(y + size * 0.05)))
        y += int(size * 1.22)
    return out


# ---------------- HUD ----------------
MX, MY, MR = 190, 1560, 128          # minimap centre / radius (bottom-left)


def minimap(t):
    lay = L(); d = ImageDraw.Draw(lay)
    m = Image.new('RGBA', (2 * MR, 2 * MR), (0, 0, 0, 0)); md = ImageDraw.Draw(m)
    md.ellipse([0, 0, 2 * MR - 1, 2 * MR - 1], fill=(28, 34, 30, 215))
    rng = np.random.default_rng(4); off = (t * 14) % 60                # map drifts slowly as if walking
    for k in range(9):                                                 # streets
        y0 = -40 + k * 40 + off
        md.line([(0, y0), (2 * MR, y0 + rng.integers(-40, 40))], fill=(92, 100, 92, 255), width=7)
    for k in range(6):
        x0 = rng.integers(0, 2 * MR)
        md.line([(x0, 0), (x0 + rng.integers(-60, 60), 2 * MR)], fill=(92, 100, 92, 255), width=7)
    md.line([(MR, MR), (MR + 60, MR - 85)], fill=(232, 120, 220, 255), width=8)       # GPS route (pink)
    mask = Image.new('L', m.size, 0); ImageDraw.Draw(mask).ellipse([0, 0, 2 * MR - 1, 2 * MR - 1], fill=255)
    m.putalpha(Image.fromarray(np.minimum(np.asarray(m.getchannel('A')), np.asarray(mask))))
    lay.alpha_composite(m, (MX - MR, MY - MR))
    d.ellipse([MX - MR, MY - MR, MX + MR, MY + MR], outline=(0, 0, 0, 255), width=5)
    # destination: little diamond = Shimmer, pulsing
    px, py = MX + 60, MY - 85; pr = 20 + 4 * math.sin(t * 6)
    d.polygon([(px, py - pr), (px + pr * 0.8, py - pr * 0.2), (px, py + pr), (px - pr * 0.8, py - pr * 0.2)], fill=YEL + (255,), outline=(0, 0, 0, 255))
    d.polygon([(MX, MY - 18), (MX + 13, MY + 14), (MX, MY + 6), (MX - 13, MY + 14)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))   # player arrow
    # health / armour bars under the map
    bw = 2 * MR; by = MY + MR + 16
    for i, (col, val) in enumerate([(GRN, 0.86), (BLU, 0.62)]):
        x0 = MX - MR + i * (bw // 2 + 4); w = bw // 2 - 4
        d.rectangle([x0, by, x0 + w, by + 14], fill=(0, 0, 0, 200))
        d.rectangle([x0 + 2, by + 2, x0 + 2 + (w - 4) * val, by + 12], fill=col + (255,))
    return lay


def money():
    lay = L(); d = ImageDraw.Draw(lay); f = sans(64, 800); txt = '$1.000.000'
    w = f.getlength(txt)
    d.text((W - 60 - w, 150), txt, font=f, fill=(120, 205, 98, 255), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    return lay


def banner():
    lay = L(); d = ImageDraw.Draw(lay)
    d.rectangle([0, 560, W, 760], fill=(0, 0, 0, 150))
    f1 = sans(40, 800); f2 = sans(92, 900)
    for txt, f, y, col in [('NOVA MISSÃO', f1, 585, (255, 255, 255)), ('Joia pra Lucia', f2, 632, YEL)]:
        w = f.getlength(txt); d.text(((W - w) / 2, y), txt, font=f, fill=col + (255,), stroke_width=5 if f is f2 else 3, stroke_fill=(0, 0, 0, 255))
    return lay


def mission_done():
    lay = L(); d = ImageDraw.Draw(lay); f = sans(112, 900)
    for i, ln in enumerate(['MISSÃO', 'CUMPRIDA']):
        w = f.getlength(ln); d.text(((W - w) / 2, 330 + i * 132), ln, font=f, fill=YEL + (255,), stroke_width=10, stroke_fill=(0, 0, 0, 255))
    lay.alpha_composite(outline(['+ ela disse sim'], size=64, y=612, em='💍'))
    return lay


A = lambda im: np.asarray(im, np.float32)
MONEY = A(money()); BANNER = A(banner()); DONE = A(mission_done())
OBJ1 = A(outline(['Compre a melhor joia', 'para a Lucia.'], size=52, y=1250, hl=['joia']))
OBJ2 = A(outline(['Vá até a Shimmer Joias.'], size=52, y=1250, hl=['shimmer', 'joias']))
CAP1 = A(outline(['Na vida real você também', 'precisa dar uma joia pra ela'], size=60, y=300, em='💍'))
CAP2 = A(outline(['Mas de boa qualidade:', 'ouro 18k e garantia vitalícia'], size=58, y=300))

# end card (pattern + official logo)
P = Image.open('/home/user/print/assets/pattern-logo.jpg').convert('RGB')
sc = H / P.height; P = P.resize((round(P.width * sc), H), Image.LANCZOS); P = P.crop(((P.width - W) // 2, 0, (P.width - W) // 2 + W, H))
a = np.asarray(P, np.float32); yy = np.arange(H, dtype=np.float32)[:, None, None]; xx = np.arange(W, dtype=np.float32)[None, :, None]
g = np.exp(-(((xx - W / 2) / 520) ** 2 + ((yy - 860) / 480) ** 2)) * 0.8
E = Image.fromarray((a * (1 - g) + np.array(IV, np.float32) * g).astype(np.uint8)).convert('RGBA')
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')
lx = (W - LOGO.width) // 2; al = Image.new('L', (W, H), 0); al.paste(LOGO.getchannel('A'), (lx, 483))
shd = Image.new('RGBA', (W, H), (60, 45, 25, 0)); shd.putalpha(al.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))); E.alpha_composite(shd); E.alpha_composite(LOGO, (lx, 480))
y = 720
t_ = solid_text('NO JOGO É VIRTUAL.', caps_font(46, 600), INK, 6); paste(E, t_, W / 2, y, anchor='center'); y += ink_size(t_)[1] + 20
t_ = gold_text('Aqui é pra sempre.', script_font(128)); paste(E, t_, W / 2, y, anchor='center'); y += ink_size(t_)[1] + 40
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 44
for txt, f, col, tr in [('JOIAS FEITAS À MÃO · OURO 18K', caps_font(34, 600), INK, 4), ('AGENDE SUA VISITA · LINK NA BIO', caps_font(34, 700), BR, 4),
                        ('atendimento na loja ou online', sans(32, 500), PARCEL_COLOR, 0)]:
    t_ = solid_text(txt, f, col, tr); paste(E, t_, W / 2, y, anchor='center'); y += ink_size(t_)[1] + 24
ENDA = np.asarray(E.convert('RGB'), np.float32)


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def smooth(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)


def over(f, arr, k, dy=0):
    if k <= 0.003: return f
    a = np.roll(arr, int(dy), axis=0) if dy else arr; al = a[..., 3:4] / 255 * k
    return f * (1 - al) + a[..., :3] * al


def clip_frames(kind, s, d):
    src = BENCH if kind == 'bench' else ALI
    vf = ('fps=30,scale=1080:1920:flags=lanczos,hqdn3d=1.5:1:4:3,eq=contrast=1.04:saturation=1.05:gamma=1.03' if kind == 'bench'
          else 'fps=30,crop=810:1440:640:0,scale=1080:1920:flags=lanczos,eq=contrast=1.03:saturation=1.04')
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', str(s), '-t', str(d), '-i', src, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
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
T = 0.0; AUD = []; EVT = {}
for i, (kind, s, d) in enumerate(SEG):
    n = int(round(d * FPS)); EVT[i] = T
    if kind in ('bench', 'ali'): AUD.append((T, kind, s, d)); gen = clip_frames(kind, s, d); last = None
    for j in range(n):
        t = j / FPS; tg = T + t
        if kind in ('bench', 'ali'):
            fr = next(gen, None); last = fr if fr is not None else last
            need = (not PREV) or any(abs(tg - p) < 0.5 / FPS for p in PREV) or j == n - 1
            if not need: continue
            if i == 1: f = zoom(last, 1.0 + 0.45 * ease(t / 0.25), W * 0.56, H * 0.47)
            elif i == 2: f = zoom(last, 1.0 + 0.28 * smooth(t / d), W * 0.5, H * 0.52)
            else: f = zoom(last, 1.0 + 0.04 * t / d)
            if j == n - 1: FREEZE = f.copy()
            # HUD (always on during gameplay)
            khud = ease(tg / 0.4)
            f = over(f, A(minimap(tg)), khud); f = over(f, MONEY, khud)
            if i == 0:
                kb = ease((t - 0.3) / 0.3) * (1 - smooth((t - 2.5) / 0.35)); f = over(f, BANNER, kb)
                f = over(f, OBJ1, ease((t - 1.0) / 0.3))
            if i == 1: f = over(f, CAP1, ease(t / 0.35), (1 - ease(t / 0.35)) * 18)
            if i == 2:
                f = over(f, CAP2, ease(t / 0.35), (1 - ease(t / 0.35)) * 18); f = over(f, OBJ2, ease((t - 0.8) / 0.3))
        elif kind == 'mission':
            if PREV and not any(abs(tg - p) < 0.5 / FPS for p in PREV): continue
            g = FREEZE.mean(2, keepdims=True); f = (FREEZE * 0.55 + g * 0.45) * (1 - 0.30 * smooth(t / 0.3))
            sc_ = 1.25 - 0.25 * ease(t / 0.25)
            dn = DONE if sc_ <= 1.001 else np.asarray(Image.fromarray(DONE.astype(np.uint8), 'RGBA').resize((int(W * sc_), int(H * sc_)), Image.BICUBIC)
                                                      .crop((int((W * sc_ - W) / 2), int((H * sc_ - H) / 2), int((W * sc_ - W) / 2) + W, int((H * sc_ - H) / 2) + H)), np.float32)
            f = over(f, dn, min(1.0, t / 0.18))
        else:
            if PREV and not any(abs(tg - p) < 0.5 / FPS for p in PREV): continue
            f = ENDA
        out = np.clip(f, 0, 255).astype(np.uint8)
        if PREV:
            if any(abs(tg - p) < 0.5 / FPS for p in PREV): Image.fromarray(out).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/hud_{tg:05.2f}.jpg', quality=85)
        else: enc.stdin.write(out.tobytes())
    if kind in ('bench', 'ali'):
        for _ in gen: pass
    T += d
if PREV: print('prev ok', T); sys.exit()
enc.stdin.close(); enc.wait()
sr = 48000; n = int(sr * T); mix = np.zeros((n, 2), np.float32)
for t0, kind, s, d in AUD:
    if kind != 'bench': continue
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(s), '-t', str(d), '-i', BENCH, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2) * 0.3; i0 = int(t0 * sr); L_ = min(len(a), n - i0)
    fd = np.ones(L_, np.float32); fl = int(0.03 * sr); fd[:fl] = np.linspace(0, 1, fl); fd[-fl:] = np.linspace(1, 0, fl)
    mix[i0:i0 + L_] += a[:L_] * fd[:, None]
def chime(t0, notes, step, amp):
    tt = np.arange(int(1.4 * sr)) / sr; ch = np.zeros_like(tt)
    for k_, fq in enumerate(notes):
        tk = np.clip(tt - k_ * step, 0, None); ch += np.sin(2 * np.pi * fq * tk) * np.exp(-3.2 * tk) * (tt >= k_ * step)
    i0 = int(t0 * sr); L_ = min(len(ch), n - i0); mix[i0:i0 + L_] += (ch[:L_] * amp)[:, None].astype(np.float32)
chime(EVT[0] + 0.3, (392.0, 523.3), 0.12, 0.07)                 # 'new mission' blip
chime(EVT[3], (523.3, 659.3, 784.0, 1046.5), 0.09, 0.09)        # 'mission complete'
with wave.open(D + '_som.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_video.mp4', '-i', D + '_som.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', D + 'reels-missao-joia-pra-lucia.mp4'], check=True)
print('ok', T)
