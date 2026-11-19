"""Reels/Story 9:16 from the 3 solitaire photos retouched in ChatGPT (1536x2048, only downscaled)."""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *

D = '/home/user/print/solitario-retoque/'
W, H, FPS = 1080, 1920, 30
INK = (58, 45, 34); BR = (110, 82, 34); DG = (146, 104, 38)
def gt(text, f):
    """Brand gold-texture lettering (PowerClip), with a faint soft shadow so it holds on the white satin."""
    from PIL import ImageFilter
    lay, bb = gold_text(text, f)
    a = lay.getchannel('A')
    sh = Image.new('RGBA', lay.size, (60, 40, 15, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.35)))
    out = Image.new('RGBA', lay.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 3)); out.alpha_composite(lay)
    return out, bb
# (photo, ring centre in the photo, scene seconds)
SC = [('2382', (666, 1116)), ('2385', (753, 1167)), ('2387', (727, 1198))]
SEG, XF = 3.2, 0.5
DUR = SEG * 3 - XF * 2 + 0.6
K = H / 2048                                   # 0.9375: downscale only


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def C(im, lay, y): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]


def texts():
    a = L(); y = C(a, solid_text('SOLITÁRIO 6 GARRAS', caps_font(32, 700), BR, 10), 330)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 50, y + 22), (W / 2 + 50, y + 22)], fill=255, width=3); a.alpha_composite(gold_fill(m))
    y = C(a, gt('O clássico', script_font(150)), y + 44)
    C(a, solid_text('que nunca sai de moda', sans(40, 600), INK), y + 14)
    b = L(); y = C(b, gt('Ponto de luz', script_font(150)), 360)
    C(b, solid_text('a pedra em destaque, firme em 6 garras', sans(38, 600), INK), y + 14)
    c = L(); y = C(c, gt('Pra ela dizer sim', script_font(128)), 360)
    C(c, solid_text('com garantia vitalícia', sans(38, 600), INK), y + 14)
    t = solid_text('Peça pelo WhatsApp · link na bio', sans(36, 700), (255, 253, 248)); tw, th = ink_size(t)
    box = [W / 2 - tw / 2 - 46, 1560, W / 2 + tw / 2 + 46, 1560 + th + 48]
    pl = L(); ImageDraw.Draw(pl).rounded_rectangle(box, radius=(th + 48) // 2, fill=(40, 32, 25, 235)); c.alpha_composite(pl)
    fr = Image.new('L', (W, H), 0); ImageDraw.Draw(fr).rounded_rectangle(box, radius=(th + 48) // 2, outline=255, width=4); c.alpha_composite(gold_fill(fr))
    paste(c, t, W / 2, 1584, anchor='center')
    return [np.asarray(x, np.float32) for x in (a, b, c)]


PH = [Image.open(D + f'{n}.png').convert('RGB') for n, _ in SC]
TX = texts()


def plate(i, lt):
    src = PH[i]; cx, cy = SC[i][1]
    z = 1.0 + 0.06 * lt / SEG                          # slow push-in toward the ring
    s = K * z                                          # <= 0.995, never upscaled
    cw, ch = W / s, H / s
    x0 = min(max(cx - cw / 2, 0), src.width - cw)
    y0 = min(max(cy - (cy * K) / s - 0, 0), src.height - ch)  # keep the ring where it sits in the frame
    return np.asarray(src.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS), np.float32)


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def scene(i, lt):
    f = plate(i, lt)
    k = ease((lt - 0.35) / 0.7)
    lay = np.roll(TX[i], int(round((1 - k) * 20)), axis=0); al = lay[..., 3:4] / 255 * k
    return f * (1 - al) + lay[..., :3] * al


def frame(t):
    starts = [i * (SEG - XF) for i in range(3)]
    i = max(j for j in range(3) if starts[j] <= t)
    f = scene(i, t - starts[i])
    if i > 0 and t - starts[i] < XF:
        a = (t - starts[i]) / XF; a = a * a * (3 - 2 * a)
        f = scene(i - 1, t - starts[i - 1]) * (1 - a) + f * a
    return np.clip(f, 0, 255).astype(np.uint8)


if len(sys.argv) > 1:
    for t in map(float, sys.argv[1:]): Image.fromarray(frame(t)).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/sr_{t}.jpg', quality=88)
    sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + 'reels-solitario-6-garras.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok', DUR)
