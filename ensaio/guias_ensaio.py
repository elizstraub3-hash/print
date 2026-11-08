import html, sys, os, hashlib, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/')
from shimmer_style import gold_text, script_font
S = '/tmp/claude-0/-home-user-print/081c4020-c9a3-5394-8b04-d630e012eb6b/scratchpad/'
GD = S + 'calgold/'; os.makedirs(GD, exist_ok=True)
R = '/home/user/print/ensaio/refs/'
SITE = '/home/user/shimmer-joias-/images/'
LOGO = '/home/user/print/marca/logo-oficial.png'
OUT = '/home/user/print/ensaio/'
e = html.escape
def G(t, h):
    fn = GD + hashlib.md5(t.encode()).hexdigest() + '.png'
    if not os.path.exists(fn):
        lay, bb = gold_text(t, script_font(260)); lay.crop((bb[0]-4, bb[1]-4, bb[2]+12, bb[3]+14)).save(fn)
    return f'<img class="g" src="file://{fn}" style="height:{h}mm">'
CSS = f"""
@font-face {{ font-family: Cinzel; src: url('file://{S}fonts/Cinzel.ttf'); font-weight: 400 900; }}
@font-face {{ font-family: Montserrat; src: url('file://{S}fonts/Montserrat.ttf'); font-weight: 100 900; }}
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Montserrat; color: #4a3b2e; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.page {{ width: 210mm; height: 297mm; background: #f4efe7; position: relative; overflow: hidden; page-break-after: always; padding: 16mm 15mm 14mm; }}
.g {{ display: block; }}
.kick {{ font-family: Cinzel; font-size: 9.5pt; letter-spacing: .14em; color: #84652e; font-weight: 600; }}
.lead {{ font-size: 9.6pt; line-height: 1.55; color: #5b4b3b; margin-top: 3mm; }}
h3 {{ font-family: Cinzel; font-size: 11pt; color: #84652e; letter-spacing: .06em; margin: 6mm 0 2.5mm; font-weight: 700; }}
ul.ck {{ list-style: none; }}
ul.ck li {{ font-size: 9.6pt; line-height: 1.45; padding: 1.6mm 0 1.6mm 8mm; position: relative; border-bottom: 1px solid #e6dccd; }}
ul.ck li:before {{ content: ''; position: absolute; left: 0; top: 2.2mm; width: 3.6mm; height: 3.6mm; border: 1.4px solid #b8965a; border-radius: .8mm; background: #fbf8f3; }}
ul.dot li {{ font-size: 9.6pt; line-height: 1.5; margin: 0 0 1.8mm 5mm; }}
b {{ color: #4a3b2e; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }}
.pose {{ display: grid; grid-template-columns: 52mm 1fr; gap: 6mm; margin-top: 5mm; align-items: start; }}
.pose img.ref {{ width: 52mm; height: 66mm; object-fit: cover; border-radius: 3mm; border: 1px solid #d8c8a8; }}
.pose .t {{ font-family: Cinzel; font-size: 11pt; font-weight: 700; color: #84652e; }}
.pose .n {{ font-size: 7.5pt; letter-spacing: .12em; color: #9a8a76; font-weight: 700; margin-bottom: 1mm; }}
.pose p {{ font-size: 9.2pt; line-height: 1.5; margin-top: 1.5mm; }}
.note {{ font-size: 8.4pt; color: #84652e; background: #fbf8f3; border: 1px solid #d8c8a8; border-radius: 2.5mm; padding: 2.5mm 3.5mm; margin-top: 2.5mm; line-height: 1.45; }}
.warn {{ background: #4a3b2e; color: #f4efe7; border-radius: 3mm; padding: 4mm 5mm; margin-top: 5mm; font-size: 9.6pt; line-height: 1.5; }}
.warn b {{ color: #e6c98d; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 3mm; }}
th {{ font-size: 7pt; letter-spacing: .12em; text-transform: uppercase; color: #8a7a66; text-align: left; padding: 0 2mm 1.8mm; border-bottom: 1.5px solid #c9b48a; }}
td {{ font-size: 8.7pt; padding: 2mm; border-bottom: 1px solid #e6dccd; vertical-align: top; line-height: 1.4; }}
td.d {{ font-family: Cinzel; font-weight: 700; color: #84652e; white-space: nowrap; font-size: 9.5pt; }}
.refs {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; margin-top: 4mm; }}
.refs figure img {{ width: 100%; height: 62mm; object-fit: cover; border-radius: 3mm; border: 1px solid #d8c8a8; }}
.refs figcaption {{ font-size: 8pt; line-height: 1.4; margin-top: 1.5mm; color: #5b4b3b; }}
.foot {{ position: absolute; bottom: 7mm; left: 15mm; right: 15mm; display: flex; justify-content: space-between; font-size: 7pt; color: #9a8a76; letter-spacing: .1em; }}
.cover {{ display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }}
.cover .frame {{ position: absolute; inset: 9mm; border: 1.2px solid #c9b48a; }}
.cover .logo {{ width: 105mm; }}
.cover .sub {{ font-size: 10.5pt; color: #6b5a47; margin-top: 6mm; line-height: 1.6; }}
"""
def foot(doc, n): return f'<div class="foot"><span>SHIMMER JOIAS · {doc} · ENSAIO 09/11/2026</span><span>{n}</span></div>'
def ck(items): return '<ul class="ck">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
def dots(items): return '<ul class="dot">' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
def head(kick, title, h=14): return f'<div class="kick">{e(kick)}</div><div style="margin-top:1mm">{G(title, h)}</div>'
def cover(title, who, sub):
    return f"""<div class="page cover"><div class="frame"></div><img class="logo" src="file://{LOGO}">
<div class="kick" style="margin-top:16mm">{e(who)}</div><div style="margin-top:3mm">{G(title, 18)}</div>
<div class="sub">{sub}</div></div>"""
def render(name, pages):
    p = OUT + name + '.html'
    open(p, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
    subprocess.run(['node', S + 'pdfit_a4.js', p, OUT + name + '.pdf'], check=True)
    os.remove(p)

# ================= MODELO =================
M = 'GUIA DA MODELO'
mp = [cover('Guia da modelo de mão', 'ENSAIO SHIMMER · SEGUNDA, 09/11', 'Como se preparar, o que levar e as poses do ensaio<br>de solitários e alianças em ouro 18k.')]
mp.append(f"""<div class="page">{head('ANTES DO ENSAIO', 'Como chegar')}
<p class="lead">As suas mãos são a vitrine das joias. Quanto mais cuidadas e relaxadas, mais a peça aparece. Este é o checklist para chegar pronta.</p>
<h3>Mãos e unhas</h3>{ck([
'<b>Unhas feitas</b> no dia anterior, curtas ou médias, formato amendoado ou quadrado suave.',
'<b>Esmalte nude ou rosado claro</b>, cremoso e sem brilho metálico (como nas referências 2 e 3). Nada descascado.',
'Cutículas feitas e pele das mãos esfoliada na véspera.',
'<b>Hidratante 1 hora antes</b>, e não na hora: pele oleosa reflete luz e mancha as joias.',
'Sem anéis, relógio ou pulseiras próprias no dia (para não marcar a pele). Tire-os na noite anterior.',
'<b>Avise antes o número do seu aro</b> (anelar da mão esquerda) para separarmos as peças certas.'])}
<h3>Roupa (levar)</h3>{ck([
'<b>Camisa social clarinha</b>: off-white, bege ou areia, de tecido liso.',
'<b>Blusa ou blazer de manga clara</b> (como na referência 3), para as fotos da mão no ombro.',
'Um tricô ou suéter branco/creme, para as fotos de aconchego de Natal (referência 6).',
'Evite estampas, cores fortes e preto: a roupa aparece ao fundo e precisa deixar o ouro em destaque.'])}
<div class="warn"><b>Importante:</b> as joias são de ouro 18k e algumas são peças únicas. Troque de anel sempre sobre a mesa ou o tecido, nunca em pé ou perto do chão.</div>
{foot(M, 2)}</div>""")
POSES = [
 ('1', 'Mão apoiada', 'ref2.jpg', 'Dorso da mão para cima sobre a mesa ou o tecido. Dedos levemente separados e alongados, pulso solto. O anel no anelar, virado para a câmera.', 'Ideal para solitários e para o catálogo. Repita com a mão um pouco mais inclinada.'),
 ('2', 'Mão no ombro', 'ref3.jpg', 'Mão apoiada na gola ou no ombro do blazer clarinho, dedos juntos e relaxados, como num gesto natural. O rosto pode aparecer só até o queixo.', 'É a pose clássica da foto da princesa Diana: perfeita para o Anel Diana e o Céu da Noite.'),
 ('3', 'Folheando um livro', 'ref4.jpg', 'Uma mão segurando a página, a outra apoiada no livro aberto. Movimento lento de virar a página para o vídeo.', 'Mostra a joia no dia a dia: ela não é só para ocasiões especiais.'),
 ('4', 'Segurando o celular', 'ref5.jpg', 'Celular com capinha clara ou nude na mão, como se estivesse digitando. O anel de frente para a câmera.', 'Bom para Stories e para o Reels “mandei esse vídeo pra ele sem querer”.'),
 ('5', 'Aconchego de Natal', 'ref6.jpg', 'A mão saindo da manga do tricô branco, dedos curvados e relaxados, com a luz batendo na pedra.', 'Para os posts de presente de Natal. Fundo claro e quentinho.'),
 ('6', 'Braço estendido', 'ref7.jpg', 'Braço esticado na frente de uma parede clara e a outra mão tocando de leve o anel ou o pulso. Gesto elegante, sem pressa.', 'Bom para mostrar solitário e aliança juntos no mesmo dedo.'),
 ('7', 'Peças na ponta dos dedos', 'ref8.jpg', 'Segure o par de alianças pendurado no dedo ou entre o polegar e o indicador, com a palma para baixo e o fundo liso.', 'A melhor forma de mostrar o par de alianças sem precisar de duas pessoas.'),
]
for chunk, pg in ((POSES[:3], 3), (POSES[3:6], 4), (POSES[6:], 5)):
    body = ''
    for n, t, img, how, tip in chunk:
        body += f"""<div class="pose"><img class="ref" src="file://{R}{img}"><div><div class="n">POSE {n} · REFERÊNCIA</div><div class="t">{e(t)}</div><p>{e(how)}</p><div class="note">{e(tip)}</div></div></div>"""
    extra = ''
    if pg == 5:
        extra = f"""<h3>Poses que fazemos sem referência</h3>{dots([
'<b>Recebendo o anel:</b> a mão estendida e outra mão (de alguém da equipe) colocando o anel devagar no dedo.',
'<b>Segurando a caixinha aberta:</b> com as duas mãos, a pedra virada para a câmera.',
'<b>Giro lento:</b> a mão girando devagar, de dorso para lado, para a pedra pegar a luz. Conte até 5 em cada posição.',
'<b>Duas mãos entrelaçadas:</b> com outra pessoa, para as alianças (se houver alguém disponível).'])}
<div class="note" style="margin-top:4mm">As referências 1, 2 e 6 mostram anéis prateados: na Shimmer as peças são de ouro amarelo. Copie só a pose e o clima.</div>"""
    title = 'As poses' if pg == 3 else 'As poses (continuação)'
    mp.append(f'<div class="page">{head("NA HORA DO ENSAIO", title)}{body}{extra}{foot(M, pg)}</div>')
mp.append(f"""<div class="page">{head('NA HORA DO ENSAIO', 'Dicas de ouro')}
{dots([
'<b>Movimentos lentos.</b> No vídeo, tudo que é rápido fica tremido. Pense em câmera lenta.',
'<b>Mão relaxada.</b> Entre um take e outro, sacuda as mãos de leve. Mão tensa mostra veias e dedos duros.',
'<b>Veias aparentes?</b> Levante as mãos acima da cabeça por 30 segundos antes da foto.',
'<b>A pedra sempre para a luz.</b> Se a fotógrafa pedir, gire o anel até a pedra ficar centralizada.',
'<b>Dedos alongados,</b> mas sem esticar demais. Polegar escondido ou de lado deixa a mão mais delicada.',
'<b>Anel largo no dedo?</b> Avise na hora: usamos um ajustador de silicone invisível.',
'<b>Pausas de 5 segundos</b> em cada pose: dão tempo para foto e vídeo ao mesmo tempo.'])}
<h3>Checklist do dia</h3>{ck([
'Unhas feitas, esmalte nude ou rosado claro, sem descascar',
'Hidratante aplicado 1 hora antes (nada na hora)',
'Sem anéis, relógio ou pulseiras próprias',
'Camisa social clarinha',
'Blusa ou blazer de manga clara',
'Tricô ou suéter branco/creme',
'Aro do anelar informado à Eliz',
'Cabelo preso, para não entrar na foto'])}
{foot(M, 6)}</div>""")
render('guia-modelo-de-mao', mp)

# ================= FOTOGRAFA =================
F = 'GUIA DA FOTÓGRAFA E VIDEOMAKER'
fp = [cover('Guia de fotos e vídeos', 'FOTÓGRAFA · VIDEOMAKER · SOCIAL MEDIA', 'Programação do ensaio de segunda, 09/11, com tudo o que<br>precisamos para os posts até o fim de novembro.')]
fp.append(f"""<div class="page">{head('ANTES DE COMEÇAR', 'O objetivo')}
<p class="lead">Fotografar o catálogo da Shimmer e gravar todo o conteúdo de novembro (Black Friday e o começo do Natal) em um único dia.</p>
<h3>Prioridades</h3>{dots([
'<b>Solitários primeiro (cerca de 60% do tempo).</b> São o que mais vende: no Instagram, cada post de solitário leva em média 7 visitas ao perfil, contra menos de 1 das alianças.',
'<b>Alianças com foco no “sob medida”:</b> o par na mão, no espelho e na caixinha. Menos quantidade, mais cuidado.',
'<b>Catálogo padronizado:</b> todas as peças com o mesmo fundo, o mesmo ângulo e a mesma distância.'])}
<h3>Regras da marca</h3>{dots([
'<b>Nunca fundo de cidade, prédios ou rua.</b> Fundo neutro: parede clara, tecido, cetim ou a própria loja.',
'<b>Sem filtros e sem brilho aplicado.</b> O ouro precisa sair com a cor real.',
'<b>Não use o modo retrato</b> do celular: o desfoque artificial borra a borda do anel.',
'Vídeos na <b>vertical (9:16), 4K, 30 fps</b>. Deixe o <b>terço de cima livre</b> para o texto do post.',
'Planos de <b>10 a 15 segundos</b>, sem cortes, com a câmera firme (tripé ou apoio).'])}
<h3>Para você usar no dia</h3>{dots([
'<b>Roupa:</b> blazer em tom neutro e cabelo preso em coque. Fica confortável e, se a sua mão ou o seu reflexo aparecer, continua elegante.',
'Leve um lenço de microfibra para limpar as peças e a lente a cada troca.'])}
{foot(F, 2)}</div>""")
fp.append(f"""<div class="page">{head('ANTES DO ENSAIO', 'Checklist de preparação')}
<h3>Equipamento</h3>{ck([
'<b>Apagar e liberar a memória do celular</b> (o dia vai gerar muito material: deixe pelo menos 50 GB livres)',
'Bateria 100% + power bank + cabo',
'Tripé com suporte de celular',
'Lente macro (clip) para os detalhes das pedras',
'Rebatedor branco (ou uma cartolina branca)',
'Lenço de microfibra e luvas de algodão',
'Lente do celular limpa antes de começar'])}
<h3>Cenário (levar)</h3>{ck([
'<b>Flores brancas delicadas</b> (mosquitinho / gipsofila), como na referência 2',
'<b>Tecidos de cetim</b> champanhe, nude e off-white (cerca de 1 m cada), como na referência 1',
'Um livro de capa clara (referência 4)',
'Uma capinha de celular nude ou clara (referência 5)',
'Fundo liso claro: parede, cartolina grande ou papel de fundo bege',
'Bandeja ou tecido para apoiar as peças entre as trocas'])}
<h3>Luz</h3>{dots([
'<b>Luz natural de janela,</b> de lado. Evite sol direto: ele estoura o ouro e faz sombra dura.',
'Rebatedor do lado oposto à janela para abrir as sombras.',
'Se precisar de luz artificial, use <b>luz contínua branca suave</b> (ring light com difusor, sem flash).'])}
{foot(F, 3)}</div>""")
fp.append(f"""<div class="page">{head('REFERÊNCIAS', 'Cenário e composição')}
<p class="lead">As referências mostram o clima: tons nude e champanhe, luz suave, pouca coisa em volta. Algumas peças das referências são prateadas; na Shimmer, o ouro amarelo é a estrela.</p>
<div class="refs">
<figure><img src="file://{R}ref1.jpg"><figcaption><b>Still no cetim:</b> anel sozinho sobre o tecido em ondas. Catálogo e posts de produto.</figcaption></figure>
<figure><img src="file://{R}ref2.jpg"><figcaption><b>Mão + flores:</b> mosquitinho desfocado ao fundo, mão apoiada.</figcaption></figure>
<figure><img src="file://{R}ref3.jpg"><figcaption><b>Mão no ombro:</b> blazer claro, close no anel.</figcaption></figure>
<figure><img src="file://{R}ref4.jpg"><figcaption><b>Lifestyle:</b> livro aberto, luz lateral quente.</figcaption></figure>
<figure><img src="file://{R}ref7.jpg"><figcaption><b>Fundo liso:</b> braço estendido contra parede clara.</figcaption></figure>
<figure><img src="file://{R}ref8.jpg"><figcaption><b>Peças nos dedos:</b> para mostrar o par de alianças.</figcaption></figure>
</div>
<h3>O padrão atual da Shimmer</h3>
<div class="refs">
<figure><img src="file://{SITE}SH-1061.jpg"><figcaption><b>Serena</b> na caixinha: foco na pedra, fundo desfocado.</figcaption></figure>
<figure><img src="file://{SITE}SH-1084.jpg"><figcaption><b>Céu da Noite</b>: peça inteira em diagonal, fundo claro.</figcaption></figure>
<figure><img src="file://{SITE}SH-1014.jpg"><figcaption><b>Clássico</b>: o post campeão de visitas do perfil.</figcaption></figure>
</div>
{foot(F, 4)}</div>""")
PROG = [
 ('12/11', 'Carrossel', 'Por que esse nome? (Diana, Ariel, Céu da Noite)', 'Still de cada um no cetim + cada um na mão (pose 1)'),
 ('14/11', 'Reels', 'Bastidores', 'Making of do próprio ensaio: montando o cenário, a modelo, a câmera (vídeos de 5 s)'),
 ('17/11', 'Reels', 'Moissanite não é imitação (Jardim de Rosas, Serena)', 'Macro da pedra + giro lento na mão'),
 ('19/11', 'Foto', 'Céu da Noite', 'Still no cetim (vertical 4:5) + mão no ombro (pose 2)'),
 ('21/11', 'Reels', '3 truques para descobrir o aro dela', 'Mãos contornando um anel no papel, marcando o dedo com caneta'),
 ('24/11', 'Reels', 'Black Friday do Solitário Maria', 'POV da caixinha abrindo + Maria na mão (poses 1 e 6)'),
 ('26/11', 'Carrossel', 'As peças da Black Friday', 'Still de catálogo de todos os solitários, mesmo fundo e ângulo'),
 ('28/11', 'Reels', 'Último dia de Black Friday', 'Mão pegando a caixinha + close das pedras'),
 ('Diário', 'Stories', 'Bom dia, peça da semana, clientes', '15 a 20 vídeos curtos (5 a 10 s) de mãos e peças, com o terço de cima livre'),
 ('Extra', 'Reels', '“Até o ano acabar vou estar com esse brilho no dedo. SERÁ?”', 'Close da mão com solitário + aliança, movimento leve'),
]
rows = ''.join(f'<tr><td class="d">{d}</td><td>{e(fm)}</td><td><b>{e(c)}</b></td><td>{e(w)}</td></tr>' for d, fm, c, w in PROG)
fp.append(f"""<div class="page">{head('PROGRAMAÇÃO ATÉ 30/11', 'O que precisamos gravar')}
<p class="lead">Cada linha é um post do calendário de novembro. Riscar a linha quando o material estiver gravado garante que nada fica faltando.</p>
<table><tr><th>Post</th><th>Formato</th><th>Conteúdo</th><th>O que fotografar ou gravar</th></tr>{rows}</table>
<h3>Catálogo (todas as peças)</h3>{ck([
'Cada solitário: frente, 45°, lateral e macro da pedra, no mesmo fundo de cetim',
'Cada solitário na caixinha aberta',
'Cada solitário na mão (pose 1), com a mesma distância para todos',
'Alianças: o par no cetim, o par na mão (pose 7) e o par na caixinha'])}
{foot(F, 5)}</div>""")
fp.append(f"""<div class="page">{head('NO DIA', 'Ordem e técnica')}
<table><tr><th>Etapa</th><th>Tempo</th><th>O quê</th></tr>
<tr><td class="d">1</td><td>20 min</td><td>Montar o cenário: cetim, flores, fundo claro, luz da janela e rebatedor</td></tr>
<tr><td class="d">2</td><td>70 min</td><td><b>Still dos solitários</b> (catálogo), sem a modelo</td></tr>
<tr><td class="d">3</td><td>60 min</td><td><b>Solitários na mão</b>: poses 1 a 6, foto e vídeo</td></tr>
<tr><td class="d">4</td><td>30 min</td><td><b>Alianças</b>: still, pose 7 e caixinha</td></tr>
<tr><td class="d">5</td><td>30 min</td><td>Black Friday e Natal: caixinha, POV e tricô</td></tr>
<tr><td class="d">6</td><td>20 min</td><td>Bastidores, Stories curtos e o Reels “SERÁ?”</td></tr></table>
<h3>Técnica na hora</h3>{dots([
'<b>Foco:</b> toque na pedra na tela e trave o foco e a exposição (segure o dedo até aparecer AE/AF).',
'<b>Exposição um pouco para baixo</b> (arraste o sol para baixo): o ouro estoura com facilidade.',
'<b>Limpe a peça antes de cada take.</b> Digital no ouro aparece muito no macro.',
'<b>Grave e fotografe a mesma pose:</b> primeiro 10 s de vídeo parado, depois as fotos.',
'<b>Ângulo:</b> a câmera um pouco acima da mão, levemente inclinada; evite fotografar de baixo.',
'<b>Reflexo indesejado</b> na pedra (você ou o celular)? Mude o ângulo ou coloque o rebatedor como escudo.',
'Fotos em <b>resolução máxima</b> (e em RAW, se o celular permitir).'])}
{foot(F, 6)}</div>""")
fp.append(f"""<div class="page">{head('DEPOIS DO ENSAIO', 'Envio pelo Dropbox')}
<p class="lead">Para não perder qualidade, o material vai pelo Dropbox, <b>nunca pelo WhatsApp</b> (ele comprime fotos e vídeos).</p>
<h3>Como enviar</h3>{dots([
'A Eliz envia o <b>link de envio do Dropbox</b>. Pelo link, você sobe os arquivos sem precisar de conta.',
'Envie os <b>arquivos originais</b>, direto da galeria ou do cabo, sem editar e sem filtro.',
'No iPhone, ative <b>Ajustes → Fotos → Transferir para Mac ou PC → Manter Originais</b>.',
'Prazo: <b>até 24 horas depois do ensaio</b>, para os posts da semana.'])}
<h3>Organização das pastas</h3>
<table><tr><th>Pasta</th><th>O que vai dentro</th></tr>
<tr><td class="d">01-catalogo</td><td>Still de cada peça (uma subpasta por peça: maria, serena, ariel...)</td></tr>
<tr><td class="d">02-maos</td><td>Fotos e vídeos com a modelo</td></tr>
<tr><td class="d">03-aliancas</td><td>Todo o material das alianças</td></tr>
<tr><td class="d">04-black-friday-natal</td><td>Caixinha, POV, tricô</td></tr>
<tr><td class="d">05-bastidores-stories</td><td>Making of e vídeos curtos</td></tr></table>
<h3>Checklist final</h3>{ck([
'Todas as linhas da programação riscadas',
'Catálogo completo: todas as peças no mesmo padrão',
'Nenhuma foto com fundo de cidade',
'Material enviado no Dropbox, em pastas, em até 24 h',
'Peças conferidas e devolvidas à loja'])}
{foot(F, 7)}</div>""")
render('guia-fotografa-videomaker', fp)
print('ok')
