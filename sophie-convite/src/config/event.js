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
 * Historinha de abertura (estilo cinema). {nome} = nome da criança.
 * art: 'sky' | 'princess' | 'unicorn' | 'invite' (cenas prontas) — troque as
 * imagens em CHILD_IMAGES/TEXT_ART ou peça novas cenas com seus personagens.
 */
export const STORY = {
  enabled: true,
  secondsPerScene: 4.2,
  // Narração (opcional): coloque um MP3 por cena em public/audio/ e informe em
  // cada cena, ex.: audio: '/audio/cena-1.mp3'. A cena dura o tempo da fala.
  scenes: [
    { art: 'sky', audio: '/audio/narracao/cena-1.mp3', text: 'Era uma vez, lá no alto das nuvens, um reino mágico cheio de arco-íris…' },
    { art: 'princess', audio: '/audio/narracao/cena-2.mp3', text: 'Lá vivia uma princesinha muito especial chamada {nome}.' },
    { art: 'unicorn', audio: '/audio/narracao/cena-3.mp3', text: 'Ela vai fazer 5 aninhos, e o seu unicórnio mágico ganhou uma missão…' },
    { art: 'invite', audio: '/audio/narracao/cena-4.mp3', text: 'entregar um convite muito especial… para você! 💌' },
  ],
}

/**
 * Artes de texto (PNG/WebP transparentes). '' = usa o texto digitado.
 *  invite: título abaixo da foto ("Aniversário da Sophie")
 *  finale: mensagem final ("Sua presença tornará...")
 */
export const TEXT_ART = {
  invite: { src: '/img/titulo-aniversario.webp', w: 960, h: 562, alt: 'Aniversário da Sophie' },
  finale: { src: '/img/mensagem-final.webp', w: 960, h: 575, alt: 'Sua presença tornará este dia ainda mais mágico' },
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
export const RSVP_PHONE = '55 41 99834-6478'

/** Nome de quem recebe as confirmações (aparece no botão e na mensagem) */
export const RSVP_CONTACT = 'Mamãe Polli'

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
  // Vídeo do YouTube (player incorporado, oficial). Usado quando não há MP3.
  // O ID é o trecho depois de youtu.be/  →  https://youtu.be/hm9lp5CsRMs
  youtubeId: 'hm9lp5CsRMs',
  title: 'Trilha mágica',
  volume: 0.45,
  // Começar a tocar quando o convidado tocar em "Abrir convite mágico"
  // (é uma interação do usuário, então os navegadores permitem).
  startOnOpen: true,
}

/**
 * Lista de presentes (opcional). Fica oculta enquanto enabled = false.
 * Cada loja pode ter: whatsapp (número), phone (fixo), instagram (@), maps (busca).
 * Só números/links REAIS informados pela família.
 */
export const GIFT_LIST = {
  enabled: true,
  url: '', // lista online (opcional)
  label: 'Ver lista de presentes',
  note: 'Sua presença é o nosso maior presente! Mas, se quiser mimar a {nome}, aqui vão algumas dicas:',
  sizes: [
    { icon: '👗', label: 'Roupas', value: 'tamanho 5 e 6' },
    { icon: '👟', label: 'Calçados', value: 'número 27/28' },
  ],
  likes: ['Barbies', 'Cavalos', 'Casinhas', 'Maquiagens', 'Acessórios de cabelo'],
  stores: [
    {
      name: 'Pipoquinha Mundo Infantil',
      place: 'Centro · Bocaiúva do Sul',
      whatsapp: '55 41 98742-2245',
      instagram: 'pipoquinhamundoinfantill',
      maps: 'Pipoquinha Mundo Infantil, Centro, Bocaiúva do Sul - PR',
    },
    {
      name: 'Milon',
      place: 'Shopping Mueller · Centro, Curitiba',
      phone: '41 3023-2336',
      instagram: 'milonmueller',
      maps: 'Milon Shopping Mueller, Curitiba - PR',
    },
    {
      name: 'Kids Teen',
      place: 'Park Shopping · Colombo',
      whatsapp: '55 41 99808-4961',
      instagram: 'kidsteencalcados',
      maps: 'Kids Teen, Park Shopping, Colombo - PR',
    },
  ],
}

/**
 * Bolo (imagem sem fundo em /public/img) sobre a mesa 3D com velinhas.
 * candles = base de cada velinha, em frações da imagem [x, y].
 */
export const CAKE = {
  src: '/img/bolo-sophie.webp',
  w: 696,
  h: 1100,
  alt: 'Bolo de dois andares com unicórnio, arco-íris, laço rosa, número 5 e topo escrito Sophie',
  // [x, y] da base de cada velinha (frações da imagem)
  // 2º andar (rosa, em cima): topo em y≈0.47 · 1º andar (lilás): chantili em y≈0.67
  candles: [
    [0.225, 0.476], // 2º andar, à esquerda do unicórnio
    [0.595, 0.472], // 2º andar, entre o unicórnio e o 5
    [0.12, 0.676], // 1º andar, esquerda
    [0.5, 0.672], //  1º andar, centro (atrás do laço)
    [0.88, 0.676], // 1º andar, direita
  ],
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
