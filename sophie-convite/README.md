# O Mundo Encantado da Sophie 🦄✨

Convite digital interativo (React + Tailwind CSS + Framer Motion), mobile-first, para compartilhar no WhatsApp.

## Rodar no computador

```bash
cd sophie-convite
npm install
npm run dev        # http://localhost:5173
npm run build      # gera a pasta dist/ (o que vai para a Vercel)
npm run preview    # testa o build final
```

## O que tem no convite

1. **Abertura**: arte do título + unicórnio 3D (modelo Blender) que "aperta" o botão junto com o convidado, com glitter.
2. **Jogo "Ei, convidado!"**: a cabecinha da Sophie pula nos tijolinhos coloridos e pega 5 estrelinhas para desbloquear o convite (chão contínuo, pulo duplo e ajuda automática após 20 s — feito para crianças). Opção "Prefiro pular o jogo".
3. **Convite**: foto da Sophie com a fantasia + mensagem + **menu mágico** com os botões ilustrados.
4. **Galeria** (opcional) · 5. **Quando e onde** + contagem regressiva · 6. **Confirmação** (WhatsApp), localização, agenda e **lojas da lista de presentes**.
7. **Raspadinhas mágicas**: 5 missões para fazer com a aniversariante, raspadas com o dedo.
8. **Final** com unicórnio e arco-íris.

## Configurar (um único arquivo)

Tudo fica em **`src/config/event.js`**:

| O quê | Constante | Observação |
|---|---|---|
| Dados da festa | `EVENT` | Data em horário de Brasília (`-03:00`). O dia da semana é calculado sozinho. |
| WhatsApp para confirmação | `RSVP_PHONE` | Ex.: `'55 41 99999-9999'`. Vazio = botão "Confirmação em breve" (nunca um link quebrado). |
| Prazo de confirmação | `RSVP_DEADLINE` | Opcional. |
| Música | `MUSIC.src` | Coloque o MP3 em `public/audio/` e use `'/audio/arquivo.mp3'`. Use só música com direito de uso. Ela só toca depois de um toque do convidado. |
| Lista de presentes | `GIFT_LIST` | `enabled: true` + `url` https real. Desligada por padrão. |
| Lojas / lista de presentes | `GIFT_LIST.stores` | Links https (Instagram, site). |
| Arte do título | `TITLE_ART` | PNG/WebP transparente. |
| Fotos da criança e rostinho do jogo | `CHILD_IMAGES` | PNG/WebP sem fundo. |
| Patterns de fundo | `BACKGROUNDS` | Abertura, jogo e final. |
| Raspadinhas | `SCRATCH_CARDS` | Arte + texto da missão ({nome} = nome da criança). |
| Galeria de fotos | `PHOTOS` | Vazio = seção oculta. |
| Compartilhamento | `SHARE` | Título, descrição e imagem do card do WhatsApp. |

### Imagem de capa do WhatsApp (Open Graph)
- Já existe `public/og-cover.jpg` (1200×630, ~50 KB) gerada a partir do próprio unicórnio do convite.
- Para trocar: substitua o arquivo (mesmo tamanho, < 300 KB) ou mude `SHARE.ogImage`.
- Para regenerar depois de mudar textos: `npm i -D playwright && npx playwright install chromium && npm run og`.
- O WhatsApp exige URL absoluta: na Vercel isso é automático (usa o domínio de produção). Com domínio próprio, preencha `SHARE.siteUrl`.

## Publicar na Vercel

**Opção A — pelo GitHub (recomendado, atualiza sozinho a cada commit)**
1. Acesse vercel.com → **Add New… → Project** → importe o repositório `print`.
2. Em **Root Directory**, escolha **`sophie-convite`**.
3. Framework: **Vite** (detectado). Build: `npm run build`. Output: `dist`.
4. **Deploy**. Em ~1 min você recebe `https://<nome>.vercel.app`.
5. (Opcional) Em **Settings → Domains**, troque para algo como `sophie5anos.vercel.app`.

**Opção B — pela linha de comando**
```bash
npm i -g vercel
cd sophie-convite
vercel          # primeira vez: responde às perguntas (aceite os padrões)
vercel --prod   # publica em produção
```

**Depois de publicar**
- Teste o card: cole o link em uma conversa do WhatsApp consigo mesma. Se a imagem não aparecer, confira se `https://SEU-DOMINIO/og-cover.jpg` abre no navegador.
- O WhatsApp guarda o card em cache: se mudar a imagem, troque o nome do arquivo (ex.: `og-cover-v2.jpg`) e atualize `SHARE.ogImage`.

## Ferramentas (para reaproveitar o modelo com outros clientes)

| Comando | O que faz |
|---|---|
| `npm run model -- arquivo.glb` | Otimiza um modelo 3D do Blender (articulações cabeça/patas/rabo, sombreamento suave). |
| `npm run poster` | Renderiza o unicórnio 3D em imagem (fallback). |
| `npm run og` | Gera a capa do WhatsApp. |
| `python3 tools/preparar-raspadinhas.py prancha.png public/img/raspadinhas` | Separa os cartões, tira o fundo e apaga o texto (o site escreve o texto certo). |

Os scripts `npm run model/poster/og` precisam do Playwright: `npm i -D playwright && npx playwright install chromium`.
O script Python precisa de `pip install opencv-python-headless pillow numpy`.

## Estrutura

```
src/
  config/event.js       ← dados editáveis
  lib/event-utils.js    ← datas, contagem, links WhatsApp/Maps/Agenda
  lib/useMusic.js       ← áudio sob demanda (respeita autoplay)
  components/
    Opening.jsx         1 · Abertura (céu, arco-íris, partículas)
    StarGame.jsx        2 · Jogo "Encontre as 5 estrelinhas"
    Invitation.jsx      3 · Convite + unicórnio
    Details.jsx         4 · Data, horário, local + contagem regressiva
    Actions.jsx         5 · Confirmar, localização, agenda, música, presentes
    Finale.jsx          6 · Mensagem final
    Unicorn.jsx, Decor.jsx, Pattern.jsx, Particles.jsx, Icons.jsx
```

Acessibilidade: navegação por teclado, foco visível, `prefers-reduced-motion` respeitado, áreas de toque ≥ 44 px, contador do jogo anunciado por leitor de tela.
