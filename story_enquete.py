import sys
sys.path.insert(0, '.')
from PIL import Image, ImageDraw
from shimmer_style import sans, save_hq
from story_nativo_lib import emoji
W = 720
o = Image.open('v3f/f_030.png').convert('RGBA')  # native frame, untouched
def pill(text, emo, cy, size, fg, bg, pad=(20, 11), r=15, cx=W/2):
    f = sans(size, 700); tw = f.getlength(text)
    es = [emoji(e, int(size*1.05)) for e in emo] if emo else []
    tot = tw + sum(e.width + 7 for e in es) + (2 if es else 0)
    asc, desc = f.getmetrics(); h = asc + desc
    x0 = cx - tot/2; d = ImageDraw.Draw(o)
    d.rounded_rectangle([x0-pad[0], cy-h/2-pad[1], x0+tot+pad[0], cy+h/2+pad[1]], radius=r, fill=bg)
    d.text((x0, cy-h/2), text, font=f, fill=fg); x = x0 + tw + 9
    for e in es: o.alpha_composite(e, (int(x), int(cy-e.height/2))); x += e.width + 7
BK, WH, DK = (20,20,20,255), (255,255,255,255), (0,0,0,165)
pill('pedido de casamento', None, 150, 38, BK, WH)
pill('ou formatura?', ['💍', '🎓'], 215, 38, BK, WH)
pill('pra qual momento você daria o Anel Diana?', None, 290, 23, WH, DK, pad=(15, 8), r=12)
pill('Anel Diana', ['💙'], 600, 24, WH, DK, pad=(15, 8), r=12, cx=565)
save_hq(o, sys.argv[1])
