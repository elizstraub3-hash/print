import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print/black-friday-kit')
sys.argv_backup = sys.argv; sys.argv = ['x']
exec(open('/home/user/print/black-friday-kit/bf_kit.py').read().split("if __name__")[0])
sys.argv = sys.argv_backup
from story_nativo_lib import emoji

W, H, FPS = 1080, 1920, 30
OUT = D + 'story-black-friday-zoom.mp4'
PREV = [float(x) for x in sys.argv[1:]]


def full(n):
    ph = photo(n)                               # 1080 x 1919
    f = np.empty((H, W, 3), np.float32); f[:] = ph[-1]; f[:len(ph)] = ph[:H]
    return f


P66, P63, P64 = full(66), full(63), full(64)

# tiny "secret" text written on the white table, in photo coordinates, drawn at 2x for a crisp zoom
TX, TY = 760, 1640
SEC = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0))
d = ImageDraw.Draw(SEC); f2 = sans(44, 700); INKD = (70, 55, 40, 255)
for i, s in enumerate(['psiu… compre o par', 'de alianças e ganhe', 'o solitário']):
    d.text((TX * 2, TY * 2 - 60 + i * 56), s, font=f2, fill=INKD, anchor='mm')
e = emoji('🤫', 46); SEC.alpha_composite(e, (int(TX * 2 + f2.getlength('o solitário') / 2 + 10), int(TY * 2 + 52 - 26)))
SECA = np.asarray(SEC, np.float32)


def zoomed(img, z, cx, cy, layer=None):
    cw, ch = W / z, H / z
    x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
    out = np.asarray(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BICUBIC), np.float32)
    if layer is not None:
        lay = Image.fromarray(layer.astype(np.uint8), 'RGBA').crop((x0 * 2, y0 * 2, (x0 + cw) * 2, (y0 + ch) * 2)).resize((W, H), Image.LANCZOS)
        la = np.asarray(lay, np.float32); al = la[..., 3:4] / 255
        out = out * (1 - al) + la[..., :3] * al
    return out


def veil(f, solid, end, k=0.84):
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    x = np.clip((yy - solid) / (end - solid), 0, 1)
    v = k * (1 - x * x * (3 - 2 * x))
    return f * (1 - v) + BLK * v


def over(f, lay, k=1.0, rise=0):
    if k <= 0: return f
    a = np.asarray(lay, np.float32)
    if rise: a = np.roll(a, rise, axis=0)
    al = a[..., 3:4] / 255 * k
    return f * (1 - al) + a[..., :3] * al


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


# static text layers
K1 = L(); C(K1, gold_text('BLACK FRIDAY SHIMMER', caps_font(36, 600), 10), 300)
K1b = L(); C(K1b, solid_text('leia o detalhe', sans(40, 700), IVT), 365); K1b.alpha_composite(emoji('👀', 44), (int(W / 2 + sans(40, 700).getlength('leia o detalhe') / 2 + 12), 360))
T2 = L(); y = C(T2, gold_text('OURO 18K', caps_font(40, 600), 12), 300); rule(T2, y + 26)
C(T2, gold_text('Solitário de brinde', script_font(118)), y + 56)
T3 = L(); y = C(T3, gold_text('BLACK FRIDAY · ATÉ 18/12', caps_font(36, 600), 10), 290); rule(T3, y + 24)
y = C(T3, solid_text('R$ 3.199,00', sans(100, 600), IVT), y + 50)
y = C(T3, solid_text('em até 10x de R$ 319,90 sem juros', sans(34, 500), SOFT), y + 22)
y = C(T3, gold_text('ou R$ 2.879,10 à vista · 10% OFF', sans(36, 700)), y + 12)
C(T3, solid_text('OURO 18K · GARANTIA VITALÍCIA', caps_font(22, 600), SOFT, 4), y + 22)
T3b = L(); C(T3b, solid_text('PAR DE ALIANÇAS + SOLITÁRIO · GARANTIA VITALÍCIA', caps_font(22, 600), IVT, 3), 1470)


def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def eout(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


SOL63 = (575, 870); SOL64 = (590, 935)   # solitaire centres (for zoom-through)
DUR = 10.0


def frame(t):
    if t < 3.9:                                         # scene 1: the whole kit, then zoom into the tiny secret
        z = 1.0 + 0.03 * t / 1.2 if t < 1.2 else 1.03 + 1.67 * ease((t - 1.2) / 0.8) + 0.05 * max(0, t - 2.0) / 1.6
        if t > 3.6: z += 2.5 * ((t - 3.6) / 0.3) ** 2   # accelerate into the next cut
        cx = W / 2 + (TX - W / 2) * ease((t - 1.0) / 1.0); cy = H / 2 + (TY - H / 2) * ease((t - 1.0) / 1.0)
        f = zoomed(veil(P66, 330, 620, 0.7 * (1 - ease((t - 1.0) / 0.6))) if t < 1.6 else P66, z, cx, cy, SECA)
        kk = 1 - ease((t - 1.0) / 0.4)
        f = over(f, K1, kk); f = over(f, K1b, kk)
        if t > 3.6: f = np.asarray(Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14 * (t - 3.6) / 0.3)), np.float32)
        return f
    if t < 6.8:                                         # scene 2: lands inside the solitaire shot, settling out
        lt = t - 3.9
        z = 1.0 + 0.9 * (1 - eout(lt / 0.7)) + 0.04 * lt / 2.9
        f = veil(P63, 420, 720)
        f = zoomed(f, z, *SOL63)
        if lt < 0.35: f = np.asarray(Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14 * (1 - lt / 0.35))), np.float32)
        f = over(f, T2, eout((lt - 0.4) / 0.6), int(round((1 - eout((lt - 0.4) / 0.6)) * 22)))
        if lt > 2.6:
            f = np.asarray(Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14 * (lt - 2.6) / 0.3)), np.float32)
        return f
    lt = t - 6.8                                        # scene 3: price
    z = 1.0 + 0.9 * (1 - eout(lt / 0.7)) + 0.03 * lt / 3.2
    f = zoomed(veil(P64, 600, 800), z, *SOL64)
    if lt < 0.35: f = np.asarray(Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14 * (1 - lt / 0.35))), np.float32)
    k = eout((lt - 0.4) / 0.6); f = over(f, T3, k, int(round((1 - k) * 22)))
    return f


if PREV:
    for t in PREV:
        Image.fromarray(np.clip(frame(t), 0, 255).astype(np.uint8)).save(f'/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/sz_{t}.jpg', quality=88)
    sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', OUT], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(np.clip(frame(n / FPS), 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
