import sys
import numpy as np
sys.path.insert(0, '.')
from shimmer_style import *
D = '/home/user/print/solitario-helena/'
W, H = 1086, 1358; M = 64
INK = (74, 59, 46); BR = (132, 101, 46)
def base(n, oy):
    return crop_native(Image.open(D + f'fotos/{n}.webp').convert('RGB'), W, H, oy=oy).convert('RGBA')   # native pixels
def band(img, a0, a1, top=False, strength=0.9):
    yy = np.arange(H, dtype=np.float32)[:, None] / H
    a = (np.clip((a1 - yy) / (a1 - a0), 0, 1) if top else np.clip((yy - a0) / (a1 - a0), 0, 1)) ** 1.2 * strength
    lay = Image.new('RGBA', (W, H), (250, 248, 244, 0)); lay.putalpha(Image.fromarray((np.broadcast_to(a, (H, W)) * 255).astype(np.uint8)))
    img.alpha_composite(lay)
def title(img, caps, script, y=58, size=210):
    c = solid_text(caps, caps_font(40, 500), INK, 3); s = gold_text(script, script_font(size))
    paste(img, c, M + 6, y); paste(img, s, M - 4, y + ink_size(c)[1] + 4)
def swipe(img):
    sw = solid_text('ARRASTE PARA O LADO  →', sans(18, 700), LABEL_COLOR, 2); paste(img, sw, W - M - ink_size(sw)[0], H - 66)
# 1 — product + price
s1 = base(58, 20); band(s1, 0.02, 0.22, top=True, strength=0.6); band(s1, 0.80, 0.90, strength=0.85)
title(s1, 'ANEL SOLITÁRIO', 'Helena')
sp = solid_text('OURO 18K · PEDRA CENTRAL 7,5 MM · 4,35 G', caps_font(19, 600), BR, 2); paste(s1, sp, M, 1105)
price_block(s1, M, 1105 + ink_size(sp)[1] + 18, 'R$ 4.050', 'ou 10x de R$ 450,00 sem juros', size=54)
swipe(s1); save_hq(s1, D + '01-helena-produto.jpg')
# 2 — meaning, over the macro of the stone
s2 = base(57, 90); band(s2, 0.02, 0.22, top=True, strength=0.7)
y = 50
c = solid_text('O SIGNIFICADO DE', caps_font(30, 500), INK, 3); paste(s2, c, W / 2, y, anchor='center')
nm = gold_text('Helena', script_font(150)); paste(s2, nm, W / 2, y + ink_size(c)[1] + 2, anchor='center')
y2 = y + ink_size(c)[1] + 2 + ink_size(nm)[1] + 10
for t in ['DO GREGO, “A QUE BRILHA”: UMA PEDRA DE 7,5 MM', 'QUE ILUMINA A MÃO E O MOMENTO DO SIM.']:
    lay = solid_text(t, caps_font(20, 600), BR, 2); paste(s2, lay, W / 2, y2, anchor='center'); y2 += ink_size(lay)[1] + 11
print('s2 text bottom', y2)
save_hq(s2, D + '02-helena-significado.jpg')
# 3 — guarantee + call to action
s3 = base(60, 45); band(s3, 0.02, 0.24, top=True, strength=0.65)
c = solid_text('AQUI VOCÊ TEM', caps_font(30, 600), INK, 4); paste(s3, c, W / 2, 70, anchor='center')
paste(s3, gold_text('garantia vitalícia', script_font(120)), W / 2, 70 + ink_size(c)[1] + 6, anchor='center')
band(s3, 0.86, 0.95, strength=0.85)
paste(s3, solid_text('PEÇA PELO NOME: HELENA', sans(22, 700), LABEL_COLOR, 3), W / 2, H - 120, anchor='center')
paste(s3, solid_text('Agende sua visita pelo WhatsApp · link na bio', sans(24, 500), PARCEL_COLOR), W / 2, H - 78, anchor='center')
save_hq(s3, D + '03-helena-garantia.jpg')
P = Image.new('RGB', (3 * 400 + 20, 500), 'white')
for i, f in enumerate(['01-helena-produto', '02-helena-significado', '03-helena-garantia']):
    P.paste(Image.open(D + f + '.jpg').resize((400, 500)), (i * 410, 0))
P.save(S + 'hel_prev.jpg', quality=90)
