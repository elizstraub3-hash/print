"""Carrossel 'Clássico & Serena' (7 slides) + 2 Stories em vídeo (tráfego pago).
Fotos: Clássico = fotos no cetim do Drive (Shimmer_Anel_03/08/11/12/13, 1086x1448);
       Serena   = SH-1061 do site (900x1272).
Fotos só recortadas (sem ampliar): slides do Clássico em 1080x1350, do Serena em 900x1125 (proporção 4:5 igual).
Texto nunca encosta na joia; script com a textura dourada; caps em Cinzel."""
import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *

D = '/home/user/print/serena-classico/'
F = D + 'fotos/'
OUT = D + 'carrossel/'
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241)
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')
PATTERN = Image.open('/home/user/print/assets/pattern-logo.jpg').convert('RGB')
import os; os.makedirs(OUT, exist_ok=True)


def shadowed(lay_bb, blur=6, alpha=0.30, dy=3, col=(70, 50, 20)):
    lay, bb = lay_bb; a = lay.getchannel('A')
    sh = Image.new('RGBA', lay.size, col + (0,)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha)))
    out = Image.new('RGBA', lay.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, dy)); out.alpha_composite(lay); return out, bb


def C(im, lay, y): paste(im, lay, im.width / 2, y, anchor='center'); return y + ink_size(lay)[1]


def fade(im, a0, a1, strength, top=True, color=IV):
    """Soft ivory fade (smoothstep). top=True: strongest at the top, gone at a1 (fractions of height)."""
    W, H = im.size
    yy = np.arange(H, dtype=np.float32)[:, None] / H
    x = np.clip((a1 - yy) / (a1 - a0), 0, 1) if top else np.clip((yy - a0) / (a1 - a0), 0, 1)
    a = x * x * (3 - 2 * x) * strength
    lay = Image.new('RGBA', (W, H), color + (0,)); lay.putalpha(Image.fromarray((np.broadcast_to(a, (H, W)) * 255).astype('uint8')))
    im.alpha_composite(lay)


def crop(name, W, H, ox=None, oy=0):
    src = Image.open(F + name).convert('RGB'); iw, ih = src.size
    ox = (iw - W) // 2 if ox is None else ox
    return src.crop((ox, oy, ox + W, oy + H)).convert('RGBA')


def pattern_bg(W, H, glow_y=None):
    sc = max(W / PATTERN.width, H / PATTERN.height)
    p = PATTERN.resize((round(PATTERN.width * sc), round(PATTERN.height * sc)), Image.LANCZOS)
    p = p.crop(((p.width - W) // 2, (p.height - H) // 2, (p.width - W) // 2 + W, (p.height - H) // 2 + H))
    a = np.asarray(p, np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]; xx = np.arange(W, dtype=np.float32)[None, :, None]
    gy = H / 2 if glow_y is None else glow_y
    g = np.exp(-(((xx - W / 2) / (W * 0.5)) ** 2 + ((yy - gy) / (H * 0.30)) ** 2)) * 0.8
    a = a * (1 - g) + np.array(IV, np.float32) * g
    return Image.fromarray(a.astype('uint8')).convert('RGBA')


def logo(im, y, width=None):
    lg = LOGO if width is None or width >= LOGO.width else LOGO.resize((width, round(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    x = (im.width - lg.width) // 2
    a = Image.new('L', im.size, 0); a.paste(lg.getchannel('A'), (x, y + 3))
    sh = Image.new('RGBA', im.size, (60, 45, 25, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.35)))
    im.alpha_composite(sh); im.alpha_composite(lg, (x, y)); return y + lg.height


def save(im, name):
    os.makedirs(os.path.dirname(OUT + name), exist_ok=True)
    im.convert('RGB').save(OUT + name, quality=100, subsampling=0)


# prices: Clássico = Eliz's feed post (R$ 1.350 no PIX, 10x de R$ 150,00); Serena = site R$ 1.999,00 -> 10% off no PIX
CL_PIX, CL_PARC = 'R$ 1.350', 'ou 10x de R$ 150,00 sem juros'
SE_PIX, SE_PARC = 'R$ 1.799,10', 'ou 10x de R$ 199,90 sem juros'
CL_PIX_STORY, SE_PIX_STORY = 'R$ 1.350 no PIX', 'R$ 1.799,10 no PIX'


M = 64
# ---------------- carrossel ----------------
def swipe(im):
    hint = solid_text('ARRASTE PARA O LADO  →', sans(22, 700), LABEL_COLOR, 2)
    paste(im, hint, im.width - M - ink_size(hint)[0], im.height - 70)


def text_slide(title, lines1, lines2, name):
    W, H = 1080, 1350
    im = pattern_bg(W, H, glow_y=650)
    y = C(im, solid_text('POR QUE', caps_font(42, 500), INK, 6), 330)
    y = C(im, shadowed(gold_text(title, script_font(210))), y + 10)
    y += 40
    for line in lines1:
        y = C(im, solid_text(line, caps_font(32, 600), INK, 3), y) + 16
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y + 26), (W / 2 + 60, y + 26)], fill=255, width=3); im.alpha_composite(gold_fill(m))
    y += 64
    for line in lines2:
        y = C(im, solid_text(line, caps_font(30, 600), BR, 3), y) + 16
    save(im, name)


def cta(name_script, pix, parc, out):
    W, H = 1080, 1350
    im = pattern_bg(W, H, glow_y=660)
    y = logo(im, 170)
    y = C(im, solid_text('ANEL SOLITÁRIO', caps_font(40, 600), INK, 6), y + 70)
    y = C(im, shadowed(gold_text(name_script, script_font(190))), y + 8)
    y = C(im, solid_text('À VISTA NO PIX', sans(26, 700), LABEL_COLOR, 2), y + 34)
    y = C(im, solid_text(pix, sans(78, 600), PRICE_COLOR), y + 18)
    y = C(im, solid_text(parc, sans(32, 500), PARCEL_COLOR), y + 20)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y + 36), (W / 2 + 60, y + 36)], fill=255, width=3); im.alpha_composite(gold_fill(m))
    y += 76
    for txt, fnt, col, tr in [('OURO 18K · GARANTIA VITALÍCIA', caps_font(30, 600), INK, 4), ('AGENDE SUA VISITA · LINK NA BIO', caps_font(30, 700), BR, 4),
                              ('atendimento na loja ou online', sans(28, 500), PARCEL_COLOR, 0)]:
        y = C(im, solid_text(txt, fnt, col, tr), y) + 20
    save(im, out)


# ---- carrossel Clássico ----
def c1():
    im = crop('classico-cetim-1.png', 1080, 1350, oy=0)          # ring ~y 640-850
    fade(im, 0.0, 0.45, 0.5)
    y = C(im, solid_text('ANEL SOLITÁRIO', caps_font(44, 600), INK, 6), 150)
    y = C(im, shadowed(gold_text('Clássico', script_font(230))), y + 8)
    C(im, solid_text('DELICADO E ATEMPORAL', caps_font(30, 600), BR, 6), y + 26)
    swipe(im); save(im, 'classico/01-capa.jpg')


def c2():
    im = crop('classico-cetim-2.png', 1080, 1350, oy=40)          # ring ~y 600-910
    fade(im, 0.0, 0.30, 0.5)
    y = 90
    for line in ['PEDRA CENTRAL 4MM · MOISSANITES', 'OURO 18K · GARANTIA VITALÍCIA']:
        t = solid_text(line, caps_font(28, 600), BR, 3); paste(im, t, M + 6, y); y += ink_size(t)[1] + 12
    fade(im, 0.74, 1.0, 0.75, top=False)
    price_block(im, M + 6, 1350 - 250, CL_PIX, CL_PARC, size=72)
    save(im, 'classico/02-valor.jpg')


def c3():
    text_slide('Clássico?', ['PORQUE É O SOLITÁRIO', 'QUE NUNCA SAI DE MODA:', 'SIMPLES, DELICADO E ATEMPORAL.'],
               ['A PEDRA CENTRAL PRESA EM 4 GARRAS', 'E AS LATERAIS CRAVEJADAS FORMAM', 'O DESENHO QUE ATRAVESSA GERAÇÕES.'], 'classico/03-por-que-classico.jpg')


def c4():
    cta('Clássico', CL_PIX, CL_PARC, 'classico/04-cta.jpg')


# ---- carrossel Serena ----
def r1():
    W, H = 1055, 1319
    im = crop('serena-editada.png', W, H, oy=0)                    # stone starts ~y 350
    k = W / 1080
    fade(im, 0.0, 0.30, 0.6)
    y = 48
    c = solid_text('ANEL SOLITÁRIO', caps_font(41, 500), INK, 3); paste(im, c, M * k + 6, y)
    sc = shadowed(gold_text('Serena', script_font(205))); paste(im, sc, M * k - 4, y + ink_size(c)[1] + 2)
    fade(im, 0.90, 1.0, 0.7, top=False)
    swipe(im); save(im, 'serena/01-capa.jpg')


def r2():
    src = Image.open(F + 'serena-editada.png').convert('RGB')
    im = src.crop((255, 300, 255 + 760, 300 + 950))                # native pixels: stone + pavé, no text
    os.makedirs(OUT + 'serena', exist_ok=True); im.save(OUT + 'serena/02-detalhe.jpg', quality=100, subsampling=0)


def r3():
    text_slide('Serena?', ['SERENA VEM DE SERENIDADE:', 'A CALMA DE UM AMOR SEGURO,', 'QUE NÃO PRECISA DE PRESSA.'],
               ['A PEDRA CENTRAL BRILHA TRANQUILA,', 'ACOMPANHADA POR PEDRAS LATERAIS', 'QUE CONDUZEM A LUZ ATÉ ELA.'], 'serena/03-por-que-serena.jpg')


def r4():
    cta('Serena', SE_PIX, SE_PARC, 'serena/04-cta.jpg')


# ---------------- stories (vídeo 10 s + imagem) ----------------
SW, SH, FPS, DUR = 1080, 1920, 30, 10.0


def story_plate(name, W0, oy_canvas, scale=1.0):
    """Photo at native size, centred; the rest of the 9:16 canvas filled with a blurred, lightened copy; edges feathered."""
    src = Image.open(F + name).convert('RGB'); iw, ih = src.size
    if scale < 1: src = src.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS); iw, ih = src.size   # downscale only
    if iw > SW: src = src.crop(((iw - SW) // 2, 0, (iw - SW) // 2 + SW, ih)); iw = SW
    sc = max(SW / iw, SH / ih) * 1.08
    bg = src.resize((round(iw * sc), round(ih * sc)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))
    bg = bg.crop(((bg.width - SW) // 2, (bg.height - SH) // 2, (bg.width - SW) // 2 + SW, (bg.height - SH) // 2 + SH))
    bga = np.asarray(bg, np.float32) * 0.85 + np.array(IV, np.float32) * 0.15
    ox = (SW - iw) // 2
    yy = np.arange(SH, dtype=np.float32)[:, None]; xx = np.arange(SW, dtype=np.float32)[None, :]
    m = np.clip((yy - oy_canvas) / 120, 0, 1) * np.clip((oy_canvas + ih - yy) / 120, 0, 1)
    if ox > 0: m = m * np.clip((xx - ox) / 90, 0, 1) * np.clip((ox + iw - xx) / 90, 0, 1)
    m = (m * m * (3 - 2 * m))[..., None]
    full = bga.copy(); full[oy_canvas:oy_canvas + ih, ox:ox + iw] = np.asarray(src, np.float32)
    return Image.fromarray((bga * (1 - m) + full * m).astype(np.uint8))


def L(): return Image.new('RGBA', (SW, SH), (0, 0, 0, 0))


def cta_layers(y0, pix, parc):
    a = L(); y = C(a, solid_text(pix, sans(52, 600), PRICE_COLOR), y0)
    y = C(a, solid_text(parc, sans(30, 500), PARCEL_COLOR), y + 14)
    y = C(a, solid_text('OURO 18K · GARANTIA VITALÍCIA', caps_font(28, 600), BR, 4), y + 18)
    b = L(); t = solid_text('CHAME NO DIRECT', caps_font(34, 700), BR, 5); w, h = ink_size(t)
    box = [SW / 2 - w / 2 - 50, y + 34, SW / 2 + w / 2 + 50, y + 34 + h + 46]
    mk = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mk).rounded_rectangle(box, radius=(h + 46) // 2, fill=255)
    pl = Image.new('RGBA', (SW, SH), (255, 253, 249, 0)); pl.putalpha(mk.point(lambda v: int(v * 0.95))); b.alpha_composite(pl)
    fr = Image.new('L', (SW, SH), 0); ImageDraw.Draw(fr).rounded_rectangle(box, radius=(h + 46) // 2, outline=255, width=3); b.alpha_composite(gold_fill(fr))
    paste(b, t, SW / 2, y + 34 + 23, anchor='center')
    return [(a, 3.2), (b, 3.9)]


def story(plate, title_layers, cta, out, fade_top=(0.0, 0.33, 0.55), fade_bot=(0.72, 1.0, 0.7)):
    base = plate.convert('RGBA'); fade(base, *fade_top); fade(base, *fade_bot, top=False)
    base = np.asarray(base.convert('RGB'), np.float32)
    layers = [(np.asarray(l, np.float32), t0) for l, t0 in title_layers + cta]
    def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
    def frame(t):
        z = 1.0 + 0.05 * t / DUR; cw, ch = SW / z, SH / z
        f = np.asarray(Image.fromarray(base.astype(np.uint8)).crop(((SW - cw) / 2, (SH - ch) * 0.55, (SW + cw) / 2, (SH - ch) * 0.55 + ch)).resize((SW, SH), Image.LANCZOS), np.float32) if z > 1.0005 else base.copy()
        for arr, t0 in layers:
            k = ease((t - t0) / 0.7)
            if k <= 0: continue
            a = np.roll(arr, int(round((1 - k) * 22)), axis=0); al = a[..., 3:4] / 255 * k
            f = f * (1 - al) + a[..., :3] * al
        return np.clip(f, 0, 255).astype(np.uint8)
    Image.fromarray(frame(DUR - 0.1)).save(D + out + '.jpg', quality=100, subsampling=0)
    enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{SW}x{SH}', '-r', str(FPS), '-i', '-',
                            '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15',
                            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', D + out + '.mp4'], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
    enc.stdin.close(); enc.wait()


def story_classico():
    plate = story_plate('classico-cetim-2.png', 1080, 236)           # ring ~y 876-1186
    a = L(); y = C(a, solid_text('ANEL SOLITÁRIO', caps_font(46, 500), INK, 6), 300)
    b = L(); y = C(b, shadowed(gold_text('Clássico', script_font(230))), y + 8)
    c = L(); C(c, solid_text('DELICADO E ATEMPORAL', caps_font(32, 600), BR, 5), y + 24)
    story(plate, [(a, 0.3), (b, 0.8), (c, 1.6)], cta_layers(1440, CL_PIX_STORY, CL_PARC), 'story-classico')


def story_serena():
    plate = story_plate('serena-editada.png', 1080, 360, scale=0.84)  # stone ~y 655, band ends ~y 1440
    a = L(); y = C(a, solid_text('ANEL SOLITÁRIO', caps_font(46, 500), INK, 6), 262)
    b = L(); y = C(b, shadowed(gold_text('Serena', script_font(230))), y + 8)
    c = L(); C(c, solid_text('A CALMA DE UM AMOR SEGURO', caps_font(32, 600), BR, 4), y + 24)
    story(plate, [(a, 0.3), (b, 0.8), (c, 1.6)], cta_layers(1475, SE_PIX_STORY, SE_PARC), 'story-serena', fade_top=(0.0, 0.36, 0.82))


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('all', 'carrossel'):
        c1(); c2(); c3(); c4(); r1(); r2(); r3(); r4()
    if what in ('all', 'stories'):
        story_classico(); story_serena()
    print('ok')
