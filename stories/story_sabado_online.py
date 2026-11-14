import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
from story_nativo_lib import emoji

VID = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/7e0eafea-IMG_9881_1.MOV'
OUT = '/home/user/print/stories/story-sabado-online.mp4'
PREV = [float(x) for x in sys.argv[1:]]
W, H, FPS, DUR = 1080, 1920, 30, 8.0
SW, SH = 2160, 3840                          # 4K source, used directly for the zoom (no upscaling)
INK = (74, 59, 46); BR = (132, 101, 46)
TX, TY = 760, 1600                           # the tiny note, bottom-right corner on the plain satin


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
def C(img, lay, y): paste(img, lay, W / 2, y, anchor='center'); return y + ink_size(lay)[1]


# main message (output coordinates)
T1 = L()
y = C(T1, gold_text('Hoje, sábado', script_font(124)), 300)
y = C(T1, solid_text('ATENDIMENTO SOMENTE ONLINE', caps_font(42, 600), INK, 4), y + 22)
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 70, y + 30), (W / 2 + 70, y + 30)], fill=255, width=3); T1.alpha_composite(gold_fill(m))
C(T1, solid_text('chame no WhatsApp · link na bio', sans(32, 500), PARCEL_COLOR), y + 58)

# tiny secret note, drawn at 4K source scale so the zoom stays crisp
NOTE = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
d = ImageDraw.Draw(NOTE); fn = sans(40, 700)
lines = ['mas dá tempo de', 'pedir a aliança dela, tá?']
for i, s in enumerate(lines):
    d.text((TX * 2 - 30, TY * 2 - 26 + i * 52), s, font=fn, fill=INK + (255,), anchor='mm')
e = emoji('😉', 44); NOTE.alpha_composite(e, (int(TX * 2 - 30 + fn.getlength(lines[1]) / 2 + 10), int(TY * 2 + 26 - 24)))
NOTEA = np.asarray(NOTE, np.float32)

# closing call to action
T3 = L()
_t = solid_text('Peça pelo WhatsApp · link na bio', sans(34, 600), PRICE_COLOR); _w, _h = ink_size(_t)
_box = [W / 2 - _w / 2 - 44, 1420, W / 2 + _w / 2 + 44, 1420 + _h + 44]
_m = Image.new('L', (W, H), 0); ImageDraw.Draw(_m).rounded_rectangle(_box, radius=(_h + 44) // 2, fill=255)
_c = Image.new('RGBA', (W, H), (255, 253, 249, 0)); _c.putalpha(_m.point(lambda v: int(v * 0.94))); T3.alpha_composite(_c)
_fr = Image.new('L', (W, H), 0); ImageDraw.Draw(_fr).rounded_rectangle(_box, radius=(_h + 44) // 2, outline=255, width=3); T3.alpha_composite(gold_fill(_fr))
paste(T3, _t, W / 2, 1442, anchor='center')


def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def eout(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def zoom_at(t):
    if t < 1.8: return 1.0, W / 2, H / 2
    if t < 2.7:
        k = ease((t - 1.8) / 0.9); return 1 + 2.4 * k, W / 2 + (TX - W / 2) * k, H / 2 + (TY - H / 2) * k
    if t < 4.9: return 3.4 + 0.08 * (t - 2.7) / 2.2, TX, TY
    k = ease((t - 4.9) / 0.8); return 3.48 - 2.48 * k, TX + (W / 2 - TX) * k, TY + (H / 2 - TY) * k


def over(f, lay, k, rise=0):
    if k <= 0.003: return f
    a = np.asarray(lay, np.float32)
    if rise: a = np.roll(a, rise, axis=0)
    al = a[..., 3:4] / 255 * k
    return f * (1 - al) + a[..., :3] * al


def compose(src, t):
    z, cx, cy = zoom_at(t)
    cw, ch = W / z, H / z
    x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
    box = (x0 * 2, y0 * 2, (x0 + cw) * 2, (y0 + ch) * 2)
    base = Image.fromarray(src).crop(box).resize((W, H), Image.LANCZOS)
    note = Image.fromarray(NOTEA.astype(np.uint8), 'RGBA').crop(box).resize((W, H), Image.LANCZOS)
    base = base.convert('RGBA'); base.alpha_composite(note)
    blur = 0
    if 1.95 < t < 2.55: blur = 6 * np.sin(np.pi * (t - 1.95) / 0.6)
    if 4.95 < t < 5.6: blur = 6 * np.sin(np.pi * (t - 4.95) / 0.65)
    if blur > 0.3: base = base.filter(ImageFilter.GaussianBlur(float(blur)))
    f = np.asarray(base.convert('RGB'), np.float32)
    f = over(f, T1, 1 - ease((t - 1.6) / 0.3))
    k = eout((t - 5.7) / 0.6); f = over(f, T3, k, int(round((1 - k) * 20)))
    k = eout((t - 5.7) / 0.6) * (1 if t > 5.7 else 0); f = over(f, T1, k * 1.0)
    return np.clip(f, 0, 255).astype(np.uint8)


dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', VID, '-vf', f'setpts=1.15*PTS,fps={FPS},scale={SW}:{SH}',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = None if PREV else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', OUT], stdin=subprocess.PIPE)
last = None
for n in range(int(DUR * FPS)):
    b = dec.stdout.read(SW * SH * 3)
    if len(b) == SW * SH * 3: last = np.frombuffer(b, np.uint8).reshape(SH, SW, 3)
    t = n / FPS
    if PREV:
        if any(abs(t - p) < 0.5 / FPS for p in PREV):
            Image.fromarray(compose(last, t)).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/sb_{t:.1f}.jpg', quality=88)
        continue
    enc.stdin.write(compose(last, t).tobytes())
dec.kill()
if enc: enc.stdin.close(); enc.wait()
print('ok')
