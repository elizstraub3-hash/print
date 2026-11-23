"""Story 'Atendimento com o Júnior' (13 s): Júnior opens the boxes -> ring on the client's hand -> ivory end card.
Source: Drive 'Shimmer – vídeos originais' IMG_0250 / IMG_0259 (only 320x568 on the Drive): FSRCNN x2 + Lanczos,
light denoise, stabilised. Text never over the jewelry: title sits on the wall/plant area at the top."""
import sys, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/user/print')
from shimmer_style import *

D = '/home/user/print/stories/junior-atendimento/'
V = '/home/user/print/videos-drive/'
W, H, FPS = 1080, 1920, 30
INK = (58, 45, 34); BR = (118, 88, 38); IVORY = (250, 247, 241)
G = "hqdn3d=2:1.5:6:5,eq=contrast=1.05:saturation=1.04:gamma=1.05,colortemperature=temperature=6000:mix=0.35"
CLIPS = [('IMG_0250.MOV', 2.4, 7.6), ('IMG_0259.MOV', 4.0, 9.4)]
END = 3.0
sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel('/home/user/print/loja/institucional-scripts/FSRCNN_x2.pb'); sr.setModel('fsrcnn', 2)


def frames(f, a, b, tag):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', V + f, '-vf', f"trim={a}:{b},setpts=PTS-STARTPTS,fps=30,vidstabdetect=shakiness=6:accuracy=15:result=/tmp/{tag}.trf", '-f', 'null', '-'], check=True)
    vf = f"trim={a}:{b},setpts=PTS-STARTPTS,fps=30,vidstabtransform=input=/tmp/{tag}.trf:smoothing=18:zoom=5:optzoom=0:interpol=bicubic,{G}"
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', V + f, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    out = []
    while True:
        b_ = dec.stdout.read(320 * 568 * 3)
        if len(b_) < 320 * 568 * 3: break
        im = np.frombuffer(b_, np.uint8).reshape(568, 320, 3)
        up = cv2.resize(sr.upsample(im), (W, H), interpolation=cv2.INTER_LANCZOS4)
        bl = cv2.GaussianBlur(up, (0, 0), 2.0); up = cv2.addWeighted(up, 1.3, bl, -0.3, 0)
        out.append(cv2.cvtColor(up, cv2.COLOR_BGR2RGB).astype(np.float32))
    return out


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def C(im, lay, y): paste(im, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]


# clip 1 title, on a light ivory fade from the top (wall + plant only)
yy = np.arange(H, dtype=np.float32)[:, None, None]
x = np.clip((yy - 330) / (640 - 330), 0, 1); TOPF = 0.82 * (1 - x * x * (3 - 2 * x))
T = []
a = L(); y = C(a, solid_text('ATENDIMENTO PERSONALIZADO', caps_font(34, 600), INK, 6), 250); T.append((a, 0.4))
b = L(); y = C(b, gold_text('Escolha com calma', script_font(132)), y + 18); T.append((b, 0.9))
c = L(); C(c, solid_text('o Júnior te mostra cada detalhe', caps_font(26, 600), BR, 3), y + 22); T.append((c, 1.5))

# end card
E = []
e1 = L(); y = C(e1, solid_text('A SUA PRÓXIMA JOIA', caps_font(36, 600), INK, 6), 700); E.append((e1, 0.15))
e2 = L(); y = C(e2, gold_text('te espera aqui', script_font(140)), y + 18); E.append((e2, 0.45))
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y + 46), (W / 2 + 60, y + 46)], fill=255, width=3)
e3 = L(); e3.alpha_composite(gold_fill(m)); y3 = C(e3, solid_text('AGENDE SUA VISITA · LINK NA BIO', caps_font(30, 600), BR, 4), y + 90)
C(e3, solid_text('Al. Dr. Muricy, 650 · 8º andar · Centro · Curitiba', sans(28, 500), PARCEL_COLOR), y3 + 30); E.append((e3, 0.8))
T = [(np.asarray(l, np.float32), t) for l, t in T]; E = [(np.asarray(l, np.float32), t) for l, t in E]


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def sm(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)


def over(f, layers, t, k_all=1.0):
    for arr, t0 in layers:
        k = ease((t - t0) / 0.6) * k_all
        if k <= 0: continue
        lay = np.roll(arr, int(round((1 - ease((t - t0) / 0.6)) * 18)), axis=0); al = lay[..., 3:4] / 255 * k
        f = f * (1 - al) + lay[..., :3] * al
    return f


c1 = frames(*CLIPS[0], 'j1'); c2 = frames(*CLIPS[1], 'j2')
XF = 12                                                     # 0.4 s cross-dissolve
seq = c1[:-XF] + [c1[-XF + i] * (1 - (i + 1) / (XF + 1)) + c2[i] * ((i + 1) / (XF + 1)) for i in range(XF)] + c2[XF:]
n1 = len(c1) - XF
IV = np.array(IVORY, np.float32)
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + 'story-junior-atendimento.mp4'], stdin=subprocess.PIPE)
total = len(seq) + int(END * FPS)
for n in range(total):
    t = n / FPS
    if n < len(seq):
        f = seq[n].copy()
        kt = 1 - sm((n - (n1 - 18)) / 18)                       # title leaves before the dissolve
        if kt > 0:
            f = f * (1 - TOPF * kt) + IV * TOPF * kt
            f = over(f, T, t, kt)
        ke = sm((n - (len(seq) - 15)) / 15)                    # fade to ivory at the end of clip 2
        if ke > 0: f = f * (1 - ke) + IV * ke
    else:
        f = np.broadcast_to(IV, (H, W, 3)).copy()
        f = over(f, E, (n - len(seq)) / FPS)
    out = np.clip(f, 0, 255).astype(np.uint8)
    if n in (45, len(seq) - 40, total - 1):
        Image.fromarray(out).save(D + f'prev_{n}.jpg', quality=90)
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait(); print('ok', total / FPS)
