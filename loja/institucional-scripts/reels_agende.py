import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *

P = '/home/user/print/'
IMGS = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/images/'
VID = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/7e0eafea-IMG_9881_1.MOV'
OUT = P + 'loja/reels-agende-e-saia-com-a-sua.mp4'
W, H, FPS = 1080, 1920, 30
INK = (74, 59, 46); BR = (132, 101, 46); IV = np.array([246, 242, 235], np.float32)
yy = np.arange(H, dtype=np.float32)[:, None, None]
TOPF = np.clip(1 - yy / 680, 0, 1) ** 1.3 * 0.84            # light fade behind the top text only


def plate(path):
    """Photo at its own pixels in the centre; a soft blurred copy fills only the leftover edges."""
    src = Image.open(path).convert('RGB')
    iw, ih = src.size
    cw, ch = min(iw, W), min(ih, H)
    crisp = np.asarray(src.crop(((iw - cw) // 2, (ih - ch) // 2, (iw - cw) // 2 + cw, (ih - ch) // 2 + ch)), np.float32)
    k = max(W / iw, H / ih)
    bg = src.resize((int(iw * k) + 1, int(ih * k) + 1), Image.BICUBIC)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40))
    f = np.asarray(bg, np.float32) * 0.92 + IV * 0.08
    px, py = (W - cw) // 2, (H - ch) // 2
    xx = np.arange(W, dtype=np.float32)[None, :, None]
    m = (np.clip((yy - py) / 40, 0, 1) * np.clip((py + ch - yy) / 40, 0, 1) *
         (np.clip((xx - px) / 30, 0, 1) * np.clip((px + cw - xx) / 30, 0, 1) if cw < W else 1))
    full = f.copy(); full[py:py + ch, px:px + cw] = crisp
    f = f * (1 - m) + full * m
    return f + (IV - f) * TOPF


# 4K clip of the Diana ring, downscaled (never upscaled) to 1080x1920
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', VID, '-vf', f'scale={W}:{H}:flags=lanczos,fps={FPS}',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
CLIP = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def clip_plate(start):
    def f(lt):
        fr = CLIP[min(len(CLIP) - 1, int((start + lt) * FPS))].astype(np.float32)
        return fr + (IV - fr) * TOPF
    return f


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def head(caps, script, y=300, size=170):
    a = L(); c = solid_text(caps, caps_font(44, 500), INK, 5); s = gold_text(script, script_font(size))
    assert ink_size(s)[0] < W - 120 and ink_size(c)[0] < W - 120, script
    paste(a, c, W / 2, y, anchor='center'); paste(a, s, W / 2, y + ink_size(c)[1] + 10, anchor='center'); return a


def end_layers():
    a = L(); paste(a, gold_text('Agende sua visita', script_font(118)), W / 2, 640, anchor='center')
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 90, 830), (W / 2 + 90, 830)], fill=255, width=4); a.alpha_composite(gold_fill(m))
    b = L(); paste(b, solid_text('ATENDIMENTO COM HORA MARCADA', caps_font(30, 600), INK, 4), W / 2, 880, anchor='center')
    paste(b, solid_text('pelo WhatsApp · link na bio', sans(34, 500), PARCEL_COLOR), W / 2, 945, anchor='center')
    c = L(); y = 1080
    for t in ['AL. DR. MURICY, 650 · 8º ANDAR', 'CENTRO · CURITIBA – PR']:
        lay = solid_text(t, caps_font(26, 600), BR, 4); paste(c, lay, W / 2, y, anchor='center'); y += ink_size(lay)[1] + 20
    d = L(); paste(d, solid_text('OURO 18K · GARANTIA VITALÍCIA', caps_font(24, 600), BR, 4), W / 2, 1300, anchor='center')
    return [(a, 0.2), (b, 0.6), (c, 1.0), (d, 1.4)]


IVP = np.empty((H, W, 3), np.float32); IVP[:] = IV
SC = [  # (start, end, plate, [(layer, t_in)])
    (0.0, 2.9, plate(IMGS + '6.webp'), [(head('AQUI VOCÊ AGENDA A VISITA', 'e já sai com...', size=150), -1.0)]),
    (2.9, 5.1, plate(P + 'aliancas-revestidas/fotos/52.webp'), [(head('A SUA', 'Aliança'), 0.25)]),
    (5.1, 7.6, clip_plate(1.0), [(head('O SEU', 'Anel de formatura', size=118), 0.25)]),
    (7.6, 9.8, plate(P + 'solitario-helena/fotos/59.webp'), [(head('O SEU', 'Solitário'), 0.25)]),
    (9.8, 13.4, IVP, end_layers()),
]
SCA = [(a, b, p, [(np.asarray(l, np.float32), t) for l, t in ls]) for a, b, p, ls in SC]
DUR = SC[-1][1]; TR = 0.4
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_io(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)


def scene_frame(i, lt):
    a, b, p, ls = SCA[i]
    f = p(lt) if callable(p) else p.copy()
    for arr, t0 in ls:
        k = ease((lt - t0) / 0.6)
        if k <= 0: continue
        lay = np.roll(arr, int(round((1 - k) * 20)), axis=0); al = lay[..., 3:4] / 255 * k
        f = f * (1 - al) + lay[..., :3] * al
    return f


def frame(t):
    for i, (a, b, p, ls) in enumerate(SCA):
        if a <= t < b or (i == len(SCA) - 1 and t >= a): break
    f = scene_frame(i, t - a)
    if i > 0 and t - a < TR:
        sft = int(round(ease_io((t - a) / TR) * W))
        prev = scene_frame(i - 1, t - SCA[i - 1][0])
        out = prev.copy()
        if sft > 0:
            out[:, :W - sft] = prev[:, sft:]
            out[:, W - sft:] = f[:, :sft]
        f = out
    return np.clip(f, 0, 255).astype(np.uint8)


if len(sys.argv) > 1 and sys.argv[1] == 'prev':
    for t in map(float, sys.argv[2:]): Image.fromarray(frame(t)).save(f'/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/ag_{t}.jpg', quality=88)
    sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', OUT], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
