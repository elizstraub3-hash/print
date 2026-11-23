"""Reels 'Ela não pediu muito...' (~20 s) com os vídeos curtos do Drive (Live Photos 1440x1920 + meia aliança no cetim).
Legendas no estilo nativo: letra branca grossa com contorno preto. Fecho com pattern + logo original.
Clipes 1440x1920 recortados no centro para 1080x1920 (pixels nativos, sem ampliar)."""
import sys, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/reels/joia-pra-sempre/'
V = '/home/user/print/videos-drive/'
W, H, FPS = 1080, 1920, 30
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
PREV = [float(x) for x in sys.argv[1:]]
SLOW = 1.25
# (file, start, dur_source, crop) crop 'c' = centre 1080 of 1440 width; 'land' = 1920x1440 landscape -> 810x1440 centre, scaled to 1080x1920
CL = [('IMG_0052.MP4', 0.0, 2.6, 'c', ['Ela não pediu muito...'], None),
      ('IMG_0068.MP4', 0.0, 1.9, 'c', ['só uma joia'], None),
      ('IMG_0074.MP4', 0.0, 2.4, 'c', ['pra usar todo dia'], '🤍'),
      ('IMG_2358.MOV', 3.0, 3.0, 'land', ['e que dure', 'pra sempre'], '💍'),
      ('IMG_2303.MP4', 0.0, 2.1, 'c', ['ouro 18k', 'com garantia vitalícia'], None),
      ('IMG_9882.MP4', 0.0, 2.7, 'c', ['feita à mão, pra ela'], None)]
END = 3.6


def outline(lines, size=66, y=330, em=None):
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(out); fnt = sans(size, 800)
    for i, ln in enumerate(lines):
        w = fnt.getlength(ln); e = emoji(em, int(size * 1.05)) if (em and i == len(lines) - 1) else None
        ew = (e.width + 12) if e else 0; x = (W - w - ew) / 2
        d.text((x, y), ln, font=fnt, fill=(255, 255, 255, 255), stroke_width=max(4, size // 12), stroke_fill=(0, 0, 0, 255))
        if e: out.alpha_composite(e, (int(x + w + 12), int(y + size * 0.05)))
        y += int(size * 1.22)
    return np.asarray(out, np.float32)


# end card
P = Image.open('/home/user/print/assets/pattern-logo.jpg').convert('RGB')
sc = H / P.height; P = P.resize((round(P.width * sc), H), Image.LANCZOS); P = P.crop(((P.width - W) // 2, 0, (P.width - W) // 2 + W, H))
a = np.asarray(P, np.float32); yy = np.arange(H, dtype=np.float32)[:, None, None]; xx = np.arange(W, dtype=np.float32)[None, :, None]
g = np.exp(-(((xx - W / 2) / 520) ** 2 + ((yy - 860) / 480) ** 2)) * 0.8
E = Image.fromarray((a * (1 - g) + np.array(IV, np.float32) * g).astype(np.uint8)).convert('RGBA')
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')
lx = (W - LOGO.width) // 2; al = Image.new('L', (W, H), 0); al.paste(LOGO.getchannel('A'), (lx, 483))
shd = Image.new('RGBA', (W, H), (60, 45, 25, 0)); shd.putalpha(al.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35))); E.alpha_composite(shd); E.alpha_composite(LOGO, (lx, 480))
y = 720
t = solid_text('TENDÊNCIAS PASSAM.', caps_font(46, 600), INK, 6); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 20
t = gold_text('Joias ficam.', script_font(170)); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 40
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 44
for txt, f, col, tr in [('OURO 18K · GARANTIA VITALÍCIA', caps_font(34, 600), INK, 4), ('AGENDE SUA VISITA · LINK NA BIO', caps_font(34, 700), BR, 4),
                        ('atendimento na loja ou online', sans(32, 500), PARCEL_COLOR, 0)]:
    t = solid_text(txt, f, col, tr); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 24
ENDA = np.asarray(E.convert('RGB'), np.float32)


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def frames(f, s, d, mode):
    vf = (f"setpts={SLOW}*PTS,fps=30," + ("crop=1080:1920:180:0" if mode == 'c' else "crop=810:1440:555:0,scale=1080:1920:flags=lanczos")
          + ",eq=contrast=1.03:saturation=1.04")
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-ss', str(s), '-t', str(d), '-i', V + f, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


XF = 8   # crossfade frames between clips
CAPS = [outline(c[4], em=c[5]) for c in CL]
out_frames = []
enc = None
if not PREV:
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-an', D + '_video.mp4'], stdin=subprocess.PIPE)
T = 0; prev_tail = None; n_out = 0
for ci, (f, s, d, mode, _, _) in enumerate(CL):
    fr = list(frames(f, s, d, mode))
    for j, x in enumerate(fr):
        t = j / FPS; tg = n_out / FPS
        img = x.astype(np.float32)
        z = 1.0 + 0.04 * j / len(fr)
        if z > 1.001:
            cw, ch = W / z, H / z
            img = np.asarray(Image.fromarray(x).crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.LANCZOS), np.float32)
        if prev_tail is not None and j < XF:
            k = (j + 1) / (XF + 1); img = prev_tail * (1 - k) + img * k
        cap = CAPS[ci]; kk = ease(t / 0.35)
        al = cap[..., 3:4] / 255 * kk; capr = np.roll(cap, int((1 - kk) * 18), axis=0)
        img = img * (1 - al) + capr[..., :3] * al
        o = np.clip(img, 0, 255).astype(np.uint8)
        if PREV:
            if any(abs(tg - p) < 0.5 / FPS for p in PREV): Image.fromarray(o).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/jp_{tg:05.2f}.jpg', quality=85)
        else: enc.stdin.write(o.tobytes())
        n_out += 1
    prev_tail = fr[-1].astype(np.float32)
for j in range(int(END * FPS)):
    k = ease(j / 12); img = prev_tail * (1 - k) + ENDA * k
    o = np.clip(img, 0, 255).astype(np.uint8); tg = n_out / FPS
    if PREV:
        if any(abs(tg - p) < 0.5 / FPS for p in PREV): Image.fromarray(o).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/jp_{tg:05.2f}.jpg', quality=85)
    else: enc.stdin.write(o.tobytes())
    n_out += 1
TOTAL = n_out / FPS
if PREV: print('prev ok', TOTAL); sys.exit()
enc.stdin.close(); enc.wait()
# silent track: she adds the trending audio in the Instagram app
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_video.mp4', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
                '-c:v', 'copy', '-c:a', 'aac', '-movflags', '+faststart', D + 'reels-ela-nao-pediu-muito.mp4'], check=True)
print('ok', TOTAL)
