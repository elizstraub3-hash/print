"""
Separa os cartões de raspadinha de uma prancha (fundo branco), deixa o
fundo transparente e APAGA o texto de instrução (o texto é escrito pelo
site, a partir de src/config/event.js → SCRATCH_CARDS).
Uso: python3 tools/preparar-raspadinhas.py prancha.png public/img/raspadinhas [previa.png]
Requer: pip install opencv-python-headless pillow numpy
"""
import sys, os, numpy as np, cv2
from PIL import Image

src, outdir = sys.argv[1], sys.argv[2]
prev = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(outdir, exist_ok=True)
rgb = np.asarray(Image.open(src).convert('RGB'))
H, W, _ = rgb.shape
white = (rgb.min(2) >= 244).astype(np.uint8) * 255
ff = cv2.copyMakeBorder(white, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=255)  # margem branca: fundo é uma região só
cv2.floodFill(ff, np.zeros((H + 4, W + 4), np.uint8), (0, 0), 128)
fg = np.where(ff[1:-1, 1:-1] == 128, 0, 255).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
cards = sorted([i for i in range(1, n) if st[i][4] > 20000], key=lambda i: (st[i][1] > H * 0.4, st[i][0]))
tiles = []
for k, i in enumerate(cards):
    x, y, w, h = st[i][:4]
    m = (lab[y:y + h, x:x + w] == i).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    # preenche buracos internos (margem de 1 px para o fundo ser uma região só)
    pad = cv2.copyMakeBorder(m, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    ffm = pad.copy(); cv2.floodFill(ffm, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 255)
    m |= cv2.bitwise_not(ffm)[1:-1, 1:-1]
    alpha = cv2.GaussianBlur(m, (3, 3), 0)
    alpha[alpha < 70] = 0  # sem pixels quase transparentes (evita riscos na silhueta)
    crop = rgb[y:y + h, x:x + w].copy()
    # ---- apaga o texto (roxo) da área de instrução ----
    x0, x1, y0, y1 = int(w * 0.36), int(w * 0.97), int(h * 0.46), int(h * 0.82)
    reg = crop[y0:y1, x0:x1].astype(int)
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    purple = (g < 120) & (b > 60) & (r < 200) & (b > g + 20)
    tm = np.zeros((h, w), np.uint8)
    tm[y0:y1, x0:x1][purple] = 255
    # junta letras e inclui o contorno branco
    tm = cv2.dilate(tm, np.ones((9, 9), np.uint8))
    bbox_mask = np.zeros_like(tm); 
    ys, xs = np.nonzero(tm)
    tb = (xs.min(), ys.min(), xs.max(), ys.max())
    crop = cv2.inpaint(crop, tm, 9, cv2.INPAINT_TELEA)
    crop = cv2.GaussianBlur(crop, (1, 1), 0)
    out = Image.fromarray(np.dstack([crop, alpha]), 'RGBA')
    out.save(os.path.join(outdir, f'raspadinha-{k + 1}.webp'), quality=86, method=6)
    print(k + 1, (w, h), 'texto em', [round(tb[0] / w, 3), round(tb[1] / h, 3), round(tb[2] / w, 3), round(tb[3] / h, 3)])
    tiles.append(out)
if prev:
    sheet = Image.new('RGBA', (sum(t.width for t in tiles) // 2 + 10, 560 * 2), (230, 220, 245, 255))
    xx = 0
    for k, t in enumerate(tiles):
        t2 = t.resize((t.width // 2, t.height // 2)); sheet.alpha_composite(t2, ((k % 3) * 265, (k // 3) * 280))
    sheet.crop((0, 0, 800, 560)).convert('RGB').save(prev)
