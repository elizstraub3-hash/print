import sys
sys.path.insert(0, '.')
from shimmer_style import *
O = '/home/user/print/marina/carrossel/'
import os; os.makedirs(O, exist_ok=True)
SRC = Image.open('/home/user/print/marina/foto-original.jpg').convert('RGB')
W, H = 1086, 1358
INK = (74, 59, 46); BR = (132, 101, 46); M = 64
STONE = 'SAFIRA AZUL'           # placeholder pedido pela cliente: confirmar antes de postar
PIX, PARC = 'R$ 2.160', '12x de R$ 200,00'   # valores de exemplo: confirmar antes de postar

def zoom(cx, cy, cw):
    ch = cw * H / W
    return SRC.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.LANCZOS).convert('RGBA')
def swipe(img):
    sw = solid_text('ARRASTE PARA O LADO  →', sans(18, 700), LABEL_COLOR, 2); paste(img, sw, W - M - ink_size(sw)[0], H - 74)

# 1 — the stone up close + big name
s1 = zoom(500, 830, 640)
c = solid_text('ANEL', caps_font(54, 500), INK, 8); n = gold_text('Marina', script_font(290))
paste(s1, c, M + 10, 64); paste(s1, n, M - 6, 64 + ink_size(c)[1] + 2)
swipe(s1)
save_hq(s1, O + '01-marina-nome.jpg')

# 2 — price in 12x
s2 = zoom(505, 800, 860)
paste(s2, solid_text('ANEL SOLITÁRIO', caps_font(34, 500), INK, 3), M + 4, 64)
paste(s2, gold_text('Marina', script_font(170)), M - 4, 64 + 40)
bottom_fade(s2, 0.62)
y = 960
sp = solid_text(STONE + ' · MOISSANITES · OURO 18K', caps_font(19, 600), BR, 2); paste(s2, sp, M, y); y += ink_size(sp)[1] + 26
p = solid_text(PARC, sans(76, 600), PRICE_COLOR); paste(s2, p, M - 2, y); y += ink_size(p)[1] + 18
paste(s2, solid_text('sem juros no cartão', sans(28, 500), PARCEL_COLOR), M, y); y += 52
paste(s2, solid_text('ou ' + PIX + ' à vista no PIX (10% OFF)', sans(28, 600), LABEL_COLOR), M, y)
swipe(s2)
save_hq(s2, O + '02-marina-valor.jpg')

# 3 — tight zoom: the stone and the moissanites, with catalogue-style labels
cx, cy, cw = 500, 820, 440
s3 = zoom(cx, cy, cw); k = W / cw; ox, oy = cx - cw / 2, cy - cw * H / W / 2
P = lambda x, y: ((x - ox) * k, (y - oy) * k)
def label(img, text, anchor_xy, at_xy, align):
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m)
    d.line([at_xy, anchor_xy], fill=255, width=3); d.ellipse([anchor_xy[0] - 7, anchor_xy[1] - 7, anchor_xy[0] + 7, anchor_xy[1] + 7], outline=255, width=3)
    img.alpha_composite(gold_fill(m))
    t = solid_text(text, caps_font(26, 600), INK, 3); tw, th = ink_size(t)
    x = at_xy[0] - (tw if align == 'right' else 0) + (-12 if align == 'right' else 12)
    paste(img, t, x, at_xy[1] - th / 2)
st = P(518, 773); ms = P(440, 836)
label(s3, STONE, (st[0] + 105, st[1] - 105), (st[0] + 260, st[1] - 300), 'right')
label(s3, 'MOISSANITES', (ms[0] - 38, ms[1] - 22), (ms[0] - 150, ms[1] - 150), 'right')
bottom_fade(s3, 0.80)
y = H - 150
paste(s3, solid_text('OURO 18K · GARANTIA VITALÍCIA', caps_font(20, 600), BR, 3), W / 2, y, anchor='center')
paste(s3, solid_text('PEÇA PELO NOME: MARINA', sans(22, 700), LABEL_COLOR, 3), W / 2, y + 50, anchor='center')
save_hq(s3, O + '03-marina-detalhes.jpg')
print('stone', st, 'moiss', ms)
