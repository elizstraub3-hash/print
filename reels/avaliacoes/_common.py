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



