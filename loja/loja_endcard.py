import sys
sys.path.insert(0, '.')
from shimmer_style import *
W, H = 720, 1280
img = Image.new('RGBA', (W, H), (244, 239, 231, 255))
paste(img, solid_text('SHIMMER JOIAS', caps_font(46, 500), (74, 59, 46), 8), W / 2, 520, anchor='center')
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, 600), (W / 2 + 60, 600)], fill=255, width=3); img.alpha_composite(gold_fill(m))
paste(img, gold_text('Venha nos visitar', script_font(84)), W / 2, 630, anchor='center')
paste(img, solid_text('CURITIBA · OURO 18K · GARANTIA VITALÍCIA', caps_font(17, 600), (132, 101, 46), 3), W / 2, 790, anchor='center')
save_hq(img, S + 'loja_end.png')
