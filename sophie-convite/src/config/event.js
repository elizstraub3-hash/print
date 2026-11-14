/**
 * ─────────────────────────────────────────────────────────────
 *  CONFIGURAÇÃO DO CONVITE — edite SOMENTE este arquivo.
 * ─────────────────────────────────────────────────────────────
 *  Este arquivo é JavaScript puro (sem imports) porque também é
 *  lido pelo vite.config.js para gerar as metatags Open Graph.
 */

/** Dados do evento */
export const EVENT = {
  projectTitle: 'O Mundo Encantado da Sophie',
  childFullName: 'Sophie Polli dos Santos',
  childFirstName: 'Sophie',
  age: 5,

  // Data/hora no horário de Brasília (UTC-03:00 — o Brasil não usa
  // horário de verão desde 2019). Mantenha o sufixo -03:00.
  startsAt: '2026-12-13T11:30:00-03:00',
  // Duração estimada (usada no "Adicionar à agenda" e para saber
  // quando a festa "está acontecendo").
  durationHours: 6,
  timeZone: 'America/Sao_Paulo',

  venueName: 'Chácara Recanto da Família',
  addressLine: 'Rua Aleixo Nodari, 985',
  neighborhood: 'Santa Gema',
  city: 'Colombo',
  state: 'PR',
  country: 'Brasil',

  message:
    'Será um delicioso almoço e uma tarde repleta de alegrias para juntos comemorarmos mais um ano da nossa pequena Sophie! Por isso, contamos com sua confirmação de presença para que possamos organizar tudo com muito carinho.',
  finalMessage: 'Sua presença tornará esse dia ainda mais mágico!',
}

/** Arte do título (PNG/WebP com fundo transparente em /public). '' = usa o título em texto */
export const TITLE_ART = {
  src: '/img/titulo-sophie.webp',
  alt: 'Aniversário da Sophie Polli dos Santos — 5 anos',
  width: 960,
  height: 860,
}

/**
 * Imagens da aniversariante (PNG/WebP sem fundo, em /public/img).
 *  photo: foto de corpo inteiro (seção do convite). '' = mostra o unicórnio 3D.
 *  gameHead: rostinho usado como personagem do mini-jogo.
 */
export const CHILD_IMAGES = {
  photo: '/img/sophie-fantasia.webp',
  photoAlt: 'Sophie com fantasia de unicórnio, tiara dourada e varinha de estrela',
  gameHead: '/img/sophie-cabeca.webp',
}

/** Patterns de fundo (imagens em /public/img). '' = usa o pattern desenhado em código */
export const BACKGROUNDS = {
  opening: '/img/pattern-lilas.webp',
  game: '/img/pattern-azul.webp',
  finale: '/img/pattern-lilas.webp',
}

/**
 * Fotos da aniversariante (opcional). Coloque os arquivos em public/fotos/
 * (JPG/WebP, ~1200 px no lado maior) e liste aqui. [] = seção oculta.
 * Ex.: { src: '/fotos/sophie-1.webp', alt: 'Sophie sorrindo', caption: 'Meu 1º aninho' }
 */
export const PHOTOS = []

/** Efeitos sonoros do jogo ("plim" das estrelinhas). Sintetizados, sem arquivo. */
export const SOUND_EFFECTS = true

/**
 * Telefone para confirmação de presença (WhatsApp).
 * Formato: código do país + DDD + número, só dígitos ou com máscara.
 * Exemplo: '55 41 99999-9999'  →  vira 5541999999999
 * Deixe '' (vazio) enquanto não tiver o número: o botão mostra
 * um estado "em configuração" em vez de um link quebrado.
 */
export const RSVP_PHONE = ''

/** Prazo para confirmar (opcional, texto livre). Ex.: '30/11/2026'. '' = não exibir */
export const RSVP_DEADLINE = ''

/**
 * Música de fundo. Coloque o seu MP3 (com direito de uso) em
 * public/audio/ e informe o caminho, ex.: '/audio/musica.mp3'.
 * '' = botão de música aparece como "indisponível".
 * A música NUNCA toca sozinha: só depois de um toque do convidado.
 */
export const MUSIC = {
  src: '',
  title: 'Trilha mágica',
  volume: 0.45,
  // Começar a tocar quando o convidado tocar em "Abrir convite mágico"
  // (é uma interação do usuário, então os navegadores permitem).
  startOnOpen: true,
}

/**
 * Lista de presentes (opcional). Fica oculta enquanto enabled = false.
 *  - url: link de uma lista online (opcional)
 *  - stores: lojas sugeridas (Instagram, site…) — só links https:// reais
 */
export const GIFT_LIST = {
  enabled: true,
  url: '',
  label: 'Ver lista de presentes',
  note: 'Sua presença é o nosso maior presente! Mas, se quiser mimar a Sophie, estas lojas têm sugestões especiais:',
  stores: [
    { name: '@milonmueller', url: 'https://www.instagram.com/milonmueller/' },
    { name: '@pipoquinhamundoinfantill', url: 'https://www.instagram.com/pipoquinhamundoinfantill/' },
    { name: '@kidsteencalcados', url: 'https://www.instagram.com/kidsteencalcados/' },
  ],
}

/**
 * Bolo (imagem sem fundo em /public/img) sobre a mesa 3D com velinha.
 * topper: redesenha a plaquinha do topo com o nome correto (a arte original
 * dizia "Sophia"). box = área da plaquinha na imagem, em px da imagem.
 */
export const CAKE = {
  src: '/img/bolo-sophie.webp',
  w: 744,
  h: 1100,
  alt: 'Bolo de dois andares com tema unicórnio, arco-íris, laço rosa e topo com o nome Sophie e o número 5',
  topper: { name: '{nome}', box: [66, 2, 604, 252], keepClear: [482, 172] },
  candle: { x: 0.25, y: 0.625 }, // posição da base da velinha (frações da imagem)
}

/**
 * Raspadinhas (missões para os convidados fazerem com a aniversariante).
 * O texto é escrito pelo site sobre a arte — {nome} vira EVENT.childFirstName.
 * textBox = área do texto na arte, em frações [x0, y0, x1, y1].
 */
export const SCRATCH_CARDS = {
  enabled: true,
  title: 'Raspadinhas mágicas',
  subtitle: 'Raspe com o dedo e descubra sua missão para a festa!',
  hint: 'Na festa, mostre sua missão e tire a foto com a {nome}! 📸',
  cards: [
    { img: '/img/raspadinhas/raspadinha-1.webp', w: 510, h: 524, textBox: [0.39, 0.49, 0.86, 0.79], lines: ['Tire uma foto', 'com a {nome}', 'fazendo', 'careta!'] },
    { img: '/img/raspadinhas/raspadinha-2.webp', w: 508, h: 526, textBox: [0.4, 0.48, 0.92, 0.78], lines: ['Tire uma foto', 'com a {nome}', 'de óculos', 'de sol!'] },
    { img: '/img/raspadinhas/raspadinha-3.webp', w: 510, h: 526, textBox: [0.44, 0.48, 0.94, 0.78], lines: ['Tire uma foto', 'com a {nome}', 'de boné e', 'óculos de sol!'] },
    { img: '/img/raspadinhas/raspadinha-4.webp', w: 516, h: 529, textBox: [0.4, 0.46, 0.88, 0.79], lines: ['Tire uma foto', 'com a {nome}', 'te dando', 'um abraço!'] },
    { img: '/img/raspadinhas/raspadinha-5.webp', w: 512, h: 528, textBox: [0.43, 0.46, 0.9, 0.78], lines: ['Tire uma foto', 'com a {nome}', 'dando muita', 'gargalhada!'] },
  ],
}

/**
 * Compartilhamento (WhatsApp / redes sociais — Open Graph).
 * siteUrl: domínio final, ex.: 'https://sophie5anos.vercel.app'.
 * Se ficar vazio, na Vercel o build usa automaticamente o domínio
 * de produção do projeto (VERCEL_PROJECT_PRODUCTION_URL).
 * ogImage: caminho de uma imagem em /public (1200×630, JPG/PNG < 300 KB).
 */
export const SHARE = {
  siteUrl: '',
  title: 'O Mundo Encantado da Sophie · 5 anos',
  description:
    'Você é nosso convidado especial! Domingo, 13/12 às 11h30, na Chácara Recanto da Família. Toque para abrir o convite mágico ✨',
  ogImage: '/og-cover.jpg',
  ogImageAlt: 'Convite O Mundo Encantado da Sophie — unicórnio, arco-íris e nuvens em tons pastel',
  themeColor: '#F8CDE3',
}
