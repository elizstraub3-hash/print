import sys, os, math
SCR = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
src = open(SCR + 'stories_destaques.py').read()
src = src[:src.index('os.makedirs(OUT')]
OUTDIR = sys.argv[1]
sys.argv = [sys.argv[0], OUTDIR]
exec(src)
os.makedirs(OUT, exist_ok=True)

def body(img, k, rows, y, size=32, gap=54, dark=None):
    return center_lines(img, k, rows, y, size, gap, dark=dark)

# 0. abertura
img, k = beige()
b = header(img, k, 'POR QUE', 'esse nome?', 560, dark=True)
gold_rule(img, 540, b + 70, 90, k)
body(img, k, ['CADA JOIA DA SHIMMER TEM UM NOME,', 'E CADA NOME CONTA UMA HISTÓRIA.'], b + 140, 34, 60, dark=True)
logo(img, k, 1680)
save(img, '0-nomes-abertura')

# (file, name, header top, rows, body gap after header, dark override)
PIECES = [
 (S + 'diana_frame.png', 'Diana', 120,
  ['INSPIRADO NO ANEL DE NOIVADO', 'DA PRINCESA DIANA: UMA SAFIRA OVAL', 'RODEADA DE PEDRAS. A REFERÊNCIA MAIS', 'FAMOSA DESSE MODELO NO MUNDO.'], None),
 (IMG + '18.webp', 'Ariel', 260,
  ['UM NOME QUE FALA DE FORÇA, CORAGEM', 'E PROTEÇÃO. COMO O AMOR QUE ESCOLHE', 'FICAR, TODOS OS DIAS.'], True),
 (SITE + 'SH-1084.jpg', 'Céu da Noite', 200,
  ['A SAFIRA AZUL PROFUNDA É O CÉU', 'À NOITE, E AS PEDRAS AO LADO', 'SÃO AS ESTRELAS.'], None),
 (SITE + 'SH-1085.jpg', 'Jardim de Rosas', 200,
  ['A PEDRA ROSA EM GOTA É A ROSA,', 'E AS MOISSANITES AO REDOR,', 'O JARDIM QUE FLORESCE EM VOLTA.'], None),
 (SITE + 'SH-1086.jpg', 'Amélia', 170,
  ['UM NOME CLÁSSICO E DELICADO,', 'CHEIO DE PERSONALIDADE, COMO', 'A AMETISTA QUE ELA CARREGA.'], None),
 (SITE + 'SH-1061.jpg', 'Serena', 'compact',
  ['DO LATIM: CALMA E LUMINOSA.', 'UM SOLITÁRIO PARA UM AMOR EM PAZ.'], True),
 (S + 'img7030.png', 'Maria', 260,
  ['O NOME MAIS PRESENTE NAS FAMÍLIAS', 'BRASILEIRAS. SIMPLES, DELICADO', 'E ETERNO, COMO O PRIMEIRO “SIM”.'], None),
]
ONLY = os.environ.get('ONLY')
for i, (f, name, top, rows, dk) in enumerate(PIECES, 1):
    if ONLY and name != ONLY: continue
    img, k = photo_canvas(f)
    if name == 'Diana':   # soft shade only behind the text block, the building is too light for white text
        W_, H_ = img.size
        yy = np.arange(H_, dtype=np.float32)[:, None]
        a = np.clip(1 - yy / (H_ * 0.36), 0, 1) ** 1.3 * 0.55
        sh = Image.new('RGBA', (W_, H_), (20, 16, 12, 0))
        sh.putalpha(Image.fromarray((np.broadcast_to(a, (H_, W_)) * 255).astype(np.uint8)))
        img.alpha_composite(sh)
    if top == 'compact':  # smaller block that fits above the ring head, on a light fade (approved degradê idea)
        W_, H_ = img.size
        yy = np.arange(H_, dtype=np.float32)[:, None]
        a = np.clip(1 - yy / (H_ * 0.215), 0, 1) ** 0.9 * 0.88
        sh = Image.new('RGBA', (W_, H_), (250, 248, 244, 0))
        sh.putalpha(Image.fromarray((np.broadcast_to(a, (H_, W_)) * 255).astype(np.uint8)))
        img.alpha_composite(sh)
        kk = k * 0.8
        b = header(img, kk, 'POR QUE SE CHAMA', name, 60 / 0.8, dark=dk)
        body(img, kk, rows, b / kk + 40, 30, 52, dark=dk)
    else:
        b = header(img, k, 'POR QUE SE CHAMA', name, top, dark=dk)
        body(img, k, rows, b / k + 45, 30, 52, dark=dk)
    fn = name.lower().replace(' ', '-').replace('é', 'e')
    save(img, f'{i}-{fn}')
print('ok')
