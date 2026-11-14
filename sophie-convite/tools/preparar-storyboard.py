"""
Recorta os 9 quadros do storyboard, remove o número (canto superior esquerdo)
e o contador de estrelas (canto inferior direito), amplia 2x e salva WebP.
Uso: python3 tools/preparar-storyboard.py storyboard.png public/img/historia
"""
import sys, os, numpy as np, cv2
from PIL import Image

src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
im = np.asarray(Image.open(src).convert('RGB'))
BOXES = [(0, 0, 454, 306), (459, 0, 814, 306), (819, 0, 1193, 306),
         (0, 311, 454, 621), (460, 311, 814, 621), (819, 311, 1193, 621),
         (0, 626, 409, 941), (416, 626, 793, 941), (801, 626, 1193, 941)]
HUD = {5, 6, 7, 8}  # quadros com o contador "x/5"
for i, (x0, y0, x1, y1) in enumerate(BOXES, 1):
    p = im[y0:y1, x0:x1].copy()
    h, w = p.shape[:2]
    m = np.zeros((h, w), np.uint8)
    # selo com o número da cena
    cv2.ellipse(m, (int(w * 0.088), int(h * 0.1)), (int(w * 0.075), int(h * 0.085)), 0, 0, 360, 255, -1)
    if i in HUD:
        cv2.rectangle(m, (int(w * 0.69), int(h * 0.84)), (w - 3, h - 3), 255, -1)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    p = cv2.inpaint(p, m, 9, cv2.INPAINT_TELEA)
    # corta 4 px da borda (sobras do quadro branco)
    p = p[4:-4, 4:-4]
    img = Image.fromarray(p).resize(((w - 8) * 2, (h - 8) * 2), Image.LANCZOS)
    img.save(os.path.join(outdir, f'cena-{i}.webp'), quality=84, method=6)
    print(i, img.size)
