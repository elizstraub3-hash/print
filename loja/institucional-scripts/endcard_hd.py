import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
W, H = 1080, 1920
img = Image.new('RGBA', (W, H), (244, 239, 231, 255))
lg = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')   # official logo, untouched
lw = 705; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
img.alpha_composite(lg, ((W - lw) // 2, 660))
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 90, 915), (W / 2 + 90, 915)], fill=255, width=4); img.alpha_composite(gold_fill(m))
paste(img, gold_text('Venha nos visitar', script_font(120)), W / 2, 960, anchor='center')
y = 1185
for t in ['AL. DR. MURICY, 650 · 8º ANDAR · CENTRO', 'CURITIBA – PR', 'ATENDIMENTO COM HORA MARCADA']:
    lay = solid_text(t, caps_font(27, 600), (132, 101, 46), 4); paste(img, lay, W / 2, y, anchor='center'); y += ink_size(lay)[1] + 24
save_hq(img, 'hd/end.png')
