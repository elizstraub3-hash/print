"""Story 'Ótima semana' (video 7 s + still) on Shimmer_Fundo_Story_6 from the Drive (native 941x1672, never upscaled)."""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/stories/otima-semana/'
IVT = (255, 251, 243)
FPS, DUR = 30, 7.0
src = Image.open(D + 'fundo-6.png').convert('RGB')
W, H = src.width + src.width % 2, src.height
src = src.resize((W, H), Image.LANCZOS) if W != src.width else src
k = W / 1080


def shadowed(lay_bb, blur=7, alpha=0.55, dy=3):
    """Soft dark shadow under a text layer so it reads on the wood."""
    lay, bb = lay_bb
    a = lay.getchannel('A')
    sh = Image.new('RGBA', lay.size, (25, 15, 5, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha)))
    out = Image.new('RGBA', lay.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, dy)); out.alpha_composite(lay)
    return out, bb


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def C(im, lay, y): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]


layers = []
a = L(); y = C(a, shadowed(solid_text('SEGUNDA-FEIRA', caps_font(int(32 * k), 600), IVT, int(12 * k))), 250)
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 50 * k, y + 22 * k), (W / 2 + 50 * k, y + 22 * k)], fill=255, width=3); a.alpha_composite(gold_fill(m))
layers.append((a, 0.2))
b = L(); y = C(b, shadowed(gold_text('Ótima semana', script_font(int(150 * k)))), y + 44 * k); layers.append((b, 0.6))
c = L(); y = C(c, shadowed(solid_text('que ela brilhe tanto quanto as nossas joias', sans(int(36 * k), 600), IVT)), y + 22 * k); layers.append((c, 1.4))
d = L(); t = shadowed(solid_text('e fique de olho: sexta tem Black Friday', sans(int(32 * k), 500), IVT))
tw = ink_size(t)[0]; e = emoji('🖤', int(38 * k))
paste(d, t, W / 2 - (e.width + 10) / 2, y + 18 * k, anchor='center')
d.alpha_composite(e, (int(W / 2 + tw / 2 - (e.width + 10) / 2 + 10), int(y + 16 * k))); layers.append((d, 2.2))
LA = [(np.asarray(l, np.float32), t0) for l, t0 in layers]


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def frame(t):
    z = 1.0 + 0.035 * t / DUR                                  # slow push-in toward the hand (bottom)
    cw, ch = W / z, H / z
    f = np.asarray(src.crop(((W - cw) / 2, H - ch, (W + cw) / 2, H)).resize((W, H), Image.LANCZOS), np.float32)
    for arr, t0 in LA:
        kk = ease((t - t0) / 0.6)
        if kk <= 0: continue
        lay = np.roll(arr, int(round((1 - kk) * 18)), axis=0); al = lay[..., 3:4] / 255 * kk
        f = f * (1 - al) + lay[..., :3] * al
    return np.clip(f, 0, 255).astype(np.uint8)


Image.fromarray(frame(6.9)).save(D + 'story-otima-semana.jpg', quality=95, subsampling=0)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + 'story-otima-semana.mp4'], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
