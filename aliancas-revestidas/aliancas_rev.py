import sys
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
D = '/home/user/print/aliancas-revestidas/'
W, H = 1086, 1358; M = 64
INK = (74, 59, 46); BR = (132, 101, 46)
def base(n, oy):
    return crop_native(Image.open(D + f'fotos/{n}.webp').convert('RGB'), W, H, oy=oy).convert('RGBA')   # native pixels, no resize
def top_fade(img, end=0.25, strength=0.86):
    yy = np.arange(H, dtype=np.float32)[:, None]
    a = np.clip(1 - yy / (H * end), 0, 1) ** 1.1 * strength
    lay = Image.new('RGBA', (W, H), (250, 248, 244, 0)); lay.putalpha(Image.fromarray((np.broadcast_to(a, (H, W)) * 255).astype(np.uint8)))
    img.alpha_composite(lay)
def band(img, a0, a1, top=False, strength=0.95):
    yy = np.arange(H, dtype=np.float32)[:, None] / H
    a = (np.clip((a1 - yy) / (a1 - a0), 0, 1) if top else np.clip((yy - a0) / (a1 - a0), 0, 1)) ** 1.2 * strength
    lay = Image.new('RGBA', (W, H), (250, 248, 244, 0)); lay.putalpha(Image.fromarray((np.broadcast_to(a, (H, W)) * 255).astype(np.uint8)))
    img.alpha_composite(lay)
def glow(img, cx, cy, rx, ry, strength=0.88):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    a = np.clip(1 - d, 0, 1) ** 0.9
    a = np.clip(a * 1.6, 0, 1) * strength
    lay = Image.new('RGBA', (W, H), (250, 248, 244, 0)); lay.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    img.alpha_composite(lay)
def title(img, caps, script, y=58, size=200):
    c = solid_text(caps, caps_font(40, 500), INK, 3); s = gold_text(script, script_font(size))
    paste(img, c, M + 6, y); paste(img, s, M - 4, y + ink_size(c)[1] + 4)
def swipe(img):
    sw = solid_text('ARRASTE PARA O LADO  →', sans(18, 700), LABEL_COLOR, 2); paste(img, sw, W - M - ink_size(sw)[0], H - 66)

# 1 — the pair + price
s1 = base(53, 45); band(s1, 0.02, 0.24, top=True, strength=0.72); band(s1, 0.77, 0.88, strength=0.92)
title(s1, 'PAR DE', 'Alianças')
sp = solid_text('REVESTIDAS · 4 MM · GARANTIA VITALÍCIA', caps_font(20, 600), BR, 2); paste(s1, sp, M, 1140); y = 1140 + ink_size(sp)[1]
price_block(s1, M, y + 18, 'R$ 2.250', 'ou 10x de R$ 250,00 sem juros', size=54)
swipe(s1); save_hq(s1, D + '01-par-de-aliancas.jpg')

# 2 — with the solitaire: the full set
s2 = base(52, 45); band(s2, 0.02, 0.23, top=True, strength=0.72); band(s2, 0.80, 0.90, strength=0.92)
title(s2, 'DO PEDIDO', 'ao altar', size=180)
y = H - 140
for t in ['Combine as alianças', 'com o seu solitário.']:
    lay = solid_text(t, caps_font(32, 500), INK, 1); paste(s2, lay, M, y); y += ink_size(lay)[1] + 12
swipe(s2); save_hq(s2, D + '02-conjunto.jpg')

# 3 — detail, made to measure
s3 = base(55, 0); band(s3, 0.02, 0.21, top=True, strength=0.72)
y = 70
lay = solid_text('FEITAS SOB MEDIDA', caps_font(30, 600), INK, 4); paste(s3, lay, W / 2, y, anchor='center'); y += ink_size(lay)[1] + 6
paste(s3, gold_text('para o casal', script_font(110)), W / 2, y, anchor='center')
save_hq(s3, D + '03-detalhes.jpg')
P = Image.new('RGB', (3 * 400 + 20, 500), 'white')
for i, f in enumerate(['01-par-de-aliancas', '02-conjunto', '03-detalhes']):
    P.paste(Image.open(D + f + '.jpg').resize((400, 500)), (i * 410, 0))
P.save(S + 'alr_prev.jpg', quality=90)
