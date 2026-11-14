"""
Recorta uma foto/ilustração de bolo com fundo "xadrez" falso (ou branco).
Uso: python3 tools/recortar-bolo.py entrada.png saida.webp [previa.png]
Requer: pip install opencv-python-headless pillow numpy
"""
import sys, numpy as np, cv2
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
prev = sys.argv[3] if len(sys.argv) > 3 else None
rgb = np.asarray(Image.open(src).convert('RGB'))
H, W, _ = rgb.shape
mx = rgb.max(2).astype(int); mn = rgb.min(2).astype(int)
neutral_light = ((mx - mn) <= 12) & (mn >= 222)
# fundo = pixels neutros-claros conectados à borda
nl = neutral_light.astype(np.uint8) * 255
pad = cv2.copyMakeBorder(nl, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=255)
cv2.floodFill(pad, np.zeros((H + 4, W + 4), np.uint8), (0, 0), 128)
bgreg = pad[1:-1, 1:-1] == 128
mask = np.where(bgreg, cv2.GC_PR_BGD, cv2.GC_PR_FGD).astype(np.uint8)
border = np.zeros((H, W), bool); border[:12, :] = border[-12:, :] = border[:, :12] = border[:, -12:] = True
mask[border & bgreg] = cv2.GC_BGD
core = cv2.erode((~bgreg).astype(np.uint8) * 255, np.ones((25, 25), np.uint8)) > 0
mask[core] = cv2.GC_FGD
bgd = np.zeros((1, 65)); fgd = np.zeros((1, 65))
cv2.grabCut(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), mask, None, bgd, fgd, 5, cv2.GC_INIT_WITH_MASK)
fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
fg = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
p2 = cv2.copyMakeBorder(fg, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
cv2.floodFill(p2, np.zeros((H + 4, W + 4), np.uint8), (0, 0), 255)
fg |= cv2.bitwise_not(p2)[1:-1, 1:-1]
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
# remove "ilhas" de xadrez falso presas dentro da arte (dois tons neutros alternados)
strict = (((mx - mn) <= 6) & (mn >= 215) & (fg > 0)).astype(np.uint8)
strict = cv2.morphologyEx(strict, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
n2, lab2, st2, _ = cv2.connectedComponentsWithStats(strict)
L = rgb.mean(2)
for k in range(1, n2):
    if st2[k, cv2.CC_STAT_AREA] < 250:
        continue
    reg = lab2 == k
    if L[reg].std() > 4.5:  # alternância clara/escura = xadrez, não cobertura branca lisa
        fg[cv2.dilate(reg.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0
alpha = cv2.GaussianBlur(fg, (5, 5), 0)
alpha[alpha < 40] = 0
res = Image.fromarray(np.dstack([rgb, alpha]), 'RGBA')
res = res.crop(res.getchannel('A').getbbox())
res.thumbnail((760, 1100), Image.LANCZOS)
res.save(out, quality=88, method=6)
print(res.size)
if prev:
    a = Image.new('RGBA', res.size, (90, 60, 110, 255)); a.alpha_composite(res)
    b = Image.new('RGBA', res.size, (200, 235, 220, 255)); b.alpha_composite(res)
    c = Image.new('RGB', (res.width * 2, res.height)); c.paste(a.convert('RGB'), (0, 0)); c.paste(b.convert('RGB'), (res.width, 0))
    c.resize((res.width, res.height // 2)).save(prev)
