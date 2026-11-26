"""Reels 'Obrigada por cada palavra' — 20 avaliações reais do Google em cards (2 por tela),
cada uma com resposta de agradecimento da Shimmer; destaques ganham toque animado (efeito clique).
Avatares = inicial em círculo (padrão do Google quando não há foto). Nome: primeiro nome + inicial.
Fecho com pattern + logo original. Som suave."""
import sys, re, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '/home/user/print')
from shimmer_style import *

D = '/home/user/print/reels/avaliacoes/'
W, H, FPS = 1080, 1920, 30
INK = (58, 45, 34); BR = (118, 88, 38); IV = (250, 247, 241); GREY = (112, 106, 98)
STAR = (214, 165, 52)
PREV = [float(x) for x in sys.argv[1:]]

# (nome exibido, quando, estrelas, texto, resposta, destaque)
R = [
 ('Emanuelle V.', 'há 4 meses', 5, 'Comprei um anel solitário e fui super bem atendida! Eu tinha muito receio de comprar joias pela internet, mas o Júnior me passou muita confiança desde o primeiro contato. Recomendo de olhos fechados!', 'Emanuelle, que alegria ter sua confiança! Seu solitário foi feito com muito carinho.', True),
 ('Erika D.', 'há 2 meses', 5, 'Ótimo atendimento, Júnior muito atencioso, as alianças ficaram lindas, perfeição.', 'Obrigada, Erika! Que essas alianças acompanhem cada capítulo de vocês.', False),
 ('Jean L.', 'há 1 ano', 5, 'Excelência e qualidade, atendimento personalizado. Por se tratar de uma joia, às vezes ficamos com um pé atrás. Mas o pessoal da Shimmer Joias é extremamente correto e transparente.', 'Jean, transparência é o nosso compromisso. Obrigada pela confiança!', True),
 ('Kelen S.', 'há 1 ano', 5, 'Um trabalho impecável, produto de ótima qualidade, ganhei de presente e foram muito ágeis na entrega do meu presente, nota 10 com certeza.', 'Kelen, que bom fazer parte desse presente tão especial!', False),
 ('Nayara B.', 'há 1 ano', 5, 'Sou de Garopaba e fiz meu pedido on-line e fui super bem atendida! A equipe foi muito atenciosa, respondeu super rápido e fez tudo do jeitinho que eu queria.', 'Nayara, de Curitiba até Garopaba com todo o nosso carinho!', True),
 ('Stephany T.', 'há 1 ano', 5, 'Sou de Garopaba-SC, recebi indicação dessa loja por uma amiga e amei!!! Super atenciosos e pacientes, chegou tudo certinho.', 'Stephany, obrigada! E um beijo para a amiga que indicou.', False),
 ('Sifarlei C.', 'há 1 mês', 5, 'A joia chegou em excelente estado e conforme a propaganda. Preço justo. Atendimento excelente. Rápido e sem enrolação.', 'Sifarlei, obrigada! Ficamos felizes que tudo chegou perfeito.', False),
 ('Brendo S.', 'há 5 meses', 5, 'Produto de extrema qualidade, chegou no prazo e ainda com um brinde... Super recomendo!', 'Brendo, o brinde foi nosso jeito de dizer obrigada!', False),
 ('Paola B.', 'há 1 ano', 5, 'Experiência incrível, parabéns aos profissionais pelo trabalho incrível. Ganhei do meu marido alianças de casamento PERFEITAS. Super indico para todos!', 'Paola, que honra fazer parte do seu casamento! Felicidades ao casal.', True),
 ('Baruc', 'há 1 ano', 5, 'Fiz meu par de alianças com eles, desde o primeiro atendimento até a entrega foi tudo perfeito, muita atenção, tudo bem explicado, amei!', 'Baruc, obrigada! Que essas alianças brilhem para sempre.', False),
 ('Allan L.', 'há 1 ano', 5, 'Excelente, desde o ótimo atendimento da atendente Ketelyn, que responde com rapidez e esclarece até as mínimas dúvidas, como também a ótima qualidade do produto.', 'Allan, a Ketelyn ficou muito feliz! Obrigada.', False),
 ('Géssica P.', 'há 1 ano', 5, 'Adquiri um cordão com eles. Qualidade nota mil e atendimento impecável. Recomendo demais!', 'Géssica, que seu cordão brilhe todos os dias!', False),
 ('Victor L.', 'há 4 meses', 5, 'Atendimento diferenciado, atenção, cordialidade e peças lindas! Super recomendo.', 'Victor, obrigada pelo carinho com a nossa equipe!', False),
 ('Luana A.', 'há 4 meses', 5, 'Peças lindas, delicadas, sofisticadas e com ótima qualidade, atendimento ótimo, super recomendo.', 'Luana, delicadeza é a nossa assinatura. Obrigada!', False),
 ('João S.', 'há 5 meses', 5, 'Qualidade incrível e comprometimento em cumprir com prazos, um atendimento excepcional. Parabéns!', 'João, prazo é promessa. Obrigada pela confiança!', False),
 ('Jackson D.', 'há 9 meses', 5, 'Mandei fazer algumas peças e ficaram muito top, atendimento nota 1.000, preço top, super recomendo.', 'Jackson, obrigada! Volte sempre para as próximas peças.', False),
 ('Jessica M.', 'há 1 ano', 5, 'Loja maravilhosa! Fui super bem atendida, com muita atenção e simpatia. As joias são lindas demais, de ótima qualidade, e o melhor: com preço justo!', 'Jessica, você é maravilhosa! Obrigada.', False),
 ('Fábio', 'há 1 ano', 5, 'Preço justo, produto de qualidade e, quanto ao atendimento, nem se fala! Estão de parabéns!', 'Fábio, obrigada! Esse é o padrão Shimmer.', False),
 ('Diogo B.', 'há 2 semanas', 5, 'Joias incríveis com acabamento refinado.', 'Diogo, o acabamento é feito à mão. Obrigada!', False),
 ('Patrick B.', 'há 1 mês', 4, 'Parabéns pelo bom trabalho ao cliente.', 'Patrick, obrigada! Seguimos melhorando por você.', False),
]
AV_COL = [(176, 138, 72), (122, 96, 74), (140, 150, 120), (176, 120, 110), (96, 110, 128)]

INTRO, PAIR, OUTRO = 3.0, 3.8, 4.2
NP = len(R) // 2
TOTAL = INTRO + NP * PAIR + OUTRO

# ---------- background: ivory + very faint pattern ----------
P = Image.open('/home/user/print/assets/pattern-logo.jpg').convert('RGB')
sc = H / P.height; P = P.resize((round(P.width * sc), H), Image.LANCZOS); P = P.crop(((P.width - W) // 2, 0, (P.width - W) // 2 + W, H))
pat = np.asarray(P, np.float32)
yy = np.arange(H, dtype=np.float32)[:, None, None]
BG = pat * 0.10 + np.array(IV, np.float32) * 0.90
BG = BG * (1 - 0.05 * (yy / H)) + np.array((236, 226, 208), np.float32) * 0.05 * (yy / H)
BGI = Image.fromarray(BG.astype(np.uint8)).convert('RGBA')


def wrap(text, fnt, maxw, maxlines):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if fnt.getlength(t) <= maxw: cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        while fnt.getlength(lines[-1] + '… mais') > maxw: lines[-1] = lines[-1].rsplit(' ', 1)[0]
        lines[-1] += '…'
    return lines


def star(d, cx, cy, r, fill):
    pts = []
    for k in range(10):
        a = -np.pi / 2 + k * np.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * np.cos(a), cy + rr * np.sin(a)))
    d.polygon(pts, fill=fill)


CW = 900
FN_NAME, FN_META, FN_BODY, FN_REP_L, FN_REP = sans(38, 700), sans(26, 500), sans(34, 500), sans(24, 700), sans(30, 500)


def card(i, hl=False):
    name, when, st, txt, rep, _ = R[i]
    body = wrap(txt, FN_BODY, CW - 96, 5)
    repl = wrap(rep, FN_REP, CW - 150, 2)
    h = 44 + 112 + 50 + len(body) * 46 + 20 + 46 + len(repl) * 40 + 60
    im = Image.new('RGBA', (CW + 60, h + 60), (0, 0, 0, 0))
    sh = Image.new('L', im.size, 0); ImageDraw.Draw(sh).rounded_rectangle([30, 36, 30 + CW, 30 + h + 6], 34, fill=70 if not hl else 110)
    im.putalpha(0); shadow = Image.new('RGBA', im.size, (70, 50, 25, 0)); shadow.putalpha(sh.filter(ImageFilter.GaussianBlur(16)))
    im = Image.alpha_composite(Image.new('RGBA', im.size, (0, 0, 0, 0)), shadow)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([30, 30, 30 + CW, 30 + h], 34, fill=(255, 255, 255, 255), outline=(STAR if hl else (232, 226, 216)), width=(5 if hl else 2))
    x0, y = 30 + 48, 30 + 44
    col = AV_COL[i % len(AV_COL)]
    d.ellipse([x0, y, x0 + 84, y + 84], fill=col)
    d.text((x0 + 42, y + 43), name[0], font=sans(44, 700), fill=(255, 255, 255), anchor='mm')
    d.text((x0 + 108, y + 4), name, font=FN_NAME, fill=INK)
    d.text((x0 + 108, y + 52), 'Avaliação no Google · ' + when, font=FN_META, fill=GREY)
    if hl:
        t = 'DESTAQUE'; tw = FN_REP_L.getlength(t) + 70
        d.rounded_rectangle([30 + CW - 40 - tw, y + 6, 30 + CW - 40, y + 50], 22, fill=(250, 240, 214))
        star(d, 30 + CW - 40 - tw + 26, y + 28, 12, STAR)
        d.text((30 + CW - 40 - tw + 46, y + 28), t, font=FN_REP_L, fill=BR, anchor='lm')
    y += 112
    for k in range(5): star(d, x0 + 18 + k * 42, y + 16, 18, STAR if k < st else (220, 214, 204))
    y += 50
    for ln in body: d.text((x0, y), ln, font=FN_BODY, fill=(48, 42, 36)); y += 46
    y += 20
    d.rounded_rectangle([x0, y, 30 + CW - 48, y + 24 + len(repl) * 40 + 22], 20, fill=(248, 243, 233))
    d.line([(x0, y + 10), (x0, y + 24 + len(repl) * 40 + 12)], fill=STAR, width=5)
    d.text((x0 + 26, y + 14), 'RESPOSTA DA SHIMMER', font=FN_REP_L, fill=BR)
    yy_ = y + 50
    for ln in repl: d.text((x0 + 26, yy_), ln, font=FN_REP, fill=(84, 72, 60)); yy_ += 40
    return im


CARDS = [card(i, R[i][5]) for i in range(len(R))]

# ---------- header (during cards) ----------
HDR = Image.new('RGBA', (W, 330), (0, 0, 0, 0))
t = solid_text('O QUE NOSSOS CLIENTES DIZEM', caps_font(42, 600), INK, 5); paste(HDR, t, W / 2, 205, anchor='center')
dh = ImageDraw.Draw(HDR)
for k in range(5): star(dh, W / 2 - 84 + k * 42, 290, 15, STAR)

# ---------- intro / outro ----------
def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))
I1 = layer(); t = solid_text('OBRIGADA', caps_font(88, 600), INK, 14); paste(I1, t, W / 2, 610, anchor='center')
I2 = layer(); t = gold_text('por cada', script_font(190)); paste(I2, t, W / 2, 700, anchor='center')
t = gold_text('palavra', script_font(190)); paste(I2, t, W / 2, 860, anchor='center')
I3 = layer(); d3 = ImageDraw.Draw(I3)
for k in range(5): star(d3, W / 2 - 120 + k * 60, 1150, 24, STAR)
t = solid_text('MAIS DE 40 AVALIAÇÕES', caps_font(44, 600), BR, 4); paste(I3, t, W / 2, 1210, anchor='center')
t = solid_text('REAIS NO GOOGLE', caps_font(44, 600), BR, 4); paste(I3, t, W / 2, 1272, anchor='center')
t = solid_text('separamos algumas delas', sans(36, 500), PARCEL_COLOR); paste(I3, t, W / 2, 1350, anchor='center')

# end card: pattern + logo original
g = np.exp(-(((np.arange(W, dtype=np.float32)[None, :, None] - W / 2) / 520) ** 2 + ((yy - 860) / 500) ** 2)) * 0.82
E = Image.fromarray((pat * (1 - g) + np.array(IV, np.float32) * g).astype(np.uint8)).convert('RGBA')
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')
lx = (W - LOGO.width) // 2; E.alpha_composite(LOGO, (lx, 470))
y = 700
t = solid_text('SUA HISTÓRIA TAMBÉM', caps_font(46, 600), INK, 6); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 16
t = gold_text('merece brilhar', script_font(170)); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 44
m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).line([(W / 2 - 60, y), (W / 2 + 60, y)], fill=255, width=3); E.alpha_composite(gold_fill(m)); y += 44
for txt, f, c, tr in [('OURO 18K · GARANTIA VITALÍCIA', caps_font(34, 600), INK, 4), ('CHAME NO DIRECT · LINK NA BIO', caps_font(34, 700), BR, 4),
                      ('atendimento na loja ou online', sans(32, 500), PARCEL_COLOR, 0)]:
    t = solid_text(txt, f, c, tr); paste(E, t, W / 2, y, anchor='center'); y += ink_size(t)[1] + 24
ENDA = np.asarray(E.convert('RGB'), np.float32)


def comp(base, L, dx, dy, alpha=1.0):
    tmp = Image.new('RGBA', base.size, (0, 0, 0, 0)); tmp.paste(L, (int(dx), int(dy)), L)
    if alpha < 1: tmp.putalpha(tmp.getchannel('A').point(lambda v: int(v * max(alpha, 0))))
    base.alpha_composite(tmp)


def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def easeio(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)


TOP, BOT = 360, 1560   # Reels safe zone
TAPS = []  # (time, x, y)


def place_pair(k):
    a, b = CARDS[2 * k], CARDS[2 * k + 1]
    gap = 36; tot = a.height + b.height + gap - 60
    y0 = TOP + max(0, (BOT - TOP - tot) // 2) - 30
    return [(a, y0, 2 * k), (b, y0 + a.height - 60 + gap, 2 * k + 1)]


def frame(t):
    if t < INTRO:
        f = BGI.copy()
        for L, t0 in [(I1, 0.15), (I2, 0.55), (I3, 1.1)]:
            k = ease((t - t0) / 0.7)
            if k > 0: comp(f, L, 0, int((1 - k) * 24), alpha=k * (1 - easeio((t - (INTRO - 0.35)) / 0.35)))
        return np.asarray(f.convert('RGB'))
    if t >= INTRO + NP * PAIR:
        tt = t - (INTRO + NP * PAIR); k = easeio(tt / 0.6)
        base = np.asarray(BGI.convert('RGB'), np.float32)
        return np.clip(base * (1 - k) + ENDA * k, 0, 255).astype(np.uint8)
    tt = t - INTRO; k_ = int(tt // PAIR); lt = tt - k_ * PAIR
    f = BGI.copy()
    ha = ease(tt / 0.6)
    comp(f, HDR, 0, 0, alpha=ha)
    for j, (im, y0, idx) in enumerate(place_pair(k_)):
        tin = 0.05 + j * 0.32
        kin = ease((lt - tin) / 0.55); kout = easeio((lt - (PAIR - 0.42)) / 0.42)
        if kin <= 0: continue
        alpha = kin * (1 - kout)
        dx = int((1 - kin) * (90 if j == 0 else -90)) ; dy = int(-kout * 40)
        s = 1.0
        hl = R[idx][5]; ttap = 1.55
        if hl and lt > ttap:
            s = 1.0 + 0.035 * np.sin(min((lt - ttap) / 0.5, 1) * np.pi / 2)
        img = im
        if s != 1.0: img = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        x = (W - img.width) // 2 + dx; yv = int(y0 - (img.height - im.height) / 2) + dy
        tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.alpha_composite(img, (max(x, -img.width + 1), yv)) if x >= 0 else tmp.paste(img, (x, yv), img)
        if alpha < 1: tmp.putalpha(tmp.getchannel('A').point(lambda v: int(v * alpha)))
        f.alpha_composite(tmp)
        # tap (efeito clique) nos destaques
        if hl:
            cx, cy = (W - img.width) // 2 + dx + img.width - 150, yv + 30 + 44 + 28
            if abs(lt - ttap) < 1 / FPS / 2 + 1e-6 or (lt >= ttap and lt < ttap + 1 / FPS):
                TAPS.append(round(INTRO + k_ * PAIR + ttap, 3))
            ph = lt - (ttap - 0.35)
            if 0 <= ph < 1.1:
                ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
                if ph < 0.35:  # finger dot approaching
                    a_ = ease(ph / 0.35); r = 34
                    do.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, int(200 * a_)), outline=(120, 90, 40, int(160 * a_)), width=3)
                else:
                    p = (ph - 0.35) / 0.75; r = 34 + 90 * ease(p); a_ = 1 - p
                    do.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(214, 165, 52, int(220 * a_)), width=6)
                    r2 = 30 * (1 - 0.3 * p)
                    do.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(255, 255, 255, int(190 * a_)))
                f.alpha_composite(ov)
    return np.asarray(f.convert('RGB'))


N = int(round(TOTAL * FPS))
if PREV:
    for p in PREV:
        Image.fromarray(frame(p)).save(f'/tmp/claude-0/-home-user/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/av_{p:05.2f}.jpg', quality=85)
    print('prev ok', TOTAL); sys.exit()

enc = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-an', D + '_video.mp4'], stdin=subprocess.PIPE)
for n in range(N): enc.stdin.write(frame(n / FPS).tobytes())
enc.stdin.close(); enc.wait()

# ---------- som suave ----------
SR = 48000; L = int(TOTAL * SR); tt = np.arange(L) / SR
pad = np.zeros(L)
for fr, a in [(220.0, .5), (277.18, .35), (329.63, .35), (440.0, .2)]:
    pad += a * np.sin(2 * np.pi * fr * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.08 * tt + fr))
pad *= 0.018 * np.minimum(1, tt / 1.5) * np.minimum(1, (TOTAL - tt) / 1.5)
fx = np.zeros(L)
def add(t0, sig):
    i = int(t0 * SR); n = min(len(sig), L - i)
    if n > 0: fx[i:i + n] += sig[:n]
def chime(f0, dur=1.2, amp=0.05):
    x = np.arange(int(dur * SR)) / SR
    return amp * np.exp(-x * 3.2) * (np.sin(2 * np.pi * f0 * x) + 0.4 * np.sin(2 * np.pi * f0 * 2.01 * x))
def whoosh(dur=0.45, amp=0.025):
    n = int(dur * SR); nz = np.random.default_rng(1).standard_normal(n)
    nz = np.convolve(nz, np.ones(40) / 40, 'same'); env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return amp * nz * env
add(0.2, chime(880)); add(0.6, chime(1318.5, amp=0.035))
for k in range(NP):
    t0 = INTRO + k * PAIR; add(t0, whoosh())
    if R[2 * k][5] or R[2 * k + 1][5]: add(t0 + 1.55, chime(1760, 0.5, 0.03))
add(INTRO + NP * PAIR, chime(659.25, 2.0, 0.045)); add(INTRO + NP * PAIR + 0.25, chime(987.77, 2.0, 0.035))
mix = np.clip(pad + fx, -1, 1)
st_ = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
with wave.open(D + '_audio.wav', 'wb') as wv:
    wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes(st_.tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', D + '_video.mp4', '-i', D + '_audio.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                '-shortest', '-movflags', '+faststart', D + 'reels-avaliacoes-obrigada.mp4'], check=True)
print('ok', TOTAL)
