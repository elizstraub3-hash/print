"""Reels narrado (animação): pedido na virada + cartório em janeiro + alianças já garantidas."""
import sys, subprocess, math
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad')
from shimmer_style import *
from story_nativo_lib import emoji

TTS = '/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/tts/'
K = '/home/user/print/black-friday-kit/'
OUT = K + 'reels-pedido-virada-cartorio.mp4'
PREV = [float(x) for x in sys.argv[1:]]
W, H, FPS = 1080, 1920, 30
IV = (246, 242, 235); INK = (58, 45, 34); BR = (132, 101, 46); SOFT = (112, 103, 93)
GAP = 0.32

# ---------- narration: trim silence, lay segments end to end ----------
segs, starts, t = [], [], 0.35
for i in range(8):
    a, sr = sf.read(TTS + f'n{i}.wav')
    nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, nz[0] - 600): nz[-1] + 1200]
    segs.append(a); starts.append(t); t += len(a) / sr + GAP
SR = sr; DUR = t + 1.6
END = [starts[i] + len(segs[i]) / SR for i in range(8)]
audio = np.zeros(int(DUR * SR) + SR)
for s, a in zip(starts, segs): audio[int(s * SR): int(s * SR) + len(a)] += a
sf.write(TTS + 'narr.wav', audio, SR)
SC = [(starts[i], starts[i + 1] if i < 7 else DUR) for i in range(8)]


def ease(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)
def eout(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def back(x):
    x = min(max(x, 0), 1); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def L(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def put(base, lay_bb, cx, y, k=1.0, scale=1.0, rise=24):
    """Paste a text/ink layer centred at cx, top at y, fading/rising in with k, optional pop scale."""
    if k <= 0.01: return
    lay, bb = lay_bb
    x0, y0, x1, y1 = bb; im = lay.crop(bb)
    if scale != 1.0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    a = im.getchannel('A').point(lambda v: int(v * min(1, k)))
    im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(y + (1 - eout(k)) * rise - (im.height - (y1 - y0)) / 2)))


def ink(text, f, color, tr=0): return solid_text(text, f, color, tr)
DG = (150, 110, 45)
def gtx(text, f, tr=0): return solid_text(text, f, DG, tr)


def card_photo(path, box, size, radius=48):
    """Rounded photo card; `box` crops the (already 2x super-resolved) photo, shown downscaled only."""
    im = Image.open(path).convert('RGB').crop(box).resize(size, Image.LANCZOS)
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    out = Image.new('RGBA', (size[0] + 12, size[1] + 12), (0, 0, 0, 0))
    fr = Image.new('L', out.size, 0); ImageDraw.Draw(fr).rounded_rectangle([0, 0, out.width - 1, out.height - 1], radius=radius + 6, fill=255)
    out.alpha_composite(gold_fill(fr)); im = im.convert('RGBA'); im.putalpha(m); out.alpha_composite(im, (6, 6))
    return out


def circle_photo(path, cx, cy, r, d):
    im = Image.open(path).convert('RGB').crop((cx - r, cy - r, cx + r, cy + r)).resize((d, d), Image.LANCZOS)
    m = Image.new('L', (d, d), 0); ImageDraw.Draw(m).ellipse([0, 0, d - 1, d - 1], fill=255)
    out = Image.new('RGBA', (d + 14, d + 14), (0, 0, 0, 0))
    fr = Image.new('L', out.size, 0); ImageDraw.Draw(fr).ellipse([0, 0, out.width - 1, out.height - 1], fill=255)
    out.alpha_composite(gold_fill(fr)); im = im.convert('RGBA'); im.putalpha(m); out.alpha_composite(im, (7, 7))
    return out


def paste_obj(base, obj, cx, cy, k, s0=0.85):
    if k <= 0.01: return
    s = s0 + (1 - s0) * back(k)
    im = obj.resize((max(1, int(obj.width * s)), max(1, int(obj.height * s))), Image.LANCZOS)
    a = im.getchannel('A').point(lambda v: int(v * min(1, k * 1.6))); im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def gold_stroke(draw_fn, k):
    """Line-art drawn progressively: draw_fn(draw, k) draws the visible part on an L mask."""
    m = Image.new('L', (W, H), 0); draw_fn(ImageDraw.Draw(m), k); return gold_fill(m) if m.getbbox() else None


# ---------- assets ----------
KIT = card_photo(K + 'fotos/66_x2.png', (0, 560, 968, 1460), (760, 706))
SOL = circle_photo(K + 'fotos/63_x2.png', 600, 760, 300, 520)
ALI = card_photo(K + 'fotos/65_x2.png', (40, 640, 900, 1480), (700, 683))
KIT_S = card_photo(K + 'fotos/66_x2.png', (0, 560, 968, 1460), (560, 520), radius=40)

F_BIG = sans(84, 800); F_MID = sans(60, 800); F_TXT = sans(40, 600); F_SM = sans(34, 500)


def bg(t):
    im = Image.new('RGBA', (W, H), IV + (255,))
    # very soft warm vignette so the ivory doesn't look flat
    return im


def ring_icon(d, k, cx=540, cy=330, r=70):
    if k <= 0: return
    d.arc([cx - r, cy - r + 30, cx + r, cy + r + 30], start=-90, end=-90 + 360 * min(1, k * 1.4), fill=255, width=9)
    if k > 0.6:
        kk = ease((k - 0.6) / 0.4); s = 34 * kk
        d.polygon([(cx, cy - 40 - s), (cx + s, cy - 40), (cx, cy - 40 + s * 0.9), (cx - s, cy - 40)], fill=255)


def calendar(base, cx, top, k, month, day, flip=1.0):
    if k <= 0.01: return
    w, h = 420, 400
    lay = L(); d = ImageDraw.Draw(lay)
    sy = max(0.02, flip)
    hh = h * sy; y0 = top + (h - hh) / 2
    d.rounded_rectangle([cx - w / 2, y0, cx + w / 2, y0 + hh], radius=34, fill=(255, 253, 249, 255), outline=(200, 170, 110, 255), width=4)
    hdr = Image.new('L', (W, H), 0); ImageDraw.Draw(hdr).rounded_rectangle([cx - w / 2, y0, cx + w / 2, y0 + 110 * sy], radius=34, fill=255)
    ImageDraw.Draw(hdr).rectangle([cx - w / 2, y0 + 60 * sy, cx + w / 2, y0 + 110 * sy], fill=255)
    lay.alpha_composite(gold_fill(hdr))
    if sy > 0.6:
        mt = ink(month, caps_font(52, 700), (255, 253, 248), 8); put(lay, mt, cx, y0 + 26 * sy, 1, rise=0)
        dy = ink(day, sans(170 if len(day) <= 2 else 120, 700), INK); put(lay, dy, cx, y0 + 150 * sy, 1, rise=0)
    a = lay.getchannel('A').point(lambda v: int(v * min(1, k))); lay.putalpha(a)
    base.alpha_composite(lay, (0, int((1 - eout(k)) * 40)))


def doc_icon(d, k, cx, cy):
    """Line-art certificate with a signature line and a seal, drawn progressively."""
    w, h = 300, 360
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2), (cx - w / 2, cy - h / 2)]
    total = 2 * (w + h); dist = total * min(1, k * 1.5)
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        if dist <= 0: break
        f = min(1, dist / seg); d.line([a, (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)], fill=255, width=7); dist -= seg
    if k > 0.55:
        kk = ease((k - 0.55) / 0.3)
        for i in range(3):
            y = cy - 110 + i * 55; d.line([(cx - 100, y), (cx - 100 + 200 * kk, y)], fill=255, width=6)
    if k > 0.8:
        kk = ease((k - 0.8) / 0.2); r = 46 * kk
        d.ellipse([cx + 40 - r, cy + 90 - r, cx + 40 + r, cy + 90 + r], outline=255, width=7)
        d.line([(cx - 120, cy + 120), (cx - 120 + 110 * kk, cy + 120)], fill=255, width=5)


def frame(t):
    im = bg(t)
    i = max(j for j in range(8) if SC[j][0] <= t) if t >= SC[0][0] else 0
    lt = t - SC[i][0]; dur = SC[i][1] - SC[i][0]
    out_k = 1 - ease((lt - (dur - 0.22)) / 0.22) if i < 7 else 1.0     # quick fade at each scene end

    if t < SC[0][0] or i == 0:                                  # hook
        lt = max(0, t - SC[0][0]) if t >= SC[0][0] else 0
        s = gold_stroke(lambda d, k: ring_icon(d, k, 540, 470, 80), eout(lt / 0.9))
        if s: im.alpha_composite(s)
        words = [(ink('Vai pedir ela em', F_BIG, INK), 700, 0.0), (gtx('casamento', script_font(190)), 810, 0.55),
                 (ink('na virada do ano?', F_BIG, INK), 1060, 1.3)]
        for lay, y, t0 in words: put(im, lay, W / 2, y, eout((lt - t0 + 0.2) / 0.35))
    elif i == 1:
        k = eout(lt / 0.3)
        put(im, ink('Então presta', F_BIG, INK), W / 2, 760, k, scale=0.8 + 0.2 * back(lt / 0.35), rise=0)
        put(im, gtx('atenção', script_font(200)), W / 2, 860, eout((lt - 0.3) / 0.3), scale=0.8 + 0.2 * back((lt - 0.3) / 0.35), rise=0)
        e = emoji('👀', 110); paste_obj(im, e, W / 2, 1210, eout((lt - 0.6) / 0.3))
    elif i == 2:
        put(im, ink('NA SHIMMER, VOCÊ LEVA', caps_font(40, 700), BR, 6), W / 2, 300, eout(lt / 0.4))
        paste_obj(im, KIT, W / 2, 760, eout((lt - 0.15) / 0.6), 0.9)
        put(im, ink('o par de alianças em ouro 18k', F_TXT, INK), W / 2, 1150, eout((lt - 0.8) / 0.4))
        put(im, gtx('+ ganha o solitário', script_font(120)), W / 2, 1220, eout((lt - 3.0) / 0.4), scale=0.85 + 0.15 * back((lt - 3.0) / 0.4))
    elif i == 3:
        calendar(im, W / 2, 300, eout(lt / 0.45), 'DEZEMBRO', '31')
        paste_obj(im, SOL, W / 2, 1060, eout((lt - 0.5) / 0.5))
        put(im, ink('na virada:', F_TXT, SOFT), W / 2, 1360, eout((lt - 0.9) / 0.4))
        put(im, gtx('o pedido', script_font(130)), W / 2, 1410, eout((lt - 1.1) / 0.4))
    elif i == 4:
        if lt < 0.25: m, d_, flip = 'DEZEMBRO', '31', 1 - ease(lt / 0.25)
        else: m, d_, flip = 'JANEIRO', '2027', ease((lt - 0.25) / 0.25)
        calendar(im, W / 2, 300, 1, m, d_, flip)
        put(im, ink('ela disse sim', F_TXT, SOFT), W / 2, 760, eout((lt - 0.3) / 0.4))
        s = gold_stroke(lambda d, k: doc_icon(d, k, W / 2, 1100), eout((lt - 0.9) / 1.2))
        if s: im.alpha_composite(s)
        put(im, gtx('e já marcam o cartório', script_font(104)), W / 2, 1330, eout((lt - 1.6) / 0.4))
    elif i == 5:
        put(im, ink('E AS ALIANÇAS?', caps_font(46, 700), BR, 6), W / 2, 300, eout(lt / 0.35))
        paste_obj(im, ALI, W / 2, 790, eout((lt - 0.4) / 0.5), 0.88)
        put(im, gtx('já estão com vocês', script_font(118)), W / 2, 1180, eout((lt - 0.9) / 0.4))
    elif i == 6:
        put(im, ink('1 presente · 2 momentos', F_MID, INK), W / 2, 520, eout(lt / 0.35))
        # name card: she gets your surname (typewriter)
        cy = 900; lay = L(); d = ImageDraw.Draw(lay)
        kc = eout((lt - 0.6) / 0.4)
        if kc > 0.01:
            d.rounded_rectangle([130, cy - 120, 950, cy + 150], radius=30, fill=(255, 253, 249, int(255 * kc)), outline=(200, 170, 110, int(255 * kc)), width=4)
            im.alpha_composite(lay)
            put(im, ink('SRA.', caps_font(30, 700), BR, 8), W / 2, cy - 90, kc, rise=0)
            put(im, ink('Ana Clara', sans(66, 700), INK), W / 2, cy - 40, kc, rise=0)
            full = '+ o seu sobrenome'
            n = int(len(full) * min(1, max(0, (lt - 1.8) / 1.1)))
            if n:
                sur = gtx(full[:n], script_font(84)); put(im, sur, W / 2, cy + 40, 1, rise=0)
                if n < len(full) and int(lt * 4) % 2 == 0:
                    xe = W / 2 + ink_size(sur)[0] / 2 + 10; ImageDraw.Draw(im).line([(xe, cy + 50), (xe, cy + 120)], fill=BR, width=4)
        e = emoji('💍', 100); paste_obj(im, e, W / 2, 1230, eout((lt - 2.9) / 0.3))
    else:                                                        # price / CTA
        put(im, ink('BLACK FRIDAY SHIMMER', caps_font(40, 700), BR, 8), W / 2, 270, eout(lt / 0.35))
        paste_obj(im, KIT_S, W / 2, 640, eout((lt - 0.1) / 0.5), 0.9)
        put(im, ink('R$ 3.199,00', sans(118, 700), INK), W / 2, 960, eout((lt - 0.3) / 0.4))
        put(im, ink('em até 10x de R$ 319,90 sem juros', F_SM, SOFT), W / 2, 1110, eout((lt - 1.4) / 0.4))
        put(im, gtx('ou R$ 2.879,10 à vista · 10% OFF', sans(38, 700)), W / 2, 1165, eout((lt - 1.8) / 0.4))
        put(im, ink('ALIANÇAS + SOLITÁRIO · OURO 18K · ATÉ 18/12', caps_font(24, 600), BR, 3), W / 2, 1240, eout((lt - 3.0) / 0.4))
        kp = eout((lt - 4.6) / 0.4)
        if kp > 0.01:
            tx = ink('Agende pelo WhatsApp · link na bio', sans(36, 700), (255, 253, 248)); tw, th = ink_size(tx)
            box = [W / 2 - tw / 2 - 46, 1330, W / 2 + tw / 2 + 46, 1330 + th + 48]
            pl = L(); ImageDraw.Draw(pl).rounded_rectangle(box, radius=(th + 48) // 2, fill=(40, 32, 25, int(255 * kp)))
            im.alpha_composite(pl)
            m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(box, radius=(th + 48) // 2, outline=int(255 * kp), width=4)
            im.alpha_composite(gold_fill(m)); put(im, tx, W / 2, 1354, kp, rise=0)
    sh = Image.new('RGBA', (W, H), IV + (255,)); sh.alpha_composite(im.crop((0, 0, W, H - 120)), (0, 120)); im = sh
    if out_k < 1:
        im = Image.blend(Image.new('RGBA', (W, H), IV + (255,)), im, out_k)
    return np.asarray(im.convert('RGB'))


if PREV:
    for t in PREV: Image.fromarray(frame(t)).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/rn_{t}.jpg', quality=88)
    print('scenes', [(round(a, 2), round(b, 2)) for a, b in SC]); sys.exit()
enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-i', TTS + 'narr.wav', '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '192k', '-af', 'loudnorm=I=-14:TP=-1.5', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait(); print('ok', DUR)
