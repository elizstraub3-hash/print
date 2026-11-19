"""Short Story video (7 s) of the holiday notice: text lines rise in one by one over a slow push-in.
Kept at the photo's native 9:16 size (942x1672) so the photo is not upscaled."""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
from story_nativo_lib import emoji

D = '/home/user/print/stories/feriado/'
INK = (58, 45, 34); BR = (132, 101, 46); SOFT = (100, 92, 84)
FPS, DUR = 30, 7.0


def layers(W, H):
    k = W / 1080; out = []
    def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
    def C(im, lay, y): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]
    a = L(); y = C(a, solid_text('AVISO', caps_font(int(30 * k), 600), BR, int(12 * k)), 270)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 50 * k, y + 22 * k), (W / 2 + 50 * k, y + 22 * k)], fill=255, width=3); a.alpha_composite(gold_fill(m)); out.append((a, 0.2))
    b = L(); y = C(b, gold_text('Amanhã é feriado', script_font(int(122 * k))), y + 44 * k); out.append((b, 0.6))
    c = L(); y = C(c, solid_text('NESTA SEXTA (20/11) NÃO TEREMOS ATENDIMENTO', caps_font(int(27 * k), 600), INK, int(3 * k)), y + 26 * k); out.append((c, 1.4))
    d = L(); y = C(d, solid_text('Retornamos na segunda-feira', sans(int(40 * k), 600), INK), y + 34 * k); out.append((d, 2.1))
    e = L(); t = solid_text('Mas qualquer dúvida, respondemos no direct', sans(int(34 * k), 500), SOFT)
    tw = ink_size(t)[0]; em = emoji('💬', int(40 * k))
    paste(e, t, W / 2 - (em.width + 10) / 2, y + 22 * k, anchor='center')
    e.alpha_composite(em, (int(W / 2 + tw / 2 - (em.width + 10) / 2 + 10), int(y + 20 * k))); out.append((e, 2.8))
    return out


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def render(bg, out):
    src = Image.open(D + bg).convert('RGB')
    W, H = src.width + src.width % 2, src.height + src.height % 2
    src = src.resize((W, H), Image.LANCZOS) if (W, H) != src.size else src
    L = [(np.asarray(l, np.float32), t0) for l, t0 in layers(W, H)]
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + out], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)):
        t = n / FPS
        z = 1.0 + 0.035 * t / DUR                                  # very slow push-in on the ring (bottom)
        cw, ch = W / z, H / z
        f = np.asarray(src.crop(((W - cw) / 2, H - ch, (W + cw) / 2, H)).resize((W, H), Image.LANCZOS), np.float32)
        for arr, t0 in L:
            k = ease((t - t0) / 0.6)
            if k <= 0: continue
            lay = np.roll(arr, int(round((1 - k) * 18)), axis=0); al = lay[..., 3:4] / 255 * k
            f = f * (1 - al) + lay[..., :3] * al
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()


render('fundo-solitario.png', 'story-feriado-solitario.mp4')
render('fundo-tres-aneis.png', 'story-feriado-tres-aneis.mp4')
print('ok')
