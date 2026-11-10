import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
W, H, FPS = 720, 1280, 30
F = ImageFont.truetype(S + 'fonts/Montserrat.ttf', 44); F.set_variation_by_axes([900])
F2 = ImageFont.truetype(S + 'fonts/Montserrat.ttf', 30); F2.set_variation_by_axes([800])
def cap(lines, y0=210, font=F, lh=58, sub=None):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k, ln in enumerate(lines):
        d.text(((W - font.getlength(ln)) / 2, y0 + k * lh), ln, font=font, fill=(255, 255, 255, 255), stroke_width=5, stroke_fill=(15, 15, 15, 255))
    if sub:
        y = y0 + len(lines) * lh + 18
        d.text(((W - F2.getlength(sub)) / 2, y), sub, font=F2, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(15, 15, 15, 255))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(lay.split()[3].filter(ImageFilter.GaussianBlur(7)).point(lambda v: int(v * .5)))
    o = Image.new('RGBA', (W, H), (0, 0, 0, 0)); o.alpha_composite(sh, (0, 5)); o.alpha_composite(lay)
    a = np.asarray(o, np.float32); return a[..., :3], a[..., 3:4] / 255
# segment times in the joined video: gate 0-4, door/room 4-11.4, client 11.4-20.1, rings 20.1-29.1
CAPS = [(0.0, 5.5, cap(['Vem conhecer a', 'Shimmer por dentro'])),
        (5.5, 9.5, cap(['Você é recebida', 'na porta'])),
        (9.5, 16.9, cap(['Um espaço pensado', 'para o seu momento'])),
        (16.9, 25.6, cap(['Atendimento com', 'calma e atenção'])),
        (25.6, 31.1, cap(['Aqui você escolhe', 'a joia da sua história'])),
        (31.1, 34.7, cap(['Venha nos visitar'], sub='Shimmer Joias · Curitiba · Ouro 18k'))]
src, out = sys.argv[1], sys.argv[2]; prev = sys.argv[3:]
dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = None if prev else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', out], stdin=subprocess.PIPE)
n = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    t = n / FPS; f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
    for a, z, (rgb, al) in CAPS:
        if a <= t < z: f = f * (1 - al) + rgb * al
    f = f.astype(np.uint8)
    if prev and any(abs(t - float(p)) < 0.017 for p in prev): Image.fromarray(f).save(S + f'lj_{t:.1f}.jpg', quality=88)
    elif enc: enc.stdin.write(f.tobytes())
    n += 1
if enc: enc.stdin.close(); enc.wait()
print('frames', n)
