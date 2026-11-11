import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
W, H = 720, 1280
img = Image.new('RGBA', (W, H), (244, 239, 231, 255))
lg = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')   # official logo, untouched
lw = 470; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
img.alpha_composite(lg, ((W - lw) // 2, 440))
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, 610), (W / 2 + 60, 610)], fill=255, width=3); img.alpha_composite(gold_fill(m))
paste(img, gold_text('Venha nos visitar', script_font(80)), W / 2, 640, anchor='center')
y = 790
for t in ['AL. DR. MURICY, 650 · 8º ANDAR · CENTRO', 'CURITIBA – PR', 'ATENDIMENTO COM HORA MARCADA']:
    lay = solid_text(t, caps_font(18, 600), (132, 101, 46), 3); paste(img, lay, W / 2, y, anchor='center'); y += ink_size(lay)[1] + 16
save_hq(img, 'end2.png')
