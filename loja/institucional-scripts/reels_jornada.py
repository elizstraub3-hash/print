import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from story_nativo_lib import emoji, sans
from shimmer_style import gold_fill

HD = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/inst2/hd/'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/print/loja/reels-jornada-shimmer.mp4'
PREV = [float(x) for x in sys.argv[2:]]
W, H, FPS = 1080, 1920, 30
FB = sans(76, 900)   # hook
FS = sans(60, 900)   # steps

# (clip, start, end, step, text, emoji, centre y, hook lines)
SC = [
    ('j0', 0.0, 2.4, 1, 'agenda seu horário', None, 1100, ['Como é comprar', 'joia na Shimmer']),
    ('j1', 0.2, 3.2, 2, 'o Júnior te recebe', None, 1420, None),
    ('s8', 0.0, 2.6, 3, 'te mostra as peças', None, 430, None),
    ('s9', 0.3, 2.8, 4, 'escolhe com calma', None, 430, None),
    ('s10', 0.0, 2.4, 5, 'experimenta', None, 1400, None),
    ('s10', 2.6, 5.6, 6, 'e já sai com a sua', '💍', 1400, None),
    ('s2', 0.0, 1.8, None, None, None, 0, None),
]


def stroke_text(d, xy, s, f):
    d.text(xy, s, font=f, fill='white', stroke_width=7, stroke_fill='black')


def caption(step, text, emo, cy, hook):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if hook:
        asc, desc = FB.getmetrics(); lh = asc + desc + 4
        e = emoji('👇', 84)
        y = 820
        for i, s in enumerate(hook):
            tw = FB.getlength(s); extra = e.width + 16 if i == len(hook) - 1 else 0
            x = 480 - (tw + extra) / 2
            stroke_text(d, (x, y), s, FB)
            if extra: lay.alpha_composite(e, (int(x + tw + 16), int(y + lh / 2 - e.height / 2)))
            y += lh
    if step:
        asc, desc = FS.getmetrics(); th = asc + desc
        R = 50
        e = emoji(emo, 70) if emo else None
        tw = FS.getlength(text) + (e.width + 14 if e else 0)
        total = 2 * R + 22 + tw
        x0 = {1: 480, 3: 440, 4: 470}.get(step, W / 2) - total / 2
        # gold numbered badge
        m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
        md.ellipse([x0 - 4, cy - R - 4, x0 + 2 * R + 4, cy + R + 4], fill=255)
        dark = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dark.putalpha(m)
        lay.alpha_composite(dark)
        m2 = Image.new('L', (W, H), 0); ImageDraw.Draw(m2).ellipse([x0, cy - R, x0 + 2 * R, cy + R], fill=255)
        lay.alpha_composite(gold_fill(m2))
        fn = sans(62, 900); n = str(step)
        d.text((x0 + R - fn.getlength(n) / 2, cy), n, font=fn, fill='white', anchor='lm', stroke_width=2, stroke_fill=(110, 80, 30))
        tx = x0 + 2 * R + 22
        d.text((tx, cy), text, font=FS, fill='white', anchor='lm', stroke_width=7, stroke_fill='black')
        if e: lay.alpha_composite(e, (int(tx + FS.getlength(text) + 14), int(cy - e.height / 2)))
    if not step and not hook:   # end card over Maria walking off
        asc, desc = FB.getmetrics(); lh = asc + desc + 4
        e = emoji('📲', 84)
        for i, s in enumerate(['Agende sua visita', 'link na bio']):
            f = FB if i == 0 else FS
            tw = f.getlength(s); extra = e.width + 16 if i == 1 else 0
            x = W / 2 - (tw + extra) / 2; y = 430 + i * lh
            stroke_text(d, (x, y), s, f)
            if extra: lay.alpha_composite(e, (int(x + tw + 16), int(y + 45 - e.height / 2)))
    bb = lay.getbbox(); assert bb[0] > 40 and bb[2] < W - 40, (text, bb)
    return lay


def frames(name, a, b):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(a), '-t', str(b - a), '-i', HD + f'{name}.mp4',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, H, W, 3)


def render(fr, cap, i, n):
    im = Image.fromarray(fr)
    z = 1.0 + 0.05 * i / n
    cw, ch = W / z, H / z
    im = im.crop(((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)).resize((W, H), Image.LANCZOS).convert('RGBA')
    im.alpha_composite(cap)
    return im.convert('RGB')


if PREV:
    t0 = 0
    for name, a, b, st, tx, emo, cy, hook in SC:
        for t in PREV:
            if t0 <= t < t0 + (b - a):
                fr = frames(name, a + t - t0, a + t - t0 + 0.05)[0]
                render(fr, caption(st, tx, emo, cy, hook), 1, 2).save(f'/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/jr_{t}.jpg', quality=88)
        t0 += b - a
    sys.exit()

enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                        '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for name, a, b, st, tx, emo, cy, hook in SC:
    fr = frames(name, a, b); cap = caption(st, tx, emo, cy, hook)
    for i, f in enumerate(fr):
        enc.stdin.write(np.asarray(render(f, cap, i, len(fr))).tobytes())
enc.stdin.close(); enc.wait(); print('ok')
