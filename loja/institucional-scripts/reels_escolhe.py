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
SC = [  # (clip, start, end, lines, emoji, centre y, left-aligned, comedy zoom)
    ('s8', 0.0, 2.6, ['Ele: “amor,', 'escolhe o que', 'você quiser”'], '🥰', 400, True, False),
    ('s9', 0.3, 2.8, ['Eu, que nunca', 'recuso um desafio:'], '😈', 430, False, False),
    ('s10', 0.0, 2.4, ['“vou só experimentar', 'esse aqui...”'], None, 1390, False, False),
    ('s10', 2.6, 4.0, ['ele vendo o preço:'], '😳', 1400, False, True),
    ('s10', 4.0, 6.5, ['Júnior: “10x sem juros”', 'ele:'], '😌', 1440, False, False),
]


def caption(lines, emo, cy, left):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    asc, desc = F.getmetrics()
    lh = asc + desc + 6
    e = emoji(emo, 74) if emo else None
    y0 = cy - lh * len(lines) / 2
    for i, s in enumerate(lines):
        tw = F.getlength(s)
        extra = (e.width + 16) if (e and i == len(lines) - 1) else 0
        x = 70 if left else W / 2 - (tw + extra) / 2
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
for name, a, b, lines, emo, cy, left, zoom in SC:
    fr = frames(name, a, b)
    cap = caption(lines, emo, cy, left)
    n = len(fr)
    for i, f in enumerate(fr):
        im = Image.fromarray(f)
        if zoom:                                     # snap comedy zoom onto his "reaction" (the hand/ring)
            z = 1.0 + 0.32 * min(1, i / 5); cx0, cy0 = 430, 1060
        else:
            z = 1.0 + 0.05 * i / n; cx0, cy0 = W / 2, H / 2   # slow punch-in keeps each cut alive
        if z > 1.001:
            cw, ch = W / z, H / z
            x0 = min(max(cx0 - cw / 2, 0), W - cw); y0 = min(max(cy0 - ch / 2, 0), H - ch)
            im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
        im = im.convert('RGBA')
        k = 1.0 if zoom else min(1.0, 0.86 + 0.14 * i / 3)          # 3-frame pop, text visible from frame 1
        if k < 1:
            c = cap.resize((int(W * k), int(H * k)), Image.LANCZOS)
            tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            tmp.alpha_composite(c, (int((W - c.width) / 2), int(cy * (1 - k))))
            im.alpha_composite(tmp)
        else:
            im.alpha_composite(cap)
        enc.stdin.write(np.asarray(im.convert('RGB')).tobytes())
enc.stdin.close(); enc.wait()
