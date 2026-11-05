import sys, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, '.')
from shimmer_style import *
OUT_MP4, OUT_PDF = sys.argv[1], sys.argv[2]
PREV = os.environ.get('PREV')
W, H, FPS = 1920, 1080, 30
BGC = (244, 239, 231); INK = (74, 59, 46); BR = (132, 101, 46)
UP = '/root/.claude/uploads/081c4020-c9a3-5394-8b04-d630e012eb6b/'
SITE = '/home/user/shimmer-joias-/images/'
LOGO = Image.open('/home/user/print/marca/logo-oficial.png').convert('RGBA')
PX, PY, PW, PH = 130, 100, 495, 880   # 9:16 reference panel

SL = [
 dict(kind='cover', dur=7),
 dict(kind='info', dur=10, kick='PARA QUE SERVE ESTE ENSAIO', title='O objetivo', ref=('img', SITE + 'SH-1084.jpg'),
      secs=[('', ['Produzir o conteúdo de novembro e dezembro: lançamento do Anel Diana, Black Friday, Natal e Réveillon.',
                  'Prioridade total para os solitários: é o que mais vende e o que vende mais rápido.',
                  'Alianças com foco no sob medida: mostrar que cada par é feito para o casal.'])]),
 dict(kind='info', dur=12, kick='O QUE O INSTAGRAM MOSTRA', title='Por que solitários', ref=('img', SITE + 'SH-1014.jpg'),
      secs=[('ÚLTIMOS 12 MESES · 97 POSTS', ['Posts de solitários levam, em média, 7 visitas ao perfil. Os de alianças, menos de 1.',
                  'Solitários são salvos 3 vezes mais que alianças.',
                  'O post campeão foi o Solitário Clássico: 39 visitas ao perfil e 17 salvamentos.',
                  'Por isso, cerca de 60% do tempo do ensaio vai para os solitários.'])]),
 dict(kind='info', dur=10, kick='O CLIMA DAS IMAGENS', title='A estética', ref=('img', SITE + 'SH-1086.jpg'),
      secs=[('', ['Luz natural e suave, de janela. Nada de flash direto.',
                  'Tons bege, off-white e dourado: linho, veludo e madeira clara.',
                  'Sem filtros e sem brilhos aplicados: a joia como ela é.',
                  'Fundo limpo, poucos objetos. A joia é a estrela.'])]),
 dict(kind='info', dur=11, kick='ANTES DE COMEÇAR', title='Regras técnicas', ref=('vid', UP + 'f2dff104-VID-20261105-WA0014.mp4', 0), guide=True,
      secs=[('', ['Vídeos na vertical (9:16), em 4K, a 30 ou 60 fps.',
                  'Fotos na vertical (4:5 e 9:16) e algumas na horizontal.',
                  'Deixe o terço de cima livre: é onde entra o texto do post.',
                  'Foco sempre na pedra. Use macro nos detalhes.',
                  'Limpe a joia com flanela antes de cada take.',
                  'Planos de 10 a 15 segundos, sem cortes, com a câmera firme.'])]),
 dict(kind='scene', dur=14, kick='CENA 1 · CENÁRIO BEGE · PRIORIDADE', title='Still dos solitários', pieces='Maria, Clássico, Infinito, Serena, Ariel, Diana, Céu da Noite, Amélia e Jardim de Rosas', ref=('img', SITE + 'SH-1061.jpg'),
      secs=[('FOTOS', ['Frente, 45° e lateral de cada solitário.', 'Macro da pedra e das garras.', 'Cada um na caixinha aberta.', 'Todos lado a lado, do menor para o maior preço (guia de presentes).']),
            ('VÍDEOS', ['Giro lento de cada solitário num prato giratório.', 'Câmera passando devagar pela peça.'])],
      tip='Um rebatedor branco do lado oposto à janela suaviza as sombras.'),
 dict(kind='scene', dur=13, kick='CENA 2 · LUZ DE JANELA OU VARANDA', title='Caixinha na mão', pieces='Serena, Diana, Céu da Noite e Clássico',
      ref=('vid', UP + 'f2dff104-VID-20261105-WA0014.mp4', 3), guide=True,
      secs=[('VÍDEOS', ['Caixinha aberta na mão, movendo devagar para a luz bater na pedra.', 'Fundo desfocado: a cidade, plantas ou a vitrine.']),
            ('FOTOS', ['A caixinha aberta com o fundo desfocado.'])],
      tip='É o formato que mais funciona no perfil: a pedra brilhando com a luz natural.'),
 dict(kind='scene', dur=13, kick='CENA 3 · O MOMENTO DO SIM', title='POV do pedido', pieces='Serena, Maria, Clássico e Diana',
      ref=('vid', UP + '550e399f-VID-20261105-WA0016.mp4', 0), guide=True,
      secs=[('VÍDEOS', ['Câmera no lugar dos olhos dela: a caixinha aparece e abre.', 'Mãos dele segurando a caixinha (só as mãos, sem rosto).', 'A mão dela recebendo o anel.']),
            ('FOTOS', ['A caixinha aberta entre as mãos do casal.'])],
      tip='Grave a abertura da caixinha devagar, pelo menos 3 vezes.'),
 dict(kind='scene', dur=13, kick='CENA 4 · MÃO DE MODELO', title='Anel na mão', pieces='Todos os solitários',
      ref=('vid', UP + 'c28071bc-VID-20261105-WA0015.mp4', 0), guide=True,
      secs=[('FOTOS', ['Mão relaxada, dedos levemente dobrados.', 'Mão no rosto, como na foto clássica da princesa Diana.', 'Comparação na mão: pedras de 2, 5 e 6 mm, uma de cada vez.']),
            ('VÍDEOS', ['A mão girando devagar para a pedra pegar a luz.'])],
      tip='Unhas curtas, esmalte nude ou claro e pele hidratada.'),
 dict(kind='scene', dur=13, kick='CENA 5 · O OURIVES TRABALHANDO', title='Na bancada', pieces='Peças em produção',
      ref=('seq', 'v2'), guide=True,
      secs=[('VÍDEOS', ['Solda com o maçarico.', 'Lixamento e polimento: a peça bruta virando joia.', 'Close nas mãos e nas ferramentas.', 'Grave o som ambiente da bancada, sem música.']),
            ('FOTOS', ['Mãos do ourives com a peça. Ferramentas sobre a bancada.'])],
      tip='É o conteúdo que mais gera confiança. Grave bastante material.'),
 dict(kind='scene', dur=12, kick='CENA 5 · DETALHES DA BANCADA', title='Cravação', pieces='Pedra central dos solitários',
      ref=('seq', 'v1'), guide=True,
      secs=[('VÍDEOS', ['Cravação das pedras, em macro.', 'As pedrinhas soltas na bancada, ao lado da peça.', 'O antes e o depois: a peça bruta e a peça pronta.'])],
      tip='Use o macro e mantenha o foco na ponta da ferramenta.'),
 dict(kind='scene', dur=13, kick='CENA 6 · SOB MEDIDA', title='Alianças', pieces='1 ou 2 pares do mostruário',
      ref=('seq', 'v3'), guide=True,
      secs=[('VÍDEOS', ['A consultora medindo o aro com o medidor.', 'A escolha da largura e do modelo com o casal.', 'A aliança sendo feita na bancada, do fio de ouro à peça pronta.']),
            ('FOTOS', ['O par sobre um espelho, com o reflexo.', 'Mãos do casal entrelaçadas com as alianças.'])],
      tip='Menos peças e mais processo: o que vende a aliança é mostrar que ela é feita para o casal.'),
 dict(kind='scene', dur=13, kick='CENA 7 · NATAL E RÉVEILLON', title='Natal e Réveillon', pieces='Céu da Noite, Maria, Serena, Jardim de Rosas, Amélia e Ariel',
      ref=('card', 'Natal'),
      secs=[('CENÁRIO', ['Pisca-pisca desfocado ao fundo, papel kraft ou bege com fita dourada, taças de espumante.']),
            ('FOTOS', ['A caixinha saindo do embrulho.', 'O Jardim de Rosas como presente para ela.', 'O Céu da Noite com as taças, para o Réveillon.']),
            ('VÍDEOS', ['Mãos desembrulhando o presente.', 'Um brinde com a mão usando o anel.'])],
      tip='As luzinhas ficam sempre desfocadas ao fundo. Nunca brilho aplicado.'),
 dict(kind='scene', dur=13, kick='CENA 8 · HUMANIZAR A MARCA', title='Loja e equipe', pieces='Ponto físico, consultora e ourives',
      ref=('card', 'Loja'),
      secs=[('FOTOS', ['Fachada e vitrine.', 'A consultora mostrando as peças.', 'Retrato da equipe e do ourives.']),
            ('VÍDEOS', ['Alguém entrando na loja.', 'Um atendimento (de costas ou com autorização).', 'A equipe dizendo “Bem-vindos à Shimmer”.', 'Cliente retirando o presente na loja.'])],
      tip='Pessoas geram conexão: grave pelo menos 3 vídeos com rosto.'),
 dict(kind='list', dur=15, kick='CHECKLIST', title='O que levar',
      cols=[['Tripé e estabilizador', 'Lente macro', 'Rebatedor branco', 'Prato giratório', 'Espelho ou vidro', 'Flanela e luvas', 'Tecidos: linho bege e veludo'],
            ['Caixinhas da Shimmer', 'Pisca-pisca', 'Papel kraft ou bege', 'Fita dourada', 'Taças de espumante', 'Enfeites de Natal discretos', 'Todas as peças limpas']]),
 dict(kind='list', dur=14, kick='CERCA DE 4 HORAS E 15 MINUTOS', title='Ordem do dia',
      steps=[('20 min', 'Chegada e montagem do cenário'), ('70 min', 'Still dos solitários (prioridade)'), ('60 min', 'Solitários na mão, caixinha e POV do pedido'),
             ('35 min', 'Bancada: solda e cravação'), ('20 min', 'Alianças sob medida'), ('30 min', 'Natal e Réveillon'), ('20 min', 'Loja e equipe')],
      tip='Comece pelo produto parado, enquanto a luz da janela está boa.'),
 dict(kind='end', dur=7),
]

def wrap(text, fnt, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if fnt.getlength(t) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=r, fill=255)
    im = im.convert('RGBA'); im.putalpha(m); return im

def fit(im):  # cover-fit a reference into the panel (reference preview only, not a post)
    iw, ih = im.size; z = max(PW / iw, PH / ih)
    im = im.resize((round(iw * z), round(ih * z)), Image.LANCZOS)
    return im.crop(((im.width - PW) // 2, (im.height - PH) // 2, (im.width - PW) // 2 + PW, (im.height - PH) // 2 + PH))

def card(word):
    c = Image.new('RGB', (PW, PH), (232, 225, 213)); d = ImageDraw.Draw(c)
    d.rectangle([22, 22, PW - 23, PH - 23], outline=(201, 180, 138), width=2)
    c = c.convert('RGBA')
    g = gold_text(word, script_font(96)); paste(c, g, PW / 2, PH / 2 - 80, anchor='center')
    for i, t in enumerate(['CENA NOVA', 'MONTAR O CENÁRIO NO DIA']):
        paste(c, solid_text(t, caps_font(19, 600), BR, 3), PW / 2, PH / 2 + 60 + i * 36, anchor='center')
    return c.convert('RGB')

def guide_layer():
    g = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    h = int(PH * 0.30)
    d.rectangle([0, 0, PW, h], fill=(255, 255, 255, 60))
    for x in range(0, PW, 18): d.line([(x, h), (x + 9, h)], fill=(255, 255, 255, 230), width=3)
    lab = solid_text('ESPAÇO PARA O TEXTO', sans(17, 700), (255, 255, 255), 2)
    f = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); paste(f, lab, PW / 2, h - 40, anchor='center')
    sh = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); sh.putalpha(f.split()[3].filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * .7)))
    g.alpha_composite(sh, (0, 2)); g.alpha_composite(f); return g
GUIDE = guide_layer()

def panel_frames(ref, n):
    kind = ref[0]
    if kind == 'img': f = fit(Image.open(ref[1]).convert('RGB')); return lambda i: f
    if kind == 'card': f = card(ref[1]); return lambda i: f
    if kind == 'seq':
        import glob
        fs = sorted(glob.glob(S + f'vclips/{ref[1]}_*.jpg')); cache = {}
        def g(i):
            k = i % len(fs)
            if k not in cache: cache[k] = fit(Image.open(fs[k]).convert('RGB'))
            return cache[k]
        return g
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(ref[2]), '-i', ref[1], '-t', str(n / FPS + 0.2), '-vf',
                          f'fps={FPS},scale={PW}:{PH}:force_original_aspect_ratio=increase,crop={PW}:{PH}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    frames = [Image.frombytes('RGB', (PW, PH), raw[i * PW * PH * 3:(i + 1) * PW * PH * 3]) for i in range(len(raw) // (PW * PH * 3))]
    return lambda i: frames[i % len(frames)] if i // len(frames) % 2 == 0 else frames[len(frames) - 1 - i % len(frames)]

SHADOW = None
def panel_shadow():
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([PX, PY + 8, PX + PW, PY + PH + 8], radius=26, fill=255)
    s = Image.new('RGBA', (W, H), (60, 45, 30, 0)); s.putalpha(m.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * .28))); return s

def text_layer(sd):
    L = Image.new('RGBA', (W, H), BGC + (255,))
    k = sd['kind']
    if k in ('cover', 'end'):
        lw = 760; lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
        L.alpha_composite(lg, ((W - lw) // 2, 250))
        if k == 'cover':
            paste(L, solid_text('ROTEIRO DE FOTOS E VÍDEOS', caps_font(30, 600), BR, 4), W / 2, 590, anchor='center')
            paste(L, gold_text('Ensaio Shimmer', script_font(150)), W / 2, 650, anchor='center')
            paste(L, solid_text('Novembro e dezembro · foco nos solitários', sans(28, 500), INK), W / 2, 880, anchor='center')
        else:
            paste(L, gold_text('Obrigada!', script_font(150)), W / 2, 600, anchor='center')
            paste(L, solid_text('Qualquer dúvida no dia, fale com a Eliz.', sans(30, 500), INK), W / 2, 820, anchor='center')
        return L, False
    x0 = 740 if 'ref' in sd else 160
    paste(L, solid_text(sd['kick'], caps_font(24, 600), BR, 3), x0, 105)
    paste(L, gold_text(sd['title'], script_font(118)), x0 - 6, 150)
    y = 300
    maxw = W - x0 - 130
    if sd.get('pieces'):
        f = sans(25, 600)
        for ln in wrap('Peças: ' + sd['pieces'], f, maxw):
            ImageDraw.Draw(L).text((x0, y - 4), ln, font=f, fill=INK); y += 34
        y += 18
    bf = sans(27, 500); d = ImageDraw.Draw(L)
    for lab, items in sd.get('secs', []):
        if lab:
            t = solid_text(lab, caps_font(21, 700), BR, 4); paste(L, t, x0, y); y += ink_size(t)[1] + 16
        for it in items:
            lines = wrap(it, bf, maxw - 34)
            d.polygon([(x0 + 6, y + 9), (x0 + 13, y + 17), (x0 + 6, y + 25), (x0 - 1, y + 17)], fill=(184, 150, 88))
            for ln in lines:
                d.text((x0 + 34, y), ln, font=bf, fill=INK); y += 38
            y += 8
        y += 16
    if 'cols' in sd:
        for c, col in enumerate(sd['cols']):
            yy = y
            for it in col:
                cx = x0 + c * 820
                d.polygon([(cx + 6, yy + 9), (cx + 13, yy + 17), (cx + 6, yy + 25), (cx - 1, yy + 17)], fill=(184, 150, 88))
                d.text((cx + 34, yy), it, font=sans(30, 500), fill=INK); yy += 62
    if 'steps' in sd:
        for i, (tm, tx) in enumerate(sd['steps']):
            yy = y + i * 82
            paste(L, gold_text(str(i + 1), caps_font(52, 600)), x0, yy)
            d.text((x0 + 70, yy + 4), tx, font=sans(31, 600), fill=INK)
            d.text((x0 + 70, yy + 44), tm, font=sans(22, 500), fill=(138, 122, 102))
        y += len(sd['steps']) * 82 + 10
    if sd.get('tip'):
        tf = sans(25, 600); lines = wrap('Dica: ' + sd['tip'], tf, maxw - 60)
        bh = 38 * len(lines) + 40; y = max(y, 0); top = min(y + 6, H - 80 - bh)
        d.rounded_rectangle([x0, top, x0 + maxw, top + bh], radius=18, fill=(251, 248, 242), outline=(201, 180, 138), width=2)
        for i, ln in enumerate(lines): d.text((x0 + 30, top + 20 + i * 38), ln, font=tf, fill=BR)
        y = top + bh
    if y > H - 60: print('OVERFLOW', sd.get('title'), y)
    if 'ref' in sd: L.alpha_composite(panel_shadow())
    return L, 'ref' in sd

pages = []
enc = None if PREV else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', OUT_MP4], stdin=subprocess.PIPE)
BGF = np.array(BGC, np.float32)
total = 0
for si, sd in enumerate(SL):
    if PREV and str(si) not in PREV.split(','): continue
    base, has = text_layer(sd); n = int(sd['dur'] * FPS); total += sd['dur']
    pf = panel_frames(sd['ref'], n) if has else None
    mask = Image.new('L', (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW - 1, PH - 1], radius=26, fill=255)
    def compose(i):
        im = base.copy()
        if pf:
            p = pf(i).convert('RGBA')
            if sd.get('guide'): p.alpha_composite(GUIDE)
            im.paste(p, (PX, PY), mask)
        return im.convert('RGB')
    rep = compose(int(n * 0.5)); pages.append(rep)
    if PREV: rep.save(f'rt_{si}.jpg', quality=88); continue
    for i in range(n):
        a = min(1, i / 12, (n - 1 - i) / 12)
        fr = np.asarray(compose(i), np.float32)
        if a < 1: fr = BGF + (fr - BGF) * a
        enc.stdin.write(fr.astype(np.uint8).tobytes())
if enc:
    enc.stdin.close(); enc.wait()
    pages[0].save(OUT_PDF, save_all=True, append_images=pages[1:], resolution=150)
print('total s', total)
