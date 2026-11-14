/**
 * Gera public/og-cover.jpg (1200×630) a partir do próprio SVG do convite.
 * Uso: npm run og   (requer Playwright/Chromium instalado: npx playwright install chromium)
 */
import { createServer } from 'vite'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import { readFileSync } from 'node:fs'
import path from 'node:path'
import React from 'react'
import { renderToStaticMarkup } from 'react-dom/server'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const require = createRequire(root + '/')
let chromium
try {
  ;({ chromium } = require('playwright'))
} catch {
  console.error('Instale o Playwright: npm i -D playwright && npx playwright install chromium')
  process.exit(1)
}

const vite = await createServer({ root, server: { middlewareMode: true }, appType: 'custom', logLevel: 'error' })
const OgCard = (await vite.ssrLoadModule('/src/og/OgCard.jsx')).default
const markup = renderToStaticMarkup(React.createElement(OgCard))
await vite.close()

// fontes embutidas em base64 (setContent não pode ler file://)
const font = (pkg, file) =>
  `data:font/woff2;base64,${readFileSync(path.join(root, 'node_modules/@fontsource', pkg, 'files', file)).toString('base64')}`
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Fredoka;font-weight:500;src:url(${font('fredoka', 'fredoka-latin-500-normal.woff2')})}
@font-face{font-family:Fredoka;font-weight:600;src:url(${font('fredoka', 'fredoka-latin-600-normal.woff2')})}
@font-face{font-family:"Dancing Script";font-weight:700;src:url(${font('dancing-script', 'dancing-script-latin-700-normal.woff2')})}
body{margin:0} .og-w{width:100%;height:auto;display:block}
.sophie-og{background:linear-gradient(100deg,#e58db8,#c39be8 38%,#7fc4e0 70%,#e2b45c);-webkit-background-clip:text;background-clip:text;color:transparent;
filter:drop-shadow(0 3px 0 #fff) drop-shadow(0 10px 16px rgba(200,140,190,.35));padding:0 .12em}
</style></head><body>${markup}</body></html>`

const browser = await chromium.launch()
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } })
await page.setContent(html, { waitUntil: 'load' })
await page.evaluate(() => document.fonts.ready)
const out = path.join(root, 'public/og-cover.jpg')
await page.screenshot({ path: out, type: 'jpeg', quality: 86 })
// ícone para iPhone (tela inicial)
await page.setViewportSize({ width: 180, height: 180 })
await page.setContent(`<body style="margin:0;background:linear-gradient(160deg,#CDECF7,#F8CDE3)"><div style="width:180px;padding:14px 22px;box-sizing:border-box">${markup.match(/<svg viewBox="0 0 320 340"[\s\S]*?<\/svg>(?=<\/div>)/)[0]}</div></body>`)
await page.screenshot({ path: path.join(root, 'public/apple-touch-icon.png') })
await browser.close()
console.log('✓ public/og-cover.jpg e public/apple-touch-icon.png gerados')
