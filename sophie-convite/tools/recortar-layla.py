"""Recorta poses da prancha da Layla (fundo rosa degradê) com GrabCut.
Uso: python3 tools/recortar-layla.py prancha.png saida_dir"""
import sys, os, numpy as np, cv2
from PIL import Image
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
img = cv2.cvtColor(np.asarray(Image.open(src).convert('RGB')), cv2.COLOR_RGB2BGR)
H, W = img.shape[:2]
cells = {  # nome: (x0, y0, x1, y1) aproximados
  'sentada': (20, 0, 400, 520), 'acenando': (400, 0, 770, 520), 'dormindo': (760, 130, 1160, 520), 'rindo': (1150, 0, 1530, 520),
  'olhando': (0, 500, 390, 1024), 'piscando': (380, 500, 760, 1024), 'em-pe': (740, 500, 1160, 1024), 'feliz': (1150, 500, 1536, 1024),
}
for name, (x0, y0, x1, y1) in cells.items():
    crop = img[y0:y1, x0:x1].copy(); h, w = crop.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    k = 6 if name == 'sentada' else 1
    rect = (k, k, w - 2 * k, h - 2 * k)
    bgd = np.zeros((1, 65)); fgd = np.zeros((1, 65))
    cv2.grabCut(crop, mask, rect, bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1: m = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    p = cv2.copyMakeBorder(m, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0); cv2.floodFill(p, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 255); m |= cv2.bitwise_not(p)[1:-1, 1:-1]
    m = cv2.GaussianBlur(cv2.erode(m, np.ones((3, 3), np.uint8)), (3, 3), 0)
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(np.dstack([rgb, m]), 'RGBA'); im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    im.save(os.path.join(out, f'layla-{name}.webp'), quality=88, method=6); print(name, im.size)
