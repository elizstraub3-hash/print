/**
 * Gera public/og-cover.jpg (1200×630) — a capa que aparece no WhatsApp.
 * Usa a arte do título + unicórnio 3D sobre o pattern (sem foto da criança).
 * Uso: npm run og   (requer: npm i -D playwright && npx playwright install chromium)
 */
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import { readFileSync, existsSync } from 'node:fs'
import path from 'node:path'
import { TITLE_ART, BACKGROUNDS, EVENT } from '../src/config/event.js'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const require = createRequire(root + '/')
let chromium
try {
  ;({ chromium } = require('playwright'))
} catch {
  console.error('Instale o Playwright: npm i -D playwright && npx playwright install chromium')
  process.exit(1)
}
const data = (p) => {
  const f = path.join(root, 'public', p.replace(/^\//, ''))
  if (!p || !existsSync(f)) return ''
  const ext = path.extname(f).slice(1).replace('jpg', 'jpeg')
  return `data:image/${ext === 'svg' ? 'svg+xml' : ext};base64,${readFileSync(f).toString('base64')}`
}
const font = (pkg, file) => `data:font/woff2;base64,${readFileSync(path.join(root, 'node_modules/@fontsource', pkg, 'files', file)).toString('base64')}`

const bg = data(BACKGROUNDS.opening || BACKGROUNDS.finale || '')
const title = data(TITLE_ART.src || '')
const uni = data('/img/unicornio-3d.webp')
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Fredoka;font-weight:600;src:url(${font('fredoka', 'fredoka-latin-600-normal.woff2')})}
body{margin:0} .c{width:1200px;height:630px;position:relative;overflow:hidden;font-family:Fredoka;
background:linear-gradient(160deg,#CDECF7,#E6E0FA 45%,#F8CDE3)}
.bg{position:absolute;inset:0;background:url(${bg}) center/cover}
.veil{position:absolute;inset:0;background:rgba(255,250,252,.55)}
.spot{position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 40% 50%,rgba(255,255,255,.85),rgba(255,255,255,0) 70%)}
.title{position:absolute;left:60px;top:12px;height:606px}
.uni{position:absolute;right:40px;bottom:70px;height:360px}
.pill{position:absolute;right:46px;bottom:34px;background:rgba(255,255,255,.92);border-radius:999px;padding:12px 28px;
font-size:30px;font-weight:600;color:#5E4466;box-shadow:0 10px 24px -12px rgba(150,100,160,.6)}
</style></head><body><div class="c">${bg ? '<div class="bg"></div><div class="veil"></div>' : ''}<div class="spot"></div>
${title ? `<img class="title" src="${title}">` : ''}<img class="uni" src="${uni}">
<div class="pill">Domingo, 13/12 · ${EVENT.startsAt.slice(11, 16).replace(':', 'h')}</div></div></body></html>`

const browser = await chromium.launch()
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } })
await page.setContent(html, { waitUntil: 'load' })
await page.evaluate(() => document.fonts.ready)
await page.screenshot({ path: path.join(root, 'public/og-cover.jpg'), type: 'jpeg', quality: 84 })
await page.setViewportSize({ width: 180, height: 180 })
await page.setContent(`<body style="margin:0;background:linear-gradient(160deg,#E6E0FA,#F8CDE3)"><img src="${uni}" style="width:180px;height:180px;object-fit:contain"></body>`, { waitUntil: 'load' })
await page.screenshot({ path: path.join(root, 'public/apple-touch-icon.png') })
await browser.close()
console.log('✓ public/og-cover.jpg e public/apple-touch-icon.png')
