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
 * Use apenas links https:// reais (loja, PIX page, lista online…).
 */
export const GIFT_LIST = {
  enabled: false,
  url: '',
  label: 'Ver lista de presentes',
  note: 'Sua presença é o nosso maior presente! Mas, se quiser mimar a Sophie, preparamos algumas sugestões.',
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
