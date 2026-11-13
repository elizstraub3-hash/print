import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from story_nativo_lib import emoji, sans

S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
OUT = sys.argv[1]
W, H, FPS = 1080, 1920, 30
F = sans(64, 900)

# (clip, start, end, lines, emoji, text centre y)
SC = [
    ('s8', 0.0, 2.6, ['POV: fui na Shimmer', '“só dar uma', 'olhadinha”'], '👀', 400),
    ('s9', 0.2, 3.0, ['aí o Júnior trouxe', 'a bandeja inteira'], '😳', 430),
    ('s10', 0.0, 2.4, ['“só pra experimentar”...'], None, 1390),
    ('s10', 2.6, 6.5, ['já mandei print', 'pro meu namorado'], '💍', 1370),
]


def caption(lines, emo, cy):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    asc, desc = F.getmetrics()
    lh = asc + desc + 6
    e = emoji(emo, 74) if emo else None
    y0 = cy - lh * len(lines) / 2
    for i, s in enumerate(lines):
        tw = F.getlength(s)
        extra = (e.width + 16) if (e and i == len(lines) - 1) else 0
        x = 70 if len(lines) == 3 else W / 2 - (tw + extra) / 2
        d.text((x, y0 + i * lh), s, font=F, fill='white', stroke_width=7, stroke_fill='black')
        if extra:
            lay.alpha_composite(e, (int(x + tw + 16), int(y0 + i * lh + lh / 2 - e.height / 2 - 4)))
    assert lay.getbbox()[0] > 40 and lay.getbbox()[2] < W - 40, lines
    return lay


def frames(name, a, b):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-t', str(b - a), '-i', S + f'inst2/hd/{name}.mp4',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    arr = np.frombuffer(p, np.uint8).reshape(-1, H, W, 3)
    return arr


enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                        '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for name, a, b, lines, emo, cy in SC:
    fr = frames(name, a, b)
    cap = caption(lines, emo, cy)
    n = len(fr)
    for i, f in enumerate(fr):
        im = Image.fromarray(f)
        z = 1.0 + 0.05 * i / n                      # slow punch-in keeps each cut alive
        if z > 1.001:
            cw, ch = W / z, H / z
            im = im.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.LANCZOS)
        im = im.convert('RGBA')
        k = min(1.0, 0.86 + 0.14 * i / 3)          # 3-frame pop, text visible from frame 1
        if k < 1:
            c = cap.resize((int(W * k), int(H * k)), Image.LANCZOS)
            tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            tmp.alpha_composite(c, (int((W - c.width) / 2), int(cy * (1 - k))))
            im.alpha_composite(tmp)
        else:
            im.alpha_composite(cap)
        enc.stdin.write(np.asarray(im.convert('RGB')).tobytes())
enc.stdin.close(); enc.wait()
