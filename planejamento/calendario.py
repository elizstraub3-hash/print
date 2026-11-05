import html, sys, os, hashlib
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/')
from shimmer_style import gold_text, script_font
GD = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/calgold/'
os.makedirs(GD, exist_ok=True)
def G(text, h_mm, extra=''):
    '''Gold script heading rendered with the brand texture (PowerClip), embedded as an image.'''
    fn = GD + hashlib.md5(text.encode()).hexdigest() + '.png'
    lay, bb = gold_text(text, script_font(260))
    lay.crop((bb[0] - 4, bb[1] - 4, bb[2] + 12, bb[3] + 14)).save(fn)
    return f'<img class="gimg" src="file://{fn}" style="height:{h_mm}mm;{extra}">'
S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
TEX = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/images/12.webp'
LOGO = '/home/user/print/marca/logo-oficial.png'
e = html.escape

# formato: R = Reels, C = Carrossel, F = Foto feed, S = Story/especial
MONTHS = [
 ('Novembro', '2026', 'Esquenta de fim de ano e Black Friday',
  'Apresentar as peças com nome e história, gerar desejo e preparar o público para a Black Friday.',
  ['27/11 · Black Friday'], ['Diana', 'Maria', 'Céu da Noite'],
  [
   ('10/11', 'Ter', 'R', 'Anel Diana', '“A princesa Diana da Inglaterra tinha um assim. Ela também merece. Então capricha ✨”', True),
   ('12/11', 'Qui', 'C', 'Diana · Ariel · Céu da Noite', 'Por que esse nome? A história por trás de cada joia', False),
   ('14/11', 'Sáb', 'R', 'Produção', 'Bastidores: “Sua joia nasce aqui”, feita à mão na bancada', True),
   ('17/11', 'Ter', 'R', 'Jardim de Rosas', '“Moissanite não é imitação de diamante”', False),
   ('19/11', 'Qui', 'F', 'Céu da Noite', 'Post de produto no padrão do feed: safira central, ouro 18k', False),
   ('21/11', 'Sáb', 'R', 'Solitários', '“3 truques de ourives para descobrir o aro dela em segredo”', False),
   ('24/11', 'Ter', 'R', 'Solitário Maria', 'Black Friday: o anel do “sim” em condição especial', True),
   ('26/11', 'Qui', 'C', 'Peças selecionadas', 'Black Friday: as peças da campanha e as condições', False),
   ('28/11', 'Sáb', 'R', 'Solitário Maria', 'Último dia de Black Friday', False),
  ]),
 ('Dezembro', '2026', 'Natal e Réveillon: presente e pedido de casamento',
  'Época de mais pedidos de casamento e presentes do ano. Foco em urgência (prazo de encomenda) e em peças a pronta entrega.',
  ['25/12 · Natal', '31/12 · Réveillon'], ['Serena', 'Maria', 'Céu da Noite', 'Alianças'],
  [
   ('01/12', 'Ter', 'R', 'Serena', '“Ela pediu um anel simples. Ele não ouviu.” Pedido de casamento no Natal', False),
   ('03/12', 'Qui', 'C', 'Maria · Amélia · Céu da Noite · Ariel · Jardim de Rosas', 'Guia de presentes de Natal por faixa de preço', False),
   ('05/12', 'Sáb', 'R', 'Produção', 'Encomendas de Natal: até quando dá para pedir', False),
   ('08/12', 'Ter', 'R', 'Anel Diana', 'POV: você abriu a caixinha e era exatamente o que sonhou', True),
   ('10/12', 'Qui', 'F', 'Jardim de Rosas', 'Presente para ela: pedra rosa em gota e moissanites', False),
   ('12/12', 'Sáb', 'R', 'Encomendas', 'Último dia para encomendar para o Natal', False),
   ('15/12', 'Ter', 'R', 'Solitário Maria', 'Pronta entrega: ainda dá tempo de pedir no Natal', False),
   ('17/12', 'Qui', 'C', 'Peças a pronta entrega', 'Ainda dá tempo: o que sai hoje da loja', False),
   ('19/12', 'Sáb', 'R', 'Par de Alianças Tradicional', 'Natal a dois: alianças em ouro 18k', False),
   ('22/12', 'Ter', 'R', 'Solitário Maria', 'Retire na loja em Curitiba: presente de última hora', False),
   ('24/12', 'Qui', 'S', 'Institucional', 'Feliz Natal da família Shimmer', False),
   ('26/12', 'Sáb', 'R', 'Céu da Noite', 'Comece o ano com o céu da noite no dedo dela', False),
   ('29/12', 'Ter', 'R', 'Céu da Noite', 'Réveillon: o pedido à meia-noite', False),
   ('31/12', 'Qui', 'S', 'Institucional', 'Feliz Ano Novo', False),
  ]),
 ('Janeiro', '2027', 'Formaturas e noivos de fim de ano',
  'Temporada de colações de grau. Mostrar a pedra de cada curso e acolher quem ficou noivo no Natal e no Réveillon.',
  ['Colações de grau', 'Recém-noivos'], ['Ariel', 'Diana', 'Céu da Noite', 'Alianças'],
  [
   ('02/01', 'Sáb', 'R', 'Clientes', '“Disseram sim”: os pedidos de fim de ano dos nossos clientes', False),
   ('05/01', 'Ter', 'R', 'Ariel · Diana', 'Qual é a pedra do seu curso? Esmeralda é Medicina, safira é Engenharia', False),
   ('07/01', 'Qui', 'C', 'Anéis de formatura', 'Anel de formatura: a pedra de cada curso', False),
   ('09/01', 'Sáb', 'R', 'Clientes', 'Depoimento de quem ficou noiva com um anel Shimmer', False),
   ('12/01', 'Ter', 'R', 'Anel Diana', '“Anos de estudo merecem uma joia que dure a vida toda”', False),
   ('14/01', 'Qui', 'F', 'Solitário Ariel', 'Esmeralda natural: o anel para a formanda de Medicina', False),
   ('16/01', 'Sáb', 'R', 'Produção', 'Da bancada para a colação de grau', False),
   ('19/01', 'Ter', 'R', 'Par de Alianças Tradicional', 'Ficou noiva no Natal? Agora são as alianças', False),
   ('21/01', 'Qui', 'C', 'Alianças', 'Como escolher a largura e o peso das alianças', False),
   ('23/01', 'Sáb', 'R', 'Alianças', 'Reels de humor no formato “É a meta”', False),
   ('26/01', 'Ter', 'R', 'Céu da Noite', 'O presente dos pais para a filha que se formou', False),
   ('28/01', 'Qui', 'C', 'Todas as peças', 'Garantia vitalícia: o que ela cobre', False),
   ('30/01', 'Sáb', 'R', 'Clientes', 'Antes e depois: do pedido do cliente à joia pronta', False),
  ]),
 ('Fevereiro', '2027', 'Carnaval com cor e Dia de São Valentim',
  'Mês mais leve: joias com cor e humor no Carnaval, e o Dia de São Valentim (14/02) como gancho para pedidos.',
  ['06 a 10/02 · Carnaval', '14/02 · São Valentim'], ['Jardim de Rosas', 'Amélia', 'Serena'],
  [
   ('02/02', 'Ter', 'R', 'Jardim de Rosas', 'Uma pedra rosa para brilhar no Carnaval', False),
   ('04/02', 'Qui', 'C', 'Jardim de Rosas · Amélia · Ariel · Céu da Noite', 'Joias com cor: qual combina com você?', False),
   ('06/02', 'Sáb', 'R', 'Humor', '“O Carnaval passa. O ouro 18k fica.”', False),
   ('09/02', 'Ter', 'S', 'Stories', 'Carnaval: só Stories leves, com enquete e caixinha de perguntas', False),
   ('11/02', 'Qui', 'R', 'Solitários', 'Passou o Carnaval: hora de planejar o pedido', False),
   ('13/02', 'Sáb', 'R', 'Serena', 'Dia de São Valentim: o dia dos namorados do mundo todo', False),
   ('16/02', 'Ter', 'R', 'Amélia', 'Ametista e haste cravejada: a delicadeza do Amélia', False),
   ('18/02', 'Qui', 'F', 'Serena', 'Post de produto no padrão do feed', False),
   ('20/02', 'Sáb', 'R', 'Moissanite', '“Moissanite ou diamante? Você não vai acertar”', True),
   ('23/02', 'Ter', 'R', 'Alianças', 'Vai casar em 2027? Comece pelas alianças', False),
   ('25/02', 'Qui', 'C', 'Alianças', 'Checklist dos noivos: o que resolver até 6 meses antes', False),
   ('27/02', 'Sáb', 'R', 'Produção', 'Bastidores: alianças sendo feitas à mão', False),
  ]),
 ('Março', '2027', 'Mês da Mulher, Noivas e Páscoa',
  'Dia da Mulher (08/03) com a mulher presenteando a si mesma, campanha de noivas e a Páscoa (28/03) como data de presente.',
  ['08/03 · Dia da Mulher', '15/03 · Dia do Consumidor', '28/03 · Páscoa'], ['Jardim de Rosas', 'Amélia', 'Alianças', 'Serena'],
  [
   ('02/03', 'Ter', 'R', 'Amélia', '“Ela não precisa esperar ganhar.” Uma joia para você mesma', False),
   ('04/03', 'Qui', 'C', 'Jardim de Rosas · Amélia · Maria', 'Presentes para o Dia da Mulher', False),
   ('06/03', 'Sáb', 'R', 'Jardim de Rosas', 'Dia da Mulher: uma rosa que não murcha', False),
   ('09/03', 'Ter', 'R', 'Par de Alianças Tradicional', 'Abertura do mês das noivas Shimmer', False),
   ('11/03', 'Qui', 'C', 'Alianças · Serena', 'Noivas Shimmer: solitário e alianças', False),
   ('13/03', 'Sáb', 'R', 'Peças selecionadas', 'Dia do Consumidor (15/03): condição especial', False),
   ('16/03', 'Ter', 'R', 'Serena', 'O pedido de casamento perfeito começa no anel', False),
   ('18/03', 'Qui', 'F', 'Anel Diana', 'Post de produto no padrão do feed', False),
   ('20/03', 'Sáb', 'R', 'Clientes', '“Disseram sim”: depoimento de uma noiva', False),
   ('23/03', 'Ter', 'R', 'Solitário Maria', 'Páscoa: um ovo com surpresa dentro', False),
   ('25/03', 'Qui', 'C', 'Maria · Amélia · Céu da Noite', 'Ideias de presente de Páscoa', False),
   ('27/03', 'Sáb', 'R', 'Alianças', 'Bastidores das alianças das noivas de março', False),
   ('30/03', 'Ter', 'R', 'Clientes', 'Encerramento do mês das noivas: os “sins” de março', False),
  ]),
]

PIECES = [
 ('Solitário Maria', 'Moissanite 2 mm · 0,80 g · pronta entrega', 'Black Friday, Natal de última hora, Páscoa', 'Entrada: o primeiro anel do “sim”'),
 ('Anel Diana', 'Safira oval 6x8 · 17 moissanites · sob encomenda', 'Lançamento, formatura (Engenharia), noivado', 'Peça de história: inspirada na princesa Diana'),
 ('Solitário Ariel', 'Esmeralda natural · 1 g', 'Formatura (Medicina), presente de Natal', 'Força, coragem e proteção'),
 ('Céu da Noite', 'Safira central 5x7 mm', 'Réveillon, formatura, presente dos pais', 'O céu à noite no dedo dela'),
 ('Jardim de Rosas', 'Pedra rosa em gota · moissanites', 'Carnaval, Dia da Mulher, Natal', 'A joia com cor e romantismo'),
 ('Amélia', 'Ametista · haste cravejada', 'Carnaval, Dia da Mulher, Páscoa', 'Delicadeza com personalidade'),
 ('Serena', 'Solitário de pedra central 5 mm', 'Pedido no Natal, São Valentim, noivas', 'O solitário clássico do pedido'),
 ('Alianças Tradicional', 'Par · 5 g · 2,5 mm de largura', 'Natal a dois, recém-noivos, noivas', 'O passo depois do “sim”'),
]

STORIES = [
 ('Segunda', 'Bom dia + bastidor da bancada'),
 ('Terça', 'Compartilhar o Reels do dia + enquete'),
 ('Quarta', 'Caixinha de perguntas: dúvidas sobre aro, ouro e pedras'),
 ('Quinta', 'Peça da semana com preço e condições'),
 ('Sexta', 'Cliente feliz: repost de quem recebeu a joia'),
 ('Sábado', 'Compartilhar o Reels + link do WhatsApp'),
]

NEEDS = [
 'Prazo de produção das peças sob encomenda, para definir o último dia de pedidos de Natal.',
 'Peças e condições da Black Friday (27/11) e do Dia do Consumidor (15/03).',
 'Preço do Anel Diana e confirmação do preço do Serena.',
 'Vídeos e fotos de clientes (pedidos, formaturas, noivas), com autorização para publicar.',
 'Vídeos curtos da bancada sempre que possível: são o conteúdo que mais gera confiança.',
]

LAB = {'R': ('Reels', 'r'), 'C': ('Carrossel', 'c'), 'F': ('Foto', 'f'), 'S': ('Especial', 's')}

css = f"""
@font-face {{ font-family: Cinzel; src: url('file://{S}fonts/Cinzel.ttf'); font-weight: 400 900; }}
@font-face {{ font-family: Parisienne; src: url('file://{S}fonts/Parisienne.ttf'); }}
@font-face {{ font-family: Montserrat; src: url('file://{S}fonts/Montserrat.ttf'); font-weight: 100 900; }}
@page {{ size: A4 landscape; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Montserrat; color: #4a3b2e; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 297mm; height: 210mm; background: #f4efe7; position: relative; overflow: hidden; page-break-after: always; padding: 15mm 17mm 13mm; }}
.gold {{ background: url('file://{TEX}') center/100% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.script {{ font-family: Parisienne; font-weight: 400; line-height: 1.05; }}
.caps {{ font-family: Cinzel; letter-spacing: .06em; text-transform: uppercase; }}
.gimg {{ display: block; }}
.rule {{ height: 2px; width: 70px; background: url('file://{TEX}') center/cover; margin: 5mm 0; }}
.foot {{ position: absolute; bottom: 7mm; left: 17mm; right: 17mm; display: flex; justify-content: space-between; font-size: 7.5pt; color: #9a8a76; letter-spacing: .08em; }}
.foot img {{ height: 7mm; opacity: .9; }}
/* cover */
.cover {{ display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }}
.cover .logo {{ width: 120mm; }}
.cover .kicker {{ font-size: 13pt; margin-top: 16mm; color: #6b5a47; }}
.cover h1 {{ font-size: 64pt; margin-top: 2mm; }}
.cover .period {{ font-size: 12pt; color: #6b5a47; letter-spacing: .18em; margin-top: 4mm; }}
.cover .frame {{ position: absolute; inset: 9mm; border: 1.2px solid #c9b48a; }}
/* headers */
.h {{ display: flex; align-items: flex-end; gap: 8mm; }}
.h .kick {{ font-size: 11pt; color: #6b5a47; }}
.h h2 {{ font-size: 40pt; }}
.lead {{ font-size: 9.5pt; line-height: 1.5; color: #5b4b3b; max-width: 200mm; }}
/* overview */
.months {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 4mm; margin-top: 6mm; }}
.mcard {{ background: #fbf8f3; border: 1px solid #e3d8c6; border-radius: 3mm; padding: 5mm 4mm; }}
.mcard .mn {{ font-size: 24pt; }}
.mcard .yr {{ font-size: 7pt; color: #9a8a76; letter-spacing: .2em; }}
.mcard .th {{ font-family: Cinzel; font-size: 8.5pt; font-weight: 600; margin: 3mm 0 2mm; color: #84652e; line-height: 1.35; }}
.mcard .lbl {{ font-size: 6.5pt; font-weight: 700; letter-spacing: .12em; color: #8a7a66; margin-top: 3mm; }}
.mcard .val {{ font-size: 8pt; line-height: 1.45; margin-top: 1mm; }}
.rhythm {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin-top: 6mm; }}
.rb {{ border-top: 2px solid #c9b48a; padding-top: 3mm; }}
.rb b {{ font-family: Cinzel; font-size: 10pt; color: #84652e; display: block; }}
.rb span {{ font-size: 8.5pt; line-height: 1.45; }}
/* tables */
table {{ width: 100%; border-collapse: collapse; margin-top: 5mm; }}
th {{ font-size: 7pt; letter-spacing: .14em; text-transform: uppercase; color: #8a7a66; text-align: left; font-weight: 700; padding: 0 3mm 2mm; border-bottom: 1.5px solid #c9b48a; }}
td {{ font-size: 8.6pt; padding: var(--pad, 2.1mm) 3mm; border-bottom: 1px solid #e6dccd; vertical-align: middle; line-height: 1.35; }}
tr:nth-child(even) td {{ background: rgba(255,255,255,.45); }}
.d {{ font-family: Cinzel; font-weight: 700; font-size: 10pt; color: #84652e; white-space: nowrap; }}
.wd {{ font-size: 7.5pt; color: #8a7a66; }}
.chip {{ display: inline-block; font-size: 6.8pt; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: 1mm 2.2mm; border-radius: 10mm; white-space: nowrap; }}
.chip.r {{ background: #84652e; color: #fff; }}
.chip.c {{ background: #e9dcc3; color: #6b5226; }}
.chip.f {{ background: #fff; color: #84652e; border: 1px solid #c9b48a; }}
.chip.s {{ background: #4a3b2e; color: #f4efe7; }}
.pc {{ font-weight: 600; color: #4a3b2e; }}
.ok {{ font-size: 6.8pt; font-weight: 700; color: #3f7a4a; letter-spacing: .06em; white-space: nowrap; }}
.mhead {{ display: flex; justify-content: space-between; align-items: flex-end; }}
.tags {{ display: flex; gap: 2mm; flex-wrap: wrap; justify-content: flex-end; max-width: 120mm; }}
.tag {{ font-size: 7.5pt; font-weight: 600; padding: 1.2mm 3mm; border: 1px solid #c9b48a; border-radius: 10mm; color: #6b5226; background: #fbf8f3; }}
.star {{ font-size: 8pt; margin-top: 2mm; color: #5b4b3b; }}
.star b {{ color: #84652e; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12mm; margin-top: 4mm; }}
.list li {{ font-size: 9pt; line-height: 1.5; margin: 0 0 2.5mm 4mm; }}
.sub {{ font-family: Cinzel; font-size: 12pt; color: #84652e; font-weight: 600; margin-top: 4mm; }}
"""

def foot(n):
    return f'<div class="foot"><span>SHIMMER JOIAS · PLANEJAMENTO DE CONTEÚDO · NOV/2026 A MAR/2027</span><span>{n}</span></div>'

pages = []
pages.append(f"""<div class="page cover"><div class="frame"></div>
<img class="logo" src="file://{LOGO}">
<div class="kicker caps">Planejamento de conteúdo</div>
<div style="margin:3mm auto 0">{G("Calendário editorial", 26)}</div>
<div class="period caps">Novembro 2026 · Março 2027</div></div>""")

cards = ''
for mn, yr, th, obj, dates, stars, rows in MONTHS:
    cards += f"""<div class="mcard"><div class="mn">{G(mn, 9.5)}</div><div class="yr">{yr}</div>
<div class="th">{e(th)}</div>
<div class="lbl">DATAS-CHAVE</div><div class="val">{'<br>'.join(e(x) for x in dates)}</div>
<div class="lbl">PEÇAS EM DESTAQUE</div><div class="val">{', '.join(e(x) for x in stars)}</div></div>"""
pages.append(f"""<div class="page"><div class="h"><div><div class="kick caps">Visão geral</div>{G("Os próximos cinco meses", 15)}</div></div>
<p class="lead">Cada mês tem um tema ligado às datas que mais vendem joias. As peças foram escolhidas pela pedra, pelo preço e pela história de cada uma, para que cada conteúdo fale com o momento certo.</p>
<div class="months">{cards}</div>
<div class="sub">Ritmo semanal</div>
<div class="rhythm">
<div class="rb"><b>Terça · 18h</b><span>Reels principal da semana: o conteúdo com mais alcance</span></div>
<div class="rb"><b>Quinta</b><span>Carrossel ou foto de produto: o conteúdo que gera salvamentos e vendas</span></div>
<div class="rb"><b>Sábado</b><span>Reels de bastidores, humor ou clientes</span></div>
<div class="rb"><b>Todos os dias</b><span>Stories com enquete, perguntas e o link do WhatsApp</span></div>
</div>{foot(2)}</div>""")

prow = ''.join(f'<tr><td class="pc">{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in PIECES)
pages.append(f"""<div class="page"><div class="h"><div><div class="kick caps">Seleção de peças</div>{G("Cada anel no seu momento", 15)}</div></div>
<p class="lead">Cada peça tem as datas em que ela vende mais. Assim, o público vê variedade ao longo dos meses, e cada anel aparece quando faz mais sentido.</p>
<table><tr><th>Peça</th><th>Detalhes</th><th>Melhores momentos</th><th>Mensagem principal</th></tr>{prow}</table>{foot(3)}</div>""")

n = 4
for mn, yr, th, obj, dates, stars, rows in MONTHS:
    trs = ''
    for d, wd, f, pc, txt, ok in rows:
        lab, cls = LAB[f]
        trs += (f'<tr><td><span class="d">{d}</span> <span class="wd">{wd}</span></td><td><span class="chip {cls}">{lab}</span></td>'
                f'<td class="pc">{e(pc)}</td><td>{e(txt)}</td><td>{"<span class=ok>✓ PRONTO</span>" if ok else ""}</td></tr>')
    pad = '1.45mm' if len(rows) > 12 else '2.1mm'
    tags = ''.join(f'<span class="tag">{e(x)}</span>' for x in dates)
    pages.append(f"""<div class="page"><div class="mhead"><div><div class="kick caps">{yr} · {e(th)}</div><div style="margin-top:1mm">{G(mn, 16)}</div></div><div class="tags">{tags}</div></div>
<p class="lead" style="margin-top:2mm">{e(obj)}</p>
<table style="--pad:{pad}"><tr><th style="width:24mm">Data</th><th style="width:24mm">Formato</th><th style="width:62mm">Peça</th><th>Conteúdo</th><th style="width:20mm"></th></tr>{trs}</table>{foot(n)}</div>""")
    n += 1

st = ''.join(f'<li><b>{a}:</b> {e(b)}</li>' for a, b in STORIES)
nd = ''.join(f'<li>{e(x)}</li>' for x in NEEDS)
pages.append(f"""<div class="page"><div class="h"><div><div class="kick caps">Para fechar</div>{G("Stories e próximos passos", 15)}</div></div>
<div class="two"><div><div class="sub">Roteiro fixo dos Stories</div><ul class="list" style="margin-top:4mm">{st}</ul>
<p class="lead" style="margin-top:4mm">Nas datas comemorativas, os Stories seguem o tema do mês, sempre com enquete ou caixinha de perguntas para abrir conversa.</p></div>
<div><div class="sub">O que precisamos da Shimmer</div><ul class="list" style="margin-top:4mm">{nd}</ul>
<p class="lead" style="margin-top:4mm">O calendário pode mudar conforme os resultados: o que der mais alcance e mais conversas no WhatsApp ganha mais espaço nas semanas seguintes.</p></div></div>
{foot(n)}</div>""")

open(S + 'calendario.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(pages)}</body></html>')
print('pages', len(pages))
