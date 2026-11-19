"""Composite: stabilized plate + grade (light/colour) + Blender helicopter + snow + bloom -> Reels 1080x1920."""
import sys, json, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = '/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
HELI = sys.argv[1] if len(sys.argv) > 1 else S + 'heli_seq/'
OUT = '/home/user/print/clientes/barbearia-natal/reels-natal-helicoptero.mp4'
PREV = [int(x) for x in sys.argv[2:]]
W, H, FPS = 1080, 1920, 30
TR = json.load(open('/home/user/print/clientes/barbearia-natal/track_stab.json'))

yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
xx = np.linspace(-1, 1, W, dtype=np.float32)[None, :, None]
VIG = 1 - 0.22 * (xx ** 2 * 0.6 + (yy * 2 - 1) ** 2 * 0.4)            # soft vignette
SKYND = np.clip(1 - yy / 0.42, 0, 1) ** 1.5                               # graduated filter on the sky


def grade(f):
    x = f.astype(np.float32) / 255
    # lift the building (shadows/mids), keep highlights
    x = np.clip((x - 0.02) / 0.96, 0, 1)
    x = x ** 0.86
    # S contrast
    x = x + 0.22 * x * (1 - x) * (x - 0.5) * 2
    # vibrance (reds of the facade, blue of the sky)
    g = x.mean(2, keepdims=True); sat = x.max(2, keepdims=True) - x.min(2, keepdims=True)
    x = np.clip(g + (x - g) * (1.0 + 0.45 * (1 - sat)), 0, 1)
    # deeper sky: darken + slight blue only at the top
    x = x * (1 - 0.18 * SKYND) + np.array([0.0, 0.01, 0.05], np.float32) * SKYND
    # warm Christmas mood: warm highlights, teal-free shadows
    lum = x.mean(2, keepdims=True)
    x = x + (np.array([0.035, 0.012, -0.03], np.float32) * lum)
    x = x * VIG
    return np.clip(x, 0, 1)


# ---- snow: 3 depth layers, deterministic ----
rng = np.random.default_rng(7)
N = 260
layer = rng.choice([0, 1, 2], N, p=[0.55, 0.3, 0.15])
SX = rng.uniform(0, W, N); SY = rng.uniform(-H, H, N)
SIZE = np.array([2.2, 4.0, 7.5])[layer] * rng.uniform(0.7, 1.3, N)
SPEED = np.array([70, 120, 210])[layer] * rng.uniform(0.8, 1.2, N)        # px / s
SWAY = rng.uniform(10, 35, N); PH = rng.uniform(0, 6.28, N); ALPHA = np.array([0.55, 0.75, 0.9])[layer]


def snow(t):
    lay = Image.new('L', (W, H), 0); d = ImageDraw.Draw(lay)
    big = Image.new('L', (W, H), 0); db = ImageDraw.Draw(big)
    for i in range(N):
        y = (SY[i] + SPEED[i] * t) % (H + 40) - 20
        x = (SX[i] + SWAY[i] * math.sin(t * 1.3 + PH[i]) + 18 * t) % W
        r = SIZE[i]
        (db if layer[i] == 2 else d).ellipse([x - r, y - r, x + r, y + r], fill=int(255 * ALPHA[i]))
    a = np.asarray(lay.filter(ImageFilter.GaussianBlur(0.8)), np.float32) + np.asarray(big.filter(ImageFilter.GaussianBlur(3.0)), np.float32)
    return np.clip(a / 255, 0, 1)[..., None]


def heli_layer(n):
    """Blender RGBA frame, shifted with a fraction of the camera move (far object = small parallax)."""
    im = Image.open(HELI + f'h_{n + 1:04d}.png').convert('RGBA')
    m = np.array(TR[n]); dx, dy = 0.08 * m[0, 2], 0.10 * m[1, 2]
    rot = math.degrees(math.atan2(m[1, 0], m[0, 0]))
    im = im.rotate(-rot * 0.6, resample=Image.BICUBIC, center=(W / 2, H * 0.28), translate=(dx, dy))
    a = np.asarray(im, np.float32) / 255
    rgb, al = a[..., :3], a[..., 3:4]
    # bloom from the Christmas bulbs (very bright saturated pixels)
    br = (rgb.max(2) > 0.96) & ((rgb.max(2) - rgb.min(2)) > 0.62)
    glow = Image.fromarray((rgb * br[..., None] * al * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))
    return rgb, al, np.asarray(glow, np.float32) / 255


def frame(n, plate):
    x = grade(plate)
    rgb, al, glow = heli_layer(n)
    x = x * (1 - al) + rgb * al
    x = np.clip(x + glow * 1.4, 0, 1)
    s = snow(n / FPS)
    x = x * (1 - s) + np.array([0.97, 0.97, 1.0], np.float32) * s
    return (x * 255 + 0.5).astype(np.uint8)


dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', S + 'barb_stab.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = None if PREV else subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart', '-c:a', 'aac', OUT], stdin=subprocess.PIPE)
n = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3 or n >= len(TR): break
    if not PREV or n in PREV:
        f = frame(n, np.frombuffer(b, np.uint8).reshape(H, W, 3))
        if PREV: Image.fromarray(f).save(S + f'bc_{n}.jpg', quality=90)
        else: enc.stdin.write(f.tobytes())
    n += 1
dec.kill()
if enc: enc.stdin.close(); enc.wait()
print('ok', n)
