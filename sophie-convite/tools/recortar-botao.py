import sys, numpy as np, cv2
from PIL import Image
src, broken, out, prev = sys.argv[1:5]
img = cv2.cvtColor(np.asarray(Image.open(src).convert('RGB')), cv2.COLOR_RGB2BGR)
a = np.asarray(Image.open(broken).convert('RGBA'))[:, :, 3]
H, W = a.shape
mask = np.full((H, W), cv2.GC_PR_BGD, np.uint8)
fg = (a > 200).astype(np.uint8)
mask[cv2.erode(fg, np.ones((5, 5), np.uint8)) > 0] = cv2.GC_FGD
near = cv2.dilate(fg, np.ones((61, 61), np.uint8))
mask[(near > 0) & (fg == 0)] = cv2.GC_PR_FGD
mask[near == 0] = cv2.GC_BGD
mask[:3, :] = mask[-3:, :] = cv2.GC_BGD; mask[:, :3] = mask[:, -3:] = cv2.GC_BGD
bgd = np.zeros((1, 65), np.float64); fgd = np.zeros((1, 65), np.float64)
cv2.grabCut(img, mask, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
m = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
# maior componente + preencher buracos
n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
k = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]); m = np.where(lab == k, 255, 0).astype(np.uint8)
ff = m.copy(); cv2.floodFill(ff, np.zeros((H + 2, W + 2), np.uint8), (0, 0), 255); m = m | cv2.bitwise_not(ff)
m = cv2.GaussianBlur(m, (3, 3), 0)
rgb = np.asarray(Image.open(src).convert('RGB'))
res = Image.fromarray(np.dstack([rgb, m]), 'RGBA')
res.save(out)
for i, c in enumerate([(235, 228, 250), (60, 40, 80)]):
    bg = Image.new('RGBA', res.size, c + (255,)); bg.alpha_composite(res); bg.convert('RGB').save(prev.replace('.png', f'{i}.png'))
