"""Preset "Shimmer Clean": the same correction for every photo so the feed looks like one brand.
1. neutral white balance (gray-world on the mid-tones) + a touch of warmth, the same for all photos
2. levels normalised to one target (black point, median, white point), so every photo has the same brightness
3. soft S contrast curve
4. vibrance that leaves skin tones alone
5. fine sharpening, so metal and stones read crisp (no fake sparkle)
"""
import sys, glob, os
import numpy as np
from PIL import Image, ImageFilter

TARGET = dict(black=20.0, mid=140.0, white=248.0)
WARMTH = (1.035, 1.0, 0.95)          # same warmth for every photo


def srgb_to_lin(x): return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
def lin_to_srgb(x): return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(np.clip(x, 0, None), 1 / 2.4) - 0.055)


def shimmer_clean(im):
    a = np.asarray(im.convert('RGB'), np.float32) / 255.0
    # 1. white balance on mid-tones only (ignores clipped whites and deep blacks)
    lum = a.mean(2)
    m = (lum > 0.2) & (lum < 0.85)
    lin = srgb_to_lin(a)
    means = lin[m].mean(0) if m.sum() > 1000 else lin.reshape(-1, 3).mean(0)
    gains = means.mean() / means
    gains = 1 + (gains - 1) * 0.5                      # 50% correction keeps the warmth of gold and skin
    lin = lin * gains * np.array(WARMTH)
    a = np.clip(lin_to_srgb(np.clip(lin, 0, 1)), 0, 1)
    # 2. levels: black point, median, white point to the same target for every photo
    L = a.mean(2) * 255
    p_lo, p_mid, p_hi = np.percentile(L, [0.8, 50, 99.6])
    p_lo = min(p_lo, 24.0)                             # bright photos keep their shadows (no darker skin)
    p_hi = max(p_hi, 235.0)
    x = np.clip((a * 255 - p_lo) / max(1, p_hi - p_lo), 0, 1)
    mid_n = np.clip((p_mid - p_lo) / max(1, p_hi - p_lo), 0.05, 0.95)
    tgt_n = (TARGET['mid'] - TARGET['black']) / (TARGET['white'] - TARGET['black'])
    g = np.log(tgt_n) / np.log(mid_n)
    g = float(np.clip(g, 0.6, 1.0))                     # brighten when needed, never darken a bright photo
    x = x ** g
    # 3. soft S curve
    s = 0.08
    x = x + s * x * (1 - x) * (x - 0.5) * 2
    x = p_lo / 255 * 0 + TARGET['black'] / 255 * (p_lo < 24) + x * (TARGET['white'] - TARGET['black'] * (p_lo < 24)) / 255
    # 4. vibrance, protecting skin (hue ~ orange)
    mx, mn = x.max(2, keepdims=True), x.min(2, keepdims=True)
    sat = (mx - mn) / (mx + 1e-6)
    r, gg, b = x[..., :1], x[..., 1:2], x[..., 2:]
    skin = ((r > gg) & (gg > b) & (sat > 0.15) & (sat < 0.6)).astype(np.float32)
    amt = 0.18 * (1 - sat) * (1 - 0.8 * skin)
    grey = x.mean(2, keepdims=True)
    x = np.clip(grey + (x - grey) * (1 + amt), 0, 1)
    out = Image.fromarray((x * 255 + 0.5).astype(np.uint8))
    # 5. fine sharpening
    return out.filter(ImageFilter.UnsharpMask(radius=2.2, percent=55, threshold=2))


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    files = sys.argv[3:] or sorted(glob.glob(src + '/*.jpg'))
    for f in files:
        f = f if os.path.isabs(f) else os.path.join(src, f)
        shimmer_clean(Image.open(f)).save(os.path.join(dst, os.path.basename(f)), quality=95, subsampling=0)
    print('ok', len(files))
