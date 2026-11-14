import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { viteSingleFile } from 'vite-plugin-singlefile'
import { EVENT, SHARE } from './src/config/event.js'

const esc = (s = '') =>
  String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

/** Domínio usado nas metatags (WhatsApp exige URL absoluta para a imagem). */
function resolveSiteUrl() {
  const fromConfig = (SHARE.siteUrl || '').trim()
  const fromVercel = process.env.VERCEL_PROJECT_PRODUCTION_URL || process.env.VERCEL_URL || ''
  const url = fromConfig || (fromVercel ? `https://${fromVercel}` : '')
  return url.replace(/\/+$/, '')
}

/** Injeta título, descrição e Open Graph a partir de src/config/event.js */
function openGraphPlugin() {
  return {
    name: 'invite-open-graph',
    transformIndexHtml(html) {
      const site = resolveSiteUrl()
      const abs = (p) => (/^https?:\/\//.test(p) ? p : `${site}${p.startsWith('/') ? '' : '/'}${p}`)
      const image = SHARE.ogImage ? abs(SHARE.ogImage) : ''
      const tags = [
        `<title>${esc(SHARE.title)}</title>`,
        `<meta name="description" content="${esc(SHARE.description)}" />`,
        `<meta name="theme-color" content="${esc(SHARE.themeColor)}" />`,
        `<meta property="og:type" content="website" />`,
        `<meta property="og:locale" content="pt_BR" />`,
        `<meta property="og:site_name" content="${esc(EVENT.projectTitle)}" />`,
        `<meta property="og:title" content="${esc(SHARE.title)}" />`,
        `<meta property="og:description" content="${esc(SHARE.description)}" />`,
        site && `<meta property="og:url" content="${esc(site)}/" />`,
        image && `<meta property="og:image" content="${esc(image)}" />`,
        image && image.startsWith('https') && `<meta property="og:image:secure_url" content="${esc(image)}" />`,
        image && `<meta property="og:image:width" content="1200" />`,
        image && `<meta property="og:image:height" content="630" />`,
        image && `<meta property="og:image:alt" content="${esc(SHARE.ogImageAlt)}" />`,
        `<meta name="twitter:card" content="summary_large_image" />`,
        `<meta name="twitter:title" content="${esc(SHARE.title)}" />`,
        `<meta name="twitter:description" content="${esc(SHARE.description)}" />`,
        image && `<meta name="twitter:image" content="${esc(image)}" />`,
      ]
        .filter(Boolean)
        .join('\n    ')
      return html.replace('<!--OG_TAGS-->', tags)
    },
  }
}

// `vite build --mode single` gera um único HTML autocontido (prévia offline).
export default defineConfig(({ mode }) => ({
  plugins: [react(), openGraphPlugin(), mode === 'single' && viteSingleFile()].filter(Boolean),
  build: {
    outDir: mode === 'single' ? 'dist-single' : 'dist',
    target: 'es2019',
    cssCodeSplit: false,
  },
}))
