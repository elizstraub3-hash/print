"""Story 'como se o Júnior tivesse postado na hora': vídeo do WhatsApp como veio (só escala p/ 1080x1920),
textos no estilo nativo do Instagram (caixa branca arredondada, letra preta), emoji, sticker de local.
Áudio original mantido."""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/user/print')
from story_nativo_lib import emoji
from shimmer_style import sans

SRC = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/2e8b9139-WhatsApp_Video_2026-11-26_at_13.14.18.mp4'
D = '/home/user/print/stories/junior-pedidos/'
W, H, FPS = 1080, 1920, 30
DUR = 33.3
PREV = [float(x) for x in sys.argv[1:]]


def bubble(lines, em=None, size=54, bg=(255, 255, 255, 255), fg=(18, 18, 18)):
    fnt = sans(size, 700); pad_x, pad_y, lh = 30, 18, int(size * 1.28)
    e = emoji(em, int(size * 1.05)) if em else None
    widths = [fnt.getlength(l) + ((e.width + 12) if (e and i == len(lines) - 1) else 0) for i, l in enumerate(lines)]
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(out)
    tot = len(lines) * lh; y = 0
    for i, (l, w) in enumerate(zip(lines, widths)):
        x = (W - w) / 2
        d.rounded_rectangle([x - pad_x, y, x + w + pad_x, y + lh + pad_y], 22, fill=bg)
        y += lh
    y = 0
    for i, (l, w) in enumerate(zip(lines, widths)):
        x = (W - w) / 2
        d.text((x, y + pad_y / 2 + 4), l, font=fnt, fill=fg)
        if e and i == len(lines) - 1: out.alpha_composite(e, (int(x + fnt.getlength(l) + 12), int(y + pad_y / 2 + 4)))
        y += lh
    return out.crop((0, 0, W, tot + pad_y + 4))


def sticker(text, em):
    fnt = sans(34, 700); e = emoji(em, 38); w = fnt.getlength(text) + e.width + 60
    im = Image.new('RGBA', (int(w), 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 69], 16, fill=(255, 255, 255, 235))
    im.alpha_composite(e, (20, 16)); d.text((20 + e.width + 10, 14), text, font=fnt, fill=(150, 60, 200))
    return im


# (inicio, fim, camada, y)
TX = [
    (0.4, 6.0, bubble(['Separando os pedidos', 'de hoje'], '✨'), 300),
    (6.3, 19.6, bubble(['Anel com a data', 'mais especial dela'], '🤍'), 300),
    (20.6, 26.2, bubble(['Solitário com esmeralda'], '💚'), 300),
    (27.6, 33.3, bubble(['E esse aqui vai virar', 'pedido de casamento'], '💍'), 300),
    (29.6, 33.3, bubble(['Quer o seu? Chama no direct'], '📩', size=46), 1470),
]
STK = sticker('SHIMMER JOIAS', '📍')


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def frames():
    vf = 'fps=30,scale=1080:-2:flags=lanczos,crop=1080:1920'
    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', SRC, '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        b = dec.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


enc = None if PREV else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-i', SRC, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', D + 'story-junior-pedidos.mp4'], stdin=subprocess.PIPE)
for n, fr in enumerate(frames()):
    t = n / FPS
    if PREV and not any(abs(t - p) < 0.5 / FPS for p in PREV): continue
    img = Image.fromarray(fr).convert('RGBA')
    img.alpha_composite(STK, (60, 190))
    for t0, t1, L, y in TX:
        if not (t0 <= t < t1 + 0.25): continue
        k = ease((t - t0) / 0.35) * (1 - ease((t - t1) / 0.25))
        sc = 0.85 + 0.15 * ease((t - t0) / 0.3)
        Ls = L.resize((int(L.width * sc), int(L.height * sc)), Image.LANCZOS) if sc < 0.999 else L
        tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.paste(Ls, ((W - Ls.width) // 2, int(y + (L.height - Ls.height) / 2)), Ls)
        if k < 1: tmp.putalpha(tmp.getchannel('A').point(lambda v: int(v * k)))
        img.alpha_composite(tmp)
    o = np.asarray(img.convert('RGB'))
    if PREV: Image.fromarray(o).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/jp2_{t:05.2f}.jpg', quality=85)
    else: enc.stdin.write(o.tobytes())
if enc: enc.stdin.close(); enc.wait()
print('ok')
